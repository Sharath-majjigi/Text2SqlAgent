import sqlite3
import pandas as pd

class DDLSchemaAgent:
    """
    DDLSchemaAgent understands the schema of SQLite database and CSV files.
    """

    def __init__(self, db_path: str):
        self.db_path = db_path


    def get_sqlite_schema(self) -> dict:
        """
        Retrieves the schema of all tables in the SQLite database.
        :return: Dictionary, where keys are table names and values are list of columns.
        """

        schema = {}
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        try:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()

            for table in tables:
                table_name = table[0]
                cursor.execute(f"PRAGMA table_info({table_name});")
                columns = cursor.fetchall()
                schema[table_name] = [col[1] for col in columns]
        finally:
            connection.close()

        return schema
    


    def get_csv_schema(self, csv_path: str) -> list:
        """
        Retrieves schema (column names) of a CSV file.

        :param csv_path: Path to the CSV file.
        :return: A list of column names.
        """
        data_frame = pd.read_csv(csv_path)
        return data_frame.columns.tolist()
