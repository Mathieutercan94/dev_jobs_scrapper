import time
import re
from bs4 import BeautifulSoup

import common.webhook
from common.database import is_url_in_database, add_url_in_database
from common.website import Website


class WTTJ(Website):

    def __init__(self):
        self.name = 'Welcome to the Jungle'
        self.url = 'https://www.welcometothejungle.com/fr/jobs?page={}&refinementList%5Bprofession_name.fr.Tech%5D%5B%5D=Dev+Fullstack&refinementList%5Bprofession_name.fr.Tech%5D%5B%5D=Dev+Backend&refinementList%5Bprofession_name.fr.Tech%5D%5B%5D=Dev+Frontend&refinementList%5Bprofession_name.fr.Tech%5D%5B%5D=Dev+Mobile&refinementList%5Bcontract_type_names.fr%5D%5B%5D=CDI&refinementList%5Bcontract_type_names.fr%5D%5B%5D=CDD+%2F+Temporaire&refinementList%5Bcontract_type_names.fr%5D%5B%5D=Freelance&aroundQuery=Paris%2C+France&aroundLatLng=48.85718%2C2.34141&aroundRadius=10000&sortBy=mostRecent'

    def scrap(self):

        page = 1

        while True:

            print("Looking for another WTTJ\'s page..")

            page_url = self.url.format(page)

            page_data = self._get_chrome_page_data(page_url)
            page_soup = BeautifulSoup(page_data, 'html.parser')
            all_jobs_raw = page_soup.find_all(
                'article', attrs={'data-role': 'jobs:thumb'})

            if len(all_jobs_raw) == 0:  # Scrap finished
                return

            print("\nWTTJ\'s found jobs ({}) :".format(len(all_jobs_raw)))
            for jobs in all_jobs_raw:
                job_company = jobs.find('h4').find(
                    'span', attrs={'class': 'ais-Highlight-nonHighlighted'}).text
                job_name = jobs.find('h3').find(
                    'span', attrs={'class': 'ais-Highlight-nonHighlighted'}).text
                job_thumbnail = jobs.find(
                    'img', attrs={'alt': job_company})['src']
                job_link = 'https://welcometothejungle.com' + \
                    jobs.find('a', href=True)['href']

                print('Job : ' + job_name)
                print('Company : ' + job_company)
                print(job_link)
                print('\n')

                if not is_url_in_database(job_link):
                    print("Found new job: {}".format(job_link))
                    add_url_in_database(job_link)
                    embed = webhook.create_embed(
                        job_name, job_company, 'Paris', job_link, job_thumbnail)
                    webhook.send_embed(embed)
                    time.sleep(4)

            print('WTTJ\'s page #{} finished'.format(page))
            page += 1
