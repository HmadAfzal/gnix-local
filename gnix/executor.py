import subprocess
import sys


def execute_command(command: str, shell: str) -> int:
    shell_binary = {
        "bash": "/bin/bash",
        "zsh":  "/bin/zsh",
    }.get(shell, "/bin/bash")

    try:
        process = subprocess.Popen(
            [shell_binary, "-c", command],  # run command in user's shell
            stdout=subprocess.PIPE,          # capture stdout
            stderr=subprocess.PIPE,          # capture stderr
            text=True,                       # decode output as text
            bufsize=1,                       # line buffered for real time output
        )
        for line in process.stdout:
            sys.stdout.write(line)
            sys.stdout.flush()

        process.wait()

        if process.returncode != 0:
            stderr_output = process.stderr.read()
            if stderr_output:
                print(f"\n Error output:")
                print(stderr_output.strip())
            print(f"\n Command exited with code {process.returncode}")

        return process.returncode

    except FileNotFoundError:
        # Shell binary not found
        print(f" Error: Shell '{shell_binary}' not found on your system.")
        return 1

    except PermissionError:
        print(f" Error: Permission denied. Try running with sudo if needed.")
        return 1

    except KeyboardInterrupt:
        print("\n Command interrupted by user.")
        process.kill()
        return 1

    except Exception as e:
        print(f" Unexpected error while running command: {e}")
        return 1