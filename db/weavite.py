import weaviate
from sentence_transformers import SentenceTransformer
from weaviate.classes.query import MetadataQuery

class WeaviateClient:
    def __init__(self):
        self.client = weaviate.Client("http://localhost:8080")
        self.model = SentenceTransformer('paraphrase-MiniLM-L6-v2')


    def store_interaction(self, user_query: str, sql_query: str):
        """
        Generates embeddings for the user query and persistsin veccotr db weaviate
        """
        print("Embeddings for store_interaction")
        embedding = self.model.encode(user_query)
        print(embedding.tolist())
        self.client.data_object.create({
            "user_query": user_query,
            "sql_query": sql_query,
            "embedding": embedding.tolist()
        }, "Interaction")


    def retrieve_similar_query(self, user_query: str):

        embedding = self.model.encode(user_query)

        try:

            # Get embeddings for user_query and perform a vector search
            embedding = self.model.encode(user_query)
            print("retrieve_similar_query embedding")
            print(embedding.tolist())
            
            vector_result = self.client.query.get("Interaction", ["user_query", "sql_query"]) \
                                .with_near_vector({"vector": embedding.tolist()}) \
                                .with_limit(1) \
                                .do()


            if 'data' in vector_result and 'Get' in vector_result['data'] and 'Interaction' in vector_result['data']['Get']:
             interactions = vector_result['data']['Get']['Interaction']
            if interactions and interactions[0].get('sql_query'):
                return interactions[0]['sql_query']  # Only return the SQL query if it exists

            return None

        except Exception as e:
            print(f"Error querying Weaviate using BM25 and vector search: {str(e)}")
            return None

