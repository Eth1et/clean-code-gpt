import argparse
import json
import subprocess
from pathlib import Path


class Stat:
    def __init__(self, minimum: int, maximum: int, avg: float, total: int):
        self.minimum = minimum
        self.maximum = maximum
        self.avg = avg
        self.total = total
        
    def handle_null_total(self):
        if self.total == 0:
            self.minimum = 0
            self.maximum = 0 


CONFIG_FOLDER_PATH = Path('./configs/').absolute()
QODANA_OUTPUT_FOLDER = Path('./qodana_output/').absolute()

ARGS = {}
QODANA_TOKEN = ''
LINTERS = {}

def apply_config():
    global LINTERS, QODANA_TOKEN
    
    with open(Path(CONFIG_FOLDER_PATH) / 'stats_config.json') as cfg:
        config = json.load(cfg)
        LINTERS, QODANA_TOKEN = config['linters'], config['qodana_token']


def parse_args():
    global ARGS
    
    parser = argparse.ArgumentParser()
    parser.version = '0.1'
    
    parser.add_argument('unclean', action='store', type=Path, help="Path to unclean files' directory.")
    parser.add_argument('clean', action='store', type=Path, help="Path to the cleaned file/files.")
    parser.add_argument('-rd', '--root-depth', action='store', default=0, type=int, help="Set the clean directories' root depth. Within this depth, the stats will be displayed grouped by folders.") # ASDAD
    parser.add_argument('-cc', '--clean-count', action='store', type=int, default=1, help="The number of times each file was cleaned per root folder.")
        
    ARGS = vars(parser.parse_args())
    
    if not Path(ARGS['unclean']).exists():
        print(f"The path to the unclean files' folder doesn't exists! {ARGS['unclean']}")
        quit()
        
    if not Path(ARGS['clean']).exists():
        print(f"The path to the clean files' folder doesn't exists! {ARGS['clean']}")
        quit()
        
    if 0 > int(ARGS['root_depth']):
        print(f"Root Depth must be in range [0,inf] actual: {ARGS['root_depth']}")
        quit()
        
    if 0 > int(ARGS['clean_count']):
        print(f"Clean Count must be in range [0,inf] actual: {ARGS['clean_count']}")
        quit()


def structure_check():
    if ARGS['root_depth'] == 0: 
        return
    
    entries = list(Path(ARGS['clean']).iterdir())
    
    for i in range(ARGS['root_depth']):
        if len(entries) == 0:
            print(f"[ERROR] The clean folder is completely empty!")
            quit()
    
        new_entries = []
        
        for entry in entries:
            if not entry.is_dir():
                print(f"[ERROR] The clean folder is badly structured or the root-depth is inproperly used.\nMake sure there are NO files in the given root-depth!\nRoot-Depth = depth from 'clean' folder to the clean result's folder")
                quit()
            
            if i != ARGS['root_depth']-1:
                new_entries.extend(entry.iterdir())
        
        entries = new_entries


def contains_file_with_extensions(abs_path: Path, extensions: list(str)):
    for entry in abs_path.glob("**/*"):
        for extension in extensions:
            if entry.is_file() and str(entry).strip().endswith(extension):
                return True

    return False


def run_linter(abs_path: Path, linter: str):
    subprocess.run(
        ['qodana', 'scan', 
         '-i', str(abs_path), 
         '-o', str(QODANA_OUTPUT_FOLDER), 
         '-l', LINTERS[linter]['name'],
         '-e', f'QODANA_TOKEN={QODANA_TOKEN}'
        ])
    
    


def check_folder(abs_path: Path):
    res = {}
    
    for linter in LINTERS.keys():
        if not contains_file_with_extensions(abs_path, LINTERS[linter]['extensions']):
            res[linter] = Stat(0, 0, 0, 0)
            continue
        
        res[linter] = run_linter(abs_path, linter)
        
    return res 


def main():
    parse_args()
    apply_config()
    structure_check()
    
    unclean_stat = check_folder(ARGS['unclean'].absolute())
    

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)


## TODO: RUN QODANA, FINISH THIS
## TODO: CHECK EVERYTHING IF WORKS FROM DIFFERENT FOLDERS --> make everything absolute project wise