/* Exact enumeration of the 900900 length-class segmentations for K=16,
 * ciphertext lengths 132 and 108. Classes have heights A=(9,7), B=(8,7),
 * C=(8,6), with 4/8/4 columns. Matchings inside a class are exact.
 *
 * Metric 1 is an upper bound for an IID-letter relaxation. Each paired column
 * may choose its own optimal substitution; its half-known coordinates may
 * independently choose the six most probable letters. These relaxations can
 * only increase the IID log likelihood. This is NOT a full language bound.
 * Metric 2 is a heuristic variance-standardized within-pair collision excess.
 * Neither metric scores global square consistency or actual pair order.
 *
 * Usage: segmentation_rank MONOGRAM_PROBABILITIES INPUT TOP_COUNT
 * INPUT: ciphertext1 ciphertext2 truth_A_mask truth_C_mask
 * Zero masks mean no evaluation key is supplied. Nonzero evaluation masks
 * affect only reported ranks, never candidate scores or search order.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include <time.h>
#define STATES 1200
#define TOTAL 900900
typedef struct {int valid,type,n,index; signed char symbols[16];} Column;
typedef struct {uint16_t a,c;double bound,excess;} Record;
static Column columns[STATES];
static double *boundweight,*excessweight,logprior[36],logtop6;
static int matching8[105][8],nmatch8,work8[8];
static const int matching4[3][4]={{0,1,2,3},{0,2,1,3},{0,3,1,2}};
static const char CO[]="ADFGVX";

static int stateid(int i,int a,int c,int type){return ((i*5+a)*5+c)*3+type;}
static int symbol(char ch){const char*p=strchr(CO,ch);return p&&ch?(int)(p-CO):-1;}
static void enumerate8(int mask,int depth){
    if(!mask){memcpy(matching8[nmatch8++],work8,sizeof work8);return;}
    int a=__builtin_ctz((unsigned)mask);mask^=1<<a;
    for(int b=a+1;b<8;b++)if(mask&(1<<b)){
        work8[depth]=a;work8[depth+1]=b;enumerate8(mask^(1<<b),depth+2);
    }
}
static void edge(int a,int b,double *bound,double *excess){
    int count[36]={0},left[6]={0},right[6]={0},n=0,halves=0;
    Column*x=&columns[a],*y=&columns[b];
    for(int j=0;j<x->n;j++){
        int p=x->symbols[j],q=y->symbols[j];
        if(p>=0&&q>=0){count[6*p+q]++;left[p]++;right[q]++;n++;}
        else if(p>=0||q>=0)halves++;
    }
    double coll=0,lc=0,rc=0;
    for(int j=0;j<36;j++)coll+=count[j]*(count[j]-1.0)/2;
    for(int j=0;j<6;j++){lc+=left[j]*(left[j]-1.0)/2;rc+=right[j]*(right[j]-1.0)/2;}
    double pairs=n*(n-1.0)/2,expected=pairs?lc*rc/pairs:0;
    *excess=(coll-expected)/sqrt(expected*(pairs?1-expected/pairs:1)+.5);
    for(int j=1;j<36;j++){int value=count[j],i=j;while(i&&count[i-1]<value){count[i]=count[i-1];i--;}count[i]=value;}
    *bound=halves*logtop6;for(int j=0;j<36;j++)*bound+=count[j]*logprior[j];
}
static void group_score(const int *ids,int size,double *bestbound,double *bestexcess,int *boundpairing,int *excesspairing){
    double b[64]={0},e[64]={0};
    for(int i=0;i<size;i++)for(int j=i+1;j<size;j++){
        b[8*i+j]=boundweight[ids[i]*STATES+ids[j]];
        e[8*i+j]=excessweight[ids[i]*STATES+ids[j]];
    }
    *bestbound=*bestexcess=-1e100;int nb=size==4?3:105;
    for(int m=0;m<nb;m++){
        const int*p=size==4?matching4[m]:matching8[m];double bs=0,es=0;
        for(int j=0;j<size;j+=2){int index=8*p[j]+p[j+1];bs+=b[index];es+=e[index];}
        if(bs>*bestbound){*bestbound=bs;if(boundpairing)memcpy(boundpairing,p,size*sizeof(int));}
        if(es>*bestexcess){*bestexcess=es;if(excesspairing)memcpy(excesspairing,p,size*sizeof(int));}
    }
}
static Record score_masks(unsigned amask,unsigned cmask,int *branks,int *eranks){
    int ids[3][8],sizes[3]={0},a=0,c=0;
    for(int i=0;i<16;i++){
        int type=(amask&(1U<<i))?0:(cmask&(1U<<i))?2:1;
        ids[type][sizes[type]++]=stateid(i,a,c,type);a+=type==0;c+=type==2;
    }
    Record result={(uint16_t)amask,(uint16_t)cmask,0,0};int at=0;
    for(int type=0;type<3;type++){
        double b,e;int bp[8],ep[8];
        group_score(ids[type],sizes[type],&b,&e,branks?bp:NULL,eranks?ep:NULL);
        result.bound+=b;result.excess+=e;
        for(int j=0;j<sizes[type];j++){
            if(branks)branks[at+j]=columns[ids[type][bp[j]]].index+1;
            if(eranks)eranks[at+j]=columns[ids[type][ep[j]]].index+1;
        }
        at+=sizes[type];
    }
    return result;
}
static int cmp_bound(const void*x,const void*y){
    const Record*a=x,*b=y;if(a->bound!=b->bound)return a->bound>b->bound?-1:1;
    if(a->a!=b->a)return a->a<b->a?-1:1;
    return a->c==b->c?0:a->c<b->c?-1:1;
}
static int cmp_excess(const void*x,const void*y){
    const Record*a=x,*b=y;if(a->excess!=b->excess)return a->excess>b->excess?-1:1;
    if(a->a!=b->a)return a->a<b->a?-1:1;
    return a->c==b->c?0:a->c<b->c?-1:1;
}
static void emit_top(Record*records,int count,const char*metric,int boundmetric){
    for(int i=0;i<count;i++){
        int branks[16],eranks[16];Record r=score_masks(records[i].a,records[i].c,branks,eranks);int*p=boundmetric?branks:eranks;
        printf("{\"kind\":\"candidate\",\"metric\":\"%s\",\"rank_zero_based\":%d,\"a_mask\":%u,\"c_mask\":%u,\"unigram_bound\":%.12f,\"collision_excess\":%.12f,\"matching_seed_ranks\":[",metric,i,r.a,r.c,r.bound,r.excess);
        for(int j=0;j<16;j++)printf("%s%d",j?",":"",p[j]);
        printf("]}\n");
    }
}
int main(int argc,char**argv){
    if(argc!=4)return 2;
    clock_t started=clock();
    FILE*f=fopen(argv[1],"r"),*input=fopen(argv[2],"r");if(!f||!input)return 2;
    double prior[36],sum=0;
    for(int i=0;i<36;i++){if(fscanf(f,"%lf",prior+i)!=1||prior[i]<=0)return 2;sum+=prior[i];}fclose(f);
    for(int i=0;i<36;i++)prior[i]/=sum;
    for(int i=1;i<36;i++){double value=prior[i];int j=i;while(j&&prior[j-1]<value){prior[j]=prior[j-1];j--;}prior[j]=value;}
    double top=0;for(int i=0;i<36;i++){logprior[i]=log10(prior[i]);if(i<6)top+=prior[i];}logtop6=log10(top);
    char ct1[256],ct2[256];unsigned ta,tc;
    if(fscanf(input,"%255s%255s%u%u",ct1,ct2,&ta,&tc)!=4||strlen(ct1)!=132||strlen(ct2)!=108)return 2;
    fclose(input);
    for(int i=0;i<132;i++)if(symbol(ct1[i])<0&&ct1[i]!='?')return 2;
    for(int i=0;i<108;i++)if(symbol(ct2[i])<0&&ct2[i]!='?')return 2;
    int hastruth=ta||tc;if(hastruth&&(__builtin_popcount(ta)!=4||__builtin_popcount(tc)!=4||(ta&tc)||ta>65535||tc>65535))return 2;
    int nvalid=0;
    for(int i=0;i<16;i++)for(int a=0;a<=4;a++)for(int c=0;c<=4;c++){
        int b=i-a-c;if(b<0||b>8)continue;
        for(int type=0;type<3;type++){
            if((type==0&&a==4)||(type==1&&b==8)||(type==2&&c==4))continue;
            Column*col=&columns[stateid(i,a,c,type)];col->valid=1;col->type=type;col->index=i;nvalid++;
            int n1=type==0?9:8,n2=type==2?6:7,off1=8*i+a,off2=7*i-c;
            if(off1+n1>132||off2+n2>108)return 3;
            for(int j=0;j<n1;j++)col->symbols[col->n++]=symbol(ct1[off1+j]);
            for(int j=0;j<n2;j++)col->symbols[col->n++]=symbol(ct2[off2+j]);
        }
    }
    size_t wsize=(size_t)STATES*STATES;
    boundweight=calloc(wsize,sizeof(double));excessweight=calloc(wsize,sizeof(double));
    Record*records=malloc(TOTAL*sizeof(Record));if(!boundweight||!excessweight||!records)return 4;
    for(int a=0;a<STATES;a++)if(columns[a].valid)for(int b=a+1;b<STATES;b++)if(columns[b].valid&&columns[a].type==columns[b].type){
        double bound,excess;edge(a,b,&bound,&excess);
        boundweight[a*STATES+b]=boundweight[b*STATES+a]=bound;
        excessweight[a*STATES+b]=excessweight[b*STATES+a]=excess;
    }
    enumerate8(255,0);if(nmatch8!=105)return 5;
    Record truth={0,0,0,0};if(hastruth)truth=score_masks(ta,tc,NULL,NULL);
    int count=0,betterb=0,bettere=0,tiedb=0,tiede=0;
    for(unsigned amask=0;amask<65536;amask++)if(__builtin_popcount(amask)==4){
        int available[12],n=0;for(int i=0;i<16;i++)if(!(amask&(1U<<i)))available[n++]=i;
        for(unsigned small=0;small<4096;small++)if(__builtin_popcount(small)==4){
            unsigned cmask=0;for(int j=0;j<12;j++)if(small&(1U<<j))cmask|=1U<<available[j];
            Record r=score_masks(amask,cmask,NULL,NULL);records[count++]=r;
            if(hastruth){
                betterb+=r.bound>truth.bound+1e-10;bettere+=r.excess>truth.excess+1e-10;
                tiedb+=fabs(r.bound-truth.bound)<=1e-10;tiede+=fabs(r.excess-truth.excess)<=1e-10;
            }
        }
    }
    if(count!=TOTAL)return 5;
    int topcount=atoi(argv[3]);if(topcount<1)topcount=1;if(topcount>TOTAL)topcount=TOTAL;
    qsort(records,TOTAL,sizeof(Record),cmp_bound);int truebrank=-1;for(int i=0;hastruth&&i<TOTAL;i++)if(records[i].a==ta&&records[i].c==tc){truebrank=i;break;}double bcut=records[topcount-1].bound,bmax=records[0].bound;emit_top(records,topcount,"unigram_bound",1);
    qsort(records,TOTAL,sizeof(Record),cmp_excess);int trueerank=-1;for(int i=0;hastruth&&i<TOTAL;i++)if(records[i].a==ta&&records[i].c==tc){trueerank=i;break;}double ecut=records[topcount-1].excess,emax=records[0].excess;emit_top(records,topcount,"collision_excess",0);
    printf("{\"kind\":\"summary\",\"enumerated_segmentations\":%d,\"precomputed_column_states\":%d,\"retained_per_metric\":%d,\"best_unigram_bound\":%.12f,\"best_collision_excess\":%.12f,\"unigram_cutoff\":%.12f,\"collision_cutoff\":%.12f,\"has_evaluation_key\":%s,\"true_unigram_bound\":%.12f,\"true_collision_excess\":%.12f,\"strictly_better_unigram_segmentations\":%d,\"strictly_better_collision_segmentations\":%d,\"tied_unigram_segmentations\":%d,\"tied_collision_segmentations\":%d,\"true_unigram_rank_zero_based\":%d,\"true_collision_rank_zero_based\":%d,\"cpu_seconds\":%.6f}\n",count,nvalid,topcount,bmax,emax,bcut,ecut,hastruth?"true":"false",truth.bound,truth.excess,betterb,bettere,tiedb,tiede,truebrank,trueerank,(double)(clock()-started)/CLOCKS_PER_SEC);
    return 0;
}
