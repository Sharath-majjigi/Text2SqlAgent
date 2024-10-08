import pandas as pd
import pandasql as ps
import json
from gemini_api import GeminiAPIClient
from agents.ddl_agent import DDLSchemaAgent
from agents.memory_agent import MemoryAgent
from db_manager import DBManager

class OrchestratorAgent:
   
    """
    OrchestratorAgent as the name suggests it orchestrates the agents to handle queries and interactions.
    Basically it is responsible for managing the flow of queries.
    """


    def __init__(self,db_path: str):
        """
        Initilize the orchestrator with Gemini Flash Api key, along with DDL Agent and DB Manager Agent
        """
        self.gemini_api = GeminiAPIClient()
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

        suggested_query = self.memory_agent.suggest_similar_query(user_query)
        if suggested_query:
            sql_query =  suggested_query.get("sql_query")
            result = self.identify_datasource_and_execute_query(user_query,sql_query)
            print("Similar query found, user_query: "+ user_query + "\n" + "sql_query: " + sql_query)

            return result
        
        
        sql_query = self.gemini_api.generate_sql_query(user_query)

        print(f"Generated SQL Query: {sql_query}")

        return self.identify_datasource_and_execute_query(user_query,sql_query)



    def identify_datasource_and_execute_query(self,user_query,sql_query:str):

        sqlite_schema = self.ddl_agent.get_sqlite_schema()

        if any(table in user_query for table in sqlite_schema.keys()):
        
            try:
                result_df = self.execute_sql(sql_query,user_query)
                return result_df

            except Exception as e:
                return {"error occured at handle_user_query": f" {str(e)}"}
        
        else:
            return self.execute_csv(sql_query,user_query)


    
    def execute_sql(self, sql_query: str, user_query: str):
        """
        Executes an SQL query
        """

        result_df = self.db_manager.execute_sql(sql_query)
        if result_df is None or result_df.empty:
            raise Exception("Oops No data found, retrying again...")
        
        result_df = result_df.to_dict(orient="records")
        self.memory_agent.add_interaction(user_query, sql_query)
        return result_df
   
   
    
    def execute_csv(self, sql_query: str,user_query: str):
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
            
            result_df = result_df.to_dict(orient="records")
            self.memory_agent.add_interaction(user_query, sql_query)

            return result_df
    
        except Exception as e:
            return {"error": f"Failed to query on CSV data: {str(e)}"}
