import sys
import time
import threading

class Color:
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    BLUE    = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN    = "\033[96m"
    WHITE   = "\033[97m"

    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    ITALIC  = "\033[3m"

    RESET   = "\033[0m"

def cyan(text):   return f"{Color.CYAN}{text}{Color.RESET}"
def green(text):  return f"{Color.GREEN}{text}{Color.RESET}"
def yellow(text): return f"{Color.YELLOW}{text}{Color.RESET}"
def red(text):    return f"{Color.RED}{text}{Color.RESET}"
def dim(text):    return f"{Color.DIM}{text}{Color.RESET}"
def bold(text):   return f"{Color.BOLD}{text}{Color.RESET}"
def magenta(text):return f"{Color.MAGENTA}{text}{Color.RESET}"

def bold_cyan(text):   return f"{Color.BOLD}{Color.CYAN}{text}{Color.RESET}"
def bold_green(text):  return f"{Color.BOLD}{Color.GREEN}{text}{Color.RESET}"
def bold_red(text):    return f"{Color.BOLD}{Color.RED}{text}{Color.RESET}"
def bold_yellow(text): return f"{Color.BOLD}{Color.YELLOW}{text}{Color.RESET}"



class Symbol:
    DIAMOND   = "◆"
    ARROW     = "▸"
    CHECK     = "✔"
    CROSS     = "✘"
    WARN      = "▲"
    DOT       = "•"
    LINE      = "─"
    SPARKLE   = "✦"
    PIPE      = "│"



class Spinner:

    FRAMES = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

    def __init__(self, message: str = "Thinking"):
        self.message   = message
        self._running  = False
        self._thread   = None

    def _spin(self):
        i = 0
        while self._running:
            frame = self.FRAMES[i % len(self.FRAMES)]
            sys.stdout.write(f"\r  {cyan(frame)} {dim(self.message)}...")
            sys.stdout.flush()
            time.sleep(0.08)
            i += 1

    def start(self):
        self._running = True
        self._thread  = threading.Thread(target=self._spin, daemon=True)
        self._thread.start()

    def stop(self, clear: bool = True):
        self._running = False
        if self._thread:
            self._thread.join()
        if clear:
            sys.stdout.write("\r" + " " * 40 + "\r")
            sys.stdout.flush()


OCTOPUS = [
    "⠀⠀⠀⠀⠀⠀⢀⣀⣠⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
    "⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣷⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
    "⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀⣠⣶⣾⣷⣶⣄⠀⠀⠀⠀⠀",
    "⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⢰⣿⠟⠉⠻⣿⣿⣷⠀⠀⠀⠀",
    "⠀⠀⠀⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⢷⣄⠘⠿⠀⠀⠀⢸⣿⣿⡆⠀⠀⠀",
    "⠀⠀⠀⠀⠈⠿⣿⣿⣿⣿⣿⣀⣸⣿⣷⣤⣴⠟⠀⠀⠀⠀⢀⣼⣿⣿⠁⠀⠀⠀",
    "⠀⠀⠀⠀⠀⠀⠈⠙⣛⣿⣿⣿⣿⣿⣿⣿⣿⣦⣀⣀⣀⣴⣾⣿⣿⡟⠀⠀⠀⠀",
    "⠀⠀⠀⢀⣠⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠋⣠⣤⣀⠀⠀",
    "⠀⠀⣴⣿⣿⣿⠿⠟⠛⠛⢛⣿⣿⣿⣿⣿⣿⣧⡈⠉⠁⠀⠀⠀⠈⠉⢻⣿⣧⠀",
    "⠀⣼⣿⣿⠋⠀⠀⠀⠀⢠⣾⣿⣿⠟⠉⠻⣿⣿⣿⣦⣄⠀⠀⠀⠀⠀⣸⣿⣿⠃",
    "⠀⣿⣿⡇⠀⠀⠀⠀⠀⣿⣿⡿⠃⠀⠀⠀⠈⠛⢿⣿⣿⣿⣿⣶⣿⣿⣿⡿⠋⠀",
    "⠀⢿⣿⣧⡀⠀⣶⣄⠘⣿⣿⡇⠀⠀⠠⠶⣿⣶⡄⠈⠙⠛⠻⠟⠛⠛⠁⠀⠀⠀",
    "⠀⠈⠻⣿⣿⣿⣿⠏⠀⢻⣿⣿⣄⠀⠀⠀⣸⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⣿⣿⣿⣶⣾⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠛⠛⠛⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
]


def show_welcome(version: str = "0.1.0"):
    import re

    GITHUB = "https://github.com/HmadAfzal/gnix-local"
    EMAIL  = "hmadafzal00@gmail.com"
    D      = "- "
    RIGHT_W = 44

    def dashed(label: str, width: int) -> str:
        fill = width - len(label) - 2
        dash = D * (fill // 4)
        return f"{dash} {label} {dash}"

    right_lines = [
        "",
        f"  {bold_cyan('GNIX')}  {dim('v' + version)}",
        "",
        f"  {bold('Natural language to shell commands.')}",
        f"  {dim('Local. Private. Free.')}",
        "",
        f"  {cyan(dashed('', RIGHT_W - 4))}",
        "",
        f"  {dim('github')}   {bold(GITHUB)}",
        f"  {dim('mail')}     {dim(EMAIL)}",
        "",
        f"  {cyan(dashed('', RIGHT_W - 4))}",
        "",
        f"  {dim('set model:')}  {bold('gnix --set-model')}",
        f"  {dim('get help:')}   {bold('gnix --help')}",
        "",
    ]

    total_rows = max(len(OCTOPUS), len(right_lines))

    print()
    for i in range(total_rows):
        oct_line = OCTOPUS[i] if i < len(OCTOPUS) else " " * 28
        left     = cyan(oct_line)
        right    = right_lines[i] if i < len(right_lines) else ""
        print(f"  {left}  {right}")
    print()


def divider(width: int = 52):
    print(f"\n  {dim(Symbol.LINE * width)}\n")


def show_session_info(shell: str, model: str):
    print()
    print(f"  {dim(Symbol.PIPE)}  {dim('shell')}   {bold(shell)}")
    print(f"  {dim(Symbol.PIPE)}  {dim('model')}   {bold(model)}")
    print()


def show_command(command: str):
    print(f"  {bold_cyan(Symbol.SPARKLE + '  Command')}")
    print(f"    {bold_green(command)}")
    print()



def show_explanation(explanation: str):

    print(f"  {dim(Symbol.ARROW)}  {dim(explanation)}")
    print()



def prompt_confirm() -> str:

    return input(f"  {dim('run this command?')} {bold('[y/n]')}: ").strip().lower()


def prompt_dangerous_confirm() -> str:

    return input(f"  {bold_red('type yes to confirm')}: ").strip().lower()


def show_warning(message: str):

    print(f"  {bold_red(Symbol.WARN + '  WARNING')}")
    print(f"  {red(message)}")
    print()


def show_error(message: str):

    print(f"\n  {bold_red(Symbol.CROSS + '  Error')}")
    print(f"  {red(message)}\n")


def show_success(message: str):

    print(f"  {bold_green(Symbol.CHECK + '  ' + message)}")


def show_cancelled():
    print(f"\n  {dim('cancelled.')}\n")


def show_dry_run():
    print(f"  {dim(Symbol.ARROW)}  {dim('dry run — command was not executed.')}\n")



def show_ollama_not_running():
    print()
    print(f"  {bold_red(Symbol.CROSS + '  Ollama is not running')}")
    print(f"  {dim('start it with:')}  {bold('ollama serve')}")
    print()


def show_ollama_not_installed():
    print()
    print(f"  {bold_red(Symbol.CROSS + '  Ollama is not installed')}")
    print(f"  {dim('install it with:')}")
    print(f"  {bold('  curl -fsSL https://ollama.com/install.sh | sh')}")
    print(f"  {dim('then run gnix again.')}")
    print()


def show_no_models():
    print()
    print(f"  {bold_yellow(Symbol.WARN + '  No models found in Ollama')}")
    print(f"  {dim('pull a model first:')}")
    print(f"  {bold('  ollama pull qwen2.5:0.5b')}")
    print(f"  {dim('browse all models at:')} {bold('https://ollama.com/library')}")
    print()


def show_model_updated(model: str):
    print()
    print(f"  {bold_green(Symbol.CHECK + '  Model updated to:')} {bold_cyan(model)}")
    print(f"  {dim('change anytime with:')} {bold('gnix --set-model')}")
    print()


def show_generating(query: str):
    print(f"  {dim(Symbol.ARROW)}  {dim(query)}")