from fastapi import FastAPI, HTTPException
from agents.orchestrator import OrchestratorAgent
from pydantic import BaseModel
from config import DB_PATH

app = FastAPI()

orchestrator_agent = OrchestratorAgent(DB_PATH)

class QueryRequest(BaseModel):
    natural_language_query: str


@app.post("/query")
async def execute_user_query(query: QueryRequest):
    """
    API which accepts user query in natural language and returns data from the database (SQL or CSV).
    """
    try:
        result = orchestrator_agent.handle_user_query(query.natural_language_query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/history")
async def get_interaction_history():
    """
    API to retrieve the history of past interactions stored in VectorDatabase (through SQLite).
    """
    return orchestrator_agent.memory_agent.get_interaction_history()
