DANGEROUS_PATTERNS = [
      # --- Recursive deletion ---
    (
        "rm -rf /",
        "This command will recursively delete everything from root. This will destroy your entire system."
    ),
    (
        "rm -rf ~",
        "This command will recursively delete your entire home directory and cannot be undone."
    ),
    (
        "rm -rf *",
        "This command will recursively delete everything in the current directory and cannot be undone."
    ),
    (
        "rm -rf .",
        "This command will recursively delete the current directory and cannot be undone."
    ),
    (
        "rm -fr /",
        "This command will recursively delete everything from root. This will destroy your entire system."
    ),
    (
        "rm -fr ~",
        "This command will recursively delete your entire home directory and cannot be undone."
    ),

    # --- Disk wiping ---
    (
        "dd if=",
        "This command writes directly to a disk device and can permanently destroy all data on it."
    ),
    (
        "> /dev/sd",
        "This command writes directly to a disk device and can permanently destroy all data on it."
    ),
    (
        "> /dev/hd",
        "This command writes directly to a disk device and can permanently destroy all data on it."
    ),
    (
        "> /dev/nvme",
        "This command writes directly to a disk device and can permanently destroy all data on it."
    ),

    # --- Filesystem formatting ---
    (
        "mkfs",
        "This command formats a disk partition and will erase all data on it permanently."
    ),
    (
        "mke2fs",
        "This command formats a disk partition and will erase all data on it permanently."
    ),
    (
        "mkswap",
        "This command overwrites a partition with swap space and will erase all existing data."
    ),

    # --- Dangerous permission changes ---
    (
        "chmod -R 777 /",
        "This command makes every file on your system world writable which is a severe security risk."
    ),
    (
        "chmod 777 /",
        "This command makes the root directory world writable which is a severe security risk."
    ),
    (
        "chown -R root /",
        "This command changes ownership of every file on your system and can break critical services."
    ),

    # --- Fork bomb ---
    (
        ":(){ :|:& };:",
        "This is a fork bomb. It will consume all system resources and crash your machine immediately."
    ),
    (
        ":(){ :|: & };:",
        "This is a fork bomb. It will consume all system resources and crash your machine immediately."
    ),

    # --- Overwriting critical system files ---
    (
        "> /etc/passwd",
        "This command will overwrite your system password file and lock all users out of the system."
    ),
    (
        "> /etc/shadow",
        "This command will overwrite your system shadow password file and is a severe security risk."
    ),
    (
        "> /etc/hosts",
        "This command will overwrite your hosts file and can break all network name resolution."
    ),

    # --- Moving everything to /dev/null ---
    (
        "mv / /dev/null",
        "This command attempts to move your entire filesystem to /dev/null which will destroy your system."
    ),

    # --- Shutdown and reboot without warning ---
    (
        "shutdown",
        "This command will shut down the system."
    ),
    (
        "reboot",
        "This command will reboot the system immediately."
    ),
    (
        "halt",
        "This command will halt the system immediately."
    ),

    # --- Dangerous curl/wget piped to shell ---
    (
        "| bash",
        "This command downloads and executes a remote script which is a severe security risk."
    ),
    (
        "| sh",
        "This command downloads and executes a remote script which is a severe security risk."
    ),
]


def check_safety(command: str) -> tuple[bool, str]:
    normalized = command.lower().strip()

    for pattern, warning in DANGEROUS_PATTERNS:
        if pattern.lower() in normalized:
            return False, warning

    return True, ""


def get_severity(command: str) -> str:
    normalized = command.lower().strip()

    CRITICAL_PATTERNS = [
        "rm -rf /", "rm -rf ~", "rm -fr /",
        "dd if=", "> /dev/sd", "mkfs",
        ":(){ :|:& };:", "> /etc/passwd"
    ]

    HIGH_PATTERNS = [
        "rm -rf *", "rm -rf .",
        "chmod -R 777", "chmod 777 /",
        "| bash", "| sh",
        "mv / /dev/null"
    ]

    MEDIUM_PATTERNS = [
        "shutdown", "reboot", "halt"
    ]

    for pattern in CRITICAL_PATTERNS:
        if pattern.lower() in normalized:
            return "critical"

    for pattern in HIGH_PATTERNS:
        if pattern.lower() in normalized:
            return "high"

    for pattern in MEDIUM_PATTERNS:
        if pattern.lower() in normalized:
            return "medium"

    return "safe"