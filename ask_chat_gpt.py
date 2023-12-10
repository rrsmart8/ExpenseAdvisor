import os
import openai
from dotenv import load_dotenv


def ask_chat_gpt(question):
    try:
        # Ensure the OPENAI_API_KEY environment variable is set
        load_dotenv()

        with open('.env', 'w') as f:
            f.write(f'OPENAI_API_KEY={"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"}\n')

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
                    "content": question + "Give me just the short answer without any explanation (it is is a number, just the number), (if there are some jobs, just list them))",
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
    question = input("Ask a question: ")
    # answer = ask_chat_gpt("List me all the states in the USA separated by a comma.")
    answer = ask_chat_gpt(question)
    print(answer)


if __name__ == "__main__":
    main()
