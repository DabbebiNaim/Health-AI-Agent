import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition
from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages

# Import existing tools
from graph_tools import get_medical_context

# 1. Load api
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# 2. Define Tools 
from langchain_core.tools import tool

@tool
def consult_medical_database(symptom_description: str):
    """Query Neo4j for diseases, symptoms, and precautions."""
    return get_medical_context(symptom_description)

@tool
def calculate_bmi(weight_kg: float, height_m: float):
    """Calculate BMI given weight (kg) and height (m)."""
    bmi = weight_kg / (height_m ** 2)
    return f"The BMI is {bmi:.2f}"

tools = [consult_medical_database, calculate_bmi]

# 3. Initialize LLM
llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0)
llm_with_tools = llm.bind_tools(tools)

# 4. Define State
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

# --- NODE 1: THE MEDICAL INTERN (Generates Answer) ---
def intern_node(state: AgentState):
    """
    The Intern tries to answer the user's question using tools.
    """
    # Force a system persona
    sys_msg = SystemMessage(content="You are a Medical Intern. Retrieve data and answer the user. Be concise.")
    
    # Filter messages to ensure system message is first (if not already)
    history = state["messages"]
    if not isinstance(history[0], SystemMessage):
        history = [sys_msg] + history
        
    response = llm_with_tools.invoke(history)
    return {"messages": [response]}

# --- NODE 2: THE SUPERVISOR (Validates & Formats Answer) ---
def supervisor_node(state: AgentState):
    """
    The Supervisor checks the Intern's work and enforces strict formatting.
    """
    messages = state["messages"]
    last_message = messages[-1]
    
    if last_message.tool_calls:
        return {"messages": []} 

    # If it's a final text answer, review and format it.
    validation_prompt = [
        SystemMessage(content="""
        You are a Senior Medical Supervisor. 
        Your goal is to format the Intern's medical advice into a clean, readable structure.

        ### FORMATTING RULES (Follow Strictly):
        1. **Keywords:** Highlight the suspected **Disease Name** and critical **Symptoms** in **bold**.
        2. **Description:** Start with a clear paragraph explaining the condition.
        3. **Action Plan:** You MUST create a section titled "**What you can do:**". 
           - Under this title, provide a Numbered List (1., 2., 3.) of the precautions.
        4. **Disclaimer:** You MUST end the message with: 
           "⚠️ **Disclaimer:** I am an AI. Please consult a doctor."

        If the Intern's draft is messy, rewrite it completely to match this format.
        """),
        HumanMessage(content=f"Intern's Draft: {last_message.content}")
    ]
    
    response = llm.invoke(validation_prompt)
    
    return {"messages": [AIMessage(content=response.content)]}
# 5. Build Graph
workflow = StateGraph(AgentState)

# Add Nodes
workflow.add_node("medical_intern", intern_node)
workflow.add_node("tools", ToolNode(tools))
workflow.add_node("supervisor", supervisor_node)
workflow.set_entry_point("medical_intern")
workflow.add_conditional_edges(
    "medical_intern",
    tools_condition,
    {
        "tools": "tools",
        "__end__": "supervisor"  # If done, go to supervisor instead of END
    }
)

workflow.add_edge("tools", "medical_intern")

# Supervisor -> End
workflow.add_edge("supervisor", END)

app = workflow.compile()

# --- Test Block ---
if __name__ == "__main__":
    print("👨‍⚕️ Multi-Agent System Ready (Intern + Supervisor)")
    user_input = "What are the symptoms of Typhoid?"
    print(f"User: {user_input}")
    
    events = app.stream({"messages": [HumanMessage(content=user_input)]}, stream_mode="values")
    for event in events:
        msg = event["messages"][-1]
        if msg.type == "ai":
            print(f"🤖 Output: {msg.content[:100]}...") 