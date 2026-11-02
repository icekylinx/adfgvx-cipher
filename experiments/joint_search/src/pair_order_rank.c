/* Exact orientation/order ranking for a fixed K18 pairing of132/108 symbols.
 * There are3! *6! =4320 height-compatible pair orders and2^8 =256 relative
 * orientations after quotienting the global coordinate-transpose symmetry.
 * All1,105,920 choices are ranked by IC2, IC3, and an independent profile
 * composite. These are substitution-invariant surrogates, not plaintext proofs.
 *
 * Usage: pair_order_rank PROFILE INPUT TOP [SECOND_MESSAGE_PAIR_OFFSET]
 * INPUT: ciphertext1 ciphertext2 followed by18 one-based column ranks.
 * The optional offset is0..8 and rotates the effective second-message key.
 * Since108 is divisible by18, this does not change its column segmentation.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include <time.h>

#define ORDERS 4320
#define ORIENTATIONS 256
#define TOTAL (ORDERS*ORIENTATIONS)
typedef struct {uint16_t order,orientation;double ic2,ic3,profile;} Record;
static int ranks[18],ns[2]={66,54},cells[2][72],orders[ORDERS][9],norders;
static int work[9],used[9],offset;
static double means[37],variances[37];
static int counts2[1296],counts3[46656],stamps2[1296],stamps3[46656],epoch;
static const char AL[]="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",CO[]="ADFGVX";
static int symbol(char ch){const char*p=strchr(CO,ch);return p&&ch?(int)(p-CO):-1;}

static void enumerate(int at){
    if(at==9){memcpy(orders[norders++],work,sizeof work);return;}
    for(int j=0;j<9;j++)if(!used[j]&&(j<3)==(at<3)){
        used[j]=1;work[at]=j;enumerate(at+1);used[j]=0;
    }
}
static int decoded(int message,int position,int order,int orientation){
    int pair=orders[order][(position%9+(message?offset:0))%9];
    int value=cells[message][position/9*9+pair];
    if(value>=0&&(orientation&(1<<pair)))value=6*(value%6)+value/6;
    return value;
}
static double mono_profile(int orientation){
    int count[36]={0},n=0;
    for(int m=0;m<2;m++)for(int i=0;i<ns[m];i++){
        int cell=cells[m][i];if(cell<0)continue;
        if(orientation&(1<<(i%9)))cell=6*(cell%6)+cell/6;
        count[cell]++;n++;
    }
    for(int i=1;i<36;i++){int v=count[i],j=i;while(j&&count[j-1]<v){count[j]=count[j-1];j--;}count[j]=v;}
    double score=0;
    for(int i=0;i<36;i++){double d=(double)count[i]/n-means[i];score-=d*d/(variances[i]+.25/(n*n));}
    return score;
}
static Record evaluate(int order,int orientation,double profile){
    int n2=0,n3=0;double collision2=0,collision3=0;epoch++;
    for(int m=0;m<2;m++){
        int previous=-1,before=-1;
        for(int i=0;i<ns[m];i++){
            int value=decoded(m,i,order,orientation);
            if(previous>=0&&value>=0){
                int code=previous*36+value;n2++;
                if(stamps2[code]!=epoch){stamps2[code]=epoch;counts2[code]=0;}
                collision2+=counts2[code]++;
                if(before>=0){
                    code=(before*36+previous)*36+value;n3++;
                    if(stamps3[code]!=epoch){stamps3[code]=epoch;counts3[code]=0;}
                    collision3+=counts3[code]++;
                }
            }
            before=previous;previous=value;
        }
    }
    double ic2=n2>1?2*collision2/(n2*(n2-1.0)):0;
    double ic3=n3>1?2*collision3/(n3*(n3-1.0)):0;
    double d=ic2-means[36];profile-=d*d/(variances[36]+1e-7);
    Record row={(uint16_t)order,(uint16_t)orientation,10000*ic2,10000*ic3,profile};return row;
}
static int compare(double a,double b){return a>b?-1:a<b?1:0;}
static int tie(const Record*a,const Record*b){
    if(a->orientation!=b->orientation)return a->orientation<b->orientation?-1:1;
    return a->order==b->order?0:a->order<b->order?-1:1;
}
static int compare2(const void*x,const void*y){
    const Record*a=x,*b=y;int r=compare(a->ic2,b->ic2);if(r)return r;
    r=compare(a->ic3,b->ic3);if(r)return r;r=compare(a->profile,b->profile);return r?r:tie(a,b);
}
static int compare3(const void*x,const void*y){
    const Record*a=x,*b=y;int r=compare(a->ic3,b->ic3);if(r)return r;
    r=compare(a->ic2,b->ic2);if(r)return r;r=compare(a->profile,b->profile);return r?r:tie(a,b);
}
static int compareprofile(const void*x,const void*y){
    const Record*a=x,*b=y;int r=compare(a->profile,b->profile);if(r)return r;
    r=compare(a->ic3,b->ic3);return r?r:tie(a,b);
}
static void emit(const Record*row,const char*metric,int rank){
    int key[18];
    for(int p=0;p<9;p++){
        int j=orders[row->order][p],flip=(row->orientation>>j)&1;
        key[2*p]=ranks[2*j+flip];key[2*p+1]=ranks[2*j+1-flip];
    }
    printf("{\"kind\":\"candidate\",\"metric\":\"%s\",\"rank_zero_based\":%d,\"ic2\":%.12f,\"ic3\":%.12f,\"profile_composite\":%.12f,\"second_message_pair_offset\":%d,\"ranks\":[",metric,rank,row->ic2,row->ic3,row->profile,offset);
    for(int i=0;i<18;i++)printf("%s%d",i?",":"",key[i]);
    printf("],\"message_ranks\":[");
    for(int m=0;m<2;m++){
        if(m)putchar(',');
        putchar('[');
        for(int i=0;i<18;i++)printf("%s%d",i?",":"",key[(i+(m?2*offset:0))%18]);
        putchar(']');
    }
    printf("],\"cells\":[");
    for(int m=0;m<2;m++){
        if(m)putchar(',');
        putchar('"');
        for(int i=0;i<ns[m];i++){int v=decoded(m,i,row->order,row->orientation);putchar(v<0?'?':AL[v]);}
        putchar('"');
    }
    printf("]}\n");
}
int main(int argc,char**argv){
    if(argc<4||argc>5)return 2;
    int keep=atoi(argv[3]);offset=argc==5?atoi(argv[4]):0;
    if(keep<1||keep>TOTAL||offset<0||offset>8)return 2;
    FILE*profile=fopen(argv[1],"r"),*input=fopen(argv[2],"r");if(!profile||!input)return 2;
    for(int i=0;i<37;i++)if(fscanf(profile,"%lf%lf",means+i,variances+i)!=2)return 2;
    fclose(profile);
    char texts[2][256];int seen[18]={0};
    for(int m=0;m<2;m++){
        if(fscanf(input,"%255s",texts[m])!=1||strlen(texts[m])!=(size_t)(2*ns[m]))return 2;
        for(int i=0;i<2*ns[m];i++)if(symbol(texts[m][i])<0&&texts[m][i]!='?')return 2;
    }
    for(int i=0;i<18;i++)if(fscanf(input,"%d",ranks+i)!=1||ranks[i]<1||ranks[i]>18||seen[ranks[i]-1]++)return 2;
    fclose(input);
    for(int m=0;m<2;m++){
        int off[18],at=0,interim[144],length=2*ns[m];
        for(int rank=1;rank<=18;rank++)for(int col=0;col<18;col++)if(ranks[col]==rank){off[col]=at;at+=length/18+(col<length%18);}
        for(int i=0;i<length;i++)interim[i]=symbol(texts[m][off[i%18]+i/18]);
        for(int i=0;i<ns[m];i++)cells[m][i]=interim[2*i]<0||interim[2*i+1]<0?-1:6*interim[2*i]+interim[2*i+1];
    }
    enumerate(0);if(norders!=ORDERS)return 3;
    Record*records=malloc(TOTAL*sizeof(Record));if(!records)return 3;
    clock_t start=clock();int count=0;
    for(int bits=0;bits<ORIENTATIONS;bits++){
        int orientation=bits<<1;double p=mono_profile(orientation);
        for(int order=0;order<norders;order++)records[count++]=evaluate(order,orientation,p);
    }
    const char*names[3]={"ic2","ic3","profile_composite"};
    int(*comparators[3])(const void*,const void*)={compare2,compare3,compareprofile};
    for(int metric=0;metric<3;metric++){
        qsort(records,TOTAL,sizeof(Record),comparators[metric]);
        for(int rank=0;rank<keep;rank++)emit(records+rank,names[metric],rank);
    }
    printf("{\"kind\":\"summary\",\"enumerated_transpositions\":%d,\"relative_orientations\":256,\"compatible_pair_orders\":4320,\"retained_per_metric\":%d,\"second_message_pair_offset\":%d,\"cpu_seconds\":%.6f}\n",count,keep,offset,(double)(clock()-start)/CLOCKS_PER_SEC);
    free(records);return 0;
}
