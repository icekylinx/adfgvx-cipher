/* ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro, 2026.
 * Apache-2.0. Derived from experiments/joint_search/src/anchored_joint.c.
 * Bounded joint search for column order, one transferred known group,
 * and an injective completion of an anchored square. Known half-coordinates
 * are preserved in scoring. No historical decryption is implied by a score.
 * Input: MODEL K RESTARTS ITERATIONS SEED GAP_SIZE FIXED_GAP,
 *        PARTIAL_SQUARE, K ranks (all zero for random starts), CIPHERTEXT, GROUP.
 * The literal GROUP is inserted at a variable boundary without editing source.
 * FIXED_GAP=-1 searches every coordinate boundary; otherwise fixes it.
 * The score averages quadgram probability over exact coordinate domains.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#define MAXK 40
#define MAXN 4096
#define QSIZE 1679616
static const char AL[]="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",CO[]="ADFGVX";
static float model[QSIZE];static double probability[QSIZE];
static int k,n,received,raw[MAXN],gap,ngap,fixedgap,perm[MAXK],initial[MAXK];
static int group[12];
static int square[36],anchors[36],unknown[36],remaining[36],nu;
static uint64_t state;
static uint64_t rn(void){uint64_t z=(state+=0x9e3779b97f4a7c15ULL);z=(z^(z>>30))*0xbf58476d1ce4e5b9ULL;z=(z^(z>>27))*0x94d049bb133111ebULL;return z^(z>>31);}
static int ri(int m){return rn()%m;}static double ru(void){return(rn()>>11)*0x1.0p-53;}
static int indexof(char c,const char *alphabet){const char*p=strchr(alphabet,c);return p&&c?(int)(p-alphabet):-1;}
static int getsource(int p){if(p<gap)return raw[p];if(p<gap+ngap)return group[p-gap];return raw[p-ngap];}
static void untranspose(int *dom){int q=n/k,e=n%k,offset[MAXK],position=0,symbols[MAXN];
 for(int r=0;r<k;r++){int col=perm[r];offset[col]=position;position+=q+(col<e);}
 for(int i=0;i<n;i++)symbols[i]=getsource(offset[i%k]+i/k);
 for(int i=0;i<n/2;i++){int a=symbols[2*i],b=symbols[2*i+1];dom[i]=a>=0?(b>=0?6*a+b:36+a):(b>=0?42+b:48);}}
static double fitness(void){int dom[MAXN],values[49][36],sizes[49];untranspose(dom);
 for(int d=0;d<36;d++){sizes[d]=1;values[d][0]=square[d];}
 for(int d=0;d<6;d++){sizes[36+d]=sizes[42+d]=6;for(int j=0;j<6;j++){values[36+d][j]=square[6*d+j];values[42+d][j]=square[6*j+d];}}
 sizes[48]=36;for(int j=0;j<36;j++)values[48][j]=j;
 double score=0;
 for(int i=0;i+3<n/2;i++){int a=dom[i],b=dom[i+1],c=dom[i+2],d=dom[i+3];
  if(a<36&&b<36&&c<36&&d<36){score+=model[((square[a]*36+square[b])*36+square[c])*36+square[d]];continue;}
  double sum=0;int count=sizes[a]*sizes[b]*sizes[c]*sizes[d];
  for(int j=0;j<sizes[a];j++)for(int l=0;l<sizes[b];l++)for(int h=0;h<sizes[c];h++){int code=((values[a][j]*36+values[b][l])*36+values[c][h])*36;for(int v=0;v<sizes[d];v++)sum+=probability[code+values[d][v]];}
  score+=log10(sum/count);
 }return score;}
static void mutate_transposition(void){int a=ri(k),b=ri(k),t,mv=ri(20);
 if(mv<9){t=perm[a];perm[a]=perm[b];perm[b]=t;}
 else if(mv<15){t=perm[a];if(a<b)for(int j=a;j<b;j++)perm[j]=perm[j+1];else for(int j=a;j>b;j--)perm[j]=perm[j-1];perm[b]=t;}
 else if(mv<17){if(a>b){t=a;a=b;b=t;}while(a<b){t=perm[a];perm[a++]=perm[b];perm[b--]=t;}}
 else{a=2*ri(k/2);b=2*ri(k/2);for(int j=0;j<k;j++){if(perm[j]==a)perm[j]=b;else if(perm[j]==b)perm[j]=a;else if(perm[j]==a+1)perm[j]=b+1;else if(perm[j]==b+1)perm[j]=a+1;}}}
static void mutate_gap(void){if(fixedgap>=0||!ngap)return;if(ri(3))gap=ri(received+1);else{gap+=(ri(2)?1:-1)*(1+ri(6));if(gap<0)gap=0;if(gap>received)gap=received;}}
static void emit(double score,int restart){int ranks[MAXK],dom[MAXN];char sq[37];for(int i=0;i<k;i++)ranks[perm[i]]=i+1;for(int i=0;i<36;i++)sq[i]=AL[square[i]];sq[36]=0;
 printf("{\"score\":%.9f,\"restart\":%d,\"known_square_cells\":%d,\"square\":\"%s\",\"gap_before_source_0based\":%d,\"gap_size\":%d,\"ranks\":[",score/(n/2-3),restart,36-nu,sq,gap,ngap);
 for(int i=0;i<k;i++)printf("%s%d",i?",":"",ranks[i]);printf("],\"plaintext\":\"");untranspose(dom);for(int i=0;i<n/2;i++)putchar(dom[i]<36?AL[square[dom[i]]]:'?');printf("\"}\n");fflush(stdout);}
int main(void){char path[1024],partial[64],buf[MAXN];int restarts,iters;unsigned long long seed;
 if(scanf("%1023s%d%d%d%llu%d%d",path,&k,&restarts,&iters,&seed,&ngap,&fixedgap)!=7||k<2||k>MAXK||restarts<1||iters<1||ngap<0||ngap>12)return 2;
 FILE*f=fopen(path,"rb");if(!f||fread(model,sizeof(float),QSIZE,f)!=QSIZE)return 3;fclose(f);for(int i=0;i<QSIZE;i++)probability[i]=pow(10.0,model[i]);
 if(scanf("%36s",partial)!=1||strlen(partial)!=36)return 2;int used[36]={0};
 for(int i=0;i<36;i++){anchors[i]=indexof(partial[i],AL);if(anchors[i]<0&&partial[i]!='?')return 2;if(anchors[i]<0)unknown[nu++]=i;else if(used[anchors[i]]++)return 2;}
 int nr=0;for(int i=0;i<36;i++)if(!used[i])remaining[nr++]=i;if(nr!=nu)return 2;
 int hasinitial=1,seen[MAXK]={0},nonzero=0;for(int i=0;i<k;i++){int rank;if(scanf("%d",&rank)!=1||rank<0||rank>k)return 2;if(!rank)hasinitial=0;else{if(seen[rank-1]++)return 2;initial[rank-1]=i;nonzero++;}}if(nonzero&&nonzero!=k)return 2;
 if(scanf("%4095s",buf)!=1)return 2;received=strlen(buf);n=received+ngap;if(n%2||n<8||n>=MAXN||fixedgap>received||fixedgap< -1)return 2;
 for(int i=0;i<received;i++){raw[i]=indexof(buf[i],CO);if(raw[i]<0&&buf[i]!='?')return 2;}
 if(scanf("%12s",buf)!=1||strlen(buf)!=ngap)return 2;
 for(int i=0;i<ngap;i++){group[i]=indexof(buf[i],CO);if(group[i]<0)return 2;}
 state=seed;double global=-1e100,printed=-1e100;int globalperm[MAXK],globalsquare[36],globalgap=0;
 for(int rs=0;rs<restarts;rs++){memcpy(square,anchors,sizeof square);for(int i=0;i<nu;i++)square[unknown[i]]=remaining[i];for(int i=nu-1;i>0;i--){int j=ri(i+1),a=unknown[i],b=unknown[j],t=square[a];square[a]=square[b];square[b]=t;}
 gap=fixedgap>=0?fixedgap:(ngap?ri(received+1):0);
 if(rs&&rs%4==1){memcpy(perm,globalperm,sizeof perm);memcpy(square,globalsquare,sizeof square);gap=globalgap;for(int j=0;j<2+ri(5);j++)mutate_transposition();if(ri(2))mutate_gap();}
 else if(hasinitial&&rs%4==0){memcpy(perm,initial,sizeof perm);for(int j=0;j<rs%9;j++)mutate_transposition();}
 else{for(int i=0;i<k;i++)perm[i]=i;for(int i=k-1;i>0;i--){int j=ri(i+1),t=perm[i];perm[i]=perm[j];perm[j]=t;}}
 double cur=fitness(),best=cur;int bp[MAXK],bs[36],bg=gap;memcpy(bp,perm,sizeof perm);memcpy(bs,square,sizeof square);
 for(int it=0;it<iters;it++){int save[MAXK],a=0,b=0,t=0,savegap=gap,type=ri(10);if(type<2&&nu>1){a=unknown[ri(nu)];b=unknown[ri(nu)];if(a==b)continue;t=square[a];square[a]=square[b];square[b]=t;type=1;}
 else if(type==2&&ngap&&fixedgap<0){mutate_gap();type=2;}else{memcpy(save,perm,sizeof perm);mutate_transposition();type=0;}
 double value=fitness(),temperature=5.0*pow(.015,(double)it/iters);
 if(value>=cur||ru()<exp((value-cur)/temperature))cur=value;else if(type==1){t=square[a];square[a]=square[b];square[b]=t;}else if(type==2)gap=savegap;else memcpy(perm,save,sizeof perm);
 if(cur>best){best=cur;memcpy(bp,perm,sizeof perm);memcpy(bs,square,sizeof square);bg=gap;}}
 memcpy(perm,bp,sizeof perm);memcpy(square,bs,sizeof square);gap=bg;cur=best;
 for(int pass=0;pass<2;pass++){int changed=0;for(int a=0;a<k;a++)for(int b=a+1;b<k;b++){int t=perm[a];perm[a]=perm[b];perm[b]=t;double v=fitness();if(v>cur+1e-8){cur=v;changed=1;}else{t=perm[a];perm[a]=perm[b];perm[b]=t;}}
 for(int i=0;i<nu;i++)for(int j=i+1;j<nu;j++){int a=unknown[i],b=unknown[j],t=square[a];square[a]=square[b];square[b]=t;double v=fitness();if(v>cur+1e-8){cur=v;changed=1;}else{t=square[a];square[a]=square[b];square[b]=t;}}
 if(ngap&&fixedgap<0){int savedgap=gap;for(int g=0;g<=received;g++){gap=g;double v=fitness();if(v>cur+1e-8){cur=v;savedgap=g;changed=1;}}gap=savedgap;}if(!changed)break;}
 if(cur>global){global=cur;memcpy(globalperm,perm,sizeof perm);memcpy(globalsquare,square,sizeof square);globalgap=gap;}
 memcpy(perm,globalperm,sizeof perm);memcpy(square,globalsquare,sizeof square);gap=globalgap;if(global>printed+1e-7){emit(global,rs);printed=global;}}
 return 0;}
