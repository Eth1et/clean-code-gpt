import openai
import json
import argparse
from pathlib import Path
import aiofiles
import asyncio
import tiktoken
from tqdm import tqdm
from tenacity import retry, wait_random_exponential, stop_after_attempt
import math


CONFIG_FOLDER_PATH = "configs"
MODELS = {}
MODEL = {}
DEFAULT_MODEL_NAME = ""
DEFAULT_INSTRUCTION_NAME = ""
INSTRUCTION = ""
INSTRUCTIONS = {}
ARGS = {}
LANGUAGE_EXTENSIONS = []
ENCODER = None
INPUT_PATH = ""
OUTPUT_PATH = ""
TOTAL_COST = 0.0


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
    global DEFAULT_INSTRUCTION_NAME, DEFAULT_MODEL_NAME
    
    with open(Path(CONFIG_FOLDER_PATH) / 'config.json') as cfg:
        config = json.load(cfg)
        openai.api_key = config['api_key']
        openai.organization = config['organization']
        DEFAULT_MODEL_NAME, DEFAULT_INSTRUCTION_NAME = config['default_model'], config['default_instruction']


def load_models():
    global MODELS
    
    with open(Path(CONFIG_FOLDER_PATH) / 'models.json', 'r') as models:
        MODELS = json.load(models)


def load_extensions():
    global LANGUAGE_EXTENSIONS
    
    with open(Path(CONFIG_FOLDER_PATH) / 'language_extensions.json', 'r') as extensions:
        LANGUAGE_EXTENSIONS = json.load(extensions)['extensions']


def load_instructions():
    global INSTRUCTIONS, CONFIG_FOLDER_PATH
    
    with open(Path(CONFIG_FOLDER_PATH) / 'instructions.json', 'r') as instructions:
        INSTRUCTIONS = json.load(instructions)
    

def parse_args():
    global ARGS, INSTRUCTION
    
    parser = argparse.ArgumentParser()
    parser.version = '0.1'

    parser.add_argument('target',
                        action='store',
                        type=Path,
                        help="The target file's or directory's path."
                        )
    parser.add_argument('-e', 
                        '--encoding', 
                        choices=('ascii', 'utf-7', 'utf-8', 'utf-16', 'utf-32'),
                        default='utf-8'
                        )
    parser.add_argument('-m', 
                        '--model', 
                        choices=tuple(MODELS.keys()),
                        default=DEFAULT_MODEL_NAME
                        )
    parser.add_argument('-p', 
                        '--preserve', 
                        action='store_true',
                        default=False
                        )
    parser.add_argument('-c', 
                        '--console', 
                        action='store_true', 
                        default=False
                        )
    parser.add_argument('-cs', 
                        '--conflict-strategy', 
                        choices=('s', 'skip', 'o', 'overwrite', 'd', 'duplicate'), 
                        default='s'
                        )
    parser.add_argument('-i', 
                        '--instruction-name',
                        action='store', 
                        default=DEFAULT_INSTRUCTION_NAME, 
                        type=str, 
                        help='The key of the chosen instruction from instructions.json.'
                        )
    
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-co', 
                       '--console_only', 
                       action='store_true'
                       )
    group.add_argument('-o', 
                       '--out', 
                       action='store', 
                       type=Path, 
                       help="The output directory's path."
                       )

    ARGS = vars(parser.parse_args())
    INSTRUCTION = INSTRUCTIONS[ARGS['instruction_name']]

    if not Path(ARGS['target']).exists():
        print("The file or directory you've tried to clean doesn't exist!")
        quit()

    if ARGS['console_only'] and ARGS['preserve']:
        print("Cannot print preserved data to console.")
        print("Do not use (-c|--console) and (-p|--preserve) at the same time!")
        quit()
    
    if ARGS['console'] and ARGS['console_only']:
        print("Do not use (-c|--console) and (-co|--console_only) at the same time!")
        quit()
    
    if ARGS['out'] and ARGS['console_only']:
        print("Do not use (-c|--console) and (-p|--preserve) at the same time!")
        quit()
    

def create_messages(code_fragment):
    return [
        {"role": "system", "content": INSTRUCTION},
        {"role": "user", "content": code_fragment}
    ]


async def execute_tasks_with_progressbar(tasks, _desc, _unit):
    if len(tasks) == 0:
        print("There is nothing to write!")
        return
        
    for task_execution in tqdm(asyncio.as_completed(tasks), desc=_desc, unit=_unit, total=len(tasks)):
        await task_execution
    

@retry(wait=wait_random_exponential(min=1, max=200), stop=stop_after_attempt(30), reraise=True)
async def chat_completion(messages):
    try:
        response = await openai.ChatCompletion.acreate(
            model=MODEL['name'],
            messages=messages
        )
    except Exception as exception:
        print(exception)
        raise exception
    
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


async def remove_gpt_markdown(code_fragment: str):
    lines = code_fragment.splitlines()
    start = end = -1
    i, j = 0, len(lines)-1 
    
    while i < j:
        if lines[i].strip().startswith("```") and start == -1:
            start = i
        if lines[j].strip().startswith("```") and end == -1:
            end = j
            
        if start != -1 and end != -1:
            break
        
        i += 1
        j -= 1
    
    if start != -1:
        lines = lines[start+1:]
        if end != -1:
            end -= 1
        
    if end != -1:
        lines = lines[:end]
    
    return '\n'.join(lines)


def fragmentize_code(code, input_tokens):
    if input_tokens > MODEL['max_tokens'] * .48:  # Only placeholder, logic will be implemented later
        print(f'[ERROR] Too large input file: {input_tokens} (max: {MODEL["max_tokens"]})')
        return []
    
    return [code]


async def clean_fragments(cleaned_file, fragments, input_tokens, output_tokens):
    global TOTAL_COST
    
    for fragment in fragments:
        try:
            clean = await chat_completion(create_messages(fragment))
        except Exception as exception:
            print("[ERROR] Couldn't finish cleaning file, because of an error:")
            print(exception)
            break
        
        cleaned_file.fragments.append(CleanedCode(fragment, await remove_gpt_markdown(clean)))
        output_tokens += len(ENCODER.encode(clean))
    
    input_price = math.ceil(input_tokens / 1000) * MODEL['input_price']
    output_price = math.ceil(output_tokens / 1000) * MODEL['output_price']
    TOTAL_COST += input_price + output_price


async def clean_file(file_path, encoding):
    with file_path.open('r', encoding=encoding) as file:
        cleaned_file = CleanedFile([], file_path.name, file_path.relative_to(INPUT_PATH).parent)
        code = ''.join(file.readlines())

        if code.strip() == '':
            return cleaned_file
        
        input_tokens = count_tokens(create_messages(code))
        output_tokens = 3

        fragments = fragmentize_code(code, input_tokens)

        if len(fragments) == 0:
            return cleaned_file
        
        await clean_fragments(cleaned_file, fragments, input_tokens, output_tokens)
        
        return cleaned_file


async def clean_files(cleaned_files, copied_files):
    files = INPUT_PATH.glob('**/*') if INPUT_PATH.is_dir() else [INPUT_PATH]
    
    async def task(entry):
        if entry.is_file():
            if entry.suffix.lower() in LANGUAGE_EXTENSIONS:
                
                if not Path(OUTPUT_PATH / entry.name).exists() or ARGS['conflict_strategy'] not in ('s', 'skip'):
                    cleaned_files.append(await clean_file(entry, ARGS['encoding']))

            elif ARGS['preserve']:
                copied_files.append(entry)
    
    tasks = [task(entry) for entry in files]
    await execute_tasks_with_progressbar(tasks, "Processing Files", "file")


async def async_copy(source: Path, destination: Path):
    async with aiofiles.open(source, 'rb') as source_file:
        async with aiofiles.open(destination, 'wb') as destination_file:
            while True:
                data = await source_file.read(8192)
                if not data:
                    break

                await destination_file.write(data)


async def copy_preserved(copied_files):
    
    async def task(copied_file):
        directory = copied_file.relative_to(INPUT_PATH).parent
        directory = OUTPUT_PATH / directory 

        if not directory.exists():
            directory.mkdir(parents=True)

        await async_copy(copied_file, directory / copied_file.name)
    
    if ARGS['preserve']:
        tasks = [task(copied_file) for copied_file in copied_files]
        await execute_tasks_with_progressbar(tasks, "Copying Preserved", "file")


async def write_file(cleaned_file, clean_code):
    directory = Path(OUTPUT_PATH) / cleaned_file.dirname
    if not directory.exists():
        directory.mkdir(parents=True)
        
    full_path = Path(directory / cleaned_file.filename)
    if full_path.exists() and ARGS['conflict_strategy'] in ('d', 'duplicate'):
        original_filename = full_path.stem
        clone_id = 0

        while full_path.exists():
            full_path = full_path.with_name(f"{original_filename} ({clone_id}){full_path.suffix}")
            if clone_id == 100: 
                return
            clone_id += 1
    
    full_path.write_text(clean_code, encoding=ARGS['encoding'])


async def write_output(cleaned_files):
    
    async def task(cleaned_file):
        clean_code = ""

        for fragment in cleaned_file.fragments:
            clean_code += fragment.clean

        if ARGS['console'] or ARGS['console_only']:
            path = Path(cleaned_file.dirname) / cleaned_file.filename
            print(f"\n\n{'='*15} START OF <{path}>{'='*15}\n{clean_code}\n{'='*15} END OF <{path}>;{'='*15}\n\n")

        if not ARGS['console_only']:
            await write_file(cleaned_file, clean_code)
    
    tasks = [task(cleaned_file) for cleaned_file in cleaned_files]
    await execute_tasks_with_progressbar(tasks, "Writing Output", "file")
        

async def main():
    global INPUT_PATH, OUTPUT_PATH, ENCODER, MODEL
    
    apply_config()
    load_models()
    load_instructions()
    parse_args()
    load_extensions()

    MODEL = MODELS[ARGS['model']]
    ENCODER = tiktoken.encoding_for_model(MODEL['name'])
    INPUT_PATH = Path(ARGS['target']).absolute()
    OUTPUT_PATH = (INPUT_PATH.parent / 'clean_code') if ARGS['out'] is None else Path(ARGS['out'])
    
    cleaned_files = []
    copied_files = []

    if not ARGS['console_only']:
        if not Path(OUTPUT_PATH).exists():
            Path(OUTPUT_PATH).mkdir(parents=True)

    await clean_files(cleaned_files, copied_files)
    await write_output(cleaned_files)
    await copy_preserved(copied_files)
        

def end_run():
    print(f"[Finished cleaning all the files | Total Cost: ~${TOTAL_COST:.5}]\n")
    quit()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(e)
        
    end_run()
