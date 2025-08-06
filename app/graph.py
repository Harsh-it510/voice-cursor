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
    
@tool
def git_init() -> str:
    """Initializes a new Git repository in the current directory."""
    try:
        output = subprocess.check_output("git init", shell=True, text=True)
        return output
    except subprocess.CalledProcessError as e:
        return f"Error: {e.output}"

@tool
def git_status() -> str:
    """Shows the current Git status."""
    try:
        output = subprocess.check_output("git status", shell=True, text=True)
        return output
    except subprocess.CalledProcessError as e:
        return f"Error: {e.output}"

@tool
def git_add_all() -> str:
    """Stages all files for commit."""
    try:
        output = subprocess.check_output("git add .", shell=True, text=True)
        return "All files added to staging area."
    except subprocess.CalledProcessError as e:
        return f"Error: {e.output}"

@tool
def git_commit(message: str) -> str:
    """Commits changes with a custom commit message."""
    try:
        output = subprocess.check_output(f"git commit -m \"{message}\"", shell=True, text=True)
        return output
    except subprocess.CalledProcessError as e:
        return f"Error: {e.output}"

@tool
def git_push(remote: str = "origin", branch: str = "main") -> str:
    """Pushes commits to the specified remote and branch."""
    try:
        output = subprocess.check_output(f"git push {remote} {branch}", shell=True, text=True)
        return output
    except subprocess.CalledProcessError as e:
        return f"Error: {e.output}"



llm = init_chat_model(
    model_provider="google_genai", model="gemini-2.5-flash"
)

llm_with_tool = llm.bind_tools(tools=[
    run_command,
    create_file,
    read_file,
    git_init,
    git_status,
    git_add_all,
    git_commit,
    git_push
])


def chatbot(state: State):
    
    system_prompt = SystemMessage(content="""
You are an AI coding assistant. Based on the user's voice commands, you can:
- Execute shell commands
- Create/read/edit code files
- Interact with Git to version control the project

Git commands you can perform include:
- git init
- git status
- git add .
- git commit -m "message"
- git push origin main

Always provide clear feedback to the user about what you did.
""")


    message = llm_with_tool.invoke([system_prompt] + state["messages"])
    # assert len(message.tool_calls) <= 1
    return {"messages": [message]}

tool_node = ToolNode(tools=[
    run_command,
    create_file,
    read_file,
    git_init,
    git_status,
    git_add_all,
    git_commit,
    git_push
])

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