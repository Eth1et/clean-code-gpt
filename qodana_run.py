import argparse
import json
import subprocess
from pathlib import Path
import shutil
from tqdm import tqdm


CONFIG_FOLDER_PATH = Path('./configs/').absolute()

FOLDER = Path()
QODANA_TOKEN = ''
LINTERS = {}


def apply_config():
    global LINTERS, QODANA_TOKEN
    
    with open(Path(CONFIG_FOLDER_PATH) / 'qodana_run_config.json') as cfg:
        config = json.load(cfg)
        LINTERS, QODANA_TOKEN = config['linters'], config['qodana_token']


def parse_args():
    global FOLDER
    
    parser = argparse.ArgumentParser()
    parser.version = '0.1'
    
    parser.add_argument('folder', action='store', type=Path, help="Path to the scanned folder.")
    
    FOLDER = vars(parser.parse_args())['folder']
    
    if not FOLDER.exists():
        print(f"The path to the unclean files' folder doesn't exists! {FOLDER}")
        quit()


def contains_file_with_extensions(abs_path: Path, extensions: [str]):
    for entry in abs_path.glob("**/*"):
        for extension in extensions:
            if entry.is_file() and str(entry).strip().endswith(extension):
                return True

    return False


def run_qodana(abs_path: Path, linter: str):
    process = subprocess.Popen(
        ['qodana', 'scan', 
         '-i', str(abs_path), 
         '-l', linter,
         '-e', f'QODANA_TOKEN={QODANA_TOKEN}'
        ],
        stdout=subprocess.PIPE,
        universal_newlines=True,
        encoding='utf-8'
    )
    
    process.communicate(b'n')
    process.wait()

    shutil.rmtree(Path(abs_path / '.idea'))


def check_folder(abs_path: Path):
    for linter in tqdm(LINTERS.keys(), desc='Running linters on the given directory', unit='linter', total=len(LINTERS.keys())):
        
        if not contains_file_with_extensions(abs_path, LINTERS[linter]['extensions']):
            continue
        
        run_qodana(abs_path, linter)


def main():
    parse_args()
    apply_config()
    check_folder(FOLDER.absolute())
    

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
