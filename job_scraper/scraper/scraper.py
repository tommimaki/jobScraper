from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup


def fetch_job_postings(url):
    service = Service(
        '/Users/Tommi/Downloads/chromedriver/chromedriver_mac_arm64/chromedriver')
    driver = webdriver.Chrome(service=service)

    driver.get(url)
    print('Web page loaded.')

    # Wait for the page to load and display job listings
    try:
        element_present = EC.presence_of_element_located(
            (By.CLASS_NAME, 'joblist'))
        WebDriverWait(driver, timeout=30).until(element_present)
        print('Job listings displayed.')
    except TimeoutException:
        print('Timed out waiting for page to load')

    # Wait for the job titles to load
    try:
        element_present = EC.presence_of_element_located(
            (By.CLASS_NAME, 'job-title'))
        WebDriverWait(driver, timeout=30).until(element_present)
        print('Job titles loaded.')
    except TimeoutException:
        print('Timed out waiting for job titles to load')

    # Extract job titles from the page
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    job_postings = []

    for job in soup.find_all('div', {'class': 'job-ad-list-item-wrapper'}):
        title_tag = job.find('span', {'class': 'text-clamped title'})
        title = title_tag.text.strip()

        link_tag = job.find('a', {'class': 'job-ad-list-item-link'})
        link = 'https://tyopaikat.oikotie.fi' + link_tag['href']
        job_postings.append({'title': title, 'link': link})

    driver.quit()
    print('Scraping complete.')
    return job_postings


url = "https://tyopaikat.oikotie.fi/tyopaikat/suomi/it-tech"
job_postings = fetch_job_postings(url)
print(job_postings)
