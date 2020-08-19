from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import webhook
import re

from database import is_url_in_database, add_url_in_database
from constants import CHROMEDRIVER_PATH, GOOGLE_CHROME_BIN

def _get_chrome_page_data(url):
    """
    Open the given url and returns the data on the page.
    """

    options = Options()
    options.headless = True
    options.binary_location = GOOGLE_CHROME_BIN
    options.add_argument("--window-size=1920,1200")
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(
        options=options, executable_path=CHROMEDRIVER_PATH)
    driver.get(url)
    driver.implicitly_wait(3)
    page_data = driver.page_source
    driver.quit()
    return page_data


def main():
    """
    Main function of the program.
    Looping every hours on the website to scrap, and send notifications on Discord.
    """

    print("Starting Station F Jobs Scrapper..")

    page = 1

    while True:

        print("Running another iteration..")

        url = 'https://jobs.stationf.co/search?query=dev{}&departments%5B0%5D=Tech&departments%5B1%5D=Tech%20%26%20Dev&departments%5B2%5D=Tech%2FDev&departments%5B3%5D=Dev&contract_types%5B0%5D=Full-Time&contract_types%5B1%5D=Freelance&contract_types%5B2%5D=Temporary'.format(
            '&page={}'.format(page) if page != 1 else '')

        page_data = _get_chrome_page_data(url)

        page_soup = BeautifulSoup(page_data, 'html.parser')
        all_jobs_raw = page_soup.find_all(
            'li', attrs={'class': 'ais-Hits-item'})

        if len(all_jobs_raw) == 0:
            print('0 jobs on page {}, restarting from page 1'.format(page))
            page = 1
            sleep(900)
            continue

        print("\nFound jobs ({}) :".format(len(all_jobs_raw)))
        for jobs in all_jobs_raw:
            job_name = jobs.find(
                'h4', attrs={'class': 'job-title'}).text.strip()
            print('Job : ' + job_name)

            job_company = jobs.find(
                'li', attrs={'class': 'job-company'}).text.strip()
            print('Company : ' + job_company)

            job_location = jobs.find(
                'li', attrs={'class': 'job-office'}).text.strip()
            print('Location : ' + job_location)

            job_link = 'https://jobs.stationf.co' + jobs.find(
                'a', attrs={'class': 'jobs-item-link'}, href=True)['href']
            print(job_link)

            job_thumbnail = re.search("(?P<url>https?://[^\s]+)", jobs.find(
                'div', attrs={'class': 'company-logo'})['style']).group("url")[:-2]
            print(job_thumbnail)
            print('\n')

            if not is_url_in_database(job_link):
                add_url_in_database(job_link)
                embed = webhook.create_embed(
                    job_name, job_company, job_location, job_link, job_thumbnail)
                webhook.send_embed(embed)
                sleep(4)

        print('Page #{} finished'.format(page))
        page += 1


if __name__ == "__main__":
    main()
