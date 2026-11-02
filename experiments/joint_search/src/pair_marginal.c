/* Joint substitution and length-compatible column-pair ordering.
 * Input: model K restarts iterations seed nmsg, initial square or 36 '?',
 * K column ranks, then ciphertexts. K and ciphertext lengths must be even.
 * This is a heuristic polish of an IC candidate, not a full-key exhaustive search.
 * Marginal four-gram variant: model base 37, index 36 means unknown plaintext.
 * Half-known coordinate information is still discarded by this representation.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#define MAXN 4096
#define MAXK 40
#define MAXM 8
#define QSIZE 1874161
static float quad[QSIZE];
static const char AL[]="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
static int K,H,nmsg,ns[MAXM],cs[MAXM][MAXN],ranks[MAXK],po[MAXK],ori[MAXK],sq[36],startsq[36],hasinitial;
static int cls[MAXK],moves[MAXK*MAXK][2],nmoves,frequency[36],order[36];
static int allorders[10001][MAXK],norders,orderoverflow,enumused[MAXK],enump[MAXK];
static uint64_t state;
static uint64_t rn(void){uint64_t z=(state+=0x9e3779b97f4a7c15ULL);z=(z^(z>>30))*0xbf58476d1ce4e5b9ULL;z=(z^(z>>27))*0x94d049bb133111ebULL;return z^(z>>31);}
static int ri(int n){return rn()%n;}
static double ru(void){return(rn()>>11)*0x1.0p-53;}
static int idx(char c,const char*a){const char*p=strchr(a,c);return p&&c?(int)(p-a):-1;}
static double fitness(void){
    double s=0;
    for(int m=0;m<nmsg;m++){
        int text[MAXN],n=ns[m];
        for(int i=0;i<n;i++){int j=po[i%H],c=cs[m][(i/H)*H+j];if(c>=0&&ori[j])c=6*(c%6)+c/6;text[i]=c<0?-1:sq[c];}
        for(int i=0;i+3<n;i++){
            int z=0;for(int j=0;j<4;j++)z=37*z+(text[i+j]<0?36:text[i+j]);s+=quad[z];
        }
    }
    return s;
}
static void enumerate_orders(int depth){
    if(orderoverflow)return;
    if(depth==H){
        if(norders==10000){orderoverflow=1;return;}
        memcpy(allorders[norders++],enump,sizeof(enump));return;
    }
    for(int j=0;j<H;j++)if(!enumused[j]&&cls[j]==cls[depth]){
        enumused[j]=1;enump[depth]=j;enumerate_orders(depth+1);enumused[j]=0;
        if(orderoverflow)return;
    }
}
static double optimize_order(void){
    double best=-1e100;int bp[MAXK];
    for(int j=0;j<norders;j++){
        memcpy(po,allorders[j],sizeof(po));double v=fitness();
        if(v>best){best=v;memcpy(bp,po,sizeof(po));}
    }
    memcpy(po,bp,sizeof(po));return best;
}
static void output(double s,int rs){
    char square[37];int total=0;for(int i=0;i<36;i++)square[i]=AL[sq[i]];square[36]=0;
    for(int m=0;m<nmsg;m++)total+=ns[m]-3;
    printf("{\"score\":%.9f,\"restart\":%d,\"version\":37,\"exact_order_count\":%d,\"square\":\"%s\",\"ranks\":[",s/total,rs,norders,square);
    for(int j=0;j<H;j++)printf("%s%d,%d",j?",":"",ranks[2*po[j]+ori[po[j]]],ranks[2*po[j]+1-ori[po[j]]]);
    printf("],\"plaintexts\":[");
    for(int m=0;m<nmsg;m++){
        if(m)putchar(',');
        putchar('"');for(int i=0;i<ns[m];i++){int j=po[i%H],c=cs[m][(i/H)*H+j];if(c>=0&&ori[j])c=6*(c%6)+c/6;putchar(c<0?'?':AL[sq[c]]);}putchar('"');
    }
    printf("]}\n");fflush(stdout);
}
int main(void){
    char path[1024],buf[MAXN],initial[64];int restarts,iters;unsigned long long seed;
    if(scanf("%1023s%d%d%d%llu%d",path,&K,&restarts,&iters,&seed,&nmsg)!=6||K<2||K>MAXK||nmsg<1||nmsg>MAXM||K%2||restarts<1||iters<1)return 2;
    H=K/2;state=seed;FILE*f=fopen(path,"rb");if(!f||fread(quad,sizeof(float),QSIZE,f)!=QSIZE)return 3;fclose(f);
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
        int offsets[MAXK],pos=0,symbols[MAXN];for(int rank=1;rank<=K;rank++)for(int j=0;j<K;j++)if(ranks[j]==rank){offsets[j]=pos;pos+=n/K+(j<n%K);}
        for(int i=0;i<n;i++)symbols[i]=idx(buf[offsets[i%K]+i/K],"ADFGVX");
        ns[m]=n/2;
        for(int i=0;i<n/2;i++){int a=symbols[2*i],b=symbols[2*i+1];int c=a<0||b<0?-1:6*a+b;cs[m][i]=c;if(c>=0)frequency[c]++;}
        for(int j=0;j<H;j++)if(j<ns[m]%H)cls[j]|=1<<m;
    }
    for(int i=0;i<H;i++)for(int j=i+1;j<H;j++)if(cls[i]==cls[j]){moves[nmoves][0]=i;moves[nmoves++][1]=j;}
    enumerate_orders(0);if(orderoverflow)norders=0;
    for(int i=0;i<36;i++)order[i]=i;
    for(int i=0;i<36;i++)for(int j=i+1;j<36;j++)if(frequency[order[j]]>frequency[order[i]]){int t=order[i];order[i]=order[j];order[j]=t;}
    const char*priority="ENISRATDHULCGMXOBWFKZPVJYQ0123456789";
    int gs[36],gp[MAXK],go[MAXK];double global=-1e100;
    for(int rs=0;rs<restarts;rs++){
        for(int i=0;i<H;i++){po[i]=i;ori[i]=0;}
        if(rs>0&&rs%3==1){memcpy(po,gp,sizeof(po));memcpy(sq,gs,sizeof(sq));memcpy(ori,go,sizeof(ori));}
        else if(hasinitial&&rs%3==0)memcpy(sq,startsq,sizeof(sq));
        else{for(int i=0;i<36;i++)sq[order[i]]=idx(priority[i],AL);for(int j=0;j<(rs?20:0);j++){int a=ri(36),b=ri(36),t=sq[a];sq[a]=sq[b];sq[b]=t;}}
        if(rs&&nmoves)for(int j=0;j<2+ri(H);j++){int z=ri(nmoves),a=moves[z][0],b=moves[z][1],t=po[a];po[a]=po[b];po[b]=t;}
        double cur=fitness();
        if(cur>global){global=cur;memcpy(gs,sq,sizeof(sq));memcpy(gp,po,sizeof(po));memcpy(go,ori,sizeof(ori));}
        for(int it=0;it<iters;it++){
            if(norders && it%5000==4999)cur=optimize_order();
            int mv=ri(10),pair=nmoves&&mv<2,flip=mv==2,a,b,t;if(pair){int z=ri(nmoves);a=moves[z][0];b=moves[z][1];t=po[a];po[a]=po[b];po[b]=t;}
            else if(flip){a=ri(H);ori[a]^=1;}
            else{a=ri(36);b=ri(36);if(a==b)continue;t=sq[a];sq[a]=sq[b];sq[b]=t;}
            double value=fitness(),phase=(double)(it%20000)/20000,T=(3.5*(1-phase)+.08)*(1-.7*(double)it/iters);
            if(value>=cur||ru()<exp((value-cur)/T))cur=value;
            else if(pair){t=po[a];po[a]=po[b];po[b]=t;}else if(flip){ori[a]^=1;}else{t=sq[a];sq[a]=sq[b];sq[b]=t;}
            if(cur>global){global=cur;memcpy(gs,sq,sizeof(sq));memcpy(gp,po,sizeof(po));memcpy(go,ori,sizeof(ori));}
        }
        memcpy(sq,gs,sizeof(sq));memcpy(po,gp,sizeof(po));memcpy(ori,go,sizeof(ori));static double printed=-1e100;
        if(global>printed+1e-7){output(global,rs);printed=global;}
    }
    return 0;
}
