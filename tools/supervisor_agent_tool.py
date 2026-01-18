from langchain.tools import tool, ToolRuntime
from langchain_core.messages import BaseMessage
from Agents.coding_agent import coding_agent
from Agents.debug_agent import debug_agent
from Agents.documentation_agent import documentation_agent

def _get_user_message(runtime: ToolRuntime) -> str:
    """Extract the original user message from parent graph state."""
    messages = runtime.state.get("messages", [])
    msg = next(
        (m for m in messages if m.__class__.__name__ == "HumanMessage"),
        None
    )
    return msg.content if msg else ""


@tool
def call_coding_agent(content: str, runtime: ToolRuntime) -> str:
    """Delegate coding tasks to Coding Agent."""
    user_text = _get_user_message(runtime)

    # Invoke subagent with isolated state
    result = coding_agent.invoke({
        "messages": [{
            "role": "user",
            "content": f"User request: {user_text}\nTask: {content}"
        }]
    })

    out = result["messages"][-1]
    return out.content if isinstance(out, BaseMessage) else str(out)


@tool
def call_debug_agent(content: str, runtime: ToolRuntime) -> str:
    """Delegate debugging tasks to Debug Agent."""
    user_text = _get_user_message(runtime)

    result = debug_agent.invoke({
        "messages": [{
            "role": "user",
            "content": f"User request: {user_text}\nIssue: {content}"
        }]
    })

    out = result["messages"][-1]
    return out.content if isinstance(out, BaseMessage) else str(out)


@tool
def call_docs_agent(content: str, runtime: ToolRuntime) -> str:
    """Delegate documentation tasks to Documentation Agent."""
    result = documentation_agent.invoke({
        "messages": [{
            "role": "user",
            "content": content
        }]
    })

    out = result["messages"][-1]
    return out.content if isinstance(out, BaseMessage) else str(out)