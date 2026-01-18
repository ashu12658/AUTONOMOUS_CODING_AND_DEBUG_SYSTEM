from langchain.tools import tool
from pathlib import Path
import os

# -----------------------------
# Workspace root
# -----------------------------
WORKSPACE_ROOT = Path(r"C:\Users\ashis\Desktop\autonomous_coding\workspace").resolve()

# -----------------------------
# Internal helper (not a tool)
# -----------------------------
def _validate_path(path: Path):
    path = path.resolve()
    if not str(path).startswith(str(WORKSPACE_ROOT)):
        raise PermissionError(f"Access outside workspace denied: {path}")

# -----------------------------
# Tools exposed to the agent
# -----------------------------
@tool
def create_dir(relative_path: str) -> str:
    """
    Create a directory inside the workspace.

    relative_path: path relative to WORKSPACE_ROOT
    """
    full_path = WORKSPACE_ROOT / relative_path
    _validate_path(full_path)
    os.makedirs(full_path, exist_ok=True)
    return f"Directory created: {full_path}"

@tool
def write_file(relative_path: str, content: str) -> str:
    """
    Write a file inside the workspace.

    relative_path: path relative to WORKSPACE_ROOT
    content: string content to write
    """
    full_path = WORKSPACE_ROOT / relative_path
    _validate_path(full_path)
    os.makedirs(full_path.parent, exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    return f"File written: {full_path}"
