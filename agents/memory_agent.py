import json
import os
from difflib import SequenceMatcher

class MemoryAgent:
    """
    MemoryAgent whose sole responsibility is storing the interactions between system and user.
    """

    def __init__(self, memory_file: str = "memory.json"):
        self.memory_file = memory_file
        self.memory = self._load_memory()


    def _load_memory(self) -> dict:
        """
        Loads memory from a JSON file if it exists (For simplicity, we can use database as well to store the converations)

        :return: A dictionary containing the past interactions.
        """
        if os.path.exists(self.memory_file):
            with open(self.memory_file, 'r') as file:
                return json.load(file)
        return {}



    def _save_memory(self):
        """
        Saves the current memory state.
        """
        with open(self.memory_file, 'w') as file:
            json.dump(self.memory, file, indent=4)



    def add_interaction(self, user_query: str, sql_query: str, result: dict):
        """
        Adds a new interaction to the memory and saves it.
        Inserts a new converation into the memory and persists it.

        :param user_query: The natural language query from the user.
        :param sql_query: SQL query generated from LLM.
        :param result: Final result after running the sql query.
        """
        interaction = {
            "user_query": user_query,
            "sql_query": sql_query,
            "result": result
        }

        if "history" not in self.memory:
            self.memory["history"] = []

        self.memory["history"].append(interaction)
        self._save_memory()

   
   
    def get_interaction_history(self) -> list:
        """
        Retrieves the history of all interactions stored in memory.

        :return: A list of past interactions.
        """
        return self.memory.get("history", [])
    

    
    def suggest_similar_query(self, new_query: str) -> dict:
        """
        Suggests a similar query from memory based on the new query.
        """
        if "history" not in self.memory:
            return None

        best_match = None
        highest_similarity = 0

        for interaction in self.memory["history"]:
            similarity = self._calculate_similarity(interaction["user_query"], new_query)
            if similarity > highest_similarity:
                best_match = interaction
                highest_similarity = similarity

        if best_match and highest_similarity > 0.99:  # Threshold for a good match
            return best_match
        return None


    def _calculate_similarity(self, query1: str, query2: str) -> float:
        """
        Calculates the similarity between two queries using SequenceMatcher.
        """
        return SequenceMatcher(None, query1, query2).ratio()
