import os
from supabase import create_client

from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


class DBConnection:
    """Singleton DB instance"""
    _instance = None

    def __init__(self):
        self.db_client = create_client(SUPABASE_URL, SUPABASE_KEY)

    def get_client(self):
        return self.db_client

    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)

        return cls._instance

    def insert(self, table_name: str, data: dict):
        try:
            result = self.db_client.table(table_name).insert(data).execute()
            print(f"[DBConnection:insert()] Inserted build #{data['build_number']} into 'builds' table.")
            return result
        except Exception as e:
            print(f"Failed to insert to table: '{table_name}'")
            raise

    def upsert(self, table_name: str, data: dict):
        try:

            result = self.db_client.table(table_name).upsert(data, on_conflict="job_name,build_number", ignore_duplicates=False).execute()

            print(f"[DBConnection:insert()] upserted build #{data['build_number']} into 'builds' table.")
            return result
        except Exception as e:
            print(f"Failed to insert to table: '{table_name}'")
            raise



if __name__ == '__main__':
    build_data = {
        "job_name": "nightly-build-2",
        "build_number": 1,
        "status": "FAILURE",
        "branch": "main",
        "triggered_by": "developer",
        "parameters": {"env": "prod", "retry": False},
        "duration_ms": 15000,
        "timestamp": "2025-07-13T12:34:56Z",
        "url": "https://jenkins.example.com/job/test-build/101",
        "console_log_url": "https://jenkins.example.com/job/test-build/101/console"
    }
    db_object = DBConnection()
