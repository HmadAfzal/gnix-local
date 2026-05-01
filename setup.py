from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="gnix",
    version="0.1.0",
    author="Hmad Afzal",
    author_email="hmadafzal00@gmail.com",
    description="Natural language to shell commands. Local. Private. Free.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HmadAfzal/gnix-local",
    license="Apache 2.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.28.0",  
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "gnix=gnix.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Environment :: Console",
        "Topic :: System :: Shells",
        "Topic :: Utilities",
        "Intended Audience :: Developers",
    ],

    keywords=[
        "shell",
        "terminal",
        "ai",
        "cli",
        "natural language",
        "bash",
        "zsh",
        "ollama",
        "local ai",
        "command line",
    ],
)