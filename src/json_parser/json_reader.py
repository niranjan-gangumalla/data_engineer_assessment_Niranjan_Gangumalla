import json
import os
from typing import Generator, Dict, List
from utils.logger_service import get_logger

class JSONReader:

    def __init__(self, file_path: str, malformed_path: str):
        self.file_path = file_path
        self.malformed_path = malformed_path
        self.malformed_records: List[dict] = []
        self.total_records = 0
        self.logger = get_logger(self.__class__.__name__)

    def _save_malformed(self):
        if not self.malformed_records:
            return

        os.makedirs(os.path.dirname(self.malformed_path), exist_ok=True)

        with open(self.malformed_path, "w", encoding="utf-8") as f:
            json.dump(self.malformed_records, f, indent=2)

        self.logger.warning(
            f"{len(self.malformed_records)} malformed records found and saved malformed records under 'audit_logs\malformed_records.json'"
        )

    def _record_malformed(self, index, buffer, error):
        self.malformed_records.append({
            "index": index,
            "error": str(error),
            "snippet": buffer[:1500],
        })

    def read_stream(self) -> Generator[Dict, None, None]:
        buffer = ""
        brace_depth = 0
        inside_object = False
        record_index = 0

        with open(self.file_path, "r", encoding="utf-8") as file:
            for line in file:
                for ch in line:
                    if ch == "{":
                        brace_depth += 1
                        inside_object = True

                    if inside_object:
                        buffer += ch

                    if ch == "}":
                        brace_depth -= 1

                        if brace_depth == 0 and inside_object:
                            try:
                                cleaned = buffer.strip().rstrip(",")
                                obj = json.loads(cleaned)
                                yield obj
                            except Exception as err:
                                self._record_malformed(record_index, buffer, err)

                            self.total_records += 1
                            record_index += 1
                            buffer = ""
                            inside_object = False
                            break

        # Save malformed JSON objects.
        self._save_malformed()

        self.logger.info(f"Finished reading JSON file: {self.total_records} records processed.")
