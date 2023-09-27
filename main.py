import openai
import json

def get_response_content(response):
    return response['choices'][0]['message']['content']

CONFIG = json.load(open("config.json"))

MODEL = CONFIG['model']
openai.api_key = CONFIG['api_key']
openai.organization = CONFIG['organization']

response = openai.ChatCompletion.create(
    model=MODEL,
    
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who is considered to be the best cs2 player so far?"}
    ]
)

print(get_response_content(response))