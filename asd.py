import subprocess
from pathlib import Path
from shutil import rmtree
import json


QODANA_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJvcmdhbml6YXRpb24iOiIzQnhXeCIsInByb2plY3QiOiJ6OEJZOSIsInRva2VuIjoicFZhYWQifQ.2irKZxTExkR6ANo4ok97dDi4A1avmi8Fo5MpH4PNU9E"


def run_qodana(abs_in: Path, abs_out: Path, linter: str) -> int:
    process = subprocess.Popen(
        ['qodana', 'scan', 
         '-i', str(abs_in), 
         '-o', str(abs_out),
         '-l', linter,
         '-e', f'QODANA_TOKEN={QODANA_TOKEN}'
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        encoding='utf-8'
    )
    
    process.wait()

    rmtree(Path(abs_in / '.idea'))
    
    total_warnings = 0
    
    with open(abs_out / 'qodana-short.sarif.json') as sarif:
        info = json.load(sarif)
        total_warnings = info['runs'][0]['properties']['qodanaNewResultSummary']['total']
        
    rmtree(abs_out)
    abs_out.mkdir()
    
    return total_warnings


print(f"eredmény: {run_qodana(Path('./sample_unclean').absolute(), Path('./qodana_output').absolute(), 'jetbrains/qodana-js:latest')}")