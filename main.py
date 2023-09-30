import openai
import json
import argparse
from pathlib import Path
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
    CONFIG = json.load(open("config.json"))

    openai.api_key = CONFIG['api_key']
    openai.organization = CONFIG['organization']
    return CONFIG['model']


def parse_args():
    parser = argparse.ArgumentParser()
    parser.version = '0.1'

    parser.add_argument('-e','--encoding', choices=('ascii', 'utf-7', 'utf-8', 'utf-16', 'utf-32'), default='utf-8')
    
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('-f', '--file', action='store')
    input_group.add_argument('-d','--dir', action='store')
    
    output_group = parser.add_mutually_exclusive_group()
    output_group.add_argument('-c','--console', action='store_true')
    output_group.add_argument('-o','--out', action='store')
    
    return vars(parser.parse_args())


def main():
    MODEL = apply_config()
    ARGS = parse_args()
    
    INPUT_PATH = Path(ARGS['file']).parent  if ARGS['file'] != None  else Path(ARGS['dir']) 
    INPUT_PATH = INPUT_PATH.absolute()
    OUTPUT_PATH = ARGS['out']  if ARGS['out'] != None  else (INPUT_PATH / 'clean_code')
    
    cleanedFiles = []
    
    file = open(ARGS['file'], "r", encoding=ARGS['encoding'])
    code = "".join(file.readlines())
    
    # TODO: handling long input
    
    # TODO: handle API call fail
    ## if error occours -> ERROR message
    
    # TODO: API call
    
    cleanedFiles.append(CleanedFile(
        [CleanedCode(code, "problem solved xd")], 
        Path(ARGS['file']).name,
        Path(ARGS['file']).parent.absolute().relative_to(INPUT_PATH)))
    
    # Creating outut directory
    Path(OUTPUT_PATH).mkdir()
    
    # Writing output into files
    for cleanedFile in cleanedFiles:
        clean_code = ""
        
        for fragment in cleanedFile.fragments:
            clean_code = clean_code + fragment.clean
        
        (Path(OUTPUT_PATH) / cleanedFile.dirname / cleanedFile.filename).write_text(clean_code, encoding=ARGS['encoding'])
    

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)

    input()
