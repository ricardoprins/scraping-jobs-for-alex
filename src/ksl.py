import time
import json
import requests
import urllib3
from random import randint
from bs4 import BeautifulSoup
from threading import Thread

urllib3.disable_warnings()
BASE_URL = "https://jobs.ksl.com/search/posted/last-7-days"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
}
JOBS = {}


def getJobDescriptions(url, headers):

    data = requests.get(url=url, headers=headers, verify=False, timeout=20)
    data.close()
    soup = BeautifulSoup(data.text, "html.parser")

    descriptionTag = soup.find_all(
        "meta", {"property": "og:description"}, "html.parser"
    )

    description = descriptionTag[0]["content"]
    JOBS[url]["description"] = description


def writeToFile():
    global JOBS
    with open("sample.json", "w") as outfile:
        json.dump(JOBS, outfile)


def getJobListings(url, headers):
    dataX = requests.get(url=url, headers=headers, verify=False, timeout=20)
    soup = BeautifulSoup(dataX.text, "html.parser")
    dataX.close()

    script = soup.find_all('script', {'type': 'application/ld+json'})
    content = script[0].contents[0]

    jobsArray = json.loads(content)["itemListElement"]
    threads = []
    for job in jobsArray:
        JOBS[job["url"]] = {
            "name": job["title"],
            "employer": job["hiringOrganization"]["name"],
            "url": job["url"],
        }
        t = Thread(target=getJobDescriptions, args=(job["url"], headers))
        threads.append(t)

    for i in threads:
        i.start()

    # Making sure all the jobs description is fetched
    for i in threads:
        i.join()

    print(f"Number of jobs Scraped {len(JOBS)}")

    writeToFile()

    next_page = soup.find("a", {"class": "next link"})

    if next_page is not None:
        getJobListings(next_page.get("href"), HEADERS)


getJobListings(BASE_URL, HEADERS)
