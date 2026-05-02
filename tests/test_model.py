import pytest
from gnix.model import clean_command


class TestCleanCommand:

    def test_removes_backticks(self):
        assert clean_command("`ls -la`") == "ls -la"

    def test_removes_markdown_bash_block(self):
        assert clean_command("```bash\nls -la\n```") == "ls -la"

    def test_removes_markdown_sh_block(self):
        assert clean_command("```sh\nls -la```") == "ls -la"

    def test_removes_markdown_zsh_block(self):
        assert clean_command("```zsh\nls -la```") == "ls -la"

    def test_removes_markdown_generic_block(self):
        assert clean_command("```\nls -la\n```") == "ls -la"

    def test_removes_dollar_prefix(self):
        assert clean_command("$ ls -la") == "ls -la"

    def test_takes_first_line_only(self):
        result = clean_command("ls -la\necho hello\npwd")
        assert result == "ls -la"

    def test_strips_whitespace(self):
        assert clean_command("   ls -la   ") == "ls -la"

    def test_normal_command_unchanged(self):
        assert clean_command("find . -name '*.py' -mtime -7") == "find . -name '*.py' -mtime -7"

    def test_complex_command_unchanged(self):
        cmd = "ps aux --sort=-%mem | head -10"
        assert clean_command(cmd) == cmd

    def test_empty_string(self):
        assert clean_command("") == ""

    def test_only_backticks(self):
        assert clean_command("```") == ""

    def test_git_command(self):
        assert clean_command("git log --oneline -10") == "git log --oneline -10"

    def test_removes_dollar_without_space(self):
        result = clean_command("$ls -la")
        # Should not remove $ if it's not followed by space
        assert result == "$ls -la"