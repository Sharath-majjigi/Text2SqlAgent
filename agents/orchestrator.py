import pandas as pd
import pandasql as ps
from gemini_api import GeminiAPIClient
from agents.ddl_agent import DDLSchemaAgent
from agents.memory_agent import MemoryAgent
from db_manager import DBManager

class OrchestratorAgent:
   
    """
    OrchestratorAgent as the name suggests it orchestrates the agents to handle queries and interactions.
    Basically it is responsible for managing the flow of queries.
    """


    def __init__(self, gemini_api_key: str, db_path: str):
        """
        Initilize the orchestrator with Gemini Flash Api key, along with DDL Agent and DB Manager Agent
        """
        self.gemini_api = GeminiAPIClient(gemini_api_key)
        self.ddl_agent = DDLSchemaAgent(db_path)
        self.memory_agent = MemoryAgent()
        self.db_manager = DBManager(db_path)
        self.csv_files = {
            "sales": "data/sales.csv",      
            "inventory": "data/inventory.csv" 
        }


    def handle_user_query(self, user_query: str) -> dict:
        """
        Handles user's natural language query by identifying the appropriate datasource,
        generating sql query, and returning the result.

        :param user_query: The natural language query from the user.
        :return: The result of the query execution as a dictionary.
        """

        sqlite_schema = self.ddl_agent.get_sqlite_schema()

        sql_query = self.gemini_api.generate_sql_query(user_query)


        # Here we identify whether the query is for SQL database or csv
        if any(table in sql_query for table in sqlite_schema.keys()):
            result_df = self.db_manager.execute_sql(sql_query)
            self.memory_agent.add_interaction(user_query, sql_query, result_df.to_dict())
            return result_df.to_dict(orient="records")
        
        else:
            return self.query_csv(sql_query)



    def query_csv(self, sql_query: str):
        """
        Handle queries for CSV data sources.
        
        :param sql_query: The SQL query to run.
        :return: The result of the query execution as a dictionary.
        """

        inventory_df = pd.read_csv(self.csv_files["inventory"])
        sales_df = pd.read_csv(self.csv_files["sales"])

        try:
            sql_query = sql_query.replace("inventory", "inventory_df").replace("sales", "sales_df")

            result_df = ps.sqldf(sql_query, {"inventory_df": inventory_df, "sales_df": sales_df})

            if result_df is None or result_df.empty:
                return {"message": "Oops no records found."}


            self.memory_agent.add_interaction(f"CSV Query: {sql_query}", sql_query, result_df.to_dict())
            return result_df.to_dict(orient="records")
        except Exception as e:
            return {"error": f"Failed to query on CSV data: {str(e)}"}
