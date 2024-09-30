from db.weavite import WeaviateClient

class MemoryAgent:
    def __init__(self):
        self.weaviate_client = WeaviateClient()

    def add_interaction(self, user_query: str, sql_query: str):
        """Persists user query & Sql query generated for it in the db"""

        # Check if a semantically similar user query already exists
        existing_query = self.weaviate_client.retrieve_similar_query(user_query)
        
        if existing_query:
            print(f"Similar query already exists: {existing_query[0]['user_query']}")
            return
        
        self.weaviate_client.store_interaction(user_query, sql_query)


    def suggest_similar_query(self, new_query: str) -> dict:
        """Suggest similar queries based on the user's input"""
        similar_query = self.weaviate_client.retrieve_similar_query(new_query)
    
        if similar_query:
            user_query = similar_query[0]['user_query']
            sql_query = similar_query[0]['sql_query']

            # # Remove '_df' if it is attached to sql query
            # sql_query = sql_query.replace("_df", "")

            return {
                "user_query": user_query,
                "sql_query": sql_query
            }

        return None

