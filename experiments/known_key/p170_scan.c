/* Rank an unchanged received fragment inside every even complete length.
 * Usage: truncation_scan ct ranks square max_length masked_quad masked_single
 *                        run_label
 * Missing prefix/suffix coordinates remain erasures. No received symbol is
 * replaced, removed, reordered, or filled. Scores are heuristic diagnostics.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAXN 2048
#define TOP 100
static const char SYMBOLS[]="ADFGVX";
static int ct[MAXN],n,key[64],width,map[MAXN];
static char square[37];
static float *quad,single[49];
typedef struct{double score;int length,offset,known,longest;char plaintext[MAXN];}Result;
static Result best[4][TOP];static int counts[4];
static int cmp(const void*a,const void*b){double d=((const Result*)b)->score-((const Result*)a)->score;return d>0?1:d<0?-1:0;}
static int symbol(char c){const char*p=strchr(SYMBOLS,c);return p?(int)(p-SYMBOLS):6;}
static void save(int heap,Result *candidate){int at=counts[heap];if(at>=TOP){at=0;for(int j=1;j<TOP;j++)if(best[heap][j].score<best[heap][at].score)at=j;if(candidate->score<=best[heap][at].score)return;}else counts[heap]++;best[heap][at]=*candidate;}
int main(int argc,char**argv){
 if(argc!=8)return 2;n=strlen(argv[1]);if(n>=MAXN)return 3;for(int i=0;i<n;i++)ct[i]=symbol(argv[1][i]);
 char *ranks=strdup(argv[2]);for(char*t=strtok(ranks,",");t;t=strtok(NULL,",")){if(width>=64)return 3;key[width++]=atoi(t);}free(ranks);
 if(strlen(argv[3])!=36||width<2)return 3;strcpy(square,argv[3]);int maximum=atoi(argv[4]);if(maximum>=MAXN)return 3;
 size_t size=49*49*49*49;quad=malloc(size*sizeof(float));FILE*f=fopen(argv[5],"rb");if(!f||fread(quad,sizeof(float),size,f)!=size)return 4;fclose(f);f=fopen(argv[6],"rb");if(!f||fread(single,sizeof(float),49,f)!=49)return 5;fclose(f);
 unsigned long long trials=0;
 for(int full=n+(n%2);full<=maximum;full+=2){int position=0;
  for(int rank=1;rank<=width;rank++)for(int column=0;column<width;column++)if(key[column]==rank)for(int j=column;j<full;j+=width)map[j]=position++;
  if(position!=full)return 6;
  for(int offset=0;offset+n<=full;offset++){
   int patterns[MAXN],length=full/2,run=0;Result result={0};result.length=full;result.offset=offset;
   for(int j=0;j<length;j++){int a=map[2*j]-offset,b=map[2*j+1]-offset,r=(a>=0&&a<n)?ct[a]:6,c=(b>=0&&b<n)?ct[b]:6;patterns[j]=7*r+c;result.score+=single[patterns[j]];char ch=(r<6&&c<6)?square[6*r+c]:'?';result.plaintext[j]=ch;if(ch!='?'&&ch!='+'){result.known++;run++;if(run>result.longest)result.longest=run;}else run=0;}
   result.plaintext[length]=0;
   for(int j=0;j+3<length;j++)result.score+=quad[((patterns[j]*49+patterns[j+1])*49+patterns[j+2])*49+patterns[j+3]]/4;
   save(0,&result);if(offset==0)save(1,&result);if(offset+n==full)save(2,&result);if(result.longest>=5&&result.known>=12)save(3,&result);trials++;
  }
 }
 printf("{\"type\":\"summary\",\"label\":\"%s\",\"received_length\":%d,\"maximum_length\":%d,\"trials\":%llu}\n",argv[7],n,maximum,trials);
 const char*names[]={"all","prefix","suffix","known_run_at_least5"};
 for(int h=0;h<4;h++){qsort(best[h],counts[h],sizeof(Result),cmp);for(int j=0;j<counts[h];j++){Result*r=&best[h][j];printf("{\"type\":\"candidate\",\"pool\":\"%s\",\"rank\":%d,\"score\":%.8f,\"length\":%d,\"offset\":%d,\"known_letters\":%d,\"longest_known_run\":%d,\"plaintext\":\"%s\"}\n",names[h],j+1,r->score,r->length,r->offset,r->known,r->longest,r->plaintext);}}
 return 0;
}
