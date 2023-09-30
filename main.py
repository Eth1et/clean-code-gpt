import openai
import json
import argparse
from pathlib import Path
from shutil import copy2
import os


class CleanedCode:
    
        original = ""
        clean = ""
        
        def __init__(self, original, clean):
            self.original = original
            self.clean = clean


class CleanedFile:  
    
    fragments = []
    filename = ""
    dirname = ""
    
    def __init__(self, fragments, filename, dirname) -> None:
        self.fragments = fragments
        self.filename = filename
        self.dirname = dirname
    

def get_response_content(response):
    return response['choices'][0]['message']['content']


def apply_config():
    
    with open("config.json") as cfg:
        CONFIG = json.load(cfg)
        openai.api_key = CONFIG['api_key']
        openai.organization = CONFIG['organization']
        return CONFIG['model']


def get_extensions():
    
    with open('language_extensions.json', 'r') as extensions:
        return json.load(extensions)['extensions']


def parse_args():
    
    parser = argparse.ArgumentParser()
    parser.version = '0.1'

    parser.add_argument('-e','--encoding', choices=('ascii', 'utf-7', 'utf-8', 'utf-16', 'utf-32'), default='utf-8')
    parser.add_argument('-cd','--copy_data', action='store_true', default=False)
    
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('-f', '--file', action='store')
    input_group.add_argument('-d','--dir', action='store')
    
    output_group = parser.add_mutually_exclusive_group()
    output_group.add_argument('-c','--console', action='store_true')
    output_group.add_argument('-o','--out', action='store')
    
    return vars(parser.parse_args())


def clean_file(file_path, input_path, encoding):
    
    with file_path.open('r', encoding=encoding) as file:
        code = ''.join(file.readline())
        
        ## TODO: handle too large input
        
        ## TODO: handle API exception
        
        ## TODO: call API
        
        cleanedFile = CleanedFile(
            [CleanedCode(code, "problem solved kekw")], 
            file_path.name, 
            file_path.relative_to(input_path).parent)
        
        return cleanedFile


def main():
    
    MODEL = apply_config()
    ARGS = parse_args()
    LANGUAGE_EXTENSIONS = get_extensions()

    INPUT_PATH = Path(ARGS['file']).parent  if ARGS['file'] != None  else Path(ARGS['dir']) 
    INPUT_PATH = INPUT_PATH.absolute()
    OUTPUT_PATH = Path(ARGS['out'])  if ARGS['out'] != None  else (INPUT_PATH / 'clean_code')
    
    cleanedFiles = []
    copiedFiles = []
    
    # Cleaning code files, marking others for copy
    if ARGS['file'] == None:
        for entry in Path(INPUT_PATH).glob('**/*'):
            
            if entry.is_file() and entry.suffix.lower() in LANGUAGE_EXTENSIONS:
                cleanedFiles.append(clean_file(entry, INPUT_PATH, ARGS['encoding']))
            
            elif entry.is_file() and ARGS['copy_data']:
                copiedFiles.append(entry)
                
    else:
        cleanedFiles.append(clean_file(Path(INPUT_PATH) / Path(ARGS['file']).name, INPUT_PATH, ARGS['encoding']))
    
    # Handling output directory
    if Path(OUTPUT_PATH).exists():
        
        if any(Path(OUTPUT_PATH).iterdir()):
            print(f"[ERROR] The output directory is not empty! ( {OUTPUT_PATH} )")
            
    else:
        Path(OUTPUT_PATH).mkdir(parents=True)
    
    # Writing output into files
    for cleanedFile in cleanedFiles:
        clean_code = ""
        
        for fragment in cleanedFile.fragments:
            clean_code = clean_code + fragment.clean
        
        dir = Path(OUTPUT_PATH) / cleanedFile.dirname
        if not dir.exists():
            dir.mkdir(parents=True)
        
        (dir / cleanedFile.filename).write_text(clean_code, encoding=ARGS['encoding'])
        
    # Copying marked files
    if ARGS['copy_data']:
        for copiedFile in copiedFiles:
            copy2(copiedFile, OUTPUT_PATH)
        

if __name__ == "__main__":
    
    try:
        main()
    except Exception as e:
        print(e)

    input('\n\nPress Enter to exit!')
