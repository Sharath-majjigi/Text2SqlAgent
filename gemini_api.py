from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()

class GeminiAPIClient:
    def __init__(self):
        self.api_url = os.getenv("GEMINI_API_URL")

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
                You are an expert SQL developer with complete knowledge of SQL joins, aggregates, filtering, and complex queries. 
                You will receive an input task, and your job is to provide only the plain SQL query with no additional formatting, explanations, or comments. 

                ### Database Schema:

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

                ### Examples:

                **Task**: List all users.
                **Output**: SELECT * FROM users;

                **Task**: Find all orders with an amount greater than 100.
                **Output**: SELECT * FROM orders WHERE amount > 100;

                **Task**: Retrieve the name and email of users who have placed an order for 'Laptop'.
                **Output**: SELECT users.name, users.email FROM users JOIN orders ON users.id = orders.user_id WHERE orders.product_name = 'Laptop';

                ### Important Rules:
                1. Do not include backticks (`` ` ``) or triple backticks (`` ``` ``).
                2. Provide the SQL query only, with no comments or extra formatting.
                3. Stick to valid SQL syntax for the given schema.
                4. The output must be a single-line SQL query.

                Now, generate a plain SQL query for the following task: {task_description}.
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

            if "candidates" in result and len(result["candidates"]) > 0:
                raw_sql = result["candidates"][0]["content"]["parts"][0]["text"]
                return raw_sql
            else:
                raise Exception("No candidates found in the response")
        
        except requests.RequestException as error:
            raise Exception(f"Error generating SQL query: {error}")
