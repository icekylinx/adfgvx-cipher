/* ADFGVX Cipher. icekylinx and GPT-6 Astra Pro (2026). Apache-2.0.
 * Experimental mixed four/six-gram component search, with ciphertext
 * segmentation fixed by an IC candidate. Column moves must preserve every
 * message's long/short column class. The observed ciphertext is never edited.
 * Input: MODEL37 SIX_MODEL SIX_WEIGHT K RESTARTS ITERATIONS SEED NMSG,
 * initial square (all ? for none), K ranks, and NMSG ciphertexts.
 * Six-gram windows containing a wholly masked plaintext slot are omitted and
 * rescaled to the full window count. This is a heuristic, not an exact
 * marginal likelihood; exact source constraints are checked independently.
 * Marginal variant: 37^4 table, wildcard sums, surviving half-coordinates lost.
 * Warm-start revision: strict input validation and initial-incumbent retention.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include "../joint_search/src/sixgram_model.h"
static double sixweight;
#define MAXN 4096
#define MAXK 40
#define MAXM 8
#define QSIZE 1874161
static const char AL[]="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
static float quad[QSIZE];
static int K,H,nmsg,ns[MAXM],bs[MAXM][MAXN],ranks[MAXK],co[MAXK],sq[36],startsq[36],hasinitial;
static int cls[MAXK],moves[MAXK*MAXK][2],nmoves,pmoves[MAXK*MAXK][2],npmoves,frequency[36],order[36];
static uint64_t state;
static uint64_t rn(void){uint64_t z=(state+=0x9e3779b97f4a7c15ULL);z=(z^(z>>30))*0xbf58476d1ce4e5b9ULL;z=(z^(z>>27))*0x94d049bb133111ebULL;return z^(z>>31);}
static int ri(int n){return rn()%n;}
static double ru(void){return(rn()>>11)*0x1.0p-53;}
static int idx(char c,const char*a){const char*p=strchr(a,c);return p&&c?(int)(p-a):-1;}
static double fitness(void){
    double s=0;
    for(int m=0;m<nmsg;m++){
        int text[MAXN],n=ns[m];
        for(int i=0;i<n;i++){
            int j=2*i,a=bs[m][(j/K)*K+co[j%K]],b=bs[m][((j+1)/K)*K+co[(j+1)%K]];
            text[i]=a<0||b<0?-1:sq[6*a+b];
        }
        double four=0,six=0;int knownsix=0;
        for(int i=0;i+3<n;i++){
            int z=0;for(int j=0;j<4;j++)z=37*z+(text[i+j]<0?36:text[i+j]);four+=quad[z];
        }
        for(int i=0;i+5<n;i++){
            uint32_t code=0;int known=1;
            for(int j=0;j<6;j++){if(text[i+j]<0){known=0;break;}code=code*36+text[i+j];}
            if(known){six+=g6_lookup(code);knownsix++;}
        }
        s+=(1-sixweight)*four+sixweight*(knownsix?six*(n-3)/knownsix:four);
    }
    return s;
}
static void output(double s,int rs){
    char square[37];int total=0;for(int i=0;i<36;i++)square[i]=AL[sq[i]];square[36]=0;
    for(int m=0;m<nmsg;m++)total+=ns[m]-3;
    printf("{\"score\":%.9f,\"restart\":%d,\"version\":37,\"square\":\"%s\",\"ranks\":[",s/total,rs,square);
    for(int j=0;j<K;j++)printf("%s%d",j?",":"",ranks[co[j]]);
    printf("],\"plaintexts\":[");
    for(int m=0;m<nmsg;m++){
        if(m)putchar(',');
        putchar('"');
        for(int i=0;i<ns[m];i++){
            int j=2*i,a=bs[m][(j/K)*K+co[j%K]],b=bs[m][((j+1)/K)*K+co[(j+1)%K]];
            putchar(a<0||b<0?'?':AL[sq[6*a+b]]);
        }
        putchar('"');
    }
    printf("]}\n");fflush(stdout);
}
int main(void){
    char path[1024],sixpath[1024],buf[MAXN],initial[64];int restarts,iters;unsigned long long seed;
    if(scanf("%1023s%1023s%lf%d%d%d%llu%d",path,sixpath,&sixweight,&K,&restarts,&iters,&seed,&nmsg)!=8||sixweight<0||sixweight>1||K<2||K>MAXK||nmsg<1||nmsg>MAXM||K%2||restarts<1||iters<1)return 2;
    if(!g6_load(sixpath))return 3;
    H=K/2;state=seed;FILE*f=fopen(path,"rb");if(!f||fread(quad,sizeof(float),QSIZE,f)!=QSIZE)return 3;fclose(f);
    for(int code=0;code<QSIZE;code++){int v=code,wild=0;for(int j=0;j<4;j++){wild+=v%37==36;v/=37;}quad[code]-=wild*log10(36.0);}
    if(scanf("%36s",initial)!=1||strlen(initial)!=36)return 2;
    int used[36]={0},questions=0;hasinitial=1;
    for(int i=0;i<36;i++){
        startsq[i]=idx(initial[i],AL);
        if(startsq[i]<0){if(initial[i]!='?')return 2;questions++;}
        else if(used[startsq[i]]++)return 2;
    }
    if(questions&&questions!=36)return 2;
    hasinitial=questions==0;
    int seen[MAXK]={0};
    for(int i=0;i<K;i++)if(scanf("%d",&ranks[i])!=1||ranks[i]<1||ranks[i]>K||seen[ranks[i]-1]++)return 2;
    for(int m=0;m<nmsg;m++){
        if(scanf("%4095s",buf)!=1)return 2;
        int n=strlen(buf);if(n%2||n<8)return 2;
        for(int i=0;i<n;i++)if(idx(buf[i],"ADFGVX")<0&&buf[i]!='?')return 2;
        int offsets[MAXK],pos=0;for(int rank=1;rank<=K;rank++)for(int j=0;j<K;j++)if(ranks[j]==rank){offsets[j]=pos;pos+=n/K+(j<n%K);}
        for(int i=0;i<n;i++)bs[m][i]=idx(buf[offsets[i%K]+i/K],"ADFGVX");
        ns[m]=n/2;
        for(int i=0;i<n/2;i++){int a=bs[m][2*i],b=bs[m][2*i+1];if(a>=0&&b>=0)frequency[6*a+b]++;}
        for(int j=0;j<K;j++)if(j<n%K)cls[j]|=1<<m;
    }
    for(int i=0;i<K;i++)for(int j=i+1;j<K;j++)if(cls[i]==cls[j]){moves[nmoves][0]=i;moves[nmoves++][1]=j;}
    for(int i=0;i<H;i++)for(int j=i+1;j<H;j++)if(cls[2*i]==cls[2*j]&&cls[2*i+1]==cls[2*j+1]){pmoves[npmoves][0]=2*i;pmoves[npmoves++][1]=2*j;}
    for(int i=0;i<36;i++)order[i]=i;
    for(int i=0;i<36;i++)for(int j=i+1;j<36;j++)if(frequency[order[j]]>frequency[order[i]]){int t=order[i];order[i]=order[j];order[j]=t;}
    const char*priority="ENISRATDHULCGMXOBWFKZPVJYQ0123456789";
    int gs[36],gc[MAXK];double global=-1e100;
    for(int rs=0;rs<restarts;rs++){
        for(int i=0;i<K;i++)co[i]=i;
        if(rs>0&&rs%3==1){memcpy(co,gc,sizeof(co));memcpy(sq,gs,sizeof(sq));}
        else if(hasinitial&&rs%3==0)memcpy(sq,startsq,sizeof(sq));
        else{for(int i=0;i<36;i++)sq[order[i]]=idx(priority[i],AL);for(int j=0;j<(rs?20:0);j++){int a=ri(36),b=ri(36),t=sq[a];sq[a]=sq[b];sq[b]=t;}}
        if(rs&&nmoves)for(int j=0;j<ri(5);j++){int z=ri(nmoves),a=moves[z][0],b=moves[z][1],t=co[a];co[a]=co[b];co[b]=t;}
        double cur=fitness();
        if(cur>global){global=cur;memcpy(gs,sq,sizeof(sq));memcpy(gc,co,sizeof(co));}
        for(int it=0;it<iters;it++){
            int mv=ri(20),type=0,a,b,t;
            if(npmoves&&mv<2){type=2;int z=ri(npmoves);a=pmoves[z][0];b=pmoves[z][1];for(int j=0;j<2;j++){t=co[a+j];co[a+j]=co[b+j];co[b+j]=t;}}
            else if(nmoves&&mv<6){type=1;int z=ri(nmoves);a=moves[z][0];b=moves[z][1];t=co[a];co[a]=co[b];co[b]=t;}
            else{a=ri(36);b=ri(36);if(a==b)continue;t=sq[a];sq[a]=sq[b];sq[b]=t;}
            double value=fitness(),phase=(double)(it%30000)/30000,T=(4.0*(1-phase)+.08)*(1-.7*(double)it/iters);
            if(value>=cur||ru()<exp((value-cur)/T))cur=value;
            else if(type==2){for(int j=0;j<2;j++){t=co[a+j];co[a+j]=co[b+j];co[b+j]=t;}}
            else if(type==1){t=co[a];co[a]=co[b];co[b]=t;}else{t=sq[a];sq[a]=sq[b];sq[b]=t;}
            if(cur>global){global=cur;memcpy(gs,sq,sizeof(sq));memcpy(gc,co,sizeof(co));}
        }
        memcpy(sq,gs,sizeof(sq));memcpy(co,gc,sizeof(co));static double printed=-1e100;
        if(global>printed+1e-7){output(global,rs);printed=global;}
    }
    return 0;
}
