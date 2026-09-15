from flask import Flask, request, jsonify
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
@app.route("/jobs")
def get_jobs():
    if not check_api_key():
        return jsonify({"error": "Invalid or missing API key"}), 401
    from database import get_all_jobs
    jobs = get_all_jobs()
    return jsonify(jobs)
if __name__ == "__main__":
    app.run(debug=True)