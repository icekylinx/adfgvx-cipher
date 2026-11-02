/* Exact post-discovery check at width 18. No language scoring.
 * Enumerate every long-column segmentation, every ordered column pairing,
 * and all injective square constraints from a supplied partial first crib.
 * The second crib is used only to count received-coordinate contradictions.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

typedef struct { int u,v,n; unsigned char letter[8],cell[8]; } Candidate;
static Candidate candidates[9][306];
static int counts[9],lmap[26],cmap[36],chosen_u[9],chosen_v[9];
static char pt1[256],ct1[512],pt2[256],ct2[512];
static int columns[18][8],lengths[18];
static const char *coords="ADFGVX";
static uint64_t segmentations,feasible_segmentations,nodes,solutions,histogram[109];
static int minimum=109;

static int coordinate(char c) { const char *p=strchr(coords,c);return p?(int)(p-coords):-1; }
static int compatible(const Candidate *a,unsigned used) {
    if ((used>>a->u&1U)||(used>>a->v&1U)) return 0;
    for(int k=0;k<a->n;k++) {
        int l=a->letter[k],c=a->cell[k];
        if((lmap[l]>=0&&lmap[l]!=c)||(cmap[c]>=0&&cmap[c]!=l))return 0;
    }
    return 1;
}
static void record_solution(void) {
    int mismatch[108],expected[108],n=0;
    for(int i=0;pt2[i];i++) {
        if(pt2[i]=='?')continue;
        int cell=lmap[pt2[i]-'A'];
        if(cell<0) { fputs("Second crib contains an unassigned letter\n",stderr);exit(4); }
        int j=i%9,row=i/9;
        int a=chosen_u[j]*6+row,b=chosen_v[j]*6+row;
        int got=coordinate(ct2[a]);if(got>=0&&got!=cell/6){mismatch[n]=a;expected[n++]=cell/6;}
        got=coordinate(ct2[b]);if(got>=0&&got!=cell%6){mismatch[n]=b;expected[n++]=cell%6;}
    }
    solutions++;histogram[n]++;if(n<minimum)minimum=n;
    if(solutions<=100) {
        printf("{\"kind\":\"solution\",\"ranks\":[");
        for(int j=0;j<9;j++)printf("%s%d,%d",j?",":"",chosen_u[j]+1,chosen_v[j]+1);
        printf("],\"partial_square\":\"");
        for(int c=0;c<36;c++)putchar(cmap[c]>=0?'A'+cmap[c]:'?');
        printf("\",\"second_crib_known_coordinate_mismatches\":%d,\"edits\":[",n);
        for(int k=0;k<n;k++)printf("%s{\"source_index\":%d,\"observed\":\"%c\",\"proposed\":\"%c\"}",k?",":"",mismatch[k],ct2[mismatch[k]],coords[expected[k]]);
        puts("]}");
    }
}
static void search(unsigned used,unsigned assigned) {
    nodes++;
    if(assigned==511U){record_solution();return;}
    int best=-1,best_count=307;
    for(int j=0;j<9;j++)if(!(assigned>>j&1U)) {
        int n=0;for(int k=0;k<counts[j];k++)n+=compatible(&candidates[j][k],used);
        if(!n)return;
        if(n<best_count){best=j;best_count=n;}
    }
    for(int k=0;k<counts[best];k++) {
        Candidate *a=&candidates[best][k];if(!compatible(a,used))continue;
        int changed[8],nc=0;
        for(int t=0;t<a->n;t++)if(lmap[a->letter[t]]<0) {
            changed[nc++]=t;lmap[a->letter[t]]=a->cell[t];cmap[a->cell[t]]=a->letter[t];
        }
        chosen_u[best]=a->u;chosen_v[best]=a->v;
        search(used|(1U<<a->u)|(1U<<a->v),assigned|(1U<<best));
        for(int t=0;t<nc;t++){int z=changed[t];lmap[a->letter[z]]=-1;cmap[a->cell[z]]=-1;}
    }
}
static void segmentation(unsigned mask) {
    segmentations++;int p=0;
    for(int i=0;i<18;i++){lengths[i]=7+(mask>>i&1U);for(int r=0;r<lengths[i];r++)columns[i][r]=coordinate(ct1[p++]);}
    for(int j=0;j<9;j++) {
        counts[j]=0;int len=j<3?8:7;
        for(int u=0;u<18;u++)if(lengths[u]==len)
        for(int v=0;v<18;v++)if(v!=u&&lengths[v]==len) {
            int lm[26],cm[36],ok=1;memset(lm,-1,sizeof lm);memset(cm,-1,sizeof cm);
            Candidate a={.u=u,.v=v,.n=0};
            for(int r=0;r<len;r++) {
                int i=9*r+j;if(i>=66||pt1[i]=='?')continue;
                int l=pt1[i]-'A',c=6*columns[u][r]+columns[v][r];
                if((lm[l]>=0&&lm[l]!=c)||(cm[c]>=0&&cm[c]!=l)){ok=0;break;}
                if(lm[l]<0){a.letter[a.n]=l;a.cell[a.n]=c;a.n++;lm[l]=c;cm[c]=l;}
            }
            if(ok)candidates[j][counts[j]++]=a;
        }
        if(!counts[j])return;
    }
    feasible_segmentations++;memset(lmap,-1,sizeof lmap);memset(cmap,-1,sizeof cmap);search(0,0);
}
static void masks(int start,int remaining,unsigned mask) {
    if(!remaining){segmentation(mask);return;}
    for(int i=start;i<=18-remaining;i++)masks(i+1,remaining-1,mask|(1U<<i));
}
int main(int argc,char **argv) {
    if(argc!=2){fputs("Usage: enumerate INPUT.txt\n",stderr);return 2;}
    FILE *f=fopen(argv[1],"r");if(!f){perror(argv[1]);return 2;}
    int n=fscanf(f,"%255s %511s %255s %511s",pt1,ct1,pt2,ct2);fclose(f);
    if(n!=4||strlen(pt1)!=66||strlen(ct1)!=132||strlen(pt2)>54||strlen(ct2)!=108)return 2;
    for(int i=0;i<132;i++)if(coordinate(ct1[i])<0)return 2;
    for(int i=0;i<66;i++)if(pt1[i]!='?'&&(pt1[i]<'A'||pt1[i]>'Z'))return 2;
    for(int i=0;pt2[i];i++)if(pt2[i]!='?'&&(pt2[i]<'A'||pt2[i]>'Z'))return 2;
    for(int i=0;i<108;i++)if(ct2[i]!='?'&&coordinate(ct2[i])<0)return 2;
    clock_t start=clock();masks(0,6,0);
    printf("{\"kind\":\"summary\",\"segmentations\":%llu,\"locally_feasible_segmentations\":%llu,\"search_nodes\":%llu,\"solutions\":%llu,\"minimum_second_crib_known_coordinate_mismatches\":%d,\"cpu_seconds\":%.6f,\"mismatch_histogram\":{",(unsigned long long)segmentations,(unsigned long long)feasible_segmentations,(unsigned long long)nodes,(unsigned long long)solutions,minimum,(double)(clock()-start)/CLOCKS_PER_SEC);
    int first=1;for(int i=0;i<109;i++)if(histogram[i]){printf("%s\"%d\":%llu",first?"":",",i,(unsigned long long)histogram[i]);first=0;}
    puts("}}");return 0;
}
