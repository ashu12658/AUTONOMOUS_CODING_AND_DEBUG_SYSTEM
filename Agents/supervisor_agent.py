from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain.agents import create_agent
from tools.supervisor_agent_tool import (
    call_coding_agent,
    call_debug_agent,
    call_docs_agent
)

model = ChatGroq(
    model='llama-3.3-70b-versatile'
)

SYSTEM_PROMPT = """You are a supervisor agent.
You understand the user requirement, make a plan,
and delegate work to sub-agents using tools.
"""

supervisor_agent = create_agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
    tools=[call_debug_agent, call_docs_agent, call_coding_agent],
)

result = supervisor_agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "make a simple calculator application with document readme"
            }
        ]
    }
)

print(result)
