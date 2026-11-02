/* Fast global-profile refinement inside retained length-class segmentations.
 * Supports even widths; pairing orientations and assignments are unknown.
 * Full 36-cell counts are updated from only the two affected column pairs.
 * All restarts randomize the within-class assignments, including restart zero.
 *
 * Usage: segmentation_profile_batch PROFILE CIPHERS SEGMENTS K R I SEED [EMIT_RESTARTS]
 * CIPHERS starts with the two 132/108-symbol strings.
 * SEGMENTS: count, then rows: long1_mask long2_mask K_rank_integers.
 * Mask bits index transmitted columns, not physical columns.
 * This is bounded stochastic pairing refinement, not exhaustive key search.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include <time.h>
#define MAXK 40
typedef struct{unsigned char symbol[36],count[36];int n,known;} Pair;
static Pair pairs[MAXK][MAXK];
static int k,ns[2]={132,108},ct[2][132],column[2][MAXK][66],height[2][MAXK];
static int ranks[MAXK],co[MAXK],cls[MAXK],moves[MAXK*MAXK][2],nmoves;
static int counts[36],known;
static double mu[36],variance[36],cost[121][36][121];
static uint64_t state;
static uint64_t rn(void){uint64_t z=(state+=0x9e3779b97f4a7c15ULL);z=(z^(z>>30))*0xbf58476d1ce4e5b9ULL;z=(z^(z>>27))*0x94d049bb133111ebULL;return z^(z>>31);}
static int ri(int n){return rn()%n;}
static double ru(void){return(rn()>>11)*0x1.0p-53;}
static int symbol(char c){const char*p=strchr("ADFGVX",c);return p&&c?(int)(p-"ADFGVX"):-1;}
static void addpair(int position,int sign){
    Pair*p=&pairs[co[position]][co[position+1]];known+=sign*p->known;
    for(int i=0;i<p->n;i++)counts[p->symbol[i]]+=sign*p->count[i];
}
static double fitness(void){
    int histogram[121]={0},maximum=0;
    for(int i=0;i<36;i++){histogram[counts[i]]++;if(counts[i]>maximum)maximum=counts[i];}
    double result=0;int rank=0;
    for(int value=maximum;value>=0;value--)for(int j=0;j<histogram[value];j++)result+=cost[known][rank++][value];
    return result;
}
static void build_pairs(void){
    for(int m=0;m<2;m++){
        int off[MAXK],position=0;
        for(int r=1;r<=k;r++)for(int c=0;c<k;c++)if(ranks[c]==r){off[c]=position;position+=height[m][c];}
        for(int c=0;c<k;c++)for(int r=0;r<height[m][c];r++)column[m][c][r]=ct[m][off[c]+r];
    }
    for(int a=0;a<k;a++)for(int b=0;b<k;b++)if(a!=b&&cls[a]==cls[b]){
        Pair*p=&pairs[a][b];int count[36]={0};p->n=p->known=0;
        for(int m=0;m<2;m++)for(int r=0;r<height[m][a];r++){
            int x=column[m][a][r],y=column[m][b][r];if(x>=0&&y>=0){count[6*x+y]++;p->known++;}
        }
        for(int c=0;c<36;c++)if(count[c]){p->symbol[p->n]=c;p->count[p->n++]=count[c];}
    }
}
static void emit(unsigned long long mask1,unsigned long long mask2,double score,int restarts,int iterations,int restart_index){
    printf("{\"long1_mask\":%llu,\"long2_mask\":%llu,\"profile_score\":%.12f,\"restarts\":%d,\"iterations_per_restart\":%d,\"restart_index\":%d,\"ranks\":[",mask1,mask2,score,restarts,iterations,restart_index);
    for(int c=0;c<k;c++)printf("%s%d",c?",":"",ranks[co[c]]);
    printf("],\"cells\":[");
    for(int m=0;m<2;m++){
        if(m)putchar(',');
        putchar('"');
        for(int i=0;i<ns[m]/2;i++){
            int p=2*i,a=column[m][co[p%k]][p/k],b=column[m][co[(p+1)%k]][(p+1)/k];
            putchar(a<0||b<0?'?':"ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"[6*a+b]);
        }
        putchar('"');
    }
    printf("]}\n");
}
int main(int argc,char**argv){
    if(argc!=8&&argc!=9)return 2;
    int emit_restarts=argc==9&&atoi(argv[8])!=0;
    k=atoi(argv[4]);int restarts=atoi(argv[5]),iterations=atoi(argv[6]);
    uint64_t seed=strtoull(argv[7],0,10);if(k<2||k>MAXK||k%2||restarts<1||iterations<1)return 2;
    FILE*profile=fopen(argv[1],"r"),*ciphers=fopen(argv[2],"r"),*segments=fopen(argv[3],"r");
    if(!profile||!ciphers||!segments)return 2;
    for(int i=0;i<36;i++)if(fscanf(profile,"%lf%lf",mu+i,variance+i)!=2)return 2;
    fclose(profile);
    for(int n=1;n<=120;n++)for(int rank=0;rank<36;rank++)for(int value=0;value<=120;value++){
        double d=(double)value/n-mu[rank];cost[n][rank][value]=-d*d/(variance[rank]+.25/(n*n));
    }
    char text[256];
    for(int m=0;m<2;m++){
        if(fscanf(ciphers,"%255s",text)!=1||strlen(text)!=(size_t)ns[m])return 2;
        for(int i=0;i<ns[m];i++){ct[m][i]=symbol(text[i]);if(ct[m][i]<0&&text[i]!='?')return 2;}
        for(int c=0;c<k;c++){height[m][c]=ns[m]/k+(c<ns[m]%k);if(c<ns[m]%k)cls[c]|=1<<m;}
    }
    fclose(ciphers);
    for(int a=0;a<k;a++)for(int b=a+1;b<k;b++)if(cls[a]==cls[b]){moves[nmoves][0]=a;moves[nmoves++][1]=b;}
    double*temperature=malloc(iterations*sizeof(double));if(!temperature)return 3;
    for(int i=0;i<iterations;i++)temperature[i]=4.5*pow(.01,(double)i/iterations);
    int total;if(fscanf(segments,"%d",&total)!=1||total<1)return 2;clock_t started=clock();setvbuf(stdout,NULL,_IOFBF,1<<20);
    for(int caseid=0;caseid<total;caseid++){
        unsigned long long mask1,mask2;if(fscanf(segments,"%llu%llu",&mask1,&mask2)!=2)return 2;
        int used[MAXK]={0};unsigned long long found1=0,found2=0;
        for(int c=0;c<k;c++){
            if(fscanf(segments,"%d",ranks+c)!=1||ranks[c]<1||ranks[c]>k||used[ranks[c]-1]++)return 2;
            if(cls[c]&1)found1|=1ULL<<(ranks[c]-1);
            if(cls[c]&2)found2|=1ULL<<(ranks[c]-1);
        }
        if(mask1!=found1||mask2!=found2)return 4;
        build_pairs();
        state=seed^(mask1*0x9e3779b97f4a7c15ULL)^(mask2*0xbf58476d1ce4e5b9ULL);
        double global=-1e100;int bestco[MAXK];
        for(int restart=0;restart<restarts;restart++){
            for(int c=0;c<k;c++)co[c]=c;
            for(int i=0;i<20*k;i++){int z=ri(nmoves),a=moves[z][0],b=moves[z][1],t=co[a];co[a]=co[b];co[b]=t;}
            memset(counts,0,sizeof counts);known=0;for(int c=0;c<k;c+=2)addpair(c,1);
            double current=fitness(),local_best=current;int local_best_co[MAXK];memcpy(local_best_co,co,sizeof co);
            if(current>global){global=current;memcpy(bestco,co,sizeof co);}
            for(int it=0;it<iterations;it++){
                int a,b;if(ri(5)==0){a=2*ri(k/2);b=a+1;}else{int z=ri(nmoves);a=moves[z][0];b=moves[z][1];}
                int pa=a&~1,pb=b&~1;addpair(pa,-1);if(pb!=pa)addpair(pb,-1);
                int t=co[a];co[a]=co[b];co[b]=t;addpair(pa,1);if(pb!=pa)addpair(pb,1);
                double value=fitness();
                if(value>=current||ru()<exp((value-current)/temperature[it])){
                    current=value;
                    if(current>local_best){local_best=current;memcpy(local_best_co,co,sizeof co);}
                    if(current>global){global=current;memcpy(bestco,co,sizeof co);}
                }else{
                    addpair(pa,-1);if(pb!=pa)addpair(pb,-1);t=co[a];co[a]=co[b];co[b]=t;
                    addpair(pa,1);if(pb!=pa)addpair(pb,1);
                }
            }
            if(emit_restarts){memcpy(co,local_best_co,sizeof co);emit(mask1,mask2,local_best,restarts,iterations,restart);}
        }
        if(!emit_restarts){memcpy(co,bestco,sizeof co);emit(mask1,mask2,global,restarts,iterations,-1);}
        if((caseid+1)%1000==0){fprintf(stderr,"Completed %d/%d segmentations.\n",caseid+1,total);fflush(stderr);}
    }
    fclose(segments);fprintf(stderr,"Completed all %d segmentations in %.3f CPU seconds.\n",total,(double)(clock()-started)/CLOCKS_PER_SEC);
    return 0;
}
