/* Unknown-square search retaining both observed ADFGVX coordinates.
 * A half-erased pair permits six cells; a fully erased pair permits 36.
 * Each four/six-gram score is log10 of the probability mass over precisely
 * those cells. Overlapping windows make this a composite objective, not an
 * exact sequence likelihood or posterior probability.
 * Usage: marginal_subsolve6 QUAD SIX SIX_WEIGHT INTERIM RESTARTS ITERATIONS SEED [SQUARE]
 * The INTERIM stream is already untransposed, with '?' as each erased slot.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include "sixgram_model.h"

#define MAXN 2048
#define MAXWIN (2*MAXN)
#define QSIZE 1679616
#define MAXCOMB 2000000
static const char AL[]="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
static const char CO[]="ADFGVX";
static float qlog[QSIZE];
static double qprob[QSIZE];
static float *sixprob;
static double sixfloorprob,sixweight;
static int n,nw,allowed[MAXN][36],sizes[MAXN];
typedef struct {int count,span;double weight;unsigned char *cells;uint64_t mask;} Window;
static Window windows[MAXWIN];
static int affected[36][MAXWIN],naffected[36];
static uint64_t state;
static uint64_t rn(void){uint64_t z=(state+=0x9e3779b97f4a7c15ULL);z=(z^(z>>30))*0xbf58476d1ce4e5b9ULL;z=(z^(z>>27))*0x94d049bb133111ebULL;return z^(z>>31);}
static int ri(int m){return rn()%m;}
static double ru(void){return(rn()>>11)*0x1.0p-53;}
static int idx(char c,const char *s){const char*p=strchr(s,c);return p&&c?(int)(p-s):-1;}
static int gramindex(const int *key,const unsigned char *p){return ((key[p[0]]*36+key[p[1]])*36+key[p[2]])*36+key[p[3]];}

static double prob6(uint32_t code){
    uint32_t key=code+1,h=key;h=(h^(h>>16))*0x7feb352dU;h=(h^(h>>15))*0x846ca68bU;h^=h>>16;
    uint32_t slot=h&g6_mask;
    while(g6_keys[slot]){if(g6_keys[slot]==key)return sixprob[slot];slot=(slot+1)&g6_mask;}
    return sixfloorprob;
}
static double value(const int *key,int i){
    Window *w=&windows[i];unsigned char *p=w->cells;
    if(w->count==1&&w->span==4)return w->weight*qlog[gramindex(key,p)];
    double total=0;
    for(int j=0;j<w->count;j++,p+=w->span){
        uint32_t code=0;for(int k=0;k<w->span;k++)code=code*36+key[p[k]];
        total+=w->span==4?qprob[code]:prob6(code);
    }
    return w->weight*log10(total);
}
static int build_window(int at,int position,int span,double weight){
    Window *w=&windows[at];w->span=span;w->weight=weight;w->count=1;
    for(int j=0;j<span;j++)w->count*=sizes[position+j];
    if(w->count>MAXCOMB)return 0;
    w->cells=malloc((size_t)w->count*span);if(!w->cells)return 0;
    for(int combo=0;combo<w->count;combo++){
        int v=combo;
        for(int j=span-1;j>=0;j--){w->cells[combo*span+j]=allowed[position+j][v%sizes[position+j]];v/=sizes[position+j];}
    }
    for(int j=0;j<span;j++)for(int z=0;z<sizes[position+j];z++)w->mask|=1ULL<<allowed[position+j][z];
    for(int cell=0;cell<36;cell++)if(w->mask&(1ULL<<cell))affected[cell][naffected[cell]++]=at;
    return 1;
}
static double fitness(const int *key,double *cache){double s=0;for(int i=0;i<nw;i++){cache[i]=value(key,i);s+=cache[i];}return s;}
static void emit(const int *key,double score,int restart){
    char square[37],plain[MAXN];for(int i=0;i<36;i++)square[i]=AL[key[i]];square[36]=0;
    for(int i=0;i<n;i++)plain[i]=sizes[i]==1?AL[key[allowed[i][0]]]:'?';
    plain[n]=0;
    printf("{\"score\":%.9f,\"restart\":%d,\"square\":\"%s\",\"plaintext\":\"%s\",\"objective\":\"mixed_four_sixgram_exact_coordinate_domains\"}\n",score/(n-3),restart,square,plain);fflush(stdout);
}
int main(int argc,char **argv){
    if(argc<8){fprintf(stderr,"usage: marginal_subsolve6 QUAD SIX SIX_WEIGHT INTERIM RESTARTS ITERATIONS SEED [SQUARE]\n");return 2;}
    FILE *f=fopen(argv[1],"rb");if(!f||fread(qlog,sizeof(float),QSIZE,f)!=QSIZE)return 3;fclose(f);
    for(int i=0;i<QSIZE;i++)qprob[i]=pow(10.0,qlog[i]);
    if(!g6_load(argv[2]))return 3;
    sixweight=atof(argv[3]);if(sixweight<0||sixweight>1)return 2;
    sixprob=malloc((size_t)g6_size*sizeof(float));if(!sixprob)return 4;
    for(uint32_t i=0;i<g6_size;i++)sixprob[i]=g6_keys[i]?pow(10.,g6_values[i]):0;
    sixfloorprob=pow(10.,g6_floor);
    int length=(int)strlen(argv[4]);if(length%2||length/2>=MAXN||length<12)return 2;n=length/2;nw=2*n-8;
    double freq[36]={0};int order[36];
    for(int i=0;i<n;i++){
        int a=idx(argv[4][2*i],CO),b=idx(argv[4][2*i+1],CO);
        for(int r=0;r<6;r++)for(int c=0;c<6;c++)if((a<0||a==r)&&(b<0||b==c))allowed[i][sizes[i]++]=r*6+c;
        for(int j=0;j<sizes[i];j++)freq[allowed[i][j]]+=1.0/sizes[i];
    }
    for(int i=0;i<n-3;i++)if(!build_window(i,i,4,1-sixweight))return 4;
    for(int i=0;i<n-5;i++)if(!build_window(n-3+i,i,6,sixweight*(n-3)/(n-5)))return 4;
    for(int i=0;i<36;i++)order[i]=i;
    for(int i=0;i<36;i++)for(int j=i+1;j<36;j++)if(freq[order[j]]>freq[order[i]]){int t=order[i];order[i]=order[j];order[j]=t;}
    const char *priority="ENISRATDHULCGMXOBWFKZPVJYQ0123456789";
    int restarts=atoi(argv[5]),iterations=atoi(argv[6]);state=strtoull(argv[7],0,10);
    int initial[36],hasinitial=argc>8&&strlen(argv[8])==36,used[36]={0};
    if(hasinitial)for(int i=0;i<36;i++){initial[i]=idx(argv[8][i],AL);if(initial[i]<0||used[initial[i]]){hasinitial=0;break;}used[initial[i]]=1;}
    int bestkey[36];double global=-1e100,printed=-1e100;
    for(int rs=0;rs<restarts;rs++){
        int key[36];double cache[MAXWIN];
        if(hasinitial&&rs%4==0)memcpy(key,initial,sizeof key);
        else if(rs>0&&rs%4==1){memcpy(key,bestkey,sizeof key);for(int j=0;j<8;j++){int a=ri(36),b=ri(36),t=key[a];key[a]=key[b];key[b]=t;}}
        else{for(int i=0;i<36;i++)key[order[i]]=idx(priority[i],AL);for(int j=0;j<(rs?40:0);j++){int a=ri(36),b=ri(36),t=key[a];key[a]=key[b];key[b]=t;}}
        double cur=fitness(key,cache);if(cur>global){global=cur;memcpy(bestkey,key,sizeof key);}
        int marks[MAXWIN]={0},epoch=0,indices[MAXWIN];double candidate[MAXWIN];
        for(int it=0;it<iterations;it++){
            int a=ri(36),b=ri(36);if(a==b||(!naffected[a]&&!naffected[b]))continue;
            int count=0;epoch++;
            for(int j=0;j<naffected[a];j++){int ix=affected[a][j];marks[ix]=epoch;indices[count++]=ix;}
            for(int j=0;j<naffected[b];j++){int ix=affected[b][j];if(marks[ix]!=epoch)indices[count++]=ix;}
            double before=0,after=0;for(int j=0;j<count;j++)before+=cache[indices[j]];
            int t=key[a];key[a]=key[b];key[b]=t;
            for(int j=0;j<count;j++){candidate[j]=value(key,indices[j]);after+=candidate[j];}
            double delta=after-before,phase=(double)(it%20000)/20000;
            double temperature=(2.8*(1-phase)+.06)*(1-.75*(double)it/iterations);
            if(delta>=0||ru()<exp(delta/temperature)){
                cur+=delta;for(int j=0;j<count;j++)cache[indices[j]]=candidate[j];
                if(cur>global+1e-7){global=cur;memcpy(bestkey,key,sizeof key);}
            }else{t=key[a];key[a]=key[b];key[b]=t;}
        }
        if(global>printed+1e-7){double check[MAXWIN];global=fitness(bestkey,check);emit(bestkey,global,rs);printed=global;}
    }
    return 0;
}
