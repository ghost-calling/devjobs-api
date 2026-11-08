from flask import Flask, request, jsonify
from database import get_job_with_details, get_filtered_jobs, init_db
from scraper import scrape_remoteok
from dotenv import load_dotenv
import os

load_dotenv()  # reads .env file, makes its values available via os.environ

app = Flask(__name__)
API_KEY = os.environ.get("API_KEY")


def check_api_key():
    # If the server has no key configured, nobody can authenticate.
    if not API_KEY:
        return False
    return request.headers.get("X-API-KEY") == API_KEY


@app.route("/")
def home():
    return """
    <html>
      <head><title>DevJobs API</title></head>
      <body style="font-family: sans-serif; max-width: 600px; margin: 60px auto;">
        <h1>DevJobs API</h1>
        <p>A REST API serving real remote developer jobs, scraped from RemoteOK
        into a normalized SQLite database (Flask, SQL, pytest).</p>
        <ul>
          <li><a href="/demo">/demo</a> - live sample: 5 jobs, no API key needed</li>
          <li><code>/jobs</code> and <code>/jobs/&lt;id&gt;</code> - full API, requires
              an <code>X-API-KEY</code> header; filters: <code>?tag=python&amp;remote=true</code></li>
          <li><a href="https://github.com/ghost-calling/devjobs-api">Source code and README</a></li>
        </ul>
        <p><small>Hosted on a free tier: the first load after idle can take up to a minute.</small></p>
      </body>
    </html>
    """


@app.route("/demo")
def demo():
    jobs = get_filtered_jobs(tag=None, remote=None)
    return jsonify(jobs[:5])


@app.route("/jobs/<int:job_id>")
def get_job(job_id):
    if not check_api_key():
        return jsonify({"error": "Invalid or missing API key"}), 401

    job = get_job_with_details(job_id)

    if not job:
        return jsonify({"error": "Job Not Found"}), 404

    return jsonify(job[0])


@app.route("/jobs")
def get_jobs():
    if not check_api_key():
        return jsonify({"error": "Invalid or missing API key"}), 401

    tag = request.args.get("tag")
    remote_param = request.args.get("remote")
    remote = None
    if remote_param is not None:
        if remote_param.lower() == "true":
            remote = True
        elif remote_param.lower() == "false":
            remote = False
        else:
            return jsonify({"error": "Invalid value for 'remote' parameter. Use 'true' or 'false'."}), 400

    jobs = get_filtered_jobs(tag=tag, remote=remote)
    return jsonify(jobs)


if __name__ == "__main__":
    init_db()
    scrape_remoteok()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)