import sqlite3
from contextlib import contextmanager
import os

DB_PATH = "data/jobs.db"
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    with get_db() as conn:
        conn.executescript("""
            
            CREATE TABLE IF NOT EXISTS companies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                description TEXT,
                website TEXT,
                logo_url TEXT);
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                description TEXT,
                company_id INTEGER,
                location TEXT,
                posted_date TEXT,
                FOREIGN KEY (company_id) REFERENCES companies(id));
            CREATE TABLE IF NOT EXISTS tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE
            );
            CREATE TABLE IF NOT EXISTS job_tags (
                job_id INTEGER,
                tag_id INTEGER,
                PRIMARY KEY (job_id, tag_id),
                FOREIGN KEY (job_id) REFERENCES jobs(id),
                FOREIGN KEY (tag_id) REFERENCES tags(id))
                  
        """)
        conn.commit()

# def insert_job(job_data: dict):
#     with get_db() as conn:
#         conn.execute("""
#             INSERT INTO matches (team1, team2, team1_score, team2_score, venue, match_date, result, key_stats)
#             VALUES (?, ?, ?, ?, ?, ?, ?, ?)
#         """, (
#             match_data["team1"], match_data["team2"],
#             match_data["team1_score"], match_data["team2_score"],
#             match_data["venue"], match_data["match_date"],
#             match_data["result"], match_data["key_stats"]
#         ))
#         conn.commit()

# def get_match(match_id: int):
#     with get_db() as conn:
#         row = conn.execute("SELECT * FROM matches WHERE id = ?", (match_id,)).fetchone()
#         return dict(row) if row else None