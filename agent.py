import os
from dotenv import load_dotenv

# --- LangChain & LangGraph Imports ---
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition

# --- Import our Graph Search Logic ---
# (We assume you have the graph_tools.py file from the previous step)
from graph_tools import get_medical_context

# 1. Load Secrets
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("❌ Error: GROQ_API_KEY is missing from .env file!")

# 2. Define the Tools 🛠️

@tool
def consult_medical_database(symptom_description: str):
    """
    Use this tool when the user describes symptoms (pain, fever, etc.) 
    or asks about specific diseases. 
    Input should be a natural language description of the symptoms.
    """
    print(f"   🕵️‍♂️ Agent is querying Neo4j for: '{symptom_description}'")
    return get_medical_context(symptom_description)

@tool
def calculate_bmi(weight_kg: float, height_m: float):
    """
    Use this tool to calculate Body Mass Index (BMI).
    Input: weight in kilograms (kg) and height in meters (m).
    """
    print(f"   🧮 Agent is calculating BMI...")
    bmi = weight_kg / (height_m ** 2)
    return f"The BMI is {bmi:.2f}"

tools = [consult_medical_database, calculate_bmi]

# 3. Initialize the Brain (LLM) 🧠
# We use Llama3-70b because it is smart enough to handle tools.
llm = ChatGroq(
    temperature=0, 
    model_name="llama-3.3-70b-versatile",
    groq_api_key=GROQ_API_KEY
)

# This tells the LLM: "Here are the tools you can use if you need them."
llm_with_tools = llm.bind_tools(tools)

# 4. Define the State 📝
# The 'State' is the memory of the conversation. 
# It keeps track of messages between the User and the AI.
from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

# 5. Define the Nodes (The Steps) 📍

def agent_node(state: AgentState):
    """
    The Thinking Node. The LLM looks at the history and decides what to do.
    """
    messages = state["messages"]
    # We invoke the LLM with the current conversation history
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

# 6. Build the Graph (The Workflow) 🕸️
workflow = StateGraph(AgentState)

# Add the nodes
workflow.add_node("agent", agent_node)
workflow.add_node("tools", ToolNode(tools))

# Set the entry point (Start here)
workflow.set_entry_point("agent")

# Add the edges (The Logic Flow)
# After the 'agent' thinks, we check:
# - Did it ask to call a tool? -> Go to 'tools' node.
# - Did it just answer? -> END.
workflow.add_conditional_edges(
    "agent",
    tools_condition,
)

# After the 'tools' run, go back to 'agent' so it can read the result and answer.
workflow.add_edge("tools", "agent")

# Compile the graph into a runnable application
app = workflow.compile()

# --- 7. Test it! (Main Loop) ---
if __name__ == "__main__":
    print("🤖 Tanit Health Agent is Ready! (Type 'quit' to exit)")
    print("-----------------------------------------------------")
    
    while True:
        user_input = input("\n👤 User: ")
        if user_input.lower() in ["quit", "exit"]:
            break
            
        # Run the agent
        events = app.stream(
            {"messages": [HumanMessage(content=user_input)]},
            stream_mode="values"
        )
        
        # Print the final response
        for event in events:
            # We get a list of messages. The last one is the latest update.
            message = event["messages"][-1]
            # Only print the AI's final answer, not the tool calls
            if message.type == "ai" and not message.tool_calls:
                print(f"🤖 AI: {message.content}")