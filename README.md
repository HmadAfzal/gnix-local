gnix/                          ← root of the project
│
├── gnix/                      ← the actual Python package
│   ├── __init__.py            ← makes it a package
│   ├── cli.py                 ← entry point
│   ├── model.py               ← talks to Ollama
│   ├── safety.py              ← dangerous command detection
│   ├── executor.py            ← runs the command
│   └── explain.py             ← explains commands
│
├── training/                  ← ML pipeline notebooks
│   ├── dataset.ipynb          ← dataset preparation
│   ├── train.ipynb            ← fine-tuning script
│   └── README.md              ← explains training folder
│
├── tests/                     ← tests (week 3)
│   ├── test_safety.py
│   ├── test_model.py
│   └── test_executor.py
│
├── README.md                  ← main project readme
├── setup.py                   ← makes it pip installable
├── requirements.txt           ← dependencies
└── .gitignore                 ← files to ignore in git