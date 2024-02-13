import os
import openai
from dotenv import load_dotenv
import sys

sys.path.append("../")
import constants as const

# Get the constants
chat_gpt_key = const.chat_gpt_key

def ask_chat_gpt(question):
    try:
        # Ensure the OPENAI_API_KEY environment variable is set
        load_dotenv()

        with open('.env', 'w') as f:
            f.write(f'OPENAI_API_KEY={chat_gpt_key}\n')

        api_key = os.environ.get("OPENAI_API_KEY")

        if not api_key:
            raise ValueError("OpenAI API key not set in environment variables.")

        # Initialize the OpenAI client
        client = openai.OpenAI(api_key=api_key)

        # Create a chat completion
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": question + "Give me just the short answer without any explanation (it is is a salary, just the aproximete number but print it), (for age range just give me an aproximatley range))",
                }
            ],
            model="gpt-4",  # Change this if you're using a different model
        )

        # Parse the response
        response = chat_completion.choices[0].message.content
        return response

    except Exception as e:
        return f"An error occurred: {e}"

def main():

    # Test the chat GPT
    question = input("Ask a question: ")
    answer = ask_chat_gpt(question)
    print(answer)

if __name__ == "__main__":
    main()
