import subprocess
import argparse
from pathlib import Path
import json
import re


CONFIG_FOLDER_PATH = Path('configs')
COST_PATTERN = r'\$(\d+(?:\.\d+)?)'

ARGS = {}
MODELS = {}
DEFAULT_MODEL_NAME = ''
INSTRUCTIONS = {}


def load_models():
    global MODELS
    
    with open(Path(CONFIG_FOLDER_PATH) / 'models.json', 'r') as models:
        MODELS = json.load(models)


def apply_config():
    global DEFAULT_MODEL_NAME
    
    with open(Path(CONFIG_FOLDER_PATH) / 'config.json') as cfg:
        DEFAULT_MODEL_NAME = json.load(cfg)['default_model']


def parse_args():
    global ARGS
    
    parser = argparse.ArgumentParser()
    parser.version = '0.1'
    
    parser.add_argument('src', 
                        action='store', 
                        type=Path, 
                        help="Path to unclean file or directory."
                        )
    parser.add_argument('out', 
                        action='store', 
                        type=Path, 
                        help="Output directory path."
                        )
    parser.add_argument('instructions_path', 
                        action='store', 
                        type=Path, 
                        help='The path to the json file that contains all the instructions you want to run the clean with. For reference check instructions.json!'
                        )
    parser.add_argument('-m', 
                        '--model', 
                        action='store', 
                        default=DEFAULT_MODEL_NAME, 
                        choices=(MODELS.keys())
                        )
    parser.add_argument('-e', 
                        '--encoding', 
                        choices=('ascii', 'utf-7', 'utf-8', 'utf-16', 'utf-32'), 
                        default='utf-8'
                        )
    parser.add_argument('-p', 
                        '--preserve', 
                        action='store_true', 
                        default=False
                        )
    parser.add_argument('-cs', 
                        '--conflict-strategy', 
                        choices=('s', 'skip', 'o', 'overwrite', 'd', 'duplicate'), 
                        default='s'
                        )
    parser.add_argument('-cc', 
                        '--clean-count', 
                        action='store', 
                        default=1 , 
                        type=int, 
                        help="The number of times you want to clean each file [1;10]. It is used for benchmark."
                        )
    
    ARGS = vars(parser.parse_args())
    
    if not Path(ARGS['src']).exists():
        print(f"The source path doesn't exist! {ARGS['src']}")
        quit()
        
    if not Path(ARGS['out']).is_dir():
        print("The output directory is not a directory")
        quit()
        
    if not Path(ARGS['instructions_path']).exists():
        print(f"The instructions path doesn't exist! {ARGS['instructions_path']}")
        quit()
        
    if not (1 <= ARGS['clean_count'] <= 10):
        print(f"The clean count is outside of allowed range [1;10]! clean_count: {ARGS['clean_count']}")
        quit()
        

def load_instructions():
    global INSTRUCTIONS
    
    with open(ARGS['instructions_path'], 'r') as instructions:
        INSTRUCTIONS = json.load(instructions)


def main():
    total_cost = 0
    
    load_models()
    apply_config()
    parse_args()
    load_instructions()
    
    if not Path(ARGS['out']).exists():
        Path(ARGS['out']).mkdir()
    
    model = MODELS[ARGS['model']]['name']
    
    for instruction, _ in INSTRUCTIONS.items():
        print(f"Using Instruction: {instruction}")
        
        target_folder = Path(Path(ARGS['out']) / model) / instruction
        
        if not target_folder.exists():
            target_folder.mkdir(parents=True)
            
        command = [
            'python', './clean.py', 
            f'{ARGS["src"]}', 
            f'-o={target_folder}',
            f'-i={instruction}',
            f'-m={model}',
            f'-cs={ARGS["conflict_strategy"]}',
            f'-e={ARGS["encoding"]}',
        ]
        
        if ARGS['preserve']:
            command.append('-p')
        
        for _ in range(ARGS['clean_count']):
            process = subprocess.Popen(command, stdout=subprocess.PIPE, universal_newlines=True, encoding=ARGS["encoding"])

            for line in iter(process.stdout.readline, ""):
                for cost in re.findall(COST_PATTERN, line):
                    try:
                        total_cost += float(cost)
                    except ValueError:
                        pass
                    
                print(line, end="", flush=True)

            process.stdout.close()
            process.wait()
    
    print(f"[Finished multi-clean | Total Cost: ~${total_cost:.5}]\n")


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
