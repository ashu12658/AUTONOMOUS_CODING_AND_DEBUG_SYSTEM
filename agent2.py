from dotenv import load_dotenv
load_dotenv()
import subprocess
import os
import webbrowser
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import InMemorySaver

checkpoint = InMemorySaver()

model = ChatGroq(model='openai/gpt-oss-120b')


@tool()
def execute_command(command: str) -> str:
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


@tool
def google_search(query: str) -> str:
    """Search Google for information.

    Args:
        query: The search query (e.g., 'best Python frameworks', 'weather in NYC')
    """
    try:
        # URL encode the query
        encoded_query = query.replace(" ", "+")
        google_url = f"https://www.google.com/search?q={encoded_query}"

        # Open search in browser
        webbrowser.open(google_url)
        return f"✓ Opened Google search for '{query}' in your browser. Search results are loading..."
    except Exception as e:
        return f"Error opening Google search: {str(e)}"


@tool
def play_youtube_song(song_name: str) -> str:
    """Search and play a song on YouTube.

    Args:
        song_name: The name of the song, artist, or music to play (e.g., 'Bohemian Rhapsody Queen')
    """
    try:
        # URL encode the song name
        encoded_query = song_name.replace(" ", "+")
        youtube_url = f"https://www.youtube.com/results?search_query={encoded_query}"

        # Open YouTube search in browser
        webbrowser.open(youtube_url)
        return f"♪ Opened YouTube search for '{song_name}'. The first video should be the song you're looking for!"
    except Exception as e:
        return f"Error opening YouTube: {str(e)}"


@tool
def youtube_direct_play(video_url: str) -> str:
    """Play a YouTube video directly from a URL.

    Args:
        video_url: The YouTube video URL (e.g., 'https://www.youtube.com/watch?v=...')
    """
    try:
        webbrowser.open(video_url)
        return f"♪ Playing YouTube video: {video_url}"
    except Exception as e:
        return f"Error playing video: {str(e)}"


# All tools for the agent
tools = [
    execute_command,
    read_file,
    write_file,
    list_directory,
    google_search,
    play_youtube_song,
    youtube_direct_play
]

agent = create_agent(
    model=model,
    checkpointer=checkpoint,
    tools=tools,
    system_prompt="""You are a helpful assistant with terminal control, web search, and music playback capabilities.

    Available capabilities:
    - Execute shell commands (ls, mkdir, git, etc.)
    - Read and write files
    - List directory contents
    - Search Google for information
    - Search and play songs on YouTube

    When the user asks to:
    - Search for something: use google_search
    - Play music/songs: use play_youtube_song
    - Execute commands: use execute_command
    - Manage files: use read_file, write_file, list_directory

    Always confirm what you're about to do before executing commands. Be helpful and friendly!"""
)

# Use the agent
if __name__ == "__main__":
    # Example 1: List current directory
    # Example 4: Search Google
    print("\n" + "=" * 60)
    print("Example 4: Google Search")
    print("=" * 60)
    result = agent.invoke({
        "messages": [{"role": "user", "content": "write in hello.txt the content is agentic ai is best"}]
    },config={"configurable": {"thread_id": "thread_01"}})
    print("Agent Response:", result["messages"][-1].content)

    # Example 5: Play a song on YouTube
    print("\n" + "=" * 60)
    print("Example 5: Play YouTube Song")
    print("=" * 60)
    result = agent.invoke({
        "messages": [{"role": "user", "content": "Play 'sultan song' on YouTube"}]
    },config={"configurable": {"thread_id": "thread_01"}})
    print("Agent Response:", result["messages"][-1].content)

    # # Example 6: Interactive mode
    # print("\n" + "=" * 60)
    # print("Interactive Mode (Type 'exit' to quit)")
    # print("=" * 60)
    # while True:
    #     user_input = input("\nYou: ").strip()
    #     if user_input.lower() in ['exit', 'quit']:
    #         print("Goodbye!")
    #         break
    #
    #     # Stream response
    #     result = agent.invoke({
    #         "messages": [{"role": "user", "content": user_input},config={"configurable": {"thread_id": "thread_01"}}]
    #     })
    #     print(f"Agent: {result['messages'][-1].content}")