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

def insert_company(company_data: dict):
    with get_db() as conn:
        conn.execute("""
            INSERT INTO companies (name , description, website, logo_url)
            VALUES (?, ?, ?, ?)
            """,(
                company_data["name"], 
                company_data["description"],
                company_data["website"],
                company_data["logo_url"]
            ))
        conn.commit()

def insert_job(job_data: dict):
    with get_db() as conn:
        conn.execute("""
            INSERT INTO jobs (title, description, company_id, location, posted_date)
            VALUES (?, ?, ?, ?, ?)
            """,(          
                job_data["title"],
                job_data["description"],
                job_data["company_id"],
                job_data["location"],
                job_data["posted_date"]
            ))
        conn.commit()

def insert_tag(tag_name: str):
    with get_db() as conn:
        conn.execute("""
            INSERT INTO tags (name)
            VALUES (?)
        """, (tag_name,))
        conn.commit()

def insert_job_tag(job_id: int, tag_id: int):
    with get_db() as conn:
        conn.execute("""
            INSERT INTO job_tags (job_id, tag_id)
            VALUES (?, ?)
        """, (job_id, tag_id))
        conn.commit()

def get_job_with_details(job_id: int):
    with get_db() as conn:
            job_row = conn.execute("""
                SELECT jobs.*, companies.name AS company_name, companies.description AS company_description,
                companies.website AS company_website, companies.logo_url AS company_logo_url, GROUP_CONCAT(tags.name) AS tags
                FROM jobs JOIN companies ON jobs.company_id = companies.id
                JOIN job_tags ON job_tags.job_id = jobs.id
                JOIN tags ON tags.id = job_tags.tag_id
                WHERE jobs.id = ?
                GROUP BY jobs.id, companies.name, companies.description, companies.website, companies.logo_url
            """, (job_id,)).fetchall()
            return [dict(row) for row in job_row]