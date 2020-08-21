import time
import re
from bs4 import BeautifulSoup

from common.webhook import create_embed, send_embed
from common.database import is_url_in_database, add_url_in_database
from common.website import Website


class JobTeaser(Website):

    def __init__(self):
        self.name = 'Job Teaser'
        self.url = 'https://www.jobteaser.com/fr/job-offers?p={}&contract=cdd,cdi&position_category_uuid=ddc0460c-ce0b-4d98-bc5d-d8829ff9cf11&location=France%3A%3A%C3%8Ele-de-France..%C3%8Ele-de-France%20(France)&locale=en,fr'
        self.discord_username = 'JOB TEASER JOBS'
        self.discord_avatar_url = 'https://d1guu6n8gz71j.cloudfront.net/system/asset/logos/27460/logo_mobile.png'
        self.should_scroll_page = False

    def scrap(self):

        page = 0

        while True:

            print("Looking for another Job Teaser\'s page..")

            page_url = self.url.format(page)

            page_data = self._get_chrome_page_data(page_url)
            page_soup = BeautifulSoup(page_data, 'html.parser')
            all_jobs_raw = page_soup.find_all(
                'a', attrs={'href': re.compile('^\/en\/job-offers\/.*')})

            if len(all_jobs_raw) == 0:  # Scrap finished
                return

            print("\nJob Teaser\'s found jobs ({}) :".format(len(all_jobs_raw)))
            for jobs in all_jobs_raw:
                job_company = jobs.find('p').text
                print('Company : ' + job_company)
                job_name = jobs.find('h1').text
                print('Job : ' + job_name)
                job_thumbnail = jobs.find(
                    'img', attrs={'alt': job_company})['src']
                job_link = 'https://www.jobteaser.com' + jobs['href']
                print('\n')

                if not is_url_in_database(job_link):
                    print("Found new job: {}".format(job_link))
                    add_url_in_database(job_link)
                    embed = create_embed(
                        job_name, job_company, 'Paris', job_link, job_thumbnail)
                    send_embed(embed, self)
                    time.sleep(4)

            print('Job Teaser\'s page #{} finished'.format(page))
            page += 1
