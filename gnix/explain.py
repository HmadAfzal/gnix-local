import requests
from gnix.config import OLLAMA_BASE_URL, get_model

OLLAMA_URL = f"{OLLAMA_BASE_URL}/api/generate"

def build_brief_prompt(shell: str) -> str:
    return f"""You are a {shell} shell expert.
Your job is to explain shell commands in plain English.

Rules:
- One sentence only
- No bullet points
- No markdown
- Plain English
- Start with a verb
- Maximum 20 words

Examples:
Command: ls -la
Explanation: Lists all files including hidden ones with detailed info like size and permissions.

Command: du -sh .
Explanation: Shows the total disk space used by the current directory in human readable format.

Command: find . -name '*.py' -mtime -7
Explanation: Finds all Python files in the current directory modified within the last 7 days.

Command: ps aux --sort=-%mem | head -10
Explanation: Shows the top 10 processes consuming the most memory on your system."""


def build_detailed_prompt(shell: str) -> str:
    return f"""You are a {shell} shell expert and teacher.
Your job is to explain shell commands clearly and in detail.

Rules:
- Explain what the command does overall in one sentence
- Then break down each part, flag, or argument
- Use plain English
- No markdown headers
- Keep it concise but complete
- Maximum 100 words total

Example:
Command: tar -czf archive.tar.gz /home/user

Explanation:
Creates a compressed archive of the /home/user directory.

  tar     — tape archive tool for bundling files
  -c      — create a new archive
  -z      — compress using gzip
  -f      — specify the output filename
  archive.tar.gz — the name of the output file
  /home/user     — the directory to archive"""


def explain_command(command: str, shell: str, detailed: bool = False) -> str:
    if detailed:
        system_prompt = build_detailed_prompt(shell)
        max_tokens    = 200     # detailed needs more tokens
    else:
        system_prompt = build_brief_prompt(shell)
        max_tokens    = 60    

    payload = {
        "model": get_model(),
        "system": system_prompt,
        "prompt": f"Command: {command}",
        "stream": False,
        "options": {
            "temperature": 0.3,         
                                       
            "num_predict": max_tokens,
            "stop": ["\n\n"]           
        }
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=30
        )

        response.raise_for_status()
        data = response.json()

        explanation = data.get("response", "").strip()
        explanation = clean_explanation(explanation)

        return explanation

    except requests.exceptions.ConnectionError:
        return "Could not connect to Ollama to generate explanation."

    except requests.exceptions.Timeout:
        return "Ollama took too long to respond."

    except requests.exceptions.RequestException as e:
        return f"Error getting explanation: {e}"



def clean_explanation(explanation: str) -> str:
    explanation = explanation.replace("**", "")
    explanation = explanation.replace("__", "")
    explanation = explanation.replace("*", "")

    prefixes_to_remove = [
        "Explanation:",
        "explanation:",
        "Answer:",
        "answer:",
    ]
    for prefix in prefixes_to_remove:
        if explanation.startswith(prefix):
            explanation = explanation[len(prefix):].strip()

    explanation = explanation.strip()

    return explanation