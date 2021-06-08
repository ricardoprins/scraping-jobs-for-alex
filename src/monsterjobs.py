import requests
import json
from time import sleep
from random import randint

MAIN_URL = "https://www.monsterindia.com"

START = 0

JSON_URL = "https://www.monsterindia.com/middleware/jobsearch?sort=1&limit=100&{0}locations=us"
HEADERS = {
    "Host": "www.monsterindia.com",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
    "Referer": "https://www.monsterindia.com/srp/results?{0}sort=1&limit=100&locations=us",
}


# DATA INSIDE EACH MAP
# jobId = {title, companyName, employerTypes, summary, experience,  locations, roles, qualifications, designations, jobURL, companyURL,}
JOBS = {}


def getJobs(url: str, headers: HEADERS):
    global START

    # This statement is just to mimic browsers Referrer header
    if START < 0:
        headers["Referer"] = headers["Referer"].format("")
        url = url.format("")
    else:
        headers["Referer"] = headers["Referer"].format(f"start={START}&")
        url = url.format(f"start={START}&")

    r = requests.get(url, headers=headers)
    jsonData = json.loads(r.text)
    jobs = jsonData["jobSearchResponse"]["data"]

    if len(jobs) == 0:
        return

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

    START += 100

    with open('monsterjobs.json', 'w') as f:
        json.dump(JOBS, f)

    print(f"Number of jobs Scraped {len(JOBS)}")

    sleep(randint(1, 5))

    getJobs(JSON_URL, HEADERS)


getJobs(JSON_URL, HEADERS)
print("All Jobs Are Scraped!!!")
