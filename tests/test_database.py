import os
import pytest
from database import init_db, get_or_create_company, get_or_create_tag, insert_job, insert_job_tag, get_job_with_details, get_filtered_jobs

TEST_DB = "data/test_jobs.db"

@pytest.fixture
def setup_db(monkeypatch):
    import database
    monkeypatch.setattr(database, "DB_PATH", TEST_DB)
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    init_db()
    yield
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

def test_get_or_create_company_no_duplicate(setup_db):
    id1 = get_or_create_company("TestCo", "", "", "")
    id2 = get_or_create_company("TestCo", "", "", "")
    assert id1 == id2

def test_get_or_create_tag_no_duplicate(setup_db):
    id1 = get_or_create_tag("python")
    id2 = get_or_create_tag("python")
    assert id1 == id2

def test_insert_job_and_get_details(setup_db):
    company_id = get_or_create_company("TestCo", "", "", "")
    job_id = insert_job({
        "title": "Backend Dev", "description": "test", "company_id": company_id,
        "location": "", "posted_date": "2026-01-01", "apply_url": "http://test.com", "remote": True
    })
    tag_id = get_or_create_tag("python")
    insert_job_tag(job_id, tag_id)

    result = get_job_with_details(job_id)
    assert len(result) == 1
    assert result[0]["title"] == "Backend Dev"
    assert result[0]["company_name"] == "TestCo"
    assert "python" in result[0]["tags"]

def test_get_filtered_jobs_by_tag(setup_db):
    company_id = get_or_create_company("TestCo", "", "", "")
    job_id = insert_job({
        "title": "Backend Dev", "description": "test", "company_id": company_id,
        "location": "", "posted_date": "2026-01-01", "apply_url": "http://test.com", "remote": True
    })
    tag_id = get_or_create_tag("python")
    insert_job_tag(job_id, tag_id)

    results = get_filtered_jobs(tag="python")
    assert len(results) == 1

    results_none = get_filtered_jobs(tag="nonexistent")
    assert len(results_none) == 0