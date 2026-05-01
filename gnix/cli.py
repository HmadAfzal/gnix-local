import argparse
import os
import sys
import requests

def check_ollama():
    try:
        response = requests.get("http://localhost:11434", timeout=3)
        return True
    except requests.exceptions.ConnectionError:
        return False


def detect_shell():
    shell_path = os.environ.get("SHELL", "/bin/bash")
    if "zsh" in shell_path:
        return "zsh"
    elif "bash" in shell_path:
        return "bash"
    else:
        return "bash"



def create_parser():
    parser = argparse.ArgumentParser(
        prog="gnix",
        description="Gnix — Natural language to shell commands. Local. Private. Free.",
        epilog="""
Examples:
  gnix "find all files larger than 1GB"
  gnix --explain "tar -czf archive.tar.gz /home/user"
  gnix --dry-run "delete all log files older than 30 days"
        """
    )

    parser.add_argument(
        "query",
        type=str,
        help="Natural language description of what you want to do"
    )

    parser.add_argument(
        "--explain",
        action="store_true",
        help="Explain what a shell command does instead of generating one"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Generate the command but do not execute it"
    )

    return parser


def main():
    parser = create_parser()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()

    if not check_ollama():
        print("\n Ollama is not running.")
        print(" Start it with:  ollama serve")
        print(" Then try again.\n")
        sys.exit(1)

    shell = detect_shell()


    # Import here to avoid circular imports
    from gnix.model import generate_command
    from gnix.safety import check_safety
    from gnix.executor import execute_command
    from gnix.explain import explain_command

    if args.explain:
        print(f"\n Explaining: {args.query}\n")
        explanation = explain_command(args.query, shell)
        print(f" {explanation}\n")
        return


    print(f"\n Detected shell: {shell}")
    print(f" Generating command for: {args.query}\n")

    command = generate_command(args.query, shell)

    if not command:
        print(" Could not generate a command. Try rephrasing your request.\n")
        sys.exit(1)

    is_safe, warning = check_safety(command)

    print(f" Command: {command}\n")

    explanation = explain_command(command, shell)
    print(f" {explanation}\n")

    if args.dry_run:
        print(" Dry run mode — command was not executed.\n")
        return

    if not is_safe:
        print(f" WARNING: {warning}")
        confirm = input(" This action may be destructive. Type 'yes' to confirm: ")
        if confirm.strip().lower() != "yes":
            print(" Cancelled.\n")
            return

    else:
        confirm = input(" Run this command? [y/n]: ")
        if confirm.strip().lower() != "y":
            print(" Cancelled.\n")
            return

    print()
    execute_command(command, shell)
    print()


if __name__ == "__main__":
    main()