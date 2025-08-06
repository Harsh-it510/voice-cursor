import os
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import StateGraph, START, END
from langchain_core.tools import tool
from langchain.schema import SystemMessage
from langfuse import observe
import subprocess
from dotenv import load_dotenv

load_dotenv()


class State(TypedDict):
    messages: Annotated[list, add_messages]

@tool
def run_command(cmd: str) -> str:
    """Executes a shell command and returns the output."""
    try:
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, text=True)
        return output
    except subprocess.CalledProcessError as e:
        return f"Error: {e.output}"
    
@tool
def create_file(filename: str, content: str) -> str:
    """
    Creates a file inside 'chat_gpt/' and writes content into it.
    Example: create_file(filename="binarysearch.cpp", content="...C++ code...")
    """
    os.makedirs("chat_gpt", exist_ok=True)
    filepath = os.path.join("chat_gpt", filename)
    with open(filepath, "w") as f:
        f.write(content)
    return f"File '{filename}' created in chat_gpt/."


@tool
def read_file(filename: str) -> str:
    """
    Reads the content of a file from 'chat_gpt/' directory.
    """
    filepath = os.path.join("chat_gpt", filename)
    if not os.path.exists(filepath):
        return f"File '{filename}' does not exist."
    with open(filepath, "r") as f:
        return f.read()
    



llm = init_chat_model(
    model_provider="google_genai", model="gemini-2.5-flash"
)
llm_with_tool = llm.bind_tools(tools=[run_command, create_file, read_file])


def chatbot(state: State):
    system_prompt = SystemMessage(content="""
You are an AI coding assistant. Based on the user's voice commands, you can:
- Execute terminal commands
- Create or read files in the 'chat_gpt/' directory
- Generate or modify code like C++, Python, etc.

When generating files, always save them in 'chat_gpt/'.
Use the appropriate tool to do the job — run_command, create_file, or read_file.
""")


    message = llm_with_tool.invoke([system_prompt] + state["messages"])
    # assert len(message.tool_calls) <= 1
    return {"messages": [message]}

tool_node = ToolNode(tools=[run_command, create_file, read_file])

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", tool_node)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge("chatbot", END)

graph = graph_builder.compile()

def create_chat_graph(checkpointer):
    return graph_builder.compile(checkpointer=checkpointer)