import argparse
import os
import sys

from gnix.config import (
    is_first_run,
    run_first_time_setup,
    get_model,
    run_model_selection,
    save_config,
    load_config,
    check_ollama_running,
)

from gnix.display import (
    show_welcome,
    show_session_info,
    show_command,
    show_explanation,
    show_warning,
    show_error,
    show_cancelled,
    show_dry_run,
    show_success,
    show_ollama_not_running,
    show_model_updated,
    show_generating,
    prompt_confirm,
    prompt_dangerous_confirm,
    Spinner,
    divider,
    bold_cyan,
    dim,
    bold,
)


def detect_shell():
    shell_path = os.environ.get("SHELL", "/bin/bash")

    if "zsh" in shell_path:
        return "zsh"
    elif "bash" in shell_path:
        return "bash"
    else:
        return "bash"




def validate_query(query: str) -> tuple[bool, str]:
    query = query.strip()

    if not query:
        return False, "Query cannot be empty."

    if len(query.split()) == 1:
        return False, (
            f"'{query}' looks like a single word, not a natural language query.\n"
            f"  {dim('try:')} {bold('gnix \"show all running processes\"')}"
        )

    if len(query) < 3:
        return False, "Query is too short. Please describe what you want to do."

    SHELL_COMMANDS = [
        "ls", "cd", "rm", "mv", "cp", "mkdir", "touch",
        "grep", "find", "cat", "echo", "sudo", "chmod",
        "chown", "ps", "kill", "top", "df", "du", "tar",
        "curl", "wget", "git", "pip", "python", "bash", "zsh"
    ]
    first_word = query.split()[0].lower()
    if first_word in SHELL_COMMANDS:
        return False, (
            f"'{query}' looks like a shell command already.\n"
            f"  {dim('to explain it use:')} {bold('gnix --explain \"' + query + '\"')}"
        )

    return True, ""


def create_parser():
    parser = argparse.ArgumentParser(
        prog="gnix",
        add_help=False,
        epilog="""
            Examples:
                gnix "find all files larger than 1GB"
                gnix --explain "tar -czf archive.tar.gz /home/user"
                gnix --dry-run "delete all log files older than 30 days"
                gnix --set-model
            """
    )

    parser.add_argument(
        "query",
        type=str,
        nargs="?",
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

    parser.add_argument(
        "--set-model",
        action="store_true",
        help="Select a different model to use with Gnix"
    )

    parser.add_argument(
    "-h", "--help",
    action="store_true",
    help="Show this help message and exit"
)

    return parser


def main():

    parser = create_parser()

    if len(sys.argv) == 1:
        show_welcome()
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()
    if args.help:
        show_welcome()
        parser.print_help()
        sys.exit(0)


    if is_first_run():
        run_first_time_setup()

    if not check_ollama_running():
        show_ollama_not_running()
        sys.exit(1)

    if args.set_model:
        print(f"\n  {bold_cyan('◆')}  {bold('Select a model')}\n")
        selected = run_model_selection()
        config = load_config()
        config["model"] = selected
        save_config(config)
        show_model_updated(selected)
        return

    if not args.query:
        show_error("Please provide a query.\n  Example: gnix \"list all files\"")
        parser.print_help()
        sys.exit(1)

    shell = detect_shell()
    model = get_model()

    if not model:
        show_error("No model configured. Run: gnix --set-model")
        sys.exit(1)

    from gnix.model import generate_command
    from gnix.safety import check_safety, get_severity
    from gnix.executor import execute_command
    from gnix.explain import explain_command

    if args.explain:
        print(f"\n  {bold_cyan('◆')}  {bold('Explain')}\n")
        show_generating(args.query)

        spinner = Spinner("reading")
        spinner.start()
        explanation = explain_command(args.query, shell, detailed=True)
        spinner.stop()

        print()
        show_explanation(explanation)
        return

    is_valid, error_msg = validate_query(args.query)
    if not is_valid:
        show_error(error_msg)
        sys.exit(1)

    show_session_info(shell, model)
    show_generating(args.query)
    print()

    spinner = Spinner("thinking")
    spinner.start()
    command = generate_command(args.query, shell, model)
    spinner.stop()

    if not command:
        show_error("Could not generate a command. Try rephrasing your request.")
        sys.exit(1)

    is_safe, warning = check_safety(command)
    severity = get_severity(command)

    show_command(command)

    spinner = Spinner("explaining")
    spinner.start()
    explanation = explain_command(command, shell, detailed=False)
    spinner.stop()

    show_explanation(explanation)

    if args.dry_run:
        show_dry_run()
        return

    if not is_safe:
        show_warning(warning)
        confirm = prompt_dangerous_confirm()
        if confirm != "yes":
            show_cancelled()
            return

    else:
        confirm = prompt_confirm()
        if confirm != "y":
            show_cancelled()
            return

    print()
    result = execute_command(command, shell)
    print()

    if result == 0:
        show_success("done")
    else:
        show_error(f"Command exited with code {result}")


if __name__ == "__main__":
    main()