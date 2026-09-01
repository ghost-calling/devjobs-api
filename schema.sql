CREATE TABLE companies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    logo_url TEXT,
);

CREATE TABLE jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    companies_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    apply_url TEXT,
    remote BOOLEAN NOT NULL DEFAULT 1,
    posted_at TEXT,
    FOREIGN KEY (companies_id) REFERENCES companies(id)
);

CREATE TABLE tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE job_tags (
    job_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    PRIMARY KEY (job_id, tag_id),
    FOREIGN KEY (job_id) REFERENCES jobs(id),
    FOREIGN KEY (tag_id) REFERENCES tags(id)
);