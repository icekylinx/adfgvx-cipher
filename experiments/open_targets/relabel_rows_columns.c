/* ADFGVX Cipher. icekylinx and GPT-6 Astra Pro (2026). Apache-2.0.
 * Exhaustive independent row and column relabelings of a published square,
 * with both pair orientations, fixed published ranks, and optional one
 * contiguous unknown gap. No observed ciphertext coordinate is changed.
 * The language objective is only a ranking heuristic; whole-letter wildcard
 * means discard known half-coordinate information during ranking.
 * Input: MODEL37 K GAP_SIZE GAP_STEP KEEP, PARTIAL_SQUARE, K ranks, CIPHERTEXT.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>
#define MAXK 40
#define MAXN 4096
#define MAXKEEP 100
#define QSIZE 1874161
static const char *CO="ADFGVX",*AL="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
static float model[QSIZE];
static int permutations[720][6],countperm,k,n,received,ngap,step,keep,raw[MAXN],ranks[MAXK],base[36];
static unsigned long long evaluations;
typedef struct{double score;int gap,row,col,swap;}Candidate;
static Candidate best[MAXKEEP];static int nb;
static int indexof(char c,const char *alphabet){const char*p=strchr(alphabet,c);return p&&c?(int)(p-alphabet):-1;}
static void generate(int at,int *p,int mask){if(at==6){memcpy(permutations[countperm++],p,6*sizeof(int));return;}for(int i=0;i<6;i++)if(!(mask&(1<<i))){p[at]=i;generate(at+1,p,mask|(1<<i));}}
static int compare(const void*a,const void*b){const Candidate*x=a,*y=b;return x->score>y->score?-1:x->score<y->score?1:x->gap-y->gap;}
static void retain(Candidate c){int at=nb;if(nb<keep)nb++;else{at=0;for(int i=1;i<nb;i++)if(best[i].score<best[at].score)at=i;if(c.score<=best[at].score)return;}best[at]=c;}
static void interim(int gap,int *first,int *second){int padded[MAXN],offset[MAXK],at=0,symbols[MAXN];
 for(int i=0;i<n;i++)padded[i]=i<gap?raw[i]:i<gap+ngap?-1:raw[i-ngap];
 for(int rank=1;rank<=k;rank++)for(int col=0;col<k;col++)if(ranks[col]==rank){offset[col]=at;at+=n/k+(col<n%k);}
 for(int i=0;i<n;i++)symbols[i]=padded[offset[i%k]+i/k];
 for(int i=0;i<n/2;i++){first[i]=symbols[2*i];second[i]=symbols[2*i+1];}}
static void mapped(int row,int col,int swap,int *square){for(int a=0;a<6;a++)for(int b=0;b<6;b++)square[6*a+b]=base[6*permutations[row][swap?b:a]+permutations[col][swap?a:b]];}
int main(void){char path[1024],sq[37],ct[MAXN];int p[6];clock_t start=clock();
 if(scanf("%1023s%d%d%d%d",path,&k,&ngap,&step,&keep)!=5||k<2||k>MAXK||ngap<0||ngap>32||step<1||keep<1||keep>MAXKEEP)return 2;
 FILE*f=fopen(path,"rb");if(!f||fread(model,sizeof(float),QSIZE,f)!=QSIZE)return 3;fclose(f);
 for(int code=0;code<QSIZE;code++){int v=code,w=0;for(int i=0;i<4;i++){w+=v%37==36;v/=37;}model[code]-=w*log10(36.0);}
 if(scanf("%36s",sq)!=1||strlen(sq)!=36)return 2;int used[36]={0};for(int i=0;i<36;i++){base[i]=indexof(sq[i],AL);if(base[i]<0){if(sq[i]!='?')return 2;base[i]=36;}else if(used[base[i]]++)return 2;}
 int seen[MAXK]={0};for(int i=0;i<k;i++)if(scanf("%d",ranks+i)!=1||ranks[i]<1||ranks[i]>k||seen[ranks[i]-1]++)return 2;
 if(scanf("%4095s",ct)!=1)return 2;received=strlen(ct);n=received+ngap;if(n%2||n<8||n>=MAXN)return 2;
 for(int i=0;i<received;i++){raw[i]=indexof(ct[i],CO);if(raw[i]<0&&ct[i]!='?')return 2;}
 generate(0,p,0);if(countperm!=720)return 4;
 for(int gap=0;gap<=(ngap?received:0);gap+=step){int a[MAXN],b[MAXN];interim(gap,a,b);
  for(int swap=0;swap<2;swap++)for(int row=0;row<720;row++)for(int col=0;col<720;col++){
   int square[36],text[MAXN];mapped(row,col,swap,square);
   for(int i=0;i<n/2;i++)text[i]=a[i]<0||b[i]<0?36:square[6*a[i]+b[i]];
   double score=0;for(int i=0;i+3<n/2;i++)score+=model[((text[i]*37+text[i+1])*37+text[i+2])*37+text[i+3]];
   evaluations++;Candidate c={score/(n/2-3),gap,row,col,swap};retain(c);
  }
 }
 qsort(best,nb,sizeof(Candidate),compare);
 for(int j=0;j<nb;j++){Candidate*c=best+j;int a[MAXN],b[MAXN],square[36];interim(c->gap,a,b);mapped(c->row,c->col,c->swap,square);
  printf("{\"kind\":\"candidate\",\"score\":%.9f,\"gap_before_source_0based\":%d,\"row_relabeling\":\"",c->score,c->gap);
  for(int i=0;i<6;i++)putchar(CO[permutations[c->row][i]]);printf("\",\"column_relabeling\":\"");for(int i=0;i<6;i++)putchar(CO[permutations[c->col][i]]);
  printf("\",\"swapped_pair_orientation\":%s,\"effective_partial_square\":\"",c->swap?"true":"false");for(int i=0;i<36;i++)putchar(square[i]==36?'?':AL[square[i]]);
  printf("\",\"partial_plaintext\":\"");for(int i=0;i<n/2;i++)putchar(a[i]<0||b[i]<0||square[6*a[i]+b[i]]==36?'?':AL[square[6*a[i]+b[i]]]);printf("\"}\n");
 }
 printf("{\"kind\":\"summary\",\"evaluations\":%llu,\"gap_size\":%d,\"gap_step\":%d,\"received_slots\":%d,\"cpu_seconds\":%.6f}\n",evaluations,ngap,step,received,(double)(clock()-start)/CLOCKS_PER_SEC);
 return 0;}
