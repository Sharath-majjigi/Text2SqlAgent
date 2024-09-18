from dotenv import load_dotenv;
import os;

load_dotenv()


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DB_PATH = os.getenv("MOCK_SQL_DB_PATH")