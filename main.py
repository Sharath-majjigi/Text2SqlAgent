from fastapi import FastAPI, HTTPException
from agents.orchestrator import OrchestratorAgent
from pydantic import BaseModel
from config import DB_PATH

app = FastAPI()

orchestrator_agent = OrchestratorAgent(DB_PATH)

# request body / pydantic
class QueryRequest(BaseModel):
    natural_language_query: str


@app.post("/query")
async def execute_user_query(query: QueryRequest):
    """
    API which accepts user query in natural language and returns the data from SQLite database 
    or a CSV file

    :param natural_language_query: The user's natural language query.
    :return: The results of the query
    """
    try:
        result = orchestrator_agent.handle_user_query(query.natural_language_query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.get("/history")
async def get_interaction_history():
    """
    API to retrieve the the history of past interactions.

    :return: A list of past interactions.
    """
    return orchestrator_agent.memory_agent.get_interaction_history()
