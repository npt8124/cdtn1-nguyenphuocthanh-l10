import sqlite3
from pathlib import Path

DB_PATH = Path("data/warranty.db")

def connect(path=DB_PATH):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path), timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db(path=DB_PATH):
    with connect(path) as con:
        con.executescript("""
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            issue_desc TEXT NOT NULL,
            predicted_category TEXT,
            confidence REAL,
            suggested_priority TEXT,
            final_category TEXT NOT NULL,
            final_priority TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        );
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            request_id INTEGER NOT NULL REFERENCES requests(id),
            field_name TEXT NOT NULL,
            old_value TEXT,
            new_value TEXT,
            changed_at TEXT NOT NULL DEFAULT (datetime('now'))
        );
        """)

def save_request(description, prediction, suggested_priority, final_category, final_priority, path=DB_PATH):
    from src.data.load import LABELS
    from src.rules import PRIORITIES
    if len(description.strip()) < 3 or final_category not in LABELS or final_priority not in PRIORITIES:
        raise ValueError("Thông tin xác nhận không hợp lệ")
    with connect(path) as con:
        cur = con.execute("""INSERT INTO requests
            (issue_desc, predicted_category, confidence, suggested_priority, final_category, final_priority)
            VALUES (?, ?, ?, ?, ?, ?)""", (description.strip(), prediction["label"],
            prediction["confidence"], suggested_priority, final_category, final_priority))
        request_id = cur.lastrowid
        for field, old, new in (("issue_category", prediction["label"], final_category),
                                ("priority", suggested_priority, final_priority)):
            if old != new:
                con.execute("INSERT INTO history (request_id, field_name, old_value, new_value) VALUES (?, ?, ?, ?)",
                            (request_id, field, old, new))
    return request_id

def list_requests(path=DB_PATH):
    with connect(path) as con:
        return [dict(row) for row in con.execute("SELECT * FROM requests ORDER BY id DESC")]

def list_history(path=DB_PATH):
    with connect(path) as con:
        return [dict(row) for row in con.execute("SELECT * FROM history ORDER BY id DESC")]
