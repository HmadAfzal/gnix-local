import os
import json
import subprocess
import requests


CONFIG_DIR      = os.path.expanduser("~/.gnix")
CONFIG_FILE     = os.path.join(CONFIG_DIR, "config.json")
OLLAMA_BASE_URL = "http://localhost:11434"


def load_config() -> dict:
    if not os.path.exists(CONFIG_FILE):
        return {}

    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def save_config(config: dict):
    os.makedirs(CONFIG_DIR, exist_ok=True)

    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)


def is_first_run() -> bool:
    return not os.path.exists(CONFIG_FILE)


def get_model() -> str:
    config = load_config()
    return config.get("model", "")


def check_ollama_installed() -> bool:
    try:
        result = subprocess.run(
            ["ollama", "--version"],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False


def check_ollama_running() -> bool:
    try:
        requests.get(f"{OLLAMA_BASE_URL}", timeout=3)
        return True
    except requests.exceptions.ConnectionError:
        return False


def get_available_models() -> list:
    try:
        response = requests.get(
            f"{OLLAMA_BASE_URL}/api/tags",
            timeout=5
        )
        response.raise_for_status()
        data = response.json()
        models = [m["name"] for m in data.get("models", [])]
        return models

    except requests.exceptions.RequestException:
        return []


def validate_model(model_name: str) -> bool:
    available = get_available_models()
    for m in available:
        if model_name.lower() in m.lower():
            return True
    return False



def pull_model(model_name: str) -> bool:
    from gnix.display import bold, dim

    print(f"\n  {dim('pulling')} {bold(model_name)} {dim('from Ollama...')}")
    print(f"  {dim('this may take several minutes depending on your connection.')}\n")

    try:
        process = subprocess.Popen(
            ["ollama", "pull", model_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        for line in process.stdout:
            print(f"  {line}", end="")

        process.wait()

        if process.returncode == 0:
            print(f"\n  {bold(model_name)} pulled successfully.")
            return True
        else:
            print(f"\n  failed to pull {bold(model_name)}.")
            return False

    except FileNotFoundError:
        print("  error: Ollama is not installed.")
        return False

    except Exception as e:
        print(f"  error pulling model: {e}")
        return False


def run_model_selection() -> str:
    from gnix.display import bold, dim, bold_cyan, Symbol

    print(f"  {dim('available models on your machine:')}\n")

    available_models = get_available_models()

    if available_models:
        for i, model in enumerate(available_models, 1):
            print(f"    {dim(str(i) + '.')} {bold_cyan(model)}")
    else:
        print(f"    {dim('no models pulled yet.')}")

    print(f"\n    {dim('c.')} {dim('enter a custom model name')}")
    print()

    while True:
        choice = input(f"  {dim('select')} {bold('[number / c]')}: ").strip()

        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(available_models):
                selected = available_models[index]
                print(f"\n  {bold_cyan(Symbol.DIAMOND)}  {bold(selected)}")
                return selected
            else:
                print(f"  {dim('invalid. enter a number between 1 and ' + str(len(available_models)))}")

        elif choice.lower() == "c":
            custom = input(f"\n  {dim('model name')} {bold('(e.g. mistral:latest)')}: ").strip()

            if not custom:
                print(f"  {dim('model name cannot be empty. try again.')}")
                continue

            if validate_model(custom):
                print(f"\n  {bold_cyan(Symbol.DIAMOND)}  {bold(custom)}")
                return custom

            else:
                print(f"\n  {dim(bold(custom) + ' is not pulled yet.')}")
                pull_choice = input(
                    f"  {dim('pull it now? may take several minutes.')} {bold('[y/n]')}: "
                ).strip().lower()

                if pull_choice == "y":
                    success = pull_model(custom)
                    if success:
                        return custom
                    else:
                        print(f"\n  {dim('could not pull')} {bold(custom)}")
                        print(f"  {dim('check the name at:')} {bold('https://ollama.com/library')}\n")
                else:
                    print(f"\n  {dim('pull cancelled.')}")
                    print(f"  {dim('pull manually with:')} {bold('ollama pull <model-name>')}\n")

        else:
            print(f"  {dim('invalid. enter a number or c for custom.')}")



def run_first_time_setup():
    from gnix.display import (
        show_welcome,
        show_ollama_not_installed,
        show_ollama_not_running,
        show_no_models,
        bold, dim, green, Symbol
    )

    show_welcome()

    if not check_ollama_installed():
        show_ollama_not_installed()
        exit(1)

    if not check_ollama_running():
        show_ollama_not_running()
        exit(1)

    print(f"  {green(Symbol.CHECK)}  ollama is running\n")

    available_models = get_available_models()
    if not available_models:
        show_no_models()
        exit(1)

    print(f"  {dim('pick a model for Gnix to use.')}")
    print(f"  {dim('change anytime with:')} {bold('gnix --set-model')}\n")

    selected_model = run_model_selection()

    config = {
        "model": selected_model,
    }
    save_config(config)

    print(f"\n  {green(Symbol.CHECK)}  config saved")
    print(f"  {dim('try:')} {bold('gnix \"list all files\"')}\n")
    print(f"  {'─' * 52}\n")

    return selected_model