/* Counter-only instrumentation by icekylinx and GPT-6 Astra Pro.
 * Original source SHA256 b45b91e6a776332feee4e3d8207dbb73deb3032a3b1c0ad03af2e64224652168.
 * Search decisions and random-number calls are unchanged.
 */
/* Joint arbitrary column permutation and completion of a partial square.
 * Source-attested square cells are immutable. Remaining plaintext symbols are
 * permuted injectively over the unknown cells. Ciphertext erasures use the
 * 37^4 wildcard marginal model; half-known coordinate information is lost.
 * Input: MODEL K RESTARTS ITERATIONS SEED NMSG, PARTIAL_SQUARE,
 *        K ranks (all zero for random starts), then ciphertexts.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#define MAXK 40
#define MAXM 8
#define MAXN 4096
#define QSIZE 1874161
static const char AL[]="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
static const char CO[]="ADFGVX";
static float model[QSIZE];
static int k,nmsg,ns[MAXM],ct[MAXM][MAXN],perm[MAXK],initial[MAXK];
static int square[36],anchors[36],unknown[36],remaining[36],nu,denominator;
static uint64_t state;
static unsigned long long fitness_calls, annealing_slots, annealing_fitness_calls, polish_fitness_calls;
static uint64_t rn(void){uint64_t z=(state+=0x9e3779b97f4a7c15ULL);z=(z^(z>>30))*0xbf58476d1ce4e5b9ULL;z=(z^(z>>27))*0x94d049bb133111ebULL;return z^(z>>31);}
static int ri(int n){return rn()%n;}
static double ru(void){return(rn()>>11)*0x1.0p-53;}
static int indexof(char c,const char *alphabet){const char*p=strchr(alphabet,c);return p&&c?(int)(p-alphabet):-1;}
static void untranspose(int m,int *cells){
    int n=ns[m],q=n/k,e=n%k,offset[MAXK],position=0,symbols[MAXN];
    for(int r=0;r<k;r++){int col=perm[r];offset[col]=position;position+=q+(col<e);}
    for(int i=0;i<n;i++)symbols[i]=ct[m][offset[i%k]+i/k];
    for(int i=0;i<n/2;i++)cells[i]=symbols[2*i]<0||symbols[2*i+1]<0?-1:6*symbols[2*i]+symbols[2*i+1];
}
static double fitness(void){
    fitness_calls++;
    double score=0;
    for(int m=0;m<nmsg;m++){
        int cells[MAXN],text[MAXN],n=ns[m]/2;untranspose(m,cells);
        for(int i=0;i<n;i++)text[i]=cells[i]<0?36:square[cells[i]];
        for(int i=0;i+3<n;i++)score+=model[((text[i]*37+text[i+1])*37+text[i+2])*37+text[i+3]];
    }
    return score;
}
static void mutate_transposition(void){
    int a=ri(k),b=ri(k),t,mv=ri(20);
    if(mv<10){t=perm[a];perm[a]=perm[b];perm[b]=t;}
    else if(mv<16){t=perm[a];if(a<b)for(int j=a;j<b;j++)perm[j]=perm[j+1];else for(int j=a;j>b;j--)perm[j]=perm[j-1];perm[b]=t;}
    else if(mv<18){if(a>b){t=a;a=b;b=t;}while(a<b){t=perm[a];perm[a++]=perm[b];perm[b--]=t;}}
    else{
        a=2*ri(k/2);b=2*ri(k/2);
        for(int j=0;j<k;j++){if(perm[j]==a)perm[j]=b;else if(perm[j]==b)perm[j]=a;else if(perm[j]==a+1)perm[j]=b+1;else if(perm[j]==b+1)perm[j]=a+1;}
    }
}
static void emit(double score,int restart){
    int ranks[MAXK];char sq[37];for(int i=0;i<k;i++)ranks[perm[i]]=i+1;
    for(int i=0;i<36;i++)sq[i]=AL[square[i]];
    sq[36]=0;
    printf("{\"score\":%.9f,\"restart\":%d,\"known_square_cells\":%d,\"square\":\"%s\",\"ranks\":[",score/denominator,restart,36-nu,sq);
    for(int i=0;i<k;i++)printf("%s%d",i?",":"",ranks[i]);
    printf("],\"plaintexts\":[");
    for(int m=0;m<nmsg;m++){
        int cells[MAXN];untranspose(m,cells);if(m)putchar(',');putchar('"');
        for(int i=0;i<ns[m]/2;i++)putchar(cells[i]<0?'?':AL[square[cells[i]]]);
        putchar('"');
    }
    printf("]}\n");fflush(stdout);
}
int main(void){
    char path[1024],partial[64],buf[MAXN];int restarts,iters;unsigned long long seed;
    if(scanf("%1023s%d%d%d%llu%d",path,&k,&restarts,&iters,&seed,&nmsg)!=6||k<2||k>MAXK||nmsg<1||nmsg>MAXM||restarts<1||iters<1)return 2;
    FILE*f=fopen(path,"rb");if(!f||fread(model,sizeof(float),QSIZE,f)!=QSIZE)return 3;fclose(f);
    if(scanf("%36s",partial)!=1||strlen(partial)!=36)return 2;
    int used[36]={0};
    for(int i=0;i<36;i++){
        anchors[i]=indexof(partial[i],AL);
        if(anchors[i]<0&&partial[i]!='?')return 2;
        if(anchors[i]<0)unknown[nu++]=i;
        else if(used[anchors[i]]++)return 2;
    }
    int nr=0;for(int i=0;i<36;i++)if(!used[i])remaining[nr++]=i;if(nr!=nu)return 2;
    int hasinitial=1,seen[MAXK]={0},nonzero=0;
    for(int i=0;i<k;i++){
        int rank;if(scanf("%d",&rank)!=1||rank<0||rank>k)return 2;
        if(!rank)hasinitial=0;else{if(seen[rank-1]++)return 2;initial[rank-1]=i;nonzero++;}
    }
    if(nonzero&&nonzero!=k)return 2;
    for(int m=0;m<nmsg;m++){
        if(scanf("%4095s",buf)!=1)return 2;
        ns[m]=strlen(buf);if(ns[m]%2||ns[m]<8)return 2;
        for(int i=0;i<ns[m];i++){
            ct[m][i]=indexof(buf[i],CO);if(ct[m][i]<0&&buf[i]!='?')return 2;
        }
        denominator+=ns[m]/2-3;
    }
    state=seed;double global=-1e100,printed=-1e100;int globalperm[MAXK],globalsquare[36];
    for(int rs=0;rs<restarts;rs++){
        memcpy(square,anchors,sizeof square);for(int i=0;i<nu;i++)square[unknown[i]]=remaining[i];
        for(int i=nu-1;i>0;i--){int j=ri(i+1),a=unknown[i],b=unknown[j],t=square[a];square[a]=square[b];square[b]=t;}
        if(rs&&rs%4==1){memcpy(perm,globalperm,sizeof perm);memcpy(square,globalsquare,sizeof square);for(int j=0;j<2+ri(5);j++)mutate_transposition();}
        else if(hasinitial&&rs%4==0){memcpy(perm,initial,sizeof perm);for(int j=0;j<rs%9;j++)mutate_transposition();}
        else{for(int i=0;i<k;i++)perm[i]=i;for(int i=k-1;i>0;i--){int j=ri(i+1),t=perm[i];perm[i]=perm[j];perm[j]=t;}}
        double cur=fitness(),best=cur;int bp[MAXK],bs[36];memcpy(bp,perm,sizeof perm);memcpy(bs,square,sizeof square);
        for(int it=0;it<iters;it++){
            annealing_slots++;
            int save[MAXK],a=0,b=0,t=0,type=nu>1&&ri(5)==0;
            if(type){a=unknown[ri(nu)];b=unknown[ri(nu)];if(a==b)continue;t=square[a];square[a]=square[b];square[b]=t;}
            else{memcpy(save,perm,sizeof perm);mutate_transposition();}
            annealing_fitness_calls++;
            double value=fitness(),temperature=5.0*pow(.015,(double)it/iters);
            if(value>=cur||ru()<exp((value-cur)/temperature))cur=value;
            else if(type){t=square[a];square[a]=square[b];square[b]=t;}
            else memcpy(perm,save,sizeof perm);
            if(cur>best){best=cur;memcpy(bp,perm,sizeof perm);memcpy(bs,square,sizeof square);}
        }
        memcpy(perm,bp,sizeof perm);memcpy(square,bs,sizeof square);cur=best;
        for(int pass=0;pass<2;pass++){
            int changed=0;
            for(int a=0;a<k;a++)for(int b=a+1;b<k;b++){
                int t=perm[a];perm[a]=perm[b];perm[b]=t;double value=fitness();polish_fitness_calls++;
                if(value>cur+1e-8){cur=value;changed=1;}else{t=perm[a];perm[a]=perm[b];perm[b]=t;}
            }
            for(int i=0;i<nu;i++)for(int j=i+1;j<nu;j++){
                int a=unknown[i],b=unknown[j],t=square[a];square[a]=square[b];square[b]=t;double value=fitness();polish_fitness_calls++;
                if(value>cur+1e-8){cur=value;changed=1;}else{t=square[a];square[a]=square[b];square[b]=t;}
            }
            if(!changed)break;
        }
        if(cur>global){global=cur;memcpy(globalperm,perm,sizeof perm);memcpy(globalsquare,square,sizeof square);}
        memcpy(perm,globalperm,sizeof perm);memcpy(square,globalsquare,sizeof square);
        if(global>printed+1e-7){emit(global,rs);printed=global;}
    }
    fprintf(stderr,"{\"completed_restarts\":%d,\"annealing_slots\":%llu,\"annealing_fitness_calls\":%llu,\"polish_fitness_calls\":%llu,\"total_fitness_calls\":%llu}\n", restarts, annealing_slots, annealing_fitness_calls, polish_fitness_calls, fitness_calls);
    return 0;
}
