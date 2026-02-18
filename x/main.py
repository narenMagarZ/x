import argparse
import subprocess
import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()

api_key = os.getenv("OPEN_ROUTER_API_KEY")


def main() -> None:

    parser = argparse.ArgumentParser(prog="x", description="Prompt-based Linux command tool")
    parser.add_argument("-p", "--prompt", required=True, help="Prompt describing the command to run")

    args = parser.parse_args()
    prompt = args.prompt
    try:
        prefix = '''Return a single valid bash command that accomplishes the task.
            Do not include explanations, comments, markdown, backticks, or additional text.
            Output only the raw command.
        '''
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
            },
            data=json.dumps({
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": f"{prefix} {prompt}"}],
            }))
        command = response.json()["choices"][0]["message"]["content"]
        subprocess.run(command, shell=True)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
