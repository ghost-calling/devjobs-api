# devjobs-api

Dev job board aggregator — scrapes real remote job listings from RemoteOK's public 
JSON API, stores them in a normalized relational database, and serves them through 
a REST API with API-key authentication and filtering.

# Why I built this

I built this project to test my current skills by working with real job listings from a live job website and to see what I can handle and where my limitations are. I included remote jobs because remote work has become a common part of the current job market, and I wanted the project to reflect that.

## Live demo
https://devjobs-api-idwk.onrender.com

## Architecture
`scraper.py` (RemoteOK JSON) → SQLite (`database.py`, 4 normalized tables) → 
Flask REST API (`app.py`, API-key auth)

## Database design
- `companies`, `jobs`, `tags` — core entities
- `job_tags` — junction table for the many-to-many relationship between jobs and tags
- Real foreign key constraints throughout, `get_or_create_*` pattern used for companies/tags to avoid duplicate-key errors during repeated scraping

## Key technical decisions
1. ** Junction table for many-to-many tags**: a job can have any number of tags, and a tag applies to many jobs — a flat/fixed-column schema can't represent this. Solved with a standard junction table (job_tags) rather than denormalizing tags into the jobs table.

2. ** `remote` flag is derived, not provided**: RemoteOK's API doesn't include a clean boolean remote/office flag — it's inferred from the `location` field (empty or containing "remote" → remote). Stated here explicitly since it's a judgment call, not ground truth from the source data.

3. ** `INSERT OR IGNORE` for job_tags**: RemoteOK's tag data occasionally has near-duplicate entries per job; rather than pre-filtering in Python, SQLite's `INSERT OR IGNORE` cleanly handles the UNIQUE constraint at the DB level.

4. ** API-key auth via `.env`**: secret key never committed to git, loaded via python-dotenv, checked against `X-API-Key` header on every protected route.

## Endpoints
- `GET /jobs` — list all jobs, optional `?tag=<name>` and `?remote=true|false` filters
- `GET /jobs/<id>` — single job with full company + tag details

## AI-assistance disclosure
Built with Claude as a learning/pair-programming tool — I wrote and debugged all 
code myself line by line, using Claude primarily for concept explanation (e.g., 
junction tables, get-or-create patterns) and error diagnosis, not code generation.

## Known limitations
- SQLite (fine for demo; production would need Postgres for concurrent writes)
- `remote` flag is heuristic, not authoritative
- No pagination on `/jobs` yet (fine for 99 jobs, would need it at scale)

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Create a `.env` file in the project root with your own API key:
   ```
   API_KEY=your-random-secret-string
   ```
3. Initialize the database:
   ```bash
   python3 -c "from database import init_db; init_db()"
   ```
4. Run the scraper to populate it:
   ```bash
   python3 -c "from scraper import scrape_remoteok; scrape_remoteok()"
   ```
5. Start the server:
   ```bash
   python3 app.py
   ```