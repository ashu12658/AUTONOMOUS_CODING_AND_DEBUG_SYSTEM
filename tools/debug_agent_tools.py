from langchain.tools import tool
from pathlib import Path
import subprocess

# -----------------------------
# Workspace root (STRICT)
# -----------------------------
WORKSPACE_ROOT = Path(r"C:\Users\ashis\Desktop\autonomous_coding\workspace").resolve()

def _validate_path(path: Path):
    path = path.resolve()
    if not str(path).startswith(str(WORKSPACE_ROOT)):
        raise PermissionError("Access outside workspace denied")

# -----------------------------
# TOOL: List files (read-only)
# -----------------------------
@tool
def list_files(relative_path: str = ".") -> str:
    """
    List files and folders inside workspace (read-only).
    """
    target = WORKSPACE_ROOT / relative_path
    _validate_path(target)

    if not target.exists():
        return f"Path does not exist: {target}"

    if target.is_file():
        return f"File: {target.name}"

    items = []
    for p in target.iterdir():
        items.append(p.name)
    return "\n".join(items)

# -----------------------------
# TOOL: Read file (read-only)
# -----------------------------
@tool
def read_file(relative_path: str) -> str:
    """
    Read a file inside workspace (read-only).
    """
    file_path = WORKSPACE_ROOT / relative_path
    _validate_path(file_path)

    if not file_path.exists():
        return f"File not found: {file_path}"

    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

# -----------------------------
# TOOL: Execute terminal command
# -----------------------------
@tool
def terminal_exec(command: str) -> str:
    """
    Execute a terminal command inside workspace only.
    """
    result = subprocess.run(
        command,
        cwd=str(WORKSPACE_ROOT),
        shell=True,
        capture_output=True,
        text=True
    )

    output = ""
    if result.stdout:
        output += f"STDOUT:\n{result.stdout}\n"
    if result.stderr:
        output += f"STDERR:\n{result.stderr}\n"

    return output or "Command executed with no output"
