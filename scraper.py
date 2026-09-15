import requests
from database import get_or_create_company, insert_job, get_or_create_tag, insert_job_tag

def scrape_remoteok():
    url = "https://remoteok.com/api"
    headers = {"User-Agent": "Mozilla/5.0"}  # RemoteOK blocks requests with no User-Agent
    response = requests.get(url, headers=headers)
    jobs_data = response.json()

    jobs_data = jobs_data[1:]  # skip index 0, the legal notice

    for job in jobs_data:
        # YOUR TURN: fill in the 3 steps we outlined:
        # 1. company_id = get_or_create_company(...)
        # 2. job_id = insert_job({...})
        # 3. loop over job["tags"], get_or_create_tag + insert_job_tag for each
        company_id = get_or_create_company(
            name = job.get("company", ""), 
            description = "",
            website = "",
            logo_url = job.get("company_logo","")
        )
        job_id = insert_job({
            "company_id": company_id,
            "title": job.get("position", ""),
            "description": job.get("description", ""),
            "location": job.get("location", ""),
            "apply_url": job.get("apply_url", ""),
            "posted_date": job.get("date", "")
        })
        for tag in job.get("tags",[]):
            tag_id = get_or_create_tag(tag)
            insert_job_tag(job_id, tag_id)
    print(f"Scraped {len(jobs_data)} jobs")