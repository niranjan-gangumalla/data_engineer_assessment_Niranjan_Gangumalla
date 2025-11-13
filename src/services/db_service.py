import pandas as pd
from sqlalchemy import text
from utils.constants import TABLE_DTYPE_MAP
from utils.util import cast_df_types
from utils.logger_service import get_logger

class DBService:

    def __init__(self, engine):
        self.engine = engine
        self.logger = get_logger(self.__class__.__name__)

    def insert_dataframe(self, df: pd.DataFrame, table_name: str):
        if df is None or df.empty:
            return

        # Normalize column names
        df.columns = df.columns.str.lower()

        # Remove duplicates
        df = df.loc[:, ~df.columns.duplicated()]

        # Apply dtype mapping
        dtype_map = TABLE_DTYPE_MAP.get(table_name.lower(), None)
        if dtype_map:
            for col, dtype in dtype_map.items():
                if col in df.columns:
                    df[col] = df[col].astype(dtype, errors="ignore")

        df.to_sql(name=table_name, con=self.engine, index=False, if_exists="append")


    def insert_batch(self, batch_dict: dict):
        for table, data in batch_dict.items():
            if data:
                df = pd.DataFrame(data)
                self.insert_dataframe(df, table)

    def truncate_tables(self, tables: list):
        """
        Safely truncate tables in correct order, disabling FK checks temporarily.
        """
        try:
            with self.engine.begin() as conn:
                conn.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
                for t in tables:
                    conn.execute(text(f"TRUNCATE TABLE {t};"))
                conn.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))
            self.logger.info(f"Truncated tables: {tables}")
        except Exception as e:
            self.logger.error(f"Error truncating tables: {e}")
            raise

    def get_count(self, table_name: str) -> int:
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
                return int(result.scalar() or 0)
        except Exception as e:
            self.logger.error(f"Error counting rows in '{table_name}': {e}")
            return 0

    def log_table_counts(self, tables: list):
        for table in tables:
            count = self.get_count(table)
            self.logger.info(f"Table '{table}' contains {count} rows.")
