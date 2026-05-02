import pytest
from gnix.executor import execute_command

class TestSuccessfulCommands:

    def test_echo(self):
        result = execute_command("echo hello", "bash")
        assert result == 0

    def test_pwd(self):
        result = execute_command("pwd", "bash")
        assert result == 0

    def test_ls(self):
        result = execute_command("ls", "bash")
        assert result == 0

    def test_true_command(self):
        result = execute_command("true", "bash")
        assert result == 0

    def test_mkdir_and_cleanup(self, tmp_path):
        result = execute_command(f"mkdir {tmp_path}/test-gnix-dir", "bash")
        assert result == 0

    def test_echo_zsh(self):
        result = execute_command("echo hello", "zsh")
        assert result == 0

    def test_piped_command(self):
        result = execute_command("echo hello | grep hello", "bash")
        assert result == 0

    def test_chained_commands(self):
        result = execute_command("echo hello && echo world", "bash")
        assert result == 0



class TestFailingCommands:

    def test_false_command(self):
        result = execute_command("false", "bash")
        assert result != 0

    def test_nonexistent_command(self):
        result = execute_command("thiscommanddoesnotexist", "bash")
        assert result != 0

    def test_grep_no_match(self):
        result = execute_command("echo hello | grep xyz", "bash")
        assert result != 0

    def test_ls_nonexistent_dir(self):
        result = execute_command("ls /nonexistent/path/xyz", "bash")
        assert result != 0



class TestShellSelection:

    def test_bash_shell(self):
        result = execute_command("echo $BASH_VERSION", "bash")
        assert result == 0

    def test_zsh_shell(self):
        result = execute_command("echo hello", "zsh")
        assert result == 0

    def test_unknown_shell_defaults_to_bash(self):
        result = execute_command("echo hello", "fish")
        assert result == 0



class TestEdgeCases:

    def test_empty_output_command(self):
        result = execute_command("true", "bash")
        assert result == 0

    def test_command_with_quotes(self):
        result = execute_command("echo 'hello world'", "bash")
        assert result == 0

    def test_command_with_env_variable(self):
        result = execute_command("echo $HOME", "bash")
        assert result == 0

    def test_multiline_output(self):
        result = execute_command("ls /usr/bin | head -5", "bash")
        assert result == 0