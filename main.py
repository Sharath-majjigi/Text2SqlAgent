from fastapi import FastAPI, File, UploadFile, HTTPException
import json
from pydantic import BaseModel
from agents.orchestrator import OrchestratorAgent
from agents.memory_agent import MemoryAgent
from config import DB_PATH
from util.util import extract_text_from_pdf;

app = FastAPI()

orchestrator_agent = OrchestratorAgent(DB_PATH)
memory_agent = MemoryAgent()

class QueryRequest(BaseModel):
    natural_language_query: str

class TrainingData(BaseModel):
    user_query: str
    sql_query: str

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


@app.post("/train-agent")
async def train_from_pdf_json(file: UploadFile = File(...)):
    """
    Endpoint to train the agent using training data extracted from a PDF file.
    The PDF is expected to contain JSON-formatted text.
    """
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF file.")

    try:
        pdf_content = extract_text_from_pdf(file.file)
        
        try:
            json_data = json.loads(pdf_content)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="The PDF content is not valid JSON.")

        for data in json_data:
            memory_agent.add_interaction(data['user_query'], data['sql_query'])

        return {"message": "Training successful", "extracted_data": json_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF file: {str(e)}")
@app.post("/train")
async def train_system(training_data: TrainingData):
    """
    API to retrieve the history of past interactions stored in VectorDatabase (through SQLite).
    """
    return orchestrator_agent.memory_agent.add_interaction(training_data.user_query, training_data.sql_query)

# TODO: Add bulk training api (Like a user can upload a pdf with training data)
