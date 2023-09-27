import openai
import json
import argparse


def get_response_content(response):
    return response['choices'][0]['message']['content']


def init():
    CONFIG = json.load(open("config.json"))

    openai.api_key = CONFIG['api_key']
    openai.organization = CONFIG['organization']
    return CONFIG['model']


def parse_args():
    parser = argparse.ArgumentParser()
    parser.version = '0.1'
    parser.add_argument('-f', '--file', action='store', metavar='file', required=True)
    return vars(parser.parse_args())


def main():
    MODEL = init()
    ARGS = parse_args()
    
    file = open(ARGS['file'])
    code = "".join(file.readlines())
    
    

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)

    input()
