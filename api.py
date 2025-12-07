from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from multi_agent import app as agent_app

app = FastAPI(title="Tanit Health AI", version="2.0")

class ChatRequest(BaseModel):
    query: str

@app.get("/")
def home():
    return {"status": "online", "system": "Multi-Agent"}

@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    try:
        user_query = request.query
        
        # Run the Multi-Agent System
        inputs = {"messages": [HumanMessage(content=user_query)]}
        result = agent_app.invoke(inputs)
        
        all_messages = result["messages"]
        final_response = all_messages[-1].content
        
        reasoning_steps = []
        
        for msg in all_messages[1:-1]:
            step_type = "unknown"
            content = msg.content
            
            if isinstance(msg, ToolMessage):
                step_type = "tool_result"
                # CRITICAL FIX: We do NOT truncate here anymore. 
                # We send the full text so the UI can parse all diseases.
            elif isinstance(msg, AIMessage):
                if msg.tool_calls:
                    step_type = "tool_call"
                    content = f"Calling Tool: {msg.tool_calls[0]['name']}"
                else:
                    step_type = "intern_draft"
            
            reasoning_steps.append({
                "type": step_type,
                "content": content
            })

        return {
            "response": final_response,
            "reasoning": reasoning_steps
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Multi-Agent API...")
    uvicorn.run(app, host="0.0.0.0", port=8000)