import requests
import json

MAIN_URL = "https://www.monsterindia.com"

JSON_URL = "https://www.monsterindia.com/middleware/jobsearch?sort=1&limit=100&locations=us"
HEADERS = {
    "Host": "www.monsterindia.com",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
    "Referer": "https://www.monsterindia.com/srp/results?sort=1&limit=100&locations=us",
}


# DATA INSIDE EACH MAP
# jobId = {title, companyName, employerTypes, summary, experience,  locations, roles, qualifications, designations, jobURL, companyURL,}
JOBS = {}


def getJobs(url, headers):

    r = requests.get(url, headers=headers)
    print(r.status_code)
    jsonData = json.loads(r.text)
    jobs = jsonData["jobSearchResponse"]["data"]

    for job in jobs:
        id = job.get("jobId")
        jobData = {
            "jobId": id,
            "title": job.get("title"),
            "companyName": job.get("companyName"),
            "employerTypes": job.get("employerTypes"),
            "summary": job.get("summary"),
            "minimumExperience": job.get("minimumExperience"),
            "maximumExperience": job.get("maximumExperience"),
            "minimumSalary": job.get("minimumSalary"),
            "maximumSalary": job.get("maximumSalary"),
            "locations": job.get("locations"),
            "roles": job.get("roles"),
            "qualifications": job.get("qualifications"),
            "designations": job.get("designations"),
            "jobUrl": MAIN_URL + (job.get("seoJdUrl") or ""),
            "companyUrl": MAIN_URL + (job.get("seoCompanyUrl") or ""),
        }

        JOBS[id] = jobData


getJobs(JSON_URL, HEADERS)

with open('monsterjobs.json', 'w') as f:
    json.dump(JOBS, f)
