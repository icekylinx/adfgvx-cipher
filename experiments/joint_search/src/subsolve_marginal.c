/* Unknown substitution square with a fixed interim cell sequence.
 * Variant: exact wildcard marginal four-gram sums. A literal | marks a
 * message boundary; no scoring window crosses it. Fixed mask only; compare
 * different erasure placements with caution (partial coordinates are lost).
 * Written for the 2026-11-02 investigation. Uses an independently trained
 * German marginal quadgram table (float32, 37^4 entries); it never trains on guesses.
 * Usage: subsolve MODEL CELLS RESTARTS ITERATIONS SEED [INITIAL_SQUARE]
 * CELLS uses ABC...Z012...9 for cells 0..35 and '?' for erasures.
 * Output JSON lines whenever the best score improves.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <math.h>

#define MAXN 4096
#define QSIZE 1874161
static const char AL[]="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
static float quad[QSIZE];
static int base=37;
static int ct[MAXN],n,valid_windows;
static int affected[36][MAXN],acount[36];
static uint64_t rng;
static uint64_t next64(void) { rng ^= rng>>12; rng ^= rng<<25; rng ^= rng>>27; return rng*2685821657736338717ULL; }
static double uniform(void) { return (next64()>>11)*0x1.0p-53; }
static int ri(int limit) { return (int)(next64()%(unsigned)limit); }
static int symbol(char c) { const char *p=strchr(AL,c); return p && c ? (int)(p-AL):-1; }
static double window(const int *key,int i) {
    int z=0;
    for(int j=0;j<4;j++) {
        if(ct[i+j]==-2)return 0.0;
        int a=ct[i+j]<0?36:key[ct[i+j]];
        z=z*base+a;
    }
    return quad[z];
}
static double fitness(const int *key) {
    double total=0;
    for(int i=0;i+3<n;i++) total+=window(key,i);
    return total;
}
static void output(double score,const int *key,int restart,int iteration) {
    char sq[37],pt[MAXN+1];
    for(int i=0;i<36;i++)sq[i]=AL[key[i]];
    sq[36]=0;
    for(int i=0;i<n;i++)pt[i]=ct[i]==-2?'|':ct[i]<0?'?':AL[key[ct[i]]];
    pt[n]=0;
    printf("{\"score\":%.8f,\"square\":\"%s\",\"plaintext\":\"%s\",\"restart\":%d,\"iteration\":%d}\n",score/valid_windows,sq,pt,restart,iteration);fflush(stdout);
}
int main(int argc,char **argv) {
    if(argc<6||argc>7){fprintf(stderr,"usage: subsolve model cells restarts iterations seed [initial]\n");return 2;}
    FILE *f=fopen(argv[1],"rb");if(!f){perror("quad model");return 2;}
    size_t qlen=fread(quad,sizeof(float),QSIZE,f);fclose(f);
    if(qlen!=1874161){fprintf(stderr,"invalid marginal model size\n");return 2;}
    n=(int)strlen(argv[2]);if(n<4||n>=MAXN)return 2;
    for(int i=0;i<n;i++){
        ct[i]=argv[2][i]=='|'?-2:symbol(argv[2][i]);
        if(ct[i]<0&&argv[2][i]!='?'&&argv[2][i]!='|')return 2;
    }
    for(int i=0;i+3<n;i++){int valid=1;for(int j=0;j<4;j++)if(ct[i+j]==-2)valid=0;valid_windows+=valid;}
    if(!valid_windows)return 2;
    for(int s=0;s<36;s++)for(int i=0;i+3<n;i++) {
        int yes=0;for(int j=0;j<4;j++)if(ct[i+j]==s)yes=1;
        if(yes)affected[s][acount[s]++]=i;
    }
    int restarts=atoi(argv[3]),iterations=atoi(argv[4]);rng=strtoull(argv[5],0,10)+1;
    if(restarts<1||iterations<1)return 2;
    if(!rng)rng=1;
    int initial[36],hasinitial=argc==7;
    if(hasinitial){
        if(strlen(argv[6])!=36)return 2;
        int used[36]={0},missing[36],nm=0;
        for(int i=0;i<36;i++){
            initial[i]=symbol(argv[6][i]);
            if(initial[i]<0){if(argv[6][i]!='?')return 2;}
            else if(used[initial[i]]++)return 2;
        }
        for(int i=0;i<36;i++)if(!used[i])missing[nm++]=i;
        for(int i=0;i<36;i++)if(initial[i]<0)initial[i]=missing[--nm];
    }
    int freq[36]={0},order[36];for(int i=0;i<n;i++)if(ct[i]>=0)freq[ct[i]]++;
    for(int i=0;i<36;i++)order[i]=i;
    for(int i=0;i<36;i++)for(int j=i+1;j<36;j++)if(freq[order[j]]>freq[order[i]]){int t=order[i];order[i]=order[j];order[j]=t;}
    const char *priority="ENISRATDHULCGMXOBWFKZPVJYQ0123456789";
    /* priority is validated instead of silently allowing duplicated letters. */
    if(strlen(priority)!=36){fprintf(stderr,"bad priority\n");return 2;}
    double global=-1e99;int globalkey[36];
    for(int rs=0;rs<restarts;rs++) {
        int key[36];for(int i=0;i<36;i++)key[order[i]]=symbol(priority[i]);
        if(hasinitial && rs%4==0)memcpy(key,initial,sizeof key);
        else for(int j=0;j<(rs?40:0);j++){int a=ri(36),b=ri(36),t=key[a];key[a]=key[b];key[b]=t;}
        double current=fitness(key);int marks[MAXN]={0},epoch=0,indices[MAXN];
        if(current>global+1e-5){global=current;memcpy(globalkey,key,sizeof key);}
        for(int it=0;it<iterations;it++) {
            int a=ri(36),b=ri(36);if(a==b || (!freq[a]&&!freq[b]))continue;
            int count=0;epoch++;
            for(int z=0;z<acount[a];z++){int i=affected[a][z];marks[i]=epoch;indices[count++]=i;}
            for(int z=0;z<acount[b];z++){int i=affected[b][z];if(marks[i]!=epoch)indices[count++]=i;}
            double old=0;for(int z=0;z<count;z++)old+=window(key,indices[z]);
            int t=key[a];key[a]=key[b];key[b]=t;
            double after=0;for(int z=0;z<count;z++)after+=window(key,indices[z]);
            double delta=after-old;
            double phase=(double)(it%20000)/20000;
            double temperature=(2.8*(1-phase)+0.08)*(1-0.7*(double)it/iterations);
            if(delta>=0 || uniform()<exp(delta/temperature))current+=delta;
            else {t=key[a];key[a]=key[b];key[b]=t;}
            if(current>global+1e-5){global=current;memcpy(globalkey,key,sizeof key);}
        }
        /* Output the global incumbent after each restart; duplicate-free. */
        static double printed=-1e99;if(global>printed+1e-5){output(global,globalkey,rs,iterations);printed=global;}
    }
    return 0;
}
