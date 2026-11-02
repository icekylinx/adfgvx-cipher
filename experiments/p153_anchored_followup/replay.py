"""Replay the bounded anchored-square cases with pinned source/model versions."""
from pathlib import Path
import argparse, hashlib, json, subprocess

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--solver',type=Path,required=True)
    p.add_argument('--model',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--case')
    a=p.parse_args(); here=Path(__file__).resolve().parent
    rows=json.loads((here/'cases.json').read_text())
    if a.case: rows=[r for r in rows if f"{r['case']}_k{r['width']}"==a.case]
    if not rows: p.error('No matching case')
    digest=hashlib.sha256(a.model.read_bytes()).hexdigest()
    if any(digest!=r['model_sha256'] for r in rows): p.error('Model SHA256 mismatch')
    a.output.mkdir(parents=True,exist_ok=True)
    for r in rows:
        label=f"{r['case']}_k{r['width']}"
        raw=f"{a.model.resolve()} {r['width']} {r['restarts']} {r['iterations_per_restart']} {r['seed']} 1\n"
        raw+=r['anchor']+'\n'+' '.join(['0']*r['width'])+'\n'+r['ciphertext']+'\n'
        (a.output/(label+'.in')).write_text(raw)
        with (a.output/(label+'.jsonl')).open('w') as out:
            subprocess.run([str(a.solver.resolve())],input=raw,text=True,stdout=out,check=True)
if __name__=='__main__': main()
