import json
import os
from difflib import SequenceMatcher
import sqlite3

class MemoryAgent:
    """
    MemoryAgent whose sole responsibility is storing the interactions between system and user.
    """

    def __init__(self, memory_file: str = "data/memory.db"):
        self.memory_file = memory_file
        self.memory = self._create_interactions_table()


    def _create_interactions_table(self):
        """
        Creates a table to store interactions in SQLite if it doesn't exist.
        """
        with sqlite3.connect(self.memory_file) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS interactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_query TEXT,
                    sql_query TEXT,
                    result TEXT
                )
            ''')



    def _save_memory(self):
        """
        Saves the current memory state.
        """
        with open(self.memory_file, 'w') as file:
            json.dump(self.memory, file, indent=4)



    def add_interaction(self, user_query: str, sql_query: str, result: str):
        """
        Adds a new interaction to the SQLite database, storing the result as a JSON string.

        :param user_query: The natural language query from the user.
        :param sql_query: The SQL query generated from the natural language query.
        :param result: The result after running the SQL query, as a JSON string.
        """
        result_in_json = json.dumps(result)
        with sqlite3.connect(self.memory_file) as conn:
            conn.execute('''
                INSERT INTO interactions (user_query, sql_query, result) 
                VALUES (?, ?, ?)
            ''', (user_query, sql_query, result_in_json))
   
   
    def get_interaction_history(self) -> list:
        """
        Retrieves the history of all interactions stored in the SQLite database.

        :return: A list of dictionaries, where each dictionary contains the user query, SQL query, and result as a JSON string.
        """
        with sqlite3.connect(self.memory_file) as conn:
            cursor = conn.execute('SELECT user_query, sql_query, result FROM interactions')
            history = []
            for row in cursor.fetchall():
                history.append({
                    "user_query": row[0],
                    "sql_query": row[1],
                    "result": row[2]  # Return the result as a JSON string, not as a dictionary
                })
        return history
    

    
    def suggest_similar_query(self, new_query: str) -> json:
        """
        Suggests a similar query from memory based on the new query using string similarity.

        :param new_query: The new natural language query provided by the user.
        :return: The closest matching interaction (including result as JSON string) if found, otherwise None.
        """
        best_match = None
        highest_similarity = 0

        # Fetch all stored interactions
        with sqlite3.connect(self.memory_file) as conn:
            cursor = conn.execute('SELECT user_query, sql_query, result FROM interactions')
            for row in cursor.fetchall():
                user_query = row[0]
                similarity = self._calculate_similarity(user_query, new_query)
                if similarity > highest_similarity:
                    best_match = {
                        "user_query": row[0],
                        "sql_query": row[1],
                        "result": json.loads(row[2])  # Keep the result as a JSON string
                    }
                    highest_similarity = similarity

        # If the best match has a high similarity score, return it
        if best_match and highest_similarity > 0.99:  # Use a threshold for matching
            return best_match
        return None

    def _calculate_similarity(self, query1: str, query2: str) -> float:
        """
        Calculates the similarity between two queries using SequenceMatcher.

        :param query1: The first query string.
        :param query2: The second query string.
        :return: A float representing the similarity between the two queries.
        """
        return SequenceMatcher(None, query1, query2).ratio()
