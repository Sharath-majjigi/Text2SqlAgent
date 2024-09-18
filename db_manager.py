import sqlite3
import pandas as pd

class DBManager:

    """
    DBManager is actually responsible for interacting with both the SQL database and CSV files.
    """


    # initialize the DBManager with path to sqlite database
    def __init__(self, db_path: str):
        self.db_path = db_path

    
    def execute_sql(self, query: str) -> pd.DataFrame:
        """
        It takes sql query as input and executes the query on SQL database and return the result as pandas Dataframe

        :param query: The SQL query to be executed.
        :return: A pandas DataFrame containing the result of the query.
        """
        connection = sqlite3.connect(self.db_path)
        try:
            df = pd.read_sql_query(query, connection)
            return df
        except Exception as ex:
            raise Exception(f"Error while executing SQL query: {ex}")
        finally:
            connection.close()

    

    def load_csv(self, file_path: str) -> pd.DataFrame:
        """
        Loads a CSV file into a pandas DataFrame.

        :param file_path: The path to the CSV file.
        :return: Pandas data frame which contains data from scv file
        """
        try:
            df = pd.read_csv(file_path)
            return df
        except FileNotFoundError as e:
            raise Exception(f"CSV file not found: {e}")
