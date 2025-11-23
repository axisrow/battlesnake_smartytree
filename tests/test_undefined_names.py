import subprocess
import sys
from pathlib import Path

PROJECT_PATHS = [Path("server.py"), Path("snake"), Path("tests")]


def test_no_undefined_names():
    cmd = [sys.executable, "-m", "pyflakes", *map(str, PROJECT_PATHS)]
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)

    output = (result.stdout or "") + (result.stderr or "")
    undefined = [
        line for line in output.splitlines()
        if "undefined name" in line.lower() or "undefined variable" in line.lower()
    ]

    assert not undefined, f"Undefined names detected:\n" + "\n".join(undefined)
