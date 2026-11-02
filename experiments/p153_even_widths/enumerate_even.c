/* Exact post-discovery partial-crib consistency check for even widths 14..26.
 * No language score. The first crib constrains transposition and square; the
 * second crib is evaluated only after a complete first-crib assignment.
 * Each message resets its own rectangle, including its own ragged heights.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>
#include <math.h>
#define MAXK 26
#define MAXH 13
#define MAXROWS 10
#define MAXCAND (MAXK*(MAXK-1))
typedef struct { unsigned char u,v,n,letter[MAXROWS],cell[MAXROWS]; } Candidate;
static Candidate candidates[MAXH][MAXCAND];
static int k,h,q,e,q2,e2,counts[MAXH],lmap[26],cmap[36],chosen_u[MAXH],chosen_v[MAXH];
static int encoded[132],columns[MAXK][MAXROWS],lengths[MAXK],first_previous[MAXH][MAXROWS],pair_order[MAXH];
static char pt1[67],ct1[133],pt2[55],ct2[109];
static const char *coords="ADFGVX";
static uint64_t segmentations,feasible,nodes,solutions,histogram[109],max_nodes,max_solutions;
static int minimum=109,stopped;
static const char *stop_reason="completed";
static clock_t start_clock;
static double max_cpu;

static int coordinate(char c){const char*p=strchr(coords,c);return p&&c?(int)(p-coords):-1;}
static int check_limit(void){
    if(stopped)return 1;
    if(max_nodes&&nodes>=max_nodes){stopped=1;stop_reason="node_limit";}
    else if(max_solutions&&solutions>=max_solutions){stopped=1;stop_reason="solution_limit";}
    else if(max_cpu>0&&(double)(clock()-start_clock)/CLOCKS_PER_SEC>=max_cpu){stopped=1;stop_reason="cpu_time_limit";}
    return stopped;
}
static int compatible(const Candidate*a,uint32_t used){
    if((used>>a->u&1U)||(used>>a->v&1U))return 0;
    for(int t=0;t<a->n;t++){int l=a->letter[t],c=a->cell[t];
        if((lmap[l]>=0&&lmap[l]!=c)||(cmap[c]>=0&&cmap[c]!=l))return 0;}
    return 1;
}
static void record_solution(void){
    int rank_to_col[MAXK],offset[MAXK],position=0,indices[108],expected[108],n=0;
    for(int j=0;j<h;j++){rank_to_col[chosen_u[j]]=2*j;rank_to_col[chosen_v[j]]=2*j+1;}
    for(int rank=0;rank<k;rank++){int col=rank_to_col[rank];offset[col]=position;position+=q2+(col<e2);}
    if(position!=108)abort();
    for(int i=0;pt2[i];i++)if(pt2[i]!='?'){
        int cell=lmap[pt2[i]-'A'];if(cell<0)abort();
        int pair=i%h,row=i/h,a=offset[2*pair]+row,b=offset[2*pair+1]+row;
        if(coordinate(ct2[a])>=0&&coordinate(ct2[a])!=cell/6){indices[n]=a;expected[n++]=cell/6;}
        if(coordinate(ct2[b])>=0&&coordinate(ct2[b])!=cell%6){indices[n]=b;expected[n++]=cell%6;}
    }
    solutions++;histogram[n]++;if(n<minimum)minimum=n;
    printf("{\"kind\":\"solution\",\"width\":%d,\"ranks\":[",k);
    for(int j=0;j<h;j++)printf("%s%d,%d",j?",":"",chosen_u[j]+1,chosen_v[j]+1);
    printf("],\"partial_square\":\"");for(int c=0;c<36;c++)putchar(cmap[c]<0?'?':'A'+cmap[c]);
    printf("\",\"second_crib_known_coordinate_mismatches\":%d,\"edits\":[",n);
    for(int i=0;i<n;i++)printf("%s{\"source_index\":%d,\"observed\":\"%c\",\"proposed\":\"%c\"}",i?",":"",indices[i],ct2[indices[i]],coords[expected[i]]);
    puts("]}");fflush(stdout);
    check_limit();
}
static void search(uint32_t used,uint32_t assigned){
    if(stopped)return;
    if(max_nodes&&nodes>=max_nodes){stopped=1;stop_reason="node_limit";return;}
    nodes++;if((nodes&4095U)==0&&check_limit())return;
    if(assigned==((1U<<h)-1U)){record_solution();return;}
    int best=-1,best_count=MAXCAND+1;
    for(int j=0;j<h;j++)if(!(assigned>>j&1U)){
        int n=0;for(int z=0;z<counts[j];z++)n+=compatible(&candidates[j][z],used);
        if(!n)return;
        if(n<best_count){best=j;best_count=n;}
    }
    for(int z=0;z<counts[best]&&!stopped;z++){
        Candidate*a=&candidates[best][z];if(!compatible(a,used))continue;
        int changed[MAXROWS],nc=0;
        for(int t=0;t<a->n;t++)if(lmap[a->letter[t]]<0){changed[nc++]=t;lmap[a->letter[t]]=a->cell[t];cmap[a->cell[t]]=a->letter[t];}
        chosen_u[best]=a->u;chosen_v[best]=a->v;
        search(used|(1U<<a->u)|(1U<<a->v),assigned|(1U<<best));
        for(int i=0;i<nc;i++){int t=changed[i];lmap[a->letter[t]]=-1;cmap[a->cell[t]]=-1;}
    }
}
static void segmentation(uint32_t mask){
    if(stopped)return;
    if((segmentations&1023U)==0&&check_limit())return;
    segmentations++;
    int pos=0;
    for(int i=0;i<k;i++){lengths[i]=q+(int)(mask>>i&1U);for(int r=0;r<lengths[i];r++)columns[i][r]=encoded[pos++];}
    if(pos!=132)abort();
    for(int jj=0;jj<h;jj++){
        int j=pair_order[jj],len=q+(2*j<e),allowed[MAXK],na=0;counts[j]=0;
        /* Repeated plaintext letters must repeat each component coordinate.
         * This necessary filter only changes evaluation order, not candidates. */
        for(int col=0;col<k;col++)if(lengths[col]==len){
            int ok=1;for(int row=0;row<len;row++)if(first_previous[j][row]>=0&&columns[col][row]!=columns[col][first_previous[j][row]]){ok=0;break;}
            if(ok)allowed[na++]=col;
        }
        if(na<2)return;
        for(int ai=0;ai<na;ai++)for(int bi=0;bi<na;bi++)if(ai!=bi){
            int u=allowed[ai],v=allowed[bi],lm[26],cm[36],ok=1;
            memset(lm,-1,sizeof lm);memset(cm,-1,sizeof cm);Candidate a={.u=(unsigned char)u,.v=(unsigned char)v,.n=0};
            for(int row=0;row<len;row++){
                int i=h*row+j;if(pt1[i]=='?')continue;
                int l=pt1[i]-'A',c=6*columns[u][row]+columns[v][row];
                if((lm[l]>=0&&lm[l]!=c)||(cm[c]>=0&&cm[c]!=l)){ok=0;break;}
                if(lm[l]<0){a.letter[a.n]=(unsigned char)l;a.cell[a.n++]=(unsigned char)c;lm[l]=c;cm[c]=l;}
            }
            if(ok){if(counts[j]>=MAXCAND)abort();candidates[j][counts[j]++]=a;}
        }
        if(!counts[j])return;
    }
    feasible++;memset(lmap,-1,sizeof lmap);memset(cmap,-1,sizeof cmap);search(0,0);
}
static void masks(int first,int remaining,uint32_t mask){
    if(stopped)return;
    if(!remaining){segmentation(mask);return;}
    for(int i=first;i<=k-remaining&&!stopped;i++)masks(i+1,remaining-1,mask|(1U<<i));
}
int main(int argc,char**argv){
    if(argc<3||argc>6){fputs("Usage: enumerate_even INPUT WIDTH [CPU_SECONDS [MAX_NODES [MAX_SOLUTIONS]]]\n",stderr);return 2;}
    char *end;long parsed_width=strtol(argv[2],&end,10);
    if(*end||parsed_width<14||parsed_width>26||parsed_width%2)return 2;
    k=(int)parsed_width;
    if(argc>3){max_cpu=strtod(argv[3],&end);if(*end||!isfinite(max_cpu)||max_cpu<0)return 2;}
    if(argc>4){max_nodes=strtoull(argv[4],&end,10);if(*end||argv[4][0]=='-')return 2;}
    if(argc>5){max_solutions=strtoull(argv[5],&end,10);if(*end||argv[5][0]=='-')return 2;}
    h=k/2;q=132/k;e=132%k;q2=108/k;e2=108%k;
    FILE*f=fopen(argv[1],"r");if(!f){perror(argv[1]);return 2;}
    char a[256],b[512],c[256],d[512];int n=fscanf(f,"%255s %511s %255s %511s",a,b,c,d);fclose(f);
    if(n!=4||strlen(a)!=66||strlen(b)!=132||strlen(c)>54||strlen(d)!=108)return 2;
    strcpy(pt1,a);strcpy(ct1,b);strcpy(pt2,c);strcpy(ct2,d);
    int seen[26]={0};
    for(int i=0;i<66;i++){if(pt1[i]!='?'&&(pt1[i]<'A'||pt1[i]>'Z'))return 2;if(pt1[i]!='?')seen[pt1[i]-'A']=1;}
    for(int i=0;pt2[i];i++)if(pt2[i]!='?'&&(pt2[i]<'A'||pt2[i]>'Z'||!seen[pt2[i]-'A']))return 2;
    for(int i=0;i<132;i++){encoded[i]=coordinate(ct1[i]);if(encoded[i]<0)return 2;}
    for(int i=0;i<108;i++)if(ct2[i]!='?'&&coordinate(ct2[i])<0)return 2;
    int repeats[MAXH];
    for(int j=0;j<h;j++){
        int last[26];memset(last,-1,sizeof last);repeats[j]=0;pair_order[j]=j;
        for(int row=0;row<q+(2*j<e);row++){
            int i=h*row+j;first_previous[j][row]=-1;
            if(pt1[i]!='?'){int l=pt1[i]-'A';first_previous[j][row]=last[l];repeats[j]+=last[l]>=0;last[l]=row;}
        }
    }
    for(int i=0;i<h;i++)for(int j=i+1;j<h;j++)if(repeats[pair_order[j]]>repeats[pair_order[i]]){int t=pair_order[i];pair_order[i]=pair_order[j];pair_order[j]=t;}
    start_clock=clock();masks(0,e,0);
    char minimum_text[16];if(solutions)snprintf(minimum_text,sizeof minimum_text,"%d",minimum);else strcpy(minimum_text,"null");
    printf("{\"kind\":\"summary\",\"width\":%d,\"complete\":%s,\"stop_reason\":\"%s\",\"segmentations\":%llu,\"locally_feasible_segmentations\":%llu,\"search_nodes\":%llu,\"solutions\":%llu,\"minimum_second_crib_known_coordinate_mismatches\":%s,\"cpu_seconds\":%.6f,\"mismatch_histogram\":{",k,stopped?"false":"true",stop_reason,(unsigned long long)segmentations,(unsigned long long)feasible,(unsigned long long)nodes,(unsigned long long)solutions,minimum_text,(double)(clock()-start_clock)/CLOCKS_PER_SEC);
    int first=1;for(int i=0;i<109;i++)if(histogram[i]){printf("%s\"%d\":%llu",first?"":",",i,(unsigned long long)histogram[i]);first=0;}puts("}}");
    return 0;
}
