from dotenv import load_dotenv
load_dotenv()
import subprocess
import os
from langchain.tools import tool
from langchain.agents import create_agent
from  langchain_groq import ChatGroq

model = ChatGroq(model='openai/gpt-oss-120b')

@tool()
def execute_command(command:str)->str:
    """
    Execute a shell command and return its output
    Args:
        command: The shell command to execute (e.g., 'ls -la', 'pwd', 'mkdir test')
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        return f"Output:\n{result.stdout}\nErrors:\n{result.stderr}" if result.stderr else result.stdout
    except subprocess.TimeoutExpired:
        return "Command timed out after 30 seconds"
    except Exception as e:
        return f"Error executing command: {str(e)}"


@tool
def read_file(filepath: str) -> str:
    """Read and return the contents of a file.

    Args:
        filepath: Path to the file to read
    """
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"


@tool
def write_file(filepath: str, content: str) -> str:
    """Write content to a file.

    Args:
        filepath: Path to the file to write
        content: Content to write to the file
    """
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            f.write(content)
        return f"Successfully wrote to {filepath}"
    except Exception as e:
        return f"Error writing file: {str(e)}"


@tool
def list_directory(path: str = ".") -> str:
    """List files and directories in a given path.

    Args:
        path: Directory path to list (default: current directory)
    """
    try:
        items = os.listdir(path)
        return "\n".join(items)
    except Exception as e:
        return f"Error listing directory: {str(e)}"

tools = [execute_command, read_file, write_file, list_directory]

agent = create_agent(
    model=model,  # Replace with your LLM
    tools=tools,
    system_prompt="You are a terminal control agent. Execute commands carefully and provide clear output. Always confirm what you're about to do before executing dangerous commands like rm or chmod."
)

# Use the agent
if __name__ == "__main__":
    # Example 1: List current directory
    result = agent.invoke({
        "messages": [{"role": "user", "content": "List all files in the current directory"}]
    })
    print("Agent Response:", result["messages"][-1].content)

    # Example 2: Create a file
    result = agent.invoke({
        "messages": [{"role": "user", "content": "Create a file called hello.txt with 'I Am Ashish' inside"}]
    })
    print("Agent Response:", result["messages"][-1].content)

    # Example 3: Read the file
    result = agent.invoke({
        "messages": [{"role": "user", "content": "Read the contents of hello.txt"}]
    })
    print("Agent Response:", result["messages"][-1].content)
