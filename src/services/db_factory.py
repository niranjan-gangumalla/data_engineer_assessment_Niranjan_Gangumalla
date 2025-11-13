import os
from sqlalchemy import create_engine

class DBFactory:

    @staticmethod
    def create_engine(db_type: str, config: dict = None, sqlite_path: str = None):
        db_type = db_type.lower()

        if db_type == "sqlite":
            if not sqlite_path:
                raise ValueError("sqlite_path must be provided for SQLite databases.")

            os.makedirs(os.path.dirname(sqlite_path), exist_ok=True)

            return create_engine(f"sqlite:///{sqlite_path}")

        if db_type == "mysql":
            if not config:
                raise ValueError("MySQL configuration must be provided.")

            user = config["user"]
            password = config["password"]
            host = config["host"]
            database = config["database"]

            mysql_url = f"mysql+pymysql://{user}:{password}@{host}/{database}"
            return create_engine(mysql_url)

        raise ValueError(f"Unsupported DB type '{db_type}'. Use 'sqlite' or 'mysql'.")
