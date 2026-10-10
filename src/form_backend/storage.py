import sqlite3
import json
import time
from typing import List, Optional, Dict, Any
from .models import Submission, FormConfig


class FormStorage:
    """Forma arizalarini SQLite bazasida saqlash."""

    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self._conn = sqlite3.connect(self.db_path)
        self._init_db()

    def _init_db(self):
        with self._conn:
            self._conn.execute(
                """
                CREATE TABLE IF NOT EXISTS submissions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    form_id TEXT NOT NULL,
                    data_json TEXT NOT NULL,
                    sender_ip TEXT NOT NULL,
                    is_spam INTEGER DEFAULT 0,
                    created_at REAL NOT NULL
                )
                """
            )

    def save_submission(self, form_id: str, data: Dict[str, Any], sender_ip: str, is_spam: bool = False) -> int:
        with self._conn:
            cur = self._conn.execute(
                """
                INSERT INTO submissions (form_id, data_json, sender_ip, is_spam, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (form_id, json.dumps(data), sender_ip, 1 if is_spam else 0, time.time()),
            )
            return cur.lastrowid

    def get_submissions(self, form_id: str, include_spam: bool = False) -> List[Submission]:
        cur = self._conn.cursor()
        sql = "SELECT id, form_id, data_json, sender_ip, is_spam, created_at FROM submissions WHERE form_id = ?"
        if not include_spam:
            sql += " AND is_spam = 0"
        sql += " ORDER BY id DESC"
        cur.execute(sql, (form_id,))
        return [
            Submission(r[0], r[1], json.loads(r[2]), r[3], bool(r[4]), r[5])
            for r in cur.fetchall()
        ]

    def close(self):
        self._conn.close()
