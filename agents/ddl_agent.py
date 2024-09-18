import sqlite3
import time
import os
import pandas as pd

class DDLSchemaAgent:
    """
    DDLSchemaAgent understands the schema of SQLite database and CSV files.
    """

    def __init__(self, db_path: str,check_interval: int = 60):
        self.db_path = db_path
        self.csv_schemas = {}
        self.sqlite_schema = {}
        self.check_interval = check_interval
        self.last_check_time = 0

        self._update_sqlite_schema()


    def _get_sqlite_schema(self) -> dict:
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
    
   
    def _update_sqlite_schema(self):
        """
        Updates the SQLite schema if changes are detected.
        """
        new_schema = self._get_sqlite_schema()
        if new_schema != self.sqlite_schema:
            print("Schema changed, updating cache...")
            self.sqlite_schema = new_schema
    

   
    def monitor_csv_files(self, csv_files: dict):
        """
        Monitors CSV files for any changes in their schema.
        """
        for csv_name, csv_path in csv_files.items():
            if os.path.exists(csv_path):
                new_schema = self._get_csv_schema(csv_path)
                if csv_name not in self.csv_schemas or self.csv_schemas[csv_name] != new_schema:
                    print(f"CSV schema for {csv_name} has changed. Updating...")
                    self.csv_schemas[csv_name] = new_schema

   
   
    def monitor_schemas(self, csv_files: dict):
        """
        Continuously monitors the database and CSV schemas for changes.
        """
        if time.time() - self.last_check_time > self.check_interval:
            self._update_sqlite_schema()
            self.monitor_csv_files(csv_files)
            self.last_check_time = time.time()


    def _get_csv_schema(self, csv_path: str) -> list:
        """
        Retrieves schema (column names) of a CSV file.

        :param csv_path: Path to the CSV file.
        :return: A list of column names.
        """
        data_frame = pd.read_csv(csv_path)
        return data_frame.columns.tolist()
    

    def get_sqlite_schema(self) -> dict:
        """
        Returns the current SQLite schema.
        """
        self.monitor_schemas({})
        return self.sqlite_schema
    

    def get_csv_schema(self, csv_path: str) -> list:
        """
        Returns the schema of a specific CSV file.
        """
        self.monitor_schemas({})
        return self.csv_schemas.get(csv_path, [])
