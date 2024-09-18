# Text-to-SQL Query System with Multi-Source Data and AI Agents

This project implements a Text-to-SQL query system that converts natural language queries into SQL queries to fetch data from multiple sources, including a MySQL database and CSV files. It uses AI agents to determine the correct data source and returns the appropriate results via a REST API.

### Tech used
- python
- Sqlite
- Gemini Flash model

  
## Features

- Converts natural language queries to SQL queries.
- Retrieves data from multiple sources: 
  - SQLite Database (mocked users, orders tables).
  - CSV files (sales, inventory).
- Memory persistence: Stores and retrieves past interactions.
- REST API to handle user queries and return results.
  
## Installation Guide

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/text-to-sql-agent.git
cd text-to-sql-agent
```
### 2. Create and Activate a Virtual Environment

``` bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

```bash
DB_PATH=your_database_path_here.db  # Path to your SQLite DB
GEMINI_API_URL=your_gemini_api_url_here
GEMINI_API_KEY=your_gemini_api_key_here
```

### 5. Set Up SQLite Database

Use the provided .sql file to generate the necessary tables in SQLite.

Run the following commands in your terminal to create the tables from the schema.sql file:

```bash
sqlite3 your_database_path_here.db < schema.sql
```

This will create the required users and orders tables in the SQLite database.

### 6. Start the FastAPI Server

``` bash
uvicorn main:app --reload
```

### 7. API Endpoints

Request Body:
```json
{
  "natural_language_query": "list all users"
}
```
Response:
```json
[
  {
    "id": 1,
    "name": "Alice",
    "email": "alice@example.com"
  },
  {
    "id": 2,
    "name": "Bob",
    "email": "bob@example.com"
  }
]
```

### 8. Notes

- Make sure to add your Gemini API credentials to the .env file before running the application. </br>
- You can extend the system by adding more complex natural language queries, new data sources, or further improving the memory system.

