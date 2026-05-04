<div align="center">

<img src="https://raw.githubusercontent.com/HmadAfzal/gnix-local/main/assets/gnix-logo.png" width="120" style="border-radius: 16px"/>

# Gnix

**Natural language to shell commands. Local. Private. Free.**

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)](LICENSE)
[![Ollama](https://img.shields.io/badge/powered%20by-Ollama-orange.svg)](https://ollama.com)
[![PyPI Downloads](https://static.pepy.tech/personalized-badge/gnix?period=total&units=INTERNATIONAL_SYSTEM&left_color=GRAY&right_color=MAGENTA&left_text=downloads)](https://pepy.tech/projects/gnix)

[Website](https://gnix-local.vercel.app) · [PyPI](https://pypi.org/project/gnix/) · [Dataset](https://huggingface.co/datasets/llhax/nlbash-cleaned)

</div>

---

Gnix converts natural language into shell commands, running entirely on your machine.

```
$ gnix "find all python files modified in the last 7 days"

  │  shell   zsh
  │  model   qwen2.5:0.5b

  ▸  find all python files modified in the last 7 days

  ✦  Command
     find . -name '*.py' -mtime -7

  ▸  Finds all Python files in the current directory modified within the last 7 days.

  run this command? [y/n]: y
```

---

## Why Gnix

Most AI terminal tools send your commands to a remote server and require a paid API key. Gnix runs the model entirely on your machine — your commands never leave your computer.

| Feature | Other tools | Gnix |
|---|---|---|
| Runs locally | ✘ | ✔ |
| No API key required | ✘ | ✔ |
| No internet required | ✘ | ✔ |
| Private by default | ✘ | ✔ |
| Free forever | ✘ | ✔ |
| Built in safety layer | ✘ | ✔ |
| Bash and Zsh support | ✔ | ✔ |
| Choose your own model | ✘ | ✔ |

---

## Installation

### 1 — Install Ollama

Gnix uses Ollama to run AI models locally.

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### 2 — Pull a model

```bash
# Lightweight — works on any machine (400MB)
ollama pull qwen2.5:0.5b

# Better quality — needs 4GB RAM (2.2GB)
ollama pull phi3.5
```

Browse all available models at [ollama.com/library](https://ollama.com/library)

### 3 — Install Gnix

```bash
pip install gnix
```

### 4 — Run

```bash
gnix "list all files larger than 1GB"
```

On first run Gnix will guide you through selecting a model.

---

## Usage

### Generate and run a command

```bash
gnix "show disk usage of current folder"
gnix "find all log files older than 30 days"
gnix "list all running processes sorted by memory"
gnix "count lines in all python files"
gnix "create a compressed backup of the src folder"
```

### Explain a command

```bash
gnix --explain "tar -czf archive.tar.gz /home/user"
gnix --explain "find / -size +1G -type f 2>/dev/null"
```

### Dry run — generate without executing

```bash
gnix --dry-run "delete all temp files older than 7 days"
```

### Change model

```bash
gnix --set-model
```

---

## Safety

Gnix has a built in safety layer that detects dangerous commands before they run.

**Dangerous commands always require explicit confirmation:**

```
$ gnix "delete everything in the current folder"

  ✦  Command
     rm -rf *

  ▲  WARNING
  This command will recursively delete everything in the current
  directory and cannot be undone.

  type yes to confirm:
```

**Patterns that trigger warnings:**

- Recursive deletion — `rm -rf /`, `rm -rf ~`, `rm -rf *`
- Disk wiping — `dd if=`, `> /dev/sda`
- Filesystem formatting — `mkfs`, `mke2fs`
- Dangerous permissions — `chmod -R 777 /`
- Fork bombs — `:(){ :|:& };:`
- Remote script execution — `| bash`, `| sh`
- System file overwriting — `> /etc/passwd`, `> /etc/shadow`
- System shutdown — `shutdown`, `reboot`, `halt`

---

## How It Works

```
User types natural language
           │
           ▼
    Input validation
           │
           ▼
    Shell detection (bash / zsh)
           │
           ▼
    Local AI model via Ollama
    (runs entirely on your machine)
           │
           ▼
    Generated shell command
           │
           ▼
    Safety checker
    ┌────────┴────────┐
    │                 │
  Safe           Dangerous
    │                 │
    ▼                 ▼
  Explain          Warn user
  command          ask for
    │              confirmation
    ▼                 │
  Ask [y/n] ←────────┘
    │
    ▼
  Execute and show output
```

---

## Supported Models

Any model available in Ollama works with Gnix. Recommended options:

| Model | Size | RAM needed | Quality |
|---|---|---|---|
| `qwen2.5:0.5b` | 400MB | 1GB | Good for most tasks |
| `qwen2.5:1.5b` | 1GB | 2GB | Better quality |
| `phi3.5:latest` | 2.2GB | 4GB | Best quality |
| `llama3.2:3b` | 2GB | 4GB | Strong at reasoning |

Switch models anytime with `gnix --set-model`.

---

## Project Structure

```
gnix/
├── gnix/
│   ├── cli.py         — entry point, argument parsing
│   ├── model.py       — Ollama integration, command generation
│   ├── safety.py      — dangerous command detection
│   ├── executor.py    — command execution
│   ├── explain.py     — command explanation
│   ├── config.py      — user config, first run setup
│   └── display.py     — colors, symbols, spinner, UI
├── training/
│   ├── dataset.ipynb  — dataset preparation
│   ├── train.ipynb    — fine-tuning pipeline
│   └── README.md
├── tests/
│   ├── test_safety.py
│   ├── test_model.py
│   ├── test_config.py
│   └── test_executor.py
├── setup.py
└── requirements.txt
└── README.md
└── LICENSE
└── .gitignore
```

---

## Running Tests

```bash
pip install pytest
pytest tests/ -v
```

---

## Contributing

Contributions are welcome. Open an issue or submit a pull request on [GitHub](https://github.com/HmadAfzal/gnix-local).

---

## License

Apache 2.0 — see [LICENSE](LICENSE)

---

<div align="center">

[Gnix](https://gnix-local.vercel.app) · Built by [Hmad Afzal](https://github.com/HmadAfzal) · [hmadafzal00@gmail.com](mailto:hmadafzal00@gmail.com)

</div>