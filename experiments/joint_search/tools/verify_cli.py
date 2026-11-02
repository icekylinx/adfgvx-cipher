"""Exercise real parser/incumbent regressions using temporary flat models.

The flat tables are test fixtures only. They are not language models and do
not contribute to any reported cryptanalytic result.
"""
from pathlib import Path
import json
import struct
import subprocess
import tempfile

ROOT=Path(__file__).resolve().parent.parent
ALPHABET='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def main():
    results=[]
    with tempfile.TemporaryDirectory(prefix='adfgvx_cli_') as directory:
        folder=Path(directory)
        q37=folder/'flat37.bin';q37.write_bytes(b'\0'*(4*37**4))
        q36=folder/'flat36.bin';q36.write_bytes(b'\0'*(4*36**4))
        six=folder/'flat6.bin';six.write_bytes(struct.pack('<8sIIfIf',b'G6HASH2\0',1,0,-10.0,0,-10.0))

        def run(name,program,args=(),stdin=None,expected=2,output=False):
            process=subprocess.run([str(ROOT/'bin'/program),*map(str,args)],input=stdin,
                                   capture_output=True,text=True,check=False)
            assert process.returncode==expected,(name,process.returncode,process.stderr)
            if output:
                lines=[json.loads(line) for line in process.stdout.splitlines()]
                assert lines and all('score' in row for row in lines),name
            results.append(dict(case=name,returncode=process.returncode,nonempty_incumbent_required=output))

        for square in ['!'*36,'A'*36,'ABC']:
            run('substitution rejects malformed square '+str(len(results)),
                'subsolve_marginal',[q37,'AAAAAAAA',1,1,0,square])
        run('substitution records initial state with one skipped proposal',
            'subsolve_marginal',[q37,'AAAAAAAA',1,1,0],expected=0,output=True)

        def pair_input(square,ciphertext='AAAAAAAA',ranks='1 2'):
            return f'{q37} 2 1 1 0 1\n{square}\n{ranks}\n{ciphertext}\n'
        for program in ['pair_marginal', 'joint_rectangle_warm']:
            for square in ['!'*36,'A'*36,'A'+'?'*35]:
                run(program+' rejects malformed square '+str(len(results)),
                    program,stdin=pair_input(square))
            run(program+' records initial state with one proposal',
                program,stdin=pair_input('?'*36),expected=0,output=True)
            run(program+' rejects odd coordinates',program,stdin=pair_input('?'*36,'AAAAAAA'))

        base=[q36,six,.7,'AAAAAAAAAAAA',1,1,0]
        for square in ['!'*36,'A'*36,'?'*36]:
            run('exact-domain solver rejects malformed complete square '+str(len(results)),
                'joint_domain_subsolve6',base+[square])
        zero=base[:];zero[4]=0
        run('exact-domain solver rejects zero restarts','joint_domain_subsolve6',zero)
        zero=base[:];zero[5]=0
        run('exact-domain solver rejects zero iterations','joint_domain_subsolve6',zero)
        odd=base[:];odd[3]='A'*13
        run('exact-domain solver rejects odd coordinates','joint_domain_subsolve6',odd)
        run('exact-domain solver emits its initial incumbent','joint_domain_subsolve6',base+[ALPHABET],expected=0,output=True)

        run('anchor solver rejects partially specified rank list','anchored_joint',stdin=pair_input('?'*36,ranks='1 0'))
        run('anchor solver rejects odd coordinates','anchored_joint',stdin=pair_input('?'*36,'AAAAAAA'))
        run('anchor solver rejects invalid unknown glyph','anchored_joint',stdin=pair_input('!'*36))
    print(json.dumps(dict(schema='adfgvx-cli-regressions-v1',passed=len(results),
                          synthetic_flat_models_are_not_training_data=True,cases=results),indent=2))


if __name__=='__main__':main()
