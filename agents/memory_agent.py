import json
from sentence_transformers import SentenceTransformer, util
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# The base for ORM models
Base = declarative_base()

# The Interaction model to represent the interactions table
class Interaction(Base):
    __tablename__ = 'interactions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_query = Column(String, nullable=False)
    sql_query = Column(String, nullable=False)


class MemoryAgent:
    """
    MemoryAgent which is responsible for storing the interactions between system and user,
    and suggesting similar queries.
    """

    def __init__(self, db_url: str = "sqlite:///db/memory.db"):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)
        self.model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

    def add_interaction(self, user_query: str, sql_query: str):
        """
        Adds a new interaction to the database after checking if a similar interaction exists.

        :param user_query: The natural language query from the user.
        :param sql_query: The SQL query generated from the natural language query.
        """
        session = self.Session()

        # Check if a similar interaction exists first
        similar_interaction = self.suggest_similar_query(user_query)

        # If no similar interaction is found or SQL queries don't match, add new interaction
        if not similar_interaction or similar_interaction['sql_query'] != sql_query:
            new_interaction = Interaction(user_query=user_query, sql_query=sql_query)
            session.add(new_interaction)
            session.commit()

        session.close()

    def get_interaction_history(self) -> list:
        """
        Retrieves the history of all interactions stored in the database.

        :return: A list of dictionaries, where each dictionary contains the user query and SQL query.
        """
        session = self.Session()
        interactions = session.query(Interaction).all()

        history = [{
            "user_query": interaction.user_query,
            "sql_query": interaction.sql_query
        } for interaction in interactions]

        session.close()
        return history

    def suggest_similar_query(self, new_query: str) -> dict:
        """
        Suggests a similar query from memory based on the new query using BERT embeddings for semantic similarity.

        :param new_query: The new natural language query provided by the user.
        :return: The closest matching interaction if found, otherwise None.
        """
        best_match = None
        highest_similarity = 0

        session = self.Session()
        past_interactions = session.query(Interaction).all()

        if not past_interactions:
            session.close()
            return None

        # Generate BERT embedding for the new query
        new_query_embedding = self.model.encode(new_query, convert_to_tensor=True)

        # Compare the new query with each past query one by one
        for interaction in past_interactions:
            past_query = interaction.user_query
            sql_query = interaction.sql_query

            # Calculate similarity
            similarity = self._calculate_similarity(new_query_embedding, past_query)

            if similarity > highest_similarity:
                best_match = {
                    "user_query": past_query,
                    "sql_query": sql_query
                }
                highest_similarity = similarity

        session.close()

        if best_match and highest_similarity > 0.70:
            return best_match
        return None

    def _calculate_similarity(self, new_query_embedding, past_query: str) -> float:
        """
        Calculates the semantic similarity between the new query embedding and the past query
        using BERT embeddings and cosine similarity.

        :param new_query_embedding: The pre-computed BERT embedding for the new query.
        :param past_query: The past query string to compare with.
        :return: A float representing the similarity between the new query and the past query.
        """
        past_query_embedding = self.model.encode(past_query, convert_to_tensor=True)

        similarity = util.pytorch_cos_sim(new_query_embedding, past_query_embedding)

        return similarity.item()
