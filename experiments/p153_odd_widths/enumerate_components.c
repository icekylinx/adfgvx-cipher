/* Exact post-discovery column/component CSP; works when digraphs cross rows.
 * Each known crib letter has a row variable and a column variable. All cells
 * must be injective. Source chunks are assigned bijectively to physical columns
 * with matching heights. The second crib never prunes the search.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>
#include <math.h>
#define MAXK 26
#define MAXROWS 10
typedef struct {unsigned char chunk,n,letter[MAXROWS];signed char row[MAXROWS],col[MAXROWS];} Candidate;
static Candidate choices[MAXK][MAXK];
static int k,q,e,q2,e2,counts[MAXK],lengths[MAXK],chunks[MAXK][MAXROWS],encoded[132];
static int spec_letter[MAXK][MAXROWS],spec_component[MAXK][MAXROWS],col_order[MAXK],chosen[MAXK];
static int rows[26],cols[26],cell_owner[36];
static char first[67],ct1[133],second[55],ct2[109];
static const char*CO="ADFGVX";
static uint64_t segmentations,feasible,nodes,solutions,histogram[109],max_nodes,max_solutions;
static int stopped,minimum=109;
static const char*stop_reason="completed";
static double max_cpu;
static clock_t start_clock;
static int ci(char c){const char*p=strchr(CO,c);return p&&c?(int)(p-CO):-1;}
static int limit(void){
 if(stopped)return 1;
 if(max_nodes&&nodes>=max_nodes){stopped=1;stop_reason="node_limit";}
 else if(max_solutions&&solutions>=max_solutions){stopped=1;stop_reason="solution_limit";}
 else if(max_cpu>0&&(double)(clock()-start_clock)/CLOCKS_PER_SEC>=max_cpu){stopped=1;stop_reason="cpu_time_limit";}
 return stopped;
}
static int compatible(const Candidate*a,uint32_t used){
 if(used>>a->chunk&1U)return 0;
 int fresh[MAXROWS],nf=0;
 for(int t=0;t<a->n;t++){
  int l=a->letter[t],r=a->row[t],c=a->col[t];
  if(r>=0&&rows[l]>=0&&r!=rows[l])return 0;
  if(c>=0&&cols[l]>=0&&c!=cols[l])return 0;
  if(r<0)r=rows[l];
  if(c<0)c=cols[l];
  if(r>=0&&c>=0){int cell=6*r+c;
   if(cell_owner[cell]>=0&&cell_owner[cell]!=l)return 0;
   for(int z=0;z<nf;z++)if(fresh[z]==cell)return 0;
   fresh[nf++]=cell;
  }
 }
 return 1;
}
static void record(void){
 int byrank[MAXK],offset[MAXK],position=0,indices[108],proposed[108],n=0;
 for(int col=0;col<k;col++)byrank[chosen[col]]=col;
 for(int rank=0;rank<k;rank++){int col=byrank[rank];offset[col]=position;position+=q2+(col<e2);}
 if(position!=108)abort();
 for(int i=0;second[i];i++)if(second[i]!='?'){
  int l=second[i]-'A';if(rows[l]<0||cols[l]<0)abort();
  for(int component=0;component<2;component++){
   int stream=2*i+component,col=stream%k,row=stream/k,index=offset[col]+row,value=component?cols[l]:rows[l];
   if(ci(ct2[index])>=0&&ci(ct2[index])!=value){indices[n]=index;proposed[n++]=value;}
  }
 }
 solutions++;histogram[n]++;if(n<minimum)minimum=n;
 printf("{\"kind\":\"solution\",\"width\":%d,\"ranks\":[",k);
 for(int col=0;col<k;col++)printf("%s%d",col?",":"",chosen[col]+1);
 printf("],\"partial_square\":\"");for(int cell=0;cell<36;cell++)putchar(cell_owner[cell]<0?'?':'A'+cell_owner[cell]);
 printf("\",\"second_crib_known_coordinate_mismatches\":%d,\"edits\":[",n);
 for(int i=0;i<n;i++)printf("%s{\"source_index\":%d,\"observed\":\"%c\",\"proposed\":\"%c\"}",i?",":"",indices[i],ct2[indices[i]],CO[proposed[i]]);
 puts("]}");fflush(stdout);limit();
}
static void search(uint32_t used,uint32_t assigned){
 if(stopped)return;
 if(max_nodes&&nodes>=max_nodes){stopped=1;stop_reason="node_limit";return;}
 nodes++;if((nodes&4095U)==0&&limit())return;
 if(assigned==((1U<<k)-1U)){record();return;}
 int best=-1,best_n=MAXK+1;
 for(int j=0;j<k;j++)if(!(assigned>>j&1U)){
  int n=0;for(int z=0;z<counts[j];z++)n+=compatible(&choices[j][z],used);
  if(!n)return;
  if(n<best_n){best=j;best_n=n;}
 }
 for(int z=0;z<counts[best]&&!stopped;z++){
  Candidate*a=&choices[best][z];if(!compatible(a,used))continue;
  int oldr[MAXROWS],oldc[MAXROWS];
  for(int t=0;t<a->n;t++){
   int l=a->letter[t];oldr[t]=rows[l];oldc[t]=cols[l];
   if(a->row[t]>=0)rows[l]=a->row[t];
   if(a->col[t]>=0)cols[l]=a->col[t];
   if(rows[l]>=0&&cols[l]>=0)cell_owner[6*rows[l]+cols[l]]=l;
  }
  chosen[best]=a->chunk;
  search(used|(1U<<a->chunk),assigned|(1U<<best));
  for(int t=0;t<a->n;t++){
   int l=a->letter[t];
   if((oldr[t]<0||oldc[t]<0)&&rows[l]>=0&&cols[l]>=0)cell_owner[6*rows[l]+cols[l]]=-1;
   rows[l]=oldr[t];cols[l]=oldc[t];
  }
 }
}
static void segmentation(uint32_t mask){
 if(stopped)return;
 if((segmentations&1023U)==0&&limit())return;
 segmentations++;int pos=0;
 for(int chunk=0;chunk<k;chunk++){lengths[chunk]=q+(int)(mask>>chunk&1U);for(int r=0;r<lengths[chunk];r++)chunks[chunk][r]=encoded[pos++];}
 if(pos!=132)abort();
 memset(rows,-1,sizeof rows);memset(cols,-1,sizeof cols);memset(cell_owner,-1,sizeof cell_owner);
 for(int jj=0;jj<k;jj++){
  int j=col_order[jj],len=q+(j<e);counts[j]=0;
  for(int chunk=0;chunk<k;chunk++)if(lengths[chunk]==len){
   int lr[26],lc[26],ok=1;memset(lr,-1,sizeof lr);memset(lc,-1,sizeof lc);
   for(int row=0;row<len;row++){
    int l=spec_letter[j][row];if(l<0)continue;
    int value=chunks[chunk][row],*v=spec_component[j][row]?&lc[l]:&lr[l];
    if(*v>=0&&*v!=value){ok=0;break;}*v=value;
   }
   if(!ok)continue;
   Candidate a={.chunk=(unsigned char)chunk,.n=0};
   for(int l=0;l<26;l++)if(lr[l]>=0||lc[l]>=0){int t=a.n++;a.letter[t]=(unsigned char)l;a.row[t]=(signed char)lr[l];a.col[t]=(signed char)lc[l];}
   if(compatible(&a,0))choices[j][counts[j]++]=a;
  }
  if(!counts[j])return;
 }
 feasible++;search(0,0);
}
static void masks(int start,int remaining,uint32_t mask){
 if(stopped)return;
 if(!remaining){segmentation(mask);return;}
 for(int i=start;i<=k-remaining&&!stopped;i++)masks(i+1,remaining-1,mask|(1U<<i));
}
int main(int argc,char**argv){
 if(argc<3||argc>6){fputs("Usage: enumerate_components INPUT WIDTH [CPU_SECONDS [MAX_NODES [MAX_SOLUTIONS]]]\n",stderr);return 2;}
 char*end;long width=strtol(argv[2],&end,10);if(*end||width<14||width>26)return 2;k=(int)width;
 if(argc>3){max_cpu=strtod(argv[3],&end);if(*end||!isfinite(max_cpu)||max_cpu<0)return 2;}
 if(argc>4){max_nodes=strtoull(argv[4],&end,10);if(*end||argv[4][0]=='-')return 2;}
 if(argc>5){max_solutions=strtoull(argv[5],&end,10);if(*end||argv[5][0]=='-')return 2;}
 q=132/k;e=132%k;q2=108/k;e2=108%k;
 char a[256],b[512],c[256],d[512];FILE*f=fopen(argv[1],"r");if(!f){perror(argv[1]);return 2;}
 int n=fscanf(f,"%255s %511s %255s %511s",a,b,c,d);fclose(f);
 if(n!=4||strlen(a)!=66||strlen(b)!=132||strlen(c)>54||strlen(d)!=108)return 2;
 strcpy(first,a);strcpy(ct1,b);strcpy(second,c);strcpy(ct2,d);int present[26]={0};
 for(int i=0;i<66;i++){if(first[i]!='?'&&(first[i]<'A'||first[i]>'Z'))return 2;if(first[i]!='?')present[first[i]-'A']=1;}
 for(int i=0;second[i];i++)if(second[i]!='?'&&(second[i]<'A'||second[i]>'Z'||!present[second[i]-'A']))return 2;
 for(int i=0;i<132;i++){encoded[i]=ci(ct1[i]);if(encoded[i]<0)return 2;}
 for(int i=0;i<108;i++)if(ct2[i]!='?'&&ci(ct2[i])<0)return 2;
 int repeats[MAXK];
 for(int j=0;j<k;j++){
  int seen[52]={0};repeats[j]=0;col_order[j]=j;
  for(int row=0;row<q+(j<e);row++){
   int index=row*k+j;spec_letter[j][row]=first[index/2]=='?'?-1:first[index/2]-'A';spec_component[j][row]=index%2;
   if(spec_letter[j][row]>=0){int v=2*spec_letter[j][row]+index%2;repeats[j]+=seen[v]++;}
  }
 }
 for(int i=0;i<k;i++)for(int j=i+1;j<k;j++)if(repeats[col_order[j]]>repeats[col_order[i]]){int t=col_order[i];col_order[i]=col_order[j];col_order[j]=t;}
 start_clock=clock();masks(0,e,0);
 char minimum_text[16];if(solutions)snprintf(minimum_text,sizeof minimum_text,"%d",minimum);else strcpy(minimum_text,"null");
 printf("{\"kind\":\"summary\",\"width\":%d,\"complete\":%s,\"stop_reason\":\"%s\",\"segmentations\":%llu,\"locally_feasible_segmentations\":%llu,\"search_nodes\":%llu,\"solutions\":%llu,\"minimum_second_crib_known_coordinate_mismatches\":%s,\"cpu_seconds\":%.6f,\"mismatch_histogram\":{",k,stopped?"false":"true",stop_reason,(unsigned long long)segmentations,(unsigned long long)feasible,(unsigned long long)nodes,(unsigned long long)solutions,minimum_text,(double)(clock()-start_clock)/CLOCKS_PER_SEC);
 int first_entry=1;for(int i=0;i<109;i++)if(histogram[i]){printf("%s\"%d\":%llu",first_entry?"":",",i,(unsigned long long)histogram[i]);first_entry=0;}puts("}}");return 0;
}
