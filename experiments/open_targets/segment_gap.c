/* ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro (2026), Apache-2.0.
 * Exact length-segmentation and monogram matching screen for even-width
 * anchored-square hypotheses. A retained matching is a heuristic seed only.
 * Reads: K GAP_SIZE GAP_STEP KEEP, partial square, 36 positive monograms,
 * ciphertext, evaluation-only gap (-1 if absent), K evaluation ranks.
 * The evaluation key has no effect on scores, pruning, or retained candidates.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include <time.h>
#define MAXK 24
#define MAXN 1024
#define MAXSTATE 1400
#define MAXH 80
#define MAXCLASS 18
#define MAXKEEP 8192
typedef struct{int valid,col,kind,height; signed char symbol[MAXH];} Column;
typedef struct{double score;unsigned mask;int gap,ranks[MAXK];} Record;
static const char *CO="ADFGVX",*AL="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
static int k,n,e,q,received,raw[MAXN],padded[MAXN],ngap,gapstep,keep,nkept;
static char partial[37];static double mono[36],logcell[49],weight[MAXSTATE][MAXSTATE];
static Column cols[MAXSTATE];static Record heap[MAXKEEP];
static int groupids[MAXK],groupsize,choice[1<<MAXCLASS],stamp[1<<MAXCLASS],epoch;
static double dp[1<<MAXCLASS];static int orient[MAXSTATE][MAXSTATE];
static int gap,truthgap,truthranks[MAXK];static unsigned truthmask;static double truthscore=-1e100,truthbest=-1e100;
static uint64_t total,better,tied;static Record bestrecord;
static int cid(int i,int a,int type){return ((i*(e+1)+a)*2+type);}
static int symbol(char c){const char*p=strchr(CO,c);return p&&c?(int)(p-CO):-1;}
static void swap(Record*a,Record*b){Record t=*a;*a=*b;*b=t;}
static void retain(Record r){if(nkept<keep){int i=nkept++;heap[i]=r;while(i&&heap[i].score<heap[(i-1)/2].score){swap(heap+i,heap+(i-1)/2);i=(i-1)/2;}}
 else if(r.score>heap[0].score){heap[0]=r;int i=0;for(;;){int j=2*i+1;if(j>=nkept)break;if(j+1<nkept&&heap[j+1].score<heap[j].score)j++;if(heap[i].score<=heap[j].score)break;swap(heap+i,heap+j);i=j;}}}
static double matching(unsigned mask){if(!mask)return 0;if(stamp[mask]==epoch)return dp[mask];stamp[mask]=epoch;
 int a=__builtin_ctz(mask);unsigned rest=mask^(1U<<a);double best=-1e100;int pick=-1;
 for(unsigned choices=rest;choices;choices&=choices-1){int b=__builtin_ctz(choices);double score=weight[groupids[a]][groupids[b]]+matching(rest^(1U<<b));if(score>best){best=score;pick=b;}}
 choice[mask]=pick;return dp[mask]=best;}
static Record evaluate(unsigned mask){Record r;memset(&r,0,sizeof r);r.mask=mask;r.gap=gap;int ids[2][MAXK],sizes[2]={0},a=0;
 for(int i=0;i<k;i++){int type=(mask>>i)&1;ids[type][sizes[type]++]=cid(i,a,type);a+=type;}
 int at=0;for(int type=1;type>=0;type--){groupsize=sizes[type];memcpy(groupids,ids[type],groupsize*sizeof(int));epoch++;
 unsigned rest=(1U<<groupsize)-1;r.score+=matching(rest);
 while(rest){int x=__builtin_ctz(rest),y=choice[rest],u=groupids[x],v=groupids[y];if(orient[u][v]){int t=u;u=v;v=t;}r.ranks[at++]=cols[u].col+1;r.ranks[at++]=cols[v].col+1;rest^=(1U<<x)|(1U<<y);}}
 return r;}
static void prepare(void){int states=k*(e+1)*2;memset(cols,0,sizeof cols);
 for(int i=0;i<received;i++)padded[i+(i>=gap?ngap:0)]=raw[i];for(int j=0;j<ngap;j++)padded[gap+j]=-1;
 for(int i=0;i<k;i++)for(int a=0;a<=e;a++){int b=i-a;if(b<0||b>k-e)continue;for(int type=0;type<2;type++){
 if((type&&a==e)||(!type&&b==k-e))continue;int id=cid(i,a,type),h=q+type,start=q*i+a;Column*c=&cols[id];c->valid=1;c->col=i;c->kind=type;c->height=h;for(int j=0;j<h;j++)c->symbol[j]=padded[start+j];}}
 for(int a=0;a<states;a++)if(cols[a].valid)for(int b=a+1;b<states;b++)if(cols[b].valid&&cols[a].kind==cols[b].kind){
 double ab=0,ba=0;for(int j=0;j<cols[a].height;j++){int u=cols[a].symbol[j],v=cols[b].symbol[j];int x=u>=0?(v>=0?6*u+v:36+u):(v>=0?42+v:48);int y=v>=0?(u>=0?6*v+u:36+v):(u>=0?42+u:48);ab+=logcell[x];ba+=logcell[y];}
 weight[a][b]=weight[b][a]=ab>=ba?ab:ba;orient[a][b]=ab<ba;orient[b][a]=ab>=ba;}}
static int compare(const void*x,const void*y){const Record*a=x,*b=y;return a->score>b->score?-1:a->score<b->score?1:a->gap<b->gap?-1:a->gap>b->gap?1:a->mask<b->mask?-1:a->mask>b->mask;}
static void scan(int collect){for(gap=0;gap<=received;gap+=gapstep){prepare();unsigned mask=e?(1U<<e)-1:0,limit=1U<<k;for(;;){Record r=evaluate(mask);if(collect){total++;if(truthgap>=0){better+=r.score>truthbest+1e-10;tied+=fabs(r.score-truthbest)<=1e-10;}retain(r);if(r.score>bestrecord.score)bestrecord=r;}
 if(!collect&&gap==truthgap&&mask==truthmask){truthbest=r.score;return;}
 if(!e)break;unsigned lo=mask&-mask,next=mask+lo;if(next>=limit)break;mask=next+(((next^mask)/lo)>>2);}}
}
int main(void){clock_t start=clock();if(scanf("%d%d%d%d",&k,&ngap,&gapstep,&keep)!=4||k<2||k>MAXK||k%2||ngap<0||gapstep<1||keep<1||keep>MAXKEEP)return 2;
 if(scanf("%36s",partial)!=1||strlen(partial)!=36)return 2;int used[36]={0},missing=0;for(int i=0;i<36;i++){const char*p=strchr(AL,partial[i]);if(partial[i]=='?'){missing++;continue;}if(!p||used[p-AL]++)return 2;}
 double sum=0,unused=0;for(int i=0;i<36;i++){if(scanf("%lf",mono+i)!=1||mono[i]<=0)return 2;sum+=mono[i];if(!used[i])unused+=mono[i];}
 double prob[36];for(int i=0;i<36;i++)prob[i]=partial[i]=='?'?unused/(missing*sum):mono[strchr(AL,partial[i])-AL]/sum;
 for(int i=0;i<36;i++)logcell[i]=log10(prob[i]);for(int i=0;i<6;i++){double a=0,b=0;for(int j=0;j<6;j++){a+=prob[6*i+j];b+=prob[6*j+i];}logcell[36+i]=log10(a/6);logcell[42+i]=log10(b/6);}logcell[48]=-log10(36.0);
 char text[MAXN];if(scanf("%1023s%d",text,&truthgap)!=2)return 2;received=strlen(text);n=received+ngap;e=n%k;q=n/k;if(n%2||e%2||e>MAXCLASS||k-e>MAXCLASS||q+1>MAXH||n>=MAXN||truthgap>received||truthgap< -1||k*(e+1)*2>MAXSTATE)return 2;
 for(int i=0;i<received;i++){raw[i]=symbol(text[i]);if(raw[i]<0&&text[i]!='?')return 2;}
 int seen[MAXK]={0};for(int i=0;i<k;i++){if(scanf("%d",truthranks+i)!=1)return 2;if(truthgap>=0){int rank=truthranks[i];if(rank<1||rank>k||seen[rank-1]++)return 2;if(i<e)truthmask|=1U<<(rank-1);}}
 bestrecord.score=-1e100;if(truthgap>=0){if(truthgap%gapstep)return 2;gap=truthgap;prepare();Record r=evaluate(truthmask);truthbest=r.score;
 int offsets[MAXK],at=0;for(int rank=1;rank<=k;rank++)for(int c=0;c<k;c++)if(truthranks[c]==rank){offsets[c]=at;at+=q+(c<e);}truthscore=0;
 for(int p=0;p<n;p+=2){int a=padded[offsets[p%k]+p/k],b=padded[offsets[(p+1)%k]+(p+1)/k];int d=a>=0?(b>=0?6*a+b:36+a):(b>=0?42+b:48);truthscore+=logcell[d];}}
 scan(1);qsort(heap,nkept,sizeof(Record),compare);for(int i=0;i<nkept;i++){Record*r=heap+i;printf("{\"kind\":\"candidate\",\"monogram_score\":%.12f,\"gap_before_source_0based\":%d,\"long_mask\":%u,\"ranks\":[",r->score,r->gap,r->mask);for(int j=0;j<k;j++)printf("%s%d",j?",":"",r->ranks[j]);printf("]}\n");}
 printf("{\"kind\":\"summary\",\"width\":%d,\"enumerated_gap_segmentations\":%llu,\"gap_step\":%d,\"retained\":%d,\"truth_geometry_best_matching_score\":%.12f,\"truth_pairing_score\":%.12f,\"strictly_better_geometries_than_truth\":%llu,\"tied_geometries_with_truth\":%llu,\"cpu_seconds\":%.6f}\n",k,(unsigned long long)total,gapstep,nkept,truthbest,truthscore,(unsigned long long)better,(unsigned long long)tied,(double)(clock()-start)/CLOCKS_PER_SEC);return 0;}
