from pydantic import BaseModel
from typing import List, Dict, Any

class VinoModel:
    def __init__(self, db_connection):
        self.db = db_connection

    def lista_vinos(self) -> List[Dict[str, Any]]:
        with self.db.cursor() as cur:
            cur.execute("""
                SELECT vino_key, nombre, marca FROM dim_vino
            """)
            return cur.fetchall()