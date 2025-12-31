import subprocess
import sys
import os
import traceback


def run_python(entry: str, cwd: str, timeout: int):
    """
    Runs a Python file in an isolated directory.

    Returns:
        stdout (str)
        stderr (str)
        exit_code (int)
    """
    try:
        result = subprocess.run(
            [sys.executable, entry],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout
        )

        return (
            result.stdout,
            result.stderr,
            result.returncode
        )

    except subprocess.TimeoutExpired:
        return (
            "",
            "Error: Execution timed out",
            -1
        )

    except Exception:
        return (
            "",
            traceback.format_exc(),
            -1
        )
