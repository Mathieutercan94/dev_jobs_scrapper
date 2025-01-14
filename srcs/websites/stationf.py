import time
import re
from bs4 import BeautifulSoup

from common.webhook import create_embed, send_embed
from common.database import is_url_in_database, add_url_in_database
from common.website import Website


class StationF(Website):

    def __init__(self):
        super().__init__(
        'Station F',
        'https://jobs.stationf.co/search?query=dev{}&departments%5B0%5D=Tech&departments%5B1%5D=Tech%20%26%20Dev&departments%5B2%5D=Tech%2FDev&departments%5B3%5D=Dev&contract_types%5B0%5D=Full-Time&contract_types%5B1%5D=Freelance&contract_types%5B2%5D=Temporary',
        'STATION F JOBS',
        'https://mbem.fr/wp-content/uploads/2018/06/station-f-logo-copie.png',
        False
        )


    def scrap(self):

        page = 1

        while True:

            print("Looking for another Station F\'s page..")
            print('test')
            self.page_url = self.url.format(
                '&page={}'.format(page) if page != 1 else '')
            self._init_driver(self.page_url)
            page_data = self._get_chrome_page_data()
            page_soup = BeautifulSoup(page_data, 'html.parser')
            all_jobs_raw = page_soup.find_all(
                'li', attrs={'class': 'ais-Hits-item'})

            if len(all_jobs_raw) == 0 or page >= 2:  # Scrap finished
                return

            print("\nStation F\'s found jobs ({}) :".format(len(all_jobs_raw)))
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
                    embed = create_embed(
                        job_name, job_company, job_location, job_link, job_thumbnail)
                    send_embed(embed, self)
                    time.sleep(4)

            print('Station F\'s page #{} finished'.format(page))
            page += 1
