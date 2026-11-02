/* ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro (2026), Apache-2.0.
 * Fixed transposition, anchored square, and M separately located missing
 * coordinates. Shared exact-domain scorer with gap_anchored.c.
 * Input: MODEL K RESTARTS ITERATIONS SEED M, partial square, K ranks, source.
 * This is a bounded stochastic deletion-channel search, not an exclusion.
 */
#define main unused_contiguous_gap_entry_point
#include "gap_anchored.c"
#undef main
#define MAXLOSS 12
static int sourcetext[MAXN],source_length,loss_count,losses[MAXLOSS];
static int compare_int(const void*a,const void*b){return *(const int*)a-*(const int*)b;}
static void pad_source(void){int at=0,j=0;for(int i=0;i<n;i++){if(j<loss_count&&losses[j]==i){raw[i]=-1;j++;}else raw[i]=sourcetext[at++];}}
static void random_losses(void){for(int i=0;i<loss_count;i++){int ok;do{losses[i]=ri(n);ok=1;for(int j=0;j<i;j++)if(losses[j]==losses[i])ok=0;}while(!ok);}qsort(losses,loss_count,sizeof(int),compare_int);}
static int move_loss(void){int at=ri(loss_count),v=ri(3)?ri(n):losses[at]+(ri(2)?1:-1)*(1+ri(6));if(v<0||v>=n)return 0;for(int i=0;i<loss_count;i++)if(i!=at&&losses[i]==v)return 0;losses[at]=v;qsort(losses,loss_count,sizeof(int),compare_int);return 1;}
static void sparse_emit(double score,int restart){int ranks[MAXK],dom[MAXN];char sq[37];for(int i=0;i<k;i++)ranks[perm[i]]=i+1;for(int i=0;i<36;i++)sq[i]=AL[square[i]];sq[36]=0;
 printf("{\"score\":%.9f,\"restart\":%d,\"square\":\"%s\",\"missing_full_ciphertext_positions_0based\":[",score/(n/2-3),restart,sq);
 for(int i=0;i<loss_count;i++)printf("%s%d",i?",":"",losses[i]);printf("],\"ranks\":[");for(int i=0;i<k;i++)printf("%s%d",i?",":"",ranks[i]);printf("],\"plaintext\":\"");untranspose(dom);for(int i=0;i<n/2;i++)putchar(dom[i]<36?AL[square[dom[i]]]:'?');printf("\"}\n");fflush(stdout);
}
int main(void){char path[1024],partial[64],buf[MAXN];int restarts,iters;unsigned long long seed;
 if(scanf("%1023s%d%d%d%llu%d",path,&k,&restarts,&iters,&seed,&loss_count)!=6||k<2||k>MAXK||restarts<1||iters<1||loss_count<1||loss_count>MAXLOSS)return 2;
 FILE*f=fopen(path,"rb");if(!f||fread(model,sizeof(float),QSIZE,f)!=QSIZE)return 3;fclose(f);for(int i=0;i<QSIZE;i++)probability[i]=pow(10.0,model[i]);
 if(scanf("%36s",partial)!=1||strlen(partial)!=36)return 2;int used[36]={0};
 for(int i=0;i<36;i++){anchors[i]=indexof(partial[i],AL);if(anchors[i]<0&&partial[i]!='?')return 2;if(anchors[i]<0)unknown[nu++]=i;else if(used[anchors[i]]++)return 2;}
 int nr=0;for(int i=0;i<36;i++)if(!used[i])remaining[nr++]=i;if(nr!=nu)return 2;
 int seen[MAXK]={0};for(int i=0;i<k;i++){int rank;if(scanf("%d",&rank)!=1||rank<1||rank>k||seen[rank-1]++)return 2;perm[rank-1]=i;}
 if(scanf("%4095s",buf)!=1)return 2;source_length=strlen(buf);n=source_length+loss_count;received=n;ngap=0;gap=0;fixedgap=0;if(n%2||n<8||n>=MAXN)return 2;
 for(int i=0;i<source_length;i++){sourcetext[i]=indexof(buf[i],CO);if(sourcetext[i]<0&&buf[i]!='?')return 2;}
 state=seed;double global=-1e100,printed=-1e100;int globalsquare[36],globalloss[MAXLOSS];
 for(int rs=0;rs<restarts;rs++){
  memcpy(square,anchors,sizeof square);for(int i=0;i<nu;i++)square[unknown[i]]=remaining[i];for(int i=nu-1;i>0;i--){int j=ri(i+1),a=unknown[i],b=unknown[j],t=square[a];square[a]=square[b];square[b]=t;}
  random_losses();if(rs%3==0){int start=ri(source_length+1);for(int i=0;i<loss_count;i++)losses[i]=start+i;}
  if(rs&&rs%3==1){memcpy(square,globalsquare,sizeof square);memcpy(losses,globalloss,sizeof losses);for(int j=0;j<1+ri(3);j++)move_loss();}
  pad_source();double cur=fitness(),best=cur;int bs[36],bl[MAXLOSS];memcpy(bs,square,sizeof square);memcpy(bl,losses,sizeof losses);
  for(int it=0;it<iters;it++){
   int sl[MAXLOSS],a=0,b=0,t=0,type=nu>1&&ri(5)==0;memcpy(sl,losses,sizeof sl);
   if(type){a=unknown[ri(nu)];b=unknown[ri(nu)];if(a==b)continue;t=square[a];square[a]=square[b];square[b]=t;}else{if(!move_loss())continue;pad_source();}
   double value=fitness(),temperature=5.0*pow(.015,(double)it/iters);
   if(value>=cur||ru()<exp((value-cur)/temperature))cur=value;else if(type){t=square[a];square[a]=square[b];square[b]=t;}else{memcpy(losses,sl,sizeof losses);pad_source();}
   if(cur>best){best=cur;memcpy(bs,square,sizeof square);memcpy(bl,losses,sizeof losses);}
  }
  memcpy(square,bs,sizeof square);memcpy(losses,bl,sizeof losses);pad_source();cur=best;
  for(int pass=0;pass<2;pass++){
   int changed=0;for(int at=0;at<loss_count;at++){
    int oldloss[MAXLOSS],bestloss[MAXLOSS];memcpy(oldloss,losses,sizeof losses);memcpy(bestloss,losses,sizeof losses);
    for(int pos=0;pos<n;pos++){
     int ok=1;for(int j=0;j<loss_count;j++)if(j!=at&&oldloss[j]==pos)ok=0;if(!ok)continue;
     memcpy(losses,oldloss,sizeof losses);losses[at]=pos;qsort(losses,loss_count,sizeof(int),compare_int);pad_source();double value=fitness();if(value>cur+1e-8){cur=value;memcpy(bestloss,losses,sizeof losses);changed=1;}
    }
    memcpy(losses,bestloss,sizeof losses);pad_source();
   }
   for(int i=0;i<nu;i++)for(int j=i+1;j<nu;j++){int a=unknown[i],b=unknown[j],t=square[a];square[a]=square[b];square[b]=t;double value=fitness();if(value>cur+1e-8){cur=value;changed=1;}else{t=square[a];square[a]=square[b];square[b]=t;}}
   if(!changed)break;
  }
  if(cur>global){global=cur;memcpy(globalsquare,square,sizeof square);memcpy(globalloss,losses,sizeof losses);}
  memcpy(square,globalsquare,sizeof square);memcpy(losses,globalloss,sizeof losses);pad_source();if(global>printed+1e-7){sparse_emit(global,rs);printed=global;}
 }
 return 0;
}
