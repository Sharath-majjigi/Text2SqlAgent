# Text-to-SQL Query System with Multi-Source Data and AI Agents

This project implements a Text-to-SQL query system that converts natural language queries into SQL queries to fetch data from multiple sources, including a MySQL database and CSV files. It uses AI agents to determine the correct data source and returns the appropriate results via a REST API.

# Demo + Explaination videos

## Demo Video

[![Demo Video](https://img.icons8.com/color/48/000000/video.png)](https://www.canva.com/design/DAGRjclYbOI/oUzDDNxnQgA7nootgboc3Q/watch?utm_content=DAGRjclYbOI&utm_campaign=designshare&utm_medium=link&utm_source=editor)

[Watch the demo video](https://www.canva.com/design/DAGRjclYbOI/oUzDDNxnQgA7nootgboc3Q/watch?utm_content=DAGRjclYbOI&utm_campaign=designshare&utm_medium=link&utm_source=editor)

## Explanation Video

[![Explanation Video](https://img.icons8.com/color/48/000000/video.png)](https://drive.google.com/file/d/1Tc8mXSWehhN3k7iXkzkOnvCYLLPrLekU/view?usp=drive_link)

[Watch the explanation video](https://drive.google.com/file/d/1Tc8mXSWehhN3k7iXkzkOnvCYLLPrLekU/view?usp=drive_link)


## 🌟 My approaches for Text2Sql

- **Tex2Sql - v1**
    - I initially built this system with memory stored in **JSON files**, using a **Sequencer** module for basic natural language query similarity checks.</br>
- **Tex2Sql - v2** 
   - Later, I shifted to storing memory in a **database** and improved efficiency with **Cosine Similarity** for better query matching accuracy. </br>
 - **Tex2Sql - v3**
    - Finally, started implementing **Retrieval-Augmented Generation (RAG)** with a **Vector Database**
      to handle larger datasets more effectively and also compare user query more semantically. </br>

<br>


_The last approach is in the branch ***feat/RAG-vector-db-text-to-sql***_

<br>

## 🛠️ Tech Used
- Python
- SQLite
- Sentence Transformers
- FastAPI for the API
- Cosine Similarity Algorithm
- RAG (Retrieval-Augmented Generation)
- Vector Database (Weavite)
- Few shots Prompting method

</br>
  
## ✨ Features

| Feature                        | Description                                                                                                       |
|---------------------------------|-------------------------------------------------------------------------------------------------------------------|
| 🔍 **Natural Language to SQL**  | Converts user queries into SQL.                                                    |
| **Cosine Similarity Search**       | Recommends similar past queries using embeddings and cosine similarity to optimize query suggestions. |
| 📊 **Multiple Data Sources**    | Retrieves data from both **SQLite** and **CSV** files.                                                            |
| 🤖 **Enhanced AI Agents**       | - 🧠 **Autonomous Schema Detection**: Automatically detects and adapts to schema changes in databases and CSV files. </br> </br> - 📈 **Learning from Past Interactions**: Suggests queries based on previous interactions, making the system smarter over time. |
| 💾 **Memory Persistence**       | Stores and retrieves past interactions to enhance query accuracy over time.                                        |

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

# 📊 Data Used

## 🗄️ SQL Tables
### Orders Table
| order_id | user_id | product  | amount ($) |
|----------|---------|----------|------------|
| 1        | 1       | Laptop   | 1500.0     |
| 2        | 1       | Mouse    | 25.0       |
| 3        | 2       | Keyboard | 45.0       |
| 4        | 3       | Monitor  | 300.0      |

#### Users Table
| user_id | name     | email             |
|---------|----------|-------------------|
| 1       | Alice    | alice@example.com |
| 2       | Bob      | bob@example.com   |
| 3       | Charlie  | charlie@example.com |


## 📄 CSV Files

### Inventory
| item_id | product    | stock |
|---------|------------|-------|
| 1       | Laptop     | 50    |
| 2       | Mouse      | 300   |
| 3       | Keyboard   | 150   |
| 4       | Monitor    | 100   |
| 5       | Smartphone | 20    |

### Sales
| sale_id | product    | quantity | price ($) |
|---------|------------|----------|-----------|
| 1       | Laptop     | 2        | 1500      |
| 2       | Mouse      | 10       | 15        |
| 3       | Keyboard   | 5        | 45        |
| 4       | Monitor    | 3        | 200       |
| 5       | Smartphone | 1        | 800       |
| 6       | Charger    | 10       | 2005      |


### 7️⃣ API

Endpoint: 

```/query```

Request Body:
```json
{
      "natural_language_query": "what is the product name whose sales price is greater than 200"
}
```
Response:
```json
[
    {
        "product": "Laptop"
    },
    {
        "product": "Smartphone"
    },
    {
        "product": "Charger"
    }
]
```
</br>

Endpoint : 

```/train```

Request body:
```json
{
  "user_query": "Show me the available stock for all products",
  "sql_query": "SELECT * FROM products WHERE stock > 0"
}
```

Response: 
200 ok

### 8️⃣ Notes

- Make sure to add your Gemini API credentials to the .env file before running the application. </br>
- If you want to try out RAG + vector DB make sure you checkout to that branch and have your **weaviate**  up and running,
  If not run this
  ```bash
  docker run -d -p 8080:8080 semitechnologies/weaviate:latest 
  ```

## Challenges Faced

| Challenge                          | Description                                                                                                                                                                                                                             |
|------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Designing Autonomous Agents**    | Understanding on Building agents - what are they, How do they behave and what agents does text2sql system should have.       |
|**Scaling with RAG & Vector DB**	       | Implementing RAG with a Vector Database - faced a challenge where i was not able to vector search based on embeddings. |
| **Handling Schema Changes**        | Handling both SQLite databases and CSV files required the system to adapt to any changes in their structure. Making agents automatically detect schema changes and update their understanding was tricky.                                  |
| **Building a Memory System**       | Creating a memory system that learns from past interactions and make the agents smarter                             |
| **Using LLM for SQL Generation**   | Using LLM to generate SQL queries from natural language was also one of the challenging aspects. It required carefully crafting prompts that provided enough context about the database schema. Multiple iterations were needed to perfect it. |
| **Learning Python**                | Not coded in Python much, so I had to learn the best practices along the way. While it was initially a challenge to adapt, I quickly found it to be fun to work with.                                                                     |


