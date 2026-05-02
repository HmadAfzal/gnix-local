import requests
import json
from gnix.config import OLLAMA_BASE_URL, get_model

OLLAMA_URL = f"{OLLAMA_BASE_URL}/api/generate"



def build_system_prompt(shell: str) -> str:
    return f"""You are an expert {shell} shell command generator.
Your job is to convert natural language instructions into {shell} shell commands.

Rules you must follow:
- Output ONLY the shell command
- No explanations
- No markdown formatting
- No backticks
- No code blocks
- Single line only
- If multiple commands are needed use && or ; to chain them
- Always prefer safe flags (e.g. use -i for rm when possible)

Examples:
User: list all files including hidden ones
Output: ls -la

User: find all python files modified in last 7 days
Output: find . -name '*.py' -mtime -7

User: show disk usage of current folder
Output: du -sh .

User: count lines in all python files
Output: find . -name '*.py' | xargs wc -l

User: show top 10 processes by memory usage
Output: ps aux --sort=-%mem | head -10"""



def generate_command(instruction: str, shell: str, model: str ) -> str:
    system_prompt = build_system_prompt(shell)
    payload = {
        "model":  get_model(),
        "system": system_prompt,
        "prompt": instruction,
        "stream": False,        
        "options": {
            "temperature": 0.1,
                               
            "num_predict": 100,
            "stop": ["\n", "```", "#"]  
        }
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=60
        )

        response.raise_for_status()
        data = response.json()

        command = data.get("response", "").strip()

        command = clean_command(command)

        return command

    except requests.exceptions.ConnectionError:
        print(" Error: Cannot connect to Ollama.")
        print(" Make sure Ollama is running: ollama serve")
        return ""

    except requests.exceptions.Timeout:
        print(" Error: Ollama took too long to respond.")
        print(" Try again or check if your model is loaded: ollama list")
        return ""

    except requests.exceptions.RequestException as e:
        print(f" Error communicating with Ollama: {e}")
        return ""


def clean_command(command: str) -> str:
    import re
    match = re.search(r'```(?:bash|zsh|sh)?\n?(.*?)(?:\n?```|$)', command, re.DOTALL)
    if match:
        command = match.group(1).strip()
    command = command.replace("`", "")

    if command.startswith("$ "):
        command = command[2:]

    command = command.split("\n")[0]
    command = command.strip()

    return command


def check_model_available(model: str ) -> bool:
    try:
        response = requests.get(
            "http://localhost:11434/api/tags",
            timeout=5
        )
        response.raise_for_status()
        data = response.json()

        available_models = [m["name"] for m in data.get("models", [])]

        for available in available_models:
            if model in available:
                return True

        return False

    except requests.exceptions.RequestException:
        return False