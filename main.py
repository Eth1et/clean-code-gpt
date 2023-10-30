import openai
import json
import argparse
from pathlib import Path
from shutil import copy2
import tiktoken
from tqdm import tqdm
from tenacity import retry, wait_random_exponential, stop_after_attempt
import math


MODELS = {}
MODEL = {}
DEFAULT_MODEL_NAME = ""
INSTRUCTION = ""
ARGS = {}
LANGUAGE_EXTENSIONS = []
ENCODER = None
INPUT_PATH = ""
OUTPUT_PATH = ""
TOTAL_COST = 0


class CleanedCode:
    def __init__(self, original, clean):
        self.original = original
        self.clean = clean


class CleanedFile:  
    def __init__(self, fragments, filename, dirname) -> None:
        self.fragments = fragments
        self.filename = filename
        self.dirname = dirname


def apply_config():
    global INSTRUCTION, DEFAULT_MODEL_NAME
    
    with open("config.json") as cfg:
        config = json.load(cfg)
        openai.api_key = config['api_key']
        openai.organization = config['organization']
        DEFAULT_MODEL_NAME, INSTRUCTION = config['default_model'], config['instruction']


def load_models():
    global MODELS
    
    with open('models.json', 'r') as models:
        MODELS = json.load(models)


def load_extensions():
    global LANGUAGE_EXTENSIONS
    
    with open('language_extensions.json', 'r') as extensions:
        LANGUAGE_EXTENSIONS = json.load(extensions)['extensions']


def parse_args():
    global ARGS
    
    parser = argparse.ArgumentParser()
    parser.version = '0.1'

    parser.add_argument('-e', '--encoding', choices=('ascii', 'utf-7', 'utf-8', 'utf-16', 'utf-32'), default='utf-8')
    parser.add_argument('-m', '--model', choices=tuple(MODELS.keys()), default=DEFAULT_MODEL_NAME)
    parser.add_argument('-p', '--preserve', action='store_true', default=False)
    parser.add_argument('-c', '--console', action='store_true', default=False)

    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('-f', '--file', action='store')
    input_group.add_argument('-d', '--dir', action='store')
    
    output_group = parser.add_mutually_exclusive_group()
    output_group.add_argument('-co', '--console_only', action='store_true')
    output_group.add_argument('-o', '--out', action='store')

    ARGS = vars(parser.parse_args())

    if ARGS['console_only'] and ARGS['preserve']:
        print("Cannot print preserved data to console.")
        print("Do not use (-c|--console) and (-p|--preserve) at the same time!")
        end_run()
    
    if ARGS['console'] and ARGS['console_only']:
        print("Do not use (-c|--console) and (-co|--console_only) at the same time!")
        end_run()
    
    if ARGS['out'] and ARGS['console_only']:
        print("Do not use (-c|--console) and (-p|--preserve) at the same time!")
        end_run()
    

def create_messages(code_fragment):
    return [
        {"role" : "system", "content": INSTRUCTION},
        {"role" : "user", "content": code_fragment}
    ]


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6), reraise=True)
def chat_completion(messages):
    response = openai.ChatCompletion.create(
        model=MODEL['name'],
        messages=messages
    )

    return response['choices'][0]['message']['content']


def count_tokens(messages):
    num_tokens = 3
    
    for message in messages:
        num_tokens += 3
        for key, value in message.items():
            num_tokens += len(ENCODER.encode(value))
            if key == "name":
                num_tokens += 1
                
    return num_tokens


def fragmentize_code(code, input_tokens):
    if input_tokens > MODEL['max_tokens']:  ## Only placeholder, logic will be implemented later
        print(f'[ERROR] Too large imput file: {input_tokens} (max: {MODEL["max_tokens"]})')
        return []
        
    return [code]


def clean_fragments(cleaned_file, fragments, input_tokens, output_tokens):
    global TOTAL_COST
    
    print(f"[Cleaning {cleaned_file.filename}]")
    
    for fragment in tqdm(fragments, desc="Processing Fragments"):
        clean = ""
        
        try:
            clean = chat_completion(create_messages(fragment))
        except Exception as e:
            print("[ERROR] Couldn't finish cleaning file, because of an error:")
            print(e)
            break
        
        cleaned_file.fragments.append(CleanedCode(fragment, clean))
        output_tokens += len(ENCODER.encode(clean))
    
    input_price = math.ceil(input_tokens / 1000) * MODEL['input_price']
    output_price = math.ceil(output_tokens / 1000) * MODEL['output_price']
    TOTAL_COST += input_price + output_price
    
    print(f"[Cleaned {cleaned_file.filename} for ~${input_price + output_price}]")


def clean_file(file_path, encoding):
    
    with file_path.open('r', encoding=encoding) as file:
        cleaned_file = CleanedFile([], file_path.name, file_path.relative_to(INPUT_PATH).parent)
        
        code = ''.join(file.readlines())
        
        input_tokens = count_tokens(create_messages(code))
        output_tokens = 3

        fragments = fragmentize_code(code, input_tokens)

        if len(fragments) == 0:
            return cleaned_file
        
        clean_fragments(cleaned_file, fragments, input_tokens, output_tokens)
        
        return cleaned_file


def clean_files(cleaned_files, copied_files):
    for entry in Path(INPUT_PATH).glob('**/*'):    
        if entry.is_file():
            if entry.suffix.lower() in LANGUAGE_EXTENSIONS and (ARGS['file'] is None or Path(ARGS['file']).samefile(entry)):
            
                file = entry if ARGS['file'] is None else (INPUT_PATH / Path(ARGS['file']).name) 
                cleaned_files.append(clean_file(file, ARGS['encoding']))

            elif ARGS['preserve']:
                copied_files.append(entry)


def copy_preserved(copied_files):
    if ARGS['preserve']:
        
        for copiedFile in copied_files:   
            dir = copiedFile.relative_to(INPUT_PATH).parent
            dir = OUTPUT_PATH / dir 
            
            if not dir.exists():
                dir.mkdir(parents=True)
            
            copy2(copiedFile, dir / copiedFile.name)


def write_output(cleaned_files):
    for cleaned_file in cleaned_files:
        clean_code = ""
        
        for fragment in cleaned_file.fragments:
            clean_code = clean_code + fragment.clean
        
        if ARGS['console'] or ARGS['console_only']:
            path = Path(cleaned_file.dirname) / cleaned_file.filename
            print(f"\n\n{'='*15} START OF <{path}>{'='*15}\n{clean_code}\n{'='*15} END OF <{path}>;{'='*15}\n\n")
        
        if not ARGS['console_only']:
            dir = Path(OUTPUT_PATH) / cleaned_file.dirname
            if not dir.exists():
                dir.mkdir(parents=True)

            (dir / cleaned_file.filename).write_text(clean_code, encoding=ARGS['encoding'])


def main():
    global INPUT_PATH, OUTPUT_PATH, ENCODER, MODEL
    
    apply_config()
    load_models()
    parse_args()
    load_extensions()

    MODEL = MODELS[ARGS['model']]
    ENCODER = tiktoken.encoding_for_model(MODEL['name'])
    INPUT_PATH = Path(ARGS['dir']  if ARGS['file'] is None else Path(ARGS['file']).parent) 
    INPUT_PATH = INPUT_PATH.absolute()
    OUTPUT_PATH = (INPUT_PATH.parent / 'clean_code') if ARGS['out'] is None else Path(ARGS['out'])
    
    cleaned_files = []
    copied_files = []

    if not ARGS['console_only']:
        if Path(OUTPUT_PATH).exists():    
            if any(Path(OUTPUT_PATH).iterdir()):
                print(f"[ERROR] The output directory is not empty! ( {OUTPUT_PATH} )")
                return
        else:
            Path(OUTPUT_PATH).mkdir(parents=True)

    clean_files(cleaned_files, copied_files)
    write_output(cleaned_files)
    copy_preserved(copied_files)
        

def end_run():
    input(f"[Finished cleaning all the files | Total Cost: ~${TOTAL_COST}]")
    quit()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        
    end_run()
