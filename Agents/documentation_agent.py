from dotenv import load_dotenv
load_dotenv()
from langgraph.checkpoint.memory import InMemorySaver
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from tools.documentation_agent_tools import  read_file,write_doc,list_files

model = ChatGroq(model='llama-3.1-8b-instant')
checkpointer = InMemorySaver()

SYSTEM_PROMPT="""You are a Documentation Agent in a multi-agent autonomous system.

Your sole responsibility is to generate clear, accurate, and concise documentation
for projects created by other agents.

You do NOT write application source code.
You only create or update documentation files such as README.md and related docs
inside the workspace directory.
"""

documentation_agent = create_agent(
    model=model,
    tools=[read_file, write_doc, list_files],
    system_prompt=SYSTEM_PROMPT,
)


