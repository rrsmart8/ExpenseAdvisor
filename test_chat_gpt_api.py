import os
from openai import OpenAI
from dotenv import load_dotenv

# CHATGPT_API_KEY
api_key = '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'

# Create or load the .env file
load_dotenv()

# Set the API key as an environment variable in the .env file
with open('.env', 'w') as f:
    f.write(f'OPENAI_API_KEY={api_key}\n')


client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "",
        }
    ],
    model="gpt-4-vision-preview",
)

print(chat_completion)
