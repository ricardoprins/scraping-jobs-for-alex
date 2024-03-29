import json
import requests
import bs4
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from requests.exceptions import RequestException

BASE_URL = "https://jobs.ksl.com/search/posted/last-7-days"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
}

KEYWORDS = ['software', 'developer', 'software engineer', 'programmer', 'data scientist', 'machine learning']

class JobScraper:
    def __init__(self, base_url, headers):
        self.base_url = base_url
        self.headers = headers
        self.session = requests.Session()
        self.jobs = {}
        self.keywords = KEYWORDS;

    def get_job_descriptions(self, url):
        try:
            data = self.session.get(url=url, headers=self.headers, timeout=20)
            soup = BeautifulSoup(data.text, "html.parser")

            description_tag = soup.find_all("meta", {"property": "og:description"})

            description = description_tag[0]["content"]
            self.jobs[url]["description"] = description
        except RequestException as e:
            print(f"Error during requests to {url} : {str(e)}")

    def write_to_file(self):
        with open("sample.json", "w") as outfile:
            json.dump(self.jobs, outfile)

    def get_job_listings(self, url):
        try:
            data = self.session.get(url=url, headers=self.headers, timeout=20)
            soup = BeautifulSoup(data.text, "html.parser")

            script = soup.find_all('script', {'type': 'application/ld+json'})
            content = script[0].contents[0]

            jobs_array = json.loads(content)["itemListElement"]
            with ThreadPoolExecutor(max_workers=5) as executor:
                for job in jobs_array:
                    # Check if any of the keywords is in the job title
                    if any(keyword.lower() in job["title"].lower() for keyword in self.keywords):
                        self.jobs[job["url"]] = {
                            "name": job["title"],
                            "employer": job["hiringOrganization"]["name"],
                            "url": job["url"],
                        }
                        executor.submit(self.get_job_descriptions, job["url"])

            print(f"Number of jobs Scraped {len(self.jobs)}")

            self.write_to_file()

            next_page = soup.find("a", {"class": "next link"})

            if next_page is not None and isinstance(next_page, bs4.Tag):
                self.get_job_listings(next_page.get("href"))
        except RequestException as e:
            print(f"Error during requests to {url} : {str(e)}")


if __name__ == "__main__":
    scraper = JobScraper(BASE_URL, HEADERS)
    scraper.get_job_listings(BASE_URL)
