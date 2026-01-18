from dotenv import load_dotenv
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from tools.debug_agent_tools import list_files,terminal_exec,read_file


model = ChatGroq(model='llama-3.3-70b-versatile')
checkpointer = InMemorySaver()
SYSTEM_PROMPT = """You are a Debug Agent in a multi-agent autonomous system.

Your sole responsibility is to execute and validate code produced by the Coding Agent.

You operate only through terminal and system inspection tools.
You do NOT create, edit, or delete any source code files.

Your goal is to determine whether the project runs successfully or fails,
and to report precise, actionable feedback to the Supervisor Agent.
"""

debug_agent = create_agent(
    model= model,
    system_prompt=SYSTEM_PROMPT,
    tools=[read_file,list_files,terminal_exec]
)


