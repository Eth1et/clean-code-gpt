import openai
import json
import argparse
from pathlib import Path
from shutil import copy2
import tiktoken


MODELS = {}
MODEL = {}
DEFAULT_MODEL_NAME = ""
INSTRUCTION = ""
ARGS = {}
LANGUAGE_EXTENSIONS = []
ENCODER = None
INPUT_PATH = ""
OUTPUT_PATH = ""


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
        CONFIG = json.load(cfg)
        openai.api_key = CONFIG['api_key']
        openai.organization = CONFIG['organization']
        DEFAULT_MODEL_NAME, INSTRUCTION = CONFIG['default_model'], CONFIG['instruction']


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

    parser.add_argument('-e','--encoding', choices=('ascii', 'utf-7', 'utf-8', 'utf-16', 'utf-32'), default='utf-8')
    parser.add_argument('-m','--model', choices=tuple(MODELS.keys()), default=DEFAULT_MODEL_NAME)
    parser.add_argument('-p','--preserve', action='store_true', default=False)

    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('-f', '--file', action='store')
    input_group.add_argument('-d','--dir', action='store')
    
    output_group = parser.add_mutually_exclusive_group()
    output_group.add_argument('-c','--console', action='store_true')
    output_group.add_argument('-o','--out', action='store')

    ARGS = vars(parser.parse_args())

    if ARGS['console'] and ARGS['preserve']:
        print("Cannot print preserved data to console.")
        print("Do not use (-c|--console) and (-p|--preserve) at the same time!")
        end_run()
    

def create_messages(code_fragment):
    return [
        {"role" : "system", "content" : INSTRUCTION},
        {"role" : "user", "content" : code_fragment}
    ]


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


def clean_file(file_path, encoding):
    
    with file_path.open('r', encoding=encoding) as file:
        cleanedFile = CleanedFile([], file_path.name, file_path.relative_to(INPUT_PATH).parent)
        
        code = ''.join(file.readlines())
        num_tokens = count_tokens(create_messages(code))
        print(num_tokens)
        
        ## TODO: handle too large input
        fragments = [code]
        
        for fragment in fragments:
            cleanedFile.fragments.append(CleanedCode(fragment, chat_completion(create_messages(fragment)))) 
            
        return cleanedFile


def clean_files(cleanedFiles, copiedFiles):
    for entry in Path(INPUT_PATH).glob('**/*'):    
        if entry.is_file():
            if entry.suffix.lower() in LANGUAGE_EXTENSIONS and (ARGS['file'] is None or Path(ARGS['file']).samefile(entry)):
            
                file = entry  if ARGS['file'] is None  else (INPUT_PATH / Path(ARGS['file']).name) 
                cleanedFiles.append(clean_file(file, ARGS['encoding']))

            elif ARGS['preserve']:
                copiedFiles.append(entry)


def copy_preserved(copiedFiles):
    if ARGS['preserve']:
        
        for copiedFile in copiedFiles:   
            dir = copiedFile.relative_to(INPUT_PATH).parent
            dir = OUTPUT_PATH / dir 
            
            if not dir.exists():
                dir.mkdir(parents=True)
            
            copy2(copiedFile, dir / copiedFile.name)


def write_output(cleanedFiles):
    for cleanedFile in cleanedFiles:
        clean_code = ""
        
        for fragment in cleanedFile.fragments:
            clean_code = clean_code + fragment.clean
        
        if ARGS['console']:
            path = Path(cleanedFile.dirname) / cleanedFile.filename
            print(f"\n\n{'='*15} START OF <{path}>{'='*15}\n{clean_code}\n{'='*15} END OF <{path}>;{'='*15}\n\n")
        else:
            dir = Path(OUTPUT_PATH) / cleanedFile.dirname
            if not dir.exists():
                dir.mkdir(parents=True)

            (dir / cleanedFile.filename).write_text(clean_code, encoding=ARGS['encoding'])


def main():
    global INPUT_PATH, OUTPUT_PATH, ENCODER, MODEL
    
    apply_config()
    load_models()
    parse_args()
    load_extensions()

    MODEL = MODELS[ARGS['model']]
    ENCODER = tiktoken.encoding_for_model(MODEL['name'])
    INPUT_PATH = Path(ARGS['file']).parent  if ARGS['file'] != None  else Path(ARGS['dir']) 
    INPUT_PATH = INPUT_PATH.absolute()
    OUTPUT_PATH = Path(ARGS['out'])  if ARGS['out'] != None  else (INPUT_PATH.parent / 'clean_code')
    
    cleanedFiles = []
    copiedFiles = []

    if ARGS['console']:
        if Path(OUTPUT_PATH).exists():    
            if any(Path(OUTPUT_PATH).iterdir()):
                print(f"[ERROR] The output directory is not empty! ( {OUTPUT_PATH} )")
                return
        else:
            Path(OUTPUT_PATH).mkdir(parents=True)

    clean_files(cleanedFiles, copiedFiles)
    write_output(cleanedFiles)
    copy_preserved(copiedFiles)
        

def end_run():
    input("Press Enter to quit!")
    quit()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        
    end_run()
