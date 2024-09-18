import requests
import json
import re

class GeminiAPIClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={self.api_key}"

    def generate_sql_query(self, task_description: str) -> str:
        """
        Sends a structured natural language prompt to the Gemini API to generate an SQL query.

        :param task_description: The task for which SQL query needs to be generated.
        :return: The generated SQL query.
        """
        headers = {
            "Content-Type": "application/json"
        }

        prompt = f"""
        You are an expert SQL developer with complete knowledge in SQL joins, aggregates, filtering, and complex queries. 
        When I give you an input, you only give me sql query and no backticks, no new lines,
        nothing just a plain simple sql query. 
        
        If you still give query like this ```sql\nSELECT * FROM orders WHERE amount < 45;\n```
        then you are looosing race with CHATGPT.

        You have access to the following database schema:

        - Table `users`:
          - `id` (INTEGER, primary key)
          - `name` (TEXT)
          - `email` (TEXT)

        - Table `orders`:
          - `id` (INTEGER, primary key)
          - `user_id` (INTEGER, foreign key referencing `users(id)`)
          - `product_name` (TEXT)
          - `amount` (REAL)

        - CSV `sales`:
          - sale_id, product, quantity, price

        - CSV `inventory`:
          - item_id, product, stock

        Your task is to generate only plain SQL queries** that interact with this schema. Ensure that:
        1. The SQL queries are valid for this schema.
        2. Do not include any additional formatting such as backticks (`` ` ``) or triple backticks (`` ``` ``), Markdown, or code blocks.
        3. Do not include comments, explanations, or labels like `sql` or `text`.

        ### Important:
        - If I ask you to list all users, the output should be: 
          - `SELECT * FROM users;`
        - DO NOT output: 
          - `` ```sql\nSELECT * FROM users;\n``` ``
          - or any variation with backticks, code blocks, or extra formatting.

        Now, please generate a plain SQL query for the following task: {task_description}.
        """

        data = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ]
        }

        try:
            response = requests.post(self.api_url, headers=headers, data=json.dumps(data))
            response.raise_for_status()

            result = response.json()
            print(result)

            if "candidates" in result and len(result["candidates"]) > 0:
                raw_sql = result["candidates"][0]["content"]["parts"][0]["text"]
                return raw_sql
            else:
                raise Exception("No candidates found in the response")
        
        except requests.RequestException as error:
            raise Exception(f"Error generating SQL query: {error}")
