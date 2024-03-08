import random
import time
from dbConnection import job_collection

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By



def delay():
    time.sleep(random.randint(10, 25))

# enable headless mode in Selenium
options = Options()
# options.add_argument('--headless=new')

driver = webdriver.Chrome(
    options=options,
    # other properties...
)
# visit your target site
driver.get('https://www.avito.ru/perm/vakansii')

# scraping logic...

soup = BeautifulSoup(driver.page_source, 'lxml')

jobs = soup.find_all('a', {'itemprop': 'url'})


jobs = set(jobs)

for job in jobs:
    print(job['href'])
    jobData = {"jobName": "",
                "foa": "",
                "workExp": "",
                "salary": "",
                "jobUrl": ""}


    jobUrl = 'https://www.avito.ru' + job['href']

    #######
    delay()
    jobData["jobUrl"] = jobUrl
    driver.get(jobUrl)

    soup = BeautifulSoup(driver.page_source, 'lxml')

    name = soup.find('h1', {'itemprop': 'name'})

    jobData["jobName"] = name.text

    scrapedJob = driver.find_elements(by=By.XPATH, value="//div[@data-marker='item-view/item-params']/ul/li")

    for data in scrapedJob:
        line = data.text.split(": ")
        if line[0] == "Сфера деятельности":
            jobData["foa"] = line[1]
        if line[0] == "Опыт работы":
            jobData["workExp"] = line[1]

    scrapedSalary = soup.find('div', {'data-marker': 'item-view/item-price-container'})
    jobData["salary"] = scrapedSalary.text.replace("\\xa0", "")

    job_collection.insert_one(jobData)

    ############
    delay()


# release the resources allocated by Selenium and shut down the browser
driver.quit()






# jobs = driver.find_elements(by=By.XPATH, value="//a[@itemprop='url']")
#
# for job in jobs:
#     print(job.text)
