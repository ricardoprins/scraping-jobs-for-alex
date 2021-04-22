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
names = []
urls = []
employers = []
descriptions = []


def getJobListings(url, headers):
    MAIN_URL = "https://jobs.ksl.com"
    dataX = requests.get(url=url, headers=headers, verify=False, timeout=20)
    soup = BeautifulSoup(dataX.text, "html.parser")

    for title in soup.find_all("h2", {"class": "job-title"}):
        anchor = title.find("a")
        names.append(anchor.text.strip())
        urls.append(anchor.get("href"))

    for employer in soup.find_all("span", {"class": "company-name"}):
        employers.append(employer.text.strip())

    for url in urls:
        newLink = MAIN_URL + url
        getJobDescriptions(newLink, HEADERS)
        time.sleep(randint(1, 15))

    if (
        len(names) == len(urls)
        and len(urls) == len(employers)
        and len(employers) == len(descriptions)
    ):
        for i in range(len(names)):
            job = {
                "name": names[i],
                "employer": employers[i],
                "url": urls[i],
                "description": descriptions[i],
            }
            JOBS[urls[i]] = job

    time.sleep(randint(1, 15))
    next_page = soup.find("a", {"class": "next link"})

    if next_page is not None:
        getJobListings(next_page.get("href"), HEADERS)

    dataX.close()


def getJobDescriptions(url, headers):
    data = requests.get(url=url, headers=headers, verify=False, timeout=20)
    soup = BeautifulSoup(data.text, "html.parser")

    for description in soup.find_all(
        "meta", {"property": "og:description"}, "html.parser"
    ):
        descriptions.append(description.text.strip())
    data.close()


getJobListings(BASE_URL, HEADERS)

with open("sample.json", "w") as outfile:
    json.dump(JOBS, outfile)
