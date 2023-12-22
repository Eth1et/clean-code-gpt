import subprocess
import argparse
from pathlib import Path
import json


CONFIG_FOLDER_PATH = Path('configs')

MODELS = {}
INSTRUCTIONS = {}


def load_models():
    global MODELS, CONFIG_FOLDER_PATH
    
    with open(Path(CONFIG_FOLDER_PATH) / 'models.json', 'r') as models:
        MODELS = json.load(models)


def parse_args():
    global ARGS
    
    parser = argparse.ArgumentParser()
    parser.version = '0.1'
    
    parser.add_argument('-s', '--src', action='store', required=True, type=Path, help="Path to unclean file or directory.")
    parser.add_argument('-o', '--out', action='store', required=True, type=Path, help="Output directory path.")
    parser.add_argument('-i', '--instructions_path', action='store', required=True, type=Path, help='The path to the json file that contains all the instructions you want to run the clean with. For reference check instructions.json!')
    parser.add_argument('-m', '--model', action='store', default='gpt-3.5-turbo', choices=(MODELS.keys()))
    parser.add_argument('-e', '--encoding', choices=('ascii', 'utf-7', 'utf-8', 'utf-16', 'utf-32'), default='utf-8')
    parser.add_argument('-p', '--preserve', action='store_true', default=False)
    parser.add_argument('-cs', '--conflict-strategy', choices=('s', 'skip', 'o', 'overwrite', 'd', 'duplicate'), default='s')
    parser.add_argument('-cc', '--clean-count', action='store', default=1 , type=int, help="The number of times you want to clean each file [1;10]. It is used for benchmark.")
    
    ARGS = vars(parser.parse_args())
    
    if not Path(ARGS['src']).exists():
        print(f"The source path doesn't exist! {ARGS['src']}")
        quit()
        
    if not Path(ARGS['out']).exists():
        print(f"The output path doesn't exist! {ARGS['out']}")
        quit()
        
    if not Path(ARGS['instructions_path']).exists():
        print(f"The instructions path doesn't exist! {ARGS['instructions_path']}")
        quit()
        
    if not (1 <= ARGS['clean_count'] <= 10):
        print(f"The clean count is outside of allowed range [1;10]! clean_count: {ARGS['clean_count']}")
        quit()
        

def load_instructions():
    global INSTRUCTIONS, CONFIG_FOLDER_PATH
    
    with open(ARGS['instructions_path'], 'r') as instructions:
        INSTRUCTIONS = json.load(instructions)
    

def main():
    global INSTRUCTIONS, ARGS
    
    load_models()
    parse_args()
    load_instructions()
    
    model = MODELS[ARGS['model']]['name']
    
    for instruction, _ in INSTRUCTIONS.items():
        target_folder = Path(Path(ARGS['out']) / model) / instruction
        
        if not target_folder.exists():
            target_folder.mkdir(parents=True)
        
        for _ in range(ARGS['clean_count']):
            subprocess.run(f"python .\clean.py {ARGS['src']} -o {target_folder} -i={instruction} -m={model} -cs={ARGS['conflict_strategy']} -e={ARGS['encoding']} {'-p' if ARGS['preserve'] else ''}")


if __name__ == '__main__':
    main()
