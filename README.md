# Text-to-SQL Query System with Multi-Source Data and AI Agents

This project implements a Text-to-SQL query system that converts natural language queries into SQL queries to fetch data from multiple sources, including a MySQL database and CSV files. It uses AI agents to determine the correct data source and returns the appropriate results via a REST API.

## 🛠️ Tech Used

🐍 **Python** </br>
🗃️ **SQLite**</br>
💡 **Gemini Flash Model** </br>

</br>
  
## ✨ Features

| Feature                        | Description                                                                                                       |
|---------------------------------|-------------------------------------------------------------------------------------------------------------------|
| 🔍 **Natural Language to SQL**  | Converts natural language queries into precise SQL queries.                                                       |
| 📊 **Multiple Data Sources**    | Retrieves data from both **SQLite** and **CSV** files.                                                            |
| 🤖 **Enhanced AI Agents**       | - 🧠 **Autonomous Schema Detection**: Automatically detects and adapts to schema changes in databases and CSV files. </br> </br> - 📈 **Learning from Past Interactions**: Suggests queries based on previous interactions, making the system smarter over time. |
| 💾 **Memory Persistence**       | Stores and retrieves past interactions to enhance query accuracy over time.                                        |
| 🌐 **REST API**                 | Exposes endpoints to handle user queries and return results in real-time.                                          |

</br>
</br>

  
## 🚀 Installation Guide

### 1️⃣ Clone the Repository

Start by cloning the repository to your local machine and navigate to the project directory:

```bash
git clone https://github.com/your-username/text-to-sql-agent.git
cd text-to-sql-agent
```

</br>

### 2️⃣ Create And activate virtual environment

``` bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

</br>

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

</br>

### 4️⃣ Set Up Environment Variables

```bash
DB_PATH=your_database_path_here.db  # Path to your SQLite DB
GEMINI_API_URL=your_gemini_api_url_here
GEMINI_API_KEY=your_gemini_api_key_here
```

</br>

### 5️⃣ Set Up SQLite Database

Use the provided .sql file to generate the necessary tables in SQLite.

Run the following commands in your terminal to create the tables from the schema.sql file:

```bash
sqlite3 your_database_path_here.db < schema.sql
```

This will create the required users and orders tables in the SQLite database.
</br>

### 6️⃣ Start the FastAPI Server

``` bash
uvicorn main:app --reload
```

</br>

### 7️⃣ API Endpoints

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
</br>

### 8️⃣ Notes

- Make sure to add your Gemini API credentials to the .env file before running the application. </br>
- You can extend the system by adding more complex natural language queries, new data sources, or further improving the memory system.

## Challenges Faced

| Challenge                          | Description                                                                                                                                                                                                                             |
|------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Using LLM for SQL Generation**   | Using LLM to generate SQL queries from natural language was one of the more challenging aspects. It required carefully crafting prompts that provided enough context about the database schema. Multiple iterations were needed to perfect it. |
| **Designing Autonomous Agents**    | Designing the system’s agents required understanding what makes an agent autonomous and how to make it react to different situations, such as changes in the database schema. Agents needed to handle tasks independently.                   |
| **Handling Schema Changes**        | Handling both SQLite databases and CSV files required the system to adapt to any changes in their structure. Making agents automatically detect schema changes and update their understanding was tricky.                                  |
| **Building a Memory System**       | It was challenging to build a memory system that not only stored past queries but also learned from them. The system had to become smarter over time by suggesting SQL queries based on similar past queries.                             |
| **Learning Python**                | Not coded in Python much, so I had to learn the best practices along the way. While it was initially a challenge to adapt, I quickly found it to be fun to work with.                                                                     |


