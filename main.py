import openai
import json
import argparse
from pathlib import Path
from shutil import copy2
import asyncio


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
        return CONFIG['model'], CONFIG['instruction']


def get_extensions():
    
    with open('language_extensions.json', 'r') as extensions:
        return json.load(extensions)['extensions']


def parse_args():
    
    parser = argparse.ArgumentParser()
    parser.version = '0.1'

    parser.add_argument('-e','--encoding', choices=('ascii', 'utf-7', 'utf-8', 'utf-16', 'utf-32'), default='utf-8')
    parser.add_argument('-p','--preserve', action='store_true', default=False)
    
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('-f', '--file', action='store')
    input_group.add_argument('-d','--dir', action='store')
    
    output_group = parser.add_mutually_exclusive_group()
    output_group.add_argument('-c','--console', action='store_true')
    output_group.add_argument('-o','--out', action='store')
    
    return vars(parser.parse_args())


async def chat_completion(code, model, instruction):
    response = await openai.ChatCompletion.create(
        model=model,
        messages=[
        {"role": "system", "content": instruction},
        {"role": "user", "content": code},
    ])
    
    print(response)
    
    return response['choices'][0]['message']['content']


async def clean_file(file_path, input_path, encoding, model, instruction):
    
    with file_path.open('r', encoding=encoding) as file:
        code = ''.join(file.readline())
        
        ## TODO: handle too large input
        
        clean_code = chat_completion(code, model, instruction)
        
        cleanedFile = CleanedFile(
            [CleanedCode(code, clean_code)], 
            file_path.name, 
            file_path.relative_to(input_path).parent)
        
        return cleanedFile


async def main():
    
    MODEL, INSTRUCTION = apply_config()
    ARGS = parse_args()
    LANGUAGE_EXTENSIONS = get_extensions()

    INPUT_PATH = Path(ARGS['file']).parent  if ARGS['file'] != None  else Path(ARGS['dir']) 
    INPUT_PATH = INPUT_PATH.absolute()
    OUTPUT_PATH = Path(ARGS['out'])  if ARGS['out'] != None  else (INPUT_PATH.parent / 'clean_code')
    
    cleanedFiles = []
    copiedFiles = []

    # Cleaning code files, marking others for copy
    for entry in Path(INPUT_PATH).glob('**/*'):
        
        if entry.is_file():
            if entry.suffix.lower() in LANGUAGE_EXTENSIONS and (ARGS['file'] == None or Path(ARGS['file']).samefile(entry)):
            
                file = entry  if ARGS['file'] == None  else (INPUT_PATH / Path(ARGS['file']).name) 
                cleanedFiles.append(clean_file(file, INPUT_PATH, ARGS['encoding'], MODEL, INSTRUCTION))
            
            elif ARGS['preserve']:
                copiedFiles.append(entry)       
    
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
    if ARGS['preserve']:
        
        for copiedFile in copiedFiles:   
            dir = copiedFile.relative_to(INPUT_PATH).parent
            dir = OUTPUT_PATH / dir 
            
            if not dir.exists():
                dir.mkdir(parents=True)
            
            copy2(copiedFile, dir / copiedFile.name)
        

if __name__ == "__main__":
    
    try:
        asyncio.run(main())
    except Exception as e:
        print(e)

    input('\n\nPress Enter to exit!')
