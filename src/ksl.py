import time
import json
import requests
import urllib3
from random import randint
from bs4 import BeautifulSoup


urllib3.disable_warnings()
BASE_URL = "https://jobs.ksl.com/search/posted/last-7-days"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
}
JOBS = {}


def getJobListings(url, headers):
    MAIN_URL = "https://jobs.ksl.com"
    dataX = requests.get(url=url, headers=headers, verify=False, timeout=20)
    soup = BeautifulSoup(dataX.text, "html.parser")
    dataX.close()

    script = soup.find_all('script', {'type': 'application/ld+json'})
    content = script[0].contents[0]

    jobsArray = json.loads(content)["itemListElement"]

    for job in jobsArray:
        JOBS[job["url"]] = {
            "name": job["title"],
            "employer": job["hiringOrganization"]["name"],
            "url": job["url"],
            "description": job["description"]
        }

    print(f"Number of jobs Scraped {len(JOBS)}")

    time.sleep(randint(1, 15))
    next_page = soup.find("a", {"class": "next link"})

    if next_page is not None:
        getJobListings(next_page.get("href"), HEADERS)


getJobListings(BASE_URL, HEADERS)

with open("sample.json", "w") as outfile:
    json.dump(JOBS, outfile)
