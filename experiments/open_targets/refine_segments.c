/* ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro, Apache-2.0 (2026).
 * Language-order refinement of fixed length-segmentation/matching seeds.
 * Exhausts every height-compatible pair order at the current orientations.
 * After screening all seeds, bounded coordinate-pair flips are refined for
 * the retained leaders. Unknown square cells and erased coordinate pairs
 * use an average whole-letter wildcard, solely for heuristic ranking.
 * Exact half-coordinate domains are restored by run_gap.py before acceptance.
 * Input: MODEL K GAP_SIZE KEEP FLIP_ROUNDS, PARTIAL_SQUARE, CIPHERTEXT,
 *        seed count, then GAP and K seed ranks per line.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>
#define MAXK 24
#define MAXPAIR 12
#define MAXN 1024
#define MAXSEED 8192
#define MAXKEEP 100
#define QSIZE 1874161
static const char *CO="ADFGVX", *AL="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
static float model[QSIZE];
static int k,h,n,np,longpairs,q,received,ngap,raw[MAXN],square[36];
static int vectors[MAXPAIR][2][MAXN],order[MAXPAIR],used[MAXPAIR],orientation[MAXPAIR];
static int seedranks[MAXK],bestorder[MAXPAIR],bestorientation[MAXPAIR];
static double best;
static unsigned long long evaluations;
typedef struct {int seed,gap,ranks[MAXK];double score;} Record;
static Record retained[MAXKEEP];static int nkeep,keep;
static int symbol(char c,const char *alphabet){const char *p=strchr(alphabet,c);return p&&c?(int)(p-alphabet):-1;}
static void build(int gap,const int *ranks){
 int padded[MAXN],offsets[MAXK],at=0;
 memcpy(seedranks,ranks,k*sizeof(int));
 for(int i=0;i<received;i++)padded[i+(i>=gap?ngap:0)]=raw[i];
 for(int j=0;j<ngap;j++)padded[gap+j]=-1;
 for(int r=1;r<=k;r++)for(int c=0;c<k;c++)if(ranks[c]==r){offsets[c]=at;at+=q+(c<n%k);}
 for(int p=0;p<h;p++)for(int r=0;r<q+(p<longpairs);r++){
  int a=padded[offsets[2*p]+r],b=padded[offsets[2*p+1]+r];
  for(int flip=0;flip<2;flip++){
   int u=flip?b:a,v=flip?a:b;
   vectors[p][flip][r]=u>=0&&v>=0?square[6*u+v]:36;
  }
 }
}
static double fitness(void){
 int text[MAXN];for(int i=0;i<np;i++){int p=order[i%h];text[i]=vectors[p][orientation[p]][i/h];}
 double score=0;for(int i=0;i+3<np;i++)score+=model[((text[i]*37+text[i+1])*37+text[i+2])*37+text[i+3]];
 evaluations++;return score;
}
static void enumerate(int at){
 if(at==h){double score=fitness();if(score>best){best=score;memcpy(bestorder,order,h*sizeof(int));memcpy(bestorientation,orientation,h*sizeof(int));}return;}
 int begin=at<longpairs?0:longpairs,end=at<longpairs?longpairs:h;
 for(int p=begin;p<end;p++)if(!used[p]){used[p]=1;order[at]=p;enumerate(at+1);used[p]=0;}
}
static void setranks(Record *r){for(int p=0;p<h;p++){int j=bestorder[p],flip=bestorientation[j];r->ranks[2*p]=seedranks[2*j+flip];r->ranks[2*p+1]=seedranks[2*j+1-flip];}r->score=best/(np-3);}
static void retain(Record r){
 int at=nkeep; if(nkeep<keep)nkeep++;else{at=0;for(int i=1;i<nkeep;i++)if(retained[i].score<retained[at].score)at=i;if(r.score<=retained[at].score)return;}
 retained[at]=r;
}
static int compare(const void *x,const void *y){const Record *a=x,*b=y;return a->score>b->score?-1:a->score<b->score?1:a->seed<b->seed?-1:a->seed>b->seed;}
int main(void){
 clock_t start=clock();char path[1024],partial[37],text[MAXN];int fliprounds;
 if(scanf("%1023s%d%d%d%d",path,&k,&ngap,&keep,&fliprounds)!=5||k<2||k>MAXK||k%2||ngap<0||keep<1||keep>MAXKEEP||fliprounds<0)return 2;
 FILE *f=fopen(path,"rb");if(!f||fread(model,sizeof(float),QSIZE,f)!=QSIZE)return 3;fclose(f);
 for(int code=0;code<QSIZE;code++){int value=code,wild=0;for(int j=0;j<4;j++){wild+=value%37==36;value/=37;}model[code]-=wild*log10(36.0);}
 if(scanf("%36s%1023s",partial,text)!=2||strlen(partial)!=36)return 2;
 for(int i=0;i<36;i++){square[i]=symbol(partial[i],AL);if(square[i]<0){if(partial[i]!='?')return 2;square[i]=36;}}
 received=strlen(text);n=received+ngap;np=n/2;h=k/2;q=n/k;longpairs=n%k/2;
 if(n%2||n>=MAXN||np<4)return 2;
 for(int i=0;i<received;i++){raw[i]=symbol(text[i],CO);if(raw[i]<0&&text[i]!='?')return 2;}
 int count;if(scanf("%d",&count)!=1||count<1||count>MAXSEED)return 2;
 for(int s=0;s<count;s++){
  Record r;int ranks[MAXK],seen[MAXK]={0};memset(&r,0,sizeof r);r.seed=s;
  if(scanf("%d",&r.gap)!=1||r.gap<0||r.gap>received)return 2;
  for(int i=0;i<k;i++){if(scanf("%d",ranks+i)!=1||ranks[i]<1||ranks[i]>k||seen[ranks[i]-1]++)return 2;}
  build(r.gap,ranks);memset(orientation,0,sizeof orientation);best=-1e100;enumerate(0);setranks(&r);retain(r);
 }
 for(int r=0;r<nkeep;r++){
  Record *record=&retained[r];build(record->gap,record->ranks);memset(orientation,0,sizeof orientation);best=-1e100;enumerate(0);
  for(int round=0;round<fliprounds;round++){
   double before=best;int startbits[MAXPAIR];memcpy(startbits,bestorientation,sizeof startbits);
   for(int p=0;p<h;p++){memcpy(orientation,startbits,sizeof orientation);orientation[p]^=1;enumerate(0);}
   if(best<=before+1e-8)break;
  }
  setranks(record);
 }
 qsort(retained,nkeep,sizeof(Record),compare);
 for(int i=0;i<nkeep;i++){
  Record *r=&retained[i];build(r->gap,r->ranks);
  printf("{\"kind\":\"candidate\",\"seed_index\":%d,\"score\":%.9f,\"gap_before_source_0based\":%d,\"ranks\":[",r->seed,r->score,r->gap);
  for(int j=0;j<k;j++)printf("%s%d",j?",":"",r->ranks[j]);
  printf("],\"partial_plaintext\":\"");for(int j=0;j<np;j++){int ch=vectors[j%h][0][j/h];putchar(ch==36?'?':AL[ch]);}printf("\"}\n");
 }
 printf("{\"kind\":\"summary\",\"seeds\":%d,\"order_evaluations\":%llu,\"retained\":%d,\"flip_rounds\":%d,\"cpu_seconds\":%.6f}\n",count,evaluations,nkeep,fliprounds,(double)(clock()-start)/CLOCKS_PER_SEC);
 return 0;
}
