#!/usr/bin/env python3
"""Render the source-count comparison from the verified p73 result.
ADFGVX Cipher. icekylinx and GPT-6 Astra Pro (2026). Apache-2.0.
"""
from pathlib import Path
import argparse,json,os,tempfile
os.environ.setdefault("MPLCONFIGDIR",str(Path(tempfile.gettempdir())/"adfgvx-matplotlib-cache"))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
HERE=Path(__file__).resolve().parent


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',type=Path,default=HERE/'p73_histogram_result.json')
    p.add_argument('--output',type=Path,default=HERE/'p73_coordinate_profile.svg')
    p.add_argument('--png',type=Path)
    args=p.parse_args();data=json.loads(args.input.read_text())
    target=next(row for row in data['inputs']if row['id']=='p73');known=target['known_coordinate_counts']
    means=[]
    for book in [71877,52118]:
        rows=[r for r in data['results']if r['target_id']=='p73'and r['book_id']==book and r['convention']=='plain']
        assert len(rows)==2
        vectors=[r['mean_counts_first_five']+[178-sum(r['mean_counts_first_five'])]for r in rows]
        means.append(np.mean(vectors,axis=0))
    plt.rcParams.update({'font.family':'DejaVu Sans','svg.fonttype':'none','svg.hashsalt':'adfgvx-p73-profile-v1','font.size':11,'axes.spines.top':False,'axes.spines.right':False})
    fig,ax=plt.subplots(figsize=(10.2,6.1));fig.subplots_adjust(left=.09,right=.98,bottom=.26,top=.79)
    x=np.arange(6);width=.245
    ax.bar(x-width,known,width,color='#244b68',label='p73: known source coordinates',zorder=3)
    ax.errorbar(x-width,known,yerr=[np.zeros(6),np.full(6,2)],fmt='none',color='#142c3e',capsize=4,lw=1.2,zorder=4)
    ax.bar(x,means[0],width,color='#6aa3a3',label='Lettow-Vorbeck reference mean',zorder=3)
    ax.bar(x+width,means[1],width,color='#c1b17b',label='Flex reference mean',zorder=3)
    for pos,value in zip(x-width,known):ax.text(pos,value+3,str(value),ha='center',va='bottom',fontsize=10,fontweight='bold',color='#142c3e')
    ax.set_xticks(x,data['coordinate_order']);ax.set_ylim(0,66);ax.set_ylabel('Coordinate count per 89-character message')
    ax.grid(axis='y',color='#d9e0e6',lw=.7,zorder=0);ax.set_axisbelow(True)
    ax.legend(loc='lower left',bbox_to_anchor=(0,1.02),frameon=False,fontsize=9.0,ncol=3,columnspacing=1.4,handlelength=1.6)
    fig.text(.09,.94,'p73 under the November 7–9 square',fontsize=20,fontweight='bold',color='#18354a')
    fig.text(.09,.88,'Coordinate totals survive every column transposition.',fontsize=12,color='#52626f')
    fig.text(.09,.15,'Whiskers show separate possibilities; only two erased coordinates exist in total.',fontsize=9,color='#40505d')
    fig.text(.09,.115,'Reference means use held-out joined-text windows and average the two unresolved 5/6 digit orders.',fontsize=9,color='#40505d')
    fig.text(.09,.08,'This comparison guides key research; it does not exclude a key or recover a plaintext.',fontsize=9,color='#40505d')
    fig.text(.09,.035,'ADFGVX Cipher · icekylinx and GPT-6 Astra Pro · Sources: Childs pp. 73, 155; PG71877; PG52118.',fontsize=8,color='#647481')
    fig.savefig(args.output,metadata={'Title':'p73 coordinate-count comparison','Creator':'icekylinx and GPT-6 Astra Pro','Date':None})
    if args.output.suffix.lower() == '.svg':
        args.output.write_text('\n'.join(line.rstrip() for line in args.output.read_text().splitlines())+'\n')
    if args.png:fig.savefig(args.png,dpi=160)
    plt.close(fig)

if __name__=='__main__':main()
