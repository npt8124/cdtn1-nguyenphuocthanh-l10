
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path("data/warranty.sqlite3")


@contextmanager
def connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row

    try:
        yield con
        con.commit()
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()


def initialize():
    with connect() as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                suggested_label TEXT NOT NULL,
                final_label TEXT NOT NULL,
                suggested_priority TEXT NOT NULL,
                final_priority TEXT NOT NULL,
                confidence REAL,
                created_at TEXT NOT NULL
            )
        """)

        con.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                request_id INTEGER NOT NULL,
                action TEXT NOT NULL,
                field TEXT NOT NULL,
                old_value TEXT,
                new_value TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY(request_id) REFERENCES requests(id)
            )
        """)


def save_request(
    description,
    result,
    suggested_priority,
    final_label,
    final_priority,
):
    now = datetime.now(timezone.utc).isoformat(
        timespec="seconds"
    )

    with connect() as con:
        cursor = con.execute(
            """
            INSERT INTO requests (
                description, suggested_label, final_label,
                suggested_priority, final_priority,
                confidence, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                description,
                result["label"],
                final_label,
                suggested_priority,
                final_priority,
                result.get("confidence"),
                now,
            ),
        )

        request_id = cursor.lastrowid

        events = [
            ("CONFIRM", "status", None, "CONFIRMED")
        ]

        if result["label"] != final_label:
            events.append(
                (
                    "ADJUST",
                    "label",
                    result["label"],
                    final_label,
                )
            )

        if suggested_priority != final_priority:
            events.append(
                (
                    "ADJUST",
                    "priority",
                    suggested_priority,
                    final_priority,
                )
            )

        con.executemany(
            """
            INSERT INTO history (
                request_id, action, field,
                old_value, new_value, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            [
                (request_id, *event, now)
                for event in events
            ],
        )

    return request_id


def list_requests():
    with connect() as con:
        return [
            dict(row)
            for row in con.execute(
                "SELECT * FROM requests ORDER BY id DESC"
            )
        ]


def list_history():
    with connect() as con:
        return [
            dict(row)
            for row in con.execute(
                "SELECT * FROM history ORDER BY id DESC"
            )
        ]
