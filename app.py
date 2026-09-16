from flask import Flask, request, jsonify
from database import get_all_jobs, get_filtered_jobs, get_job_with_details
from database import get_all_jobs
from dotenv import load_dotenv
import os

load_dotenv()  # reads .env file, makes its values available via os.environ

app = Flask(__name__)
API_KEY = os.environ.get("API_KEY")
def check_api_key():
    key = request.headers.get("X-API-KEY")
    if key == API_KEY:
        return True
    else:
        return False 
       
@app.route("/jobs/<int:job_id>")
def get_job(job_id):
    # your turn
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
            return jsonify({"error": "Invalid value for 'remote' parameter. Use 'true' or 'false',"}), 400

    jobs = get_filtered_jobs(tag=tag, remote=remote)
    return jsonify(jobs)
if __name__ == "__main__":
    app.run(debug=True)