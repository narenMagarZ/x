import argparse
import subprocess
import os
from dotenv import load_dotenv
import requests
import json
from pathlib import Path
from datetime import datetime

load_dotenv()


api_key = os.getenv("OPEN_ROUTER_API_KEY")
gpt_model = os.getenv("GPT_MODEL")
role = os.getenv("ROLE")

if api_key is None or gpt_model is None or role is None:
    print("Please set the OPEN_ROUTER_API_KEY, GPT_MODEL, and ROLE environment variables.")
    exit(1)


def write_log(command: str, prompt: str) -> None:
    try:
        home_path = Path.home() 
        x_log_path = f"{home_path}/.local/state/x"   
        os.makedirs(x_log_path, exist_ok=True)
        with open(f"{x_log_path}/x.log", "a") as file:
            file.write(f"[INFO {datetime.now()}] [COMMAND] {command} [PROMPT] {prompt}\n")
    except Exception as e:
        print("Failed to log command prompt")

def main() -> None:

    parser = argparse.ArgumentParser(prog="x", description="Prompt-based Linux command tool")
    parser.add_argument("-p", "--prompt", required=True, help="Prompt describing the command to run")

    args = parser.parse_args()
    prompt = args.prompt
    try:
        # TODO: verify if command is safe to use
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
                "model": gpt_model,
                "messages": [{"role": role, "content": f"{prefix} {prompt}"}],
            }))
        command = response.json()["choices"][0]["message"]["content"]

        write_log(command, prompt)

        subprocess.run(command, shell=True)
        
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
