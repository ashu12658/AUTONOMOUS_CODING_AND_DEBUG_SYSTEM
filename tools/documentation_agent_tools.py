from langchain.tools import tool
from pathlib import Path
import os

# -----------------------------
# Workspace root
# -----------------------------
WORKSPACE_ROOT = Path(r"C:\Users\ashis\Desktop\autonomous_coding\workspace").resolve()

def _validate_path(path: Path):
    path = path.resolve()
    if not str(path).startswith(str(WORKSPACE_ROOT)):
        raise PermissionError("Access outside workspace denied")

# -----------------------------
# TOOL: Read file (read-only)
# -----------------------------
@tool
def read_file(relative_path: str) -> str:
    """
    Read a file inside the workspace (read-only).
    """
    file_path = WORKSPACE_ROOT / relative_path
    _validate_path(file_path)

    if not file_path.exists():
        return f"File not found: {file_path}"

    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

# -----------------------------
# TOOL: List files
# -----------------------------
@tool
def list_files(relative_path: str = ".") -> str:
    """
    List files and directories inside workspace.
    """
    target = WORKSPACE_ROOT / relative_path
    _validate_path(target)

    if not target.exists():
        return f"Path does not exist: {target}"

    return "\n".join([p.name for p in target.iterdir()])

# -----------------------------
# TOOL: Write documentation file
# -----------------------------
@tool
def write_doc(relative_path: str, content: str) -> str:
    """
    Write documentation file (README.md, docs/*.md) inside workspace.
    """
    file_path = WORKSPACE_ROOT / relative_path
    _validate_path(file_path)

    os.makedirs(file_path.parent, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    return f"Documentation written: {file_path}"
