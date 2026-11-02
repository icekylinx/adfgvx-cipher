/* Unknown-square search retaining both observed ADFGVX coordinates.
 * A half-erased pair permits six cells; a fully erased pair permits 36.
 * Each four-gram score is log10 of the probability mass over precisely
 * those cells. Overlapping windows make this a composite objective, not an
 * exact sequence likelihood or posterior probability.
 * Usage: marginal_subsolve QUAD_MODEL INTERIM RESTARTS ITERATIONS SEED [SQUARE]
 * The INTERIM stream is already untransposed, with '?' as each erased slot.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>

#define MAXN 2048
#define QSIZE 1679616
#define MAXCOMB 2000000
static const char AL[]="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
static const char CO[]="ADFGVX";
static float qlog[QSIZE];
static double qprob[QSIZE];
static int n,nw,allowed[MAXN][36],sizes[MAXN];
typedef struct {int count;unsigned char *cells;uint64_t mask;} Window;
static Window windows[MAXN];
static int affected[36][MAXN],naffected[36];
static uint64_t state;
static uint64_t rn(void){uint64_t z=(state+=0x9e3779b97f4a7c15ULL);z=(z^(z>>30))*0xbf58476d1ce4e5b9ULL;z=(z^(z>>27))*0x94d049bb133111ebULL;return z^(z>>31);}
static int ri(int m){return rn()%m;}
static double ru(void){return(rn()>>11)*0x1.0p-53;}
static int idx(char c,const char *s){const char*p=strchr(s,c);return p&&c?(int)(p-s):-1;}
static int gramindex(const int *key,const unsigned char *p){return ((key[p[0]]*36+key[p[1]])*36+key[p[2]])*36+key[p[3]];}

static double value(const int *key,int i){
    Window *w=&windows[i];unsigned char *p=w->cells;
    if(w->count==1)return qlog[gramindex(key,p)];
    double total=0;
    for(int j=0;j<w->count;j++,p+=4)total+=qprob[gramindex(key,p)];
    return log10(total);
}
static double fitness(const int *key,double *cache){double s=0;for(int i=0;i<nw;i++){cache[i]=value(key,i);s+=cache[i];}return s;}
static void emit(const int *key,double score,int restart){
    char square[37],plain[MAXN];for(int i=0;i<36;i++)square[i]=AL[key[i]];square[36]=0;
    for(int i=0;i<n;i++)plain[i]=sizes[i]==1?AL[key[allowed[i][0]]]:'?';
    plain[n]=0;
    printf("{\"score\":%.9f,\"restart\":%d,\"square\":\"%s\",\"plaintext\":\"%s\",\"objective\":\"quadgram_exact_coordinate_domains\"}\n",score/nw,restart,square,plain);fflush(stdout);
}
int main(int argc,char **argv){
    if(argc<6){fprintf(stderr,"usage: marginal_subsolve QUAD INTERIM RESTARTS ITERATIONS SEED [SQUARE]\n");return 2;}
    FILE *f=fopen(argv[1],"rb");if(!f||fread(qlog,sizeof(float),QSIZE,f)!=QSIZE)return 3;fclose(f);
    for(int i=0;i<QSIZE;i++)qprob[i]=pow(10.0,qlog[i]);
    int length=(int)strlen(argv[2]);if(length%2||length/2>=MAXN||length<8)return 2;n=length/2;nw=n-3;
    double freq[36]={0};int order[36];
    for(int i=0;i<n;i++){
        int a=idx(argv[2][2*i],CO),b=idx(argv[2][2*i+1],CO);
        for(int r=0;r<6;r++)for(int c=0;c<6;c++)if((a<0||a==r)&&(b<0||b==c))allowed[i][sizes[i]++]=r*6+c;
        for(int j=0;j<sizes[i];j++)freq[allowed[i][j]]+=1.0/sizes[i];
    }
    for(int i=0;i<nw;i++){
        Window *w=&windows[i];w->count=sizes[i]*sizes[i+1]*sizes[i+2]*sizes[i+3];
        if(w->count>MAXCOMB){fprintf(stderr,"domain expansion limit\n");return 4;}
        w->cells=malloc((size_t)w->count*4);if(!w->cells)return 4;int at=0;
        for(int a=0;a<sizes[i];a++)for(int b=0;b<sizes[i+1];b++)for(int c=0;c<sizes[i+2];c++)for(int d=0;d<sizes[i+3];d++){
            w->cells[at++]=allowed[i][a];w->cells[at++]=allowed[i+1][b];w->cells[at++]=allowed[i+2][c];w->cells[at++]=allowed[i+3][d];
        }
        for(int j=0;j<4;j++)for(int z=0;z<sizes[i+j];z++)w->mask|=1ULL<<allowed[i+j][z];
        for(int cell=0;cell<36;cell++)if(w->mask&(1ULL<<cell))affected[cell][naffected[cell]++]=i;
    }
    for(int i=0;i<36;i++)order[i]=i;
    for(int i=0;i<36;i++)for(int j=i+1;j<36;j++)if(freq[order[j]]>freq[order[i]]){int t=order[i];order[i]=order[j];order[j]=t;}
    const char *priority="ENISRATDHULCGMXOBWFKZPVJYQ0123456789";
    int restarts=atoi(argv[3]),iterations=atoi(argv[4]);state=strtoull(argv[5],0,10);
    int initial[36],hasinitial=argc>6&&strlen(argv[6])==36,used[36]={0};
    if(hasinitial)for(int i=0;i<36;i++){initial[i]=idx(argv[6][i],AL);if(initial[i]<0||used[initial[i]]){hasinitial=0;break;}used[initial[i]]=1;}
    int bestkey[36];double global=-1e100,printed=-1e100;
    for(int rs=0;rs<restarts;rs++){
        int key[36];double cache[MAXN];
        if(hasinitial&&rs%4==0)memcpy(key,initial,sizeof key);
        else if(rs>0&&rs%4==1){memcpy(key,bestkey,sizeof key);for(int j=0;j<8;j++){int a=ri(36),b=ri(36),t=key[a];key[a]=key[b];key[b]=t;}}
        else{for(int i=0;i<36;i++)key[order[i]]=idx(priority[i],AL);for(int j=0;j<(rs?40:0);j++){int a=ri(36),b=ri(36),t=key[a];key[a]=key[b];key[b]=t;}}
        double cur=fitness(key,cache);if(cur>global){global=cur;memcpy(bestkey,key,sizeof key);}
        int marks[MAXN]={0},epoch=0,indices[MAXN];double candidate[MAXN];
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
        if(global>printed+1e-7){double check[MAXN];global=fitness(bestkey,check);emit(bestkey,global,rs);printed=global;}
    }
    return 0;
}
