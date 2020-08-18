from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import webhook
import re

from database import is_url_in_database, add_url_in_database


URL = 'https://jobs.stationf.co/search?query=dev&page=1&departments%5B0%5D=Tech&departments%5B1%5D=Tech%20%26%20Dev&departments%5B2%5D=Tech%2FDev&departments%5B3%5D=Dev&contract_types%5B0%5D=Full-Time&contract_types%5B1%5D=Freelance&contract_types%5B2%5D=Temporary'


def _get_chrome_page_data():
	options = Options()
	options.headless = True
	options.add_argument("--window-size=1920,1200")

	driver = webdriver.Chrome(
		options=options, executable_path='/usr/local/bin/chromedriver')
	driver.get(URL)
	page_data = driver.page_source
	driver.quit()
	return page_data


def main():
	print("Starting Station F Jobs Scrapper..")

	page_data = _get_chrome_page_data()

	page_soup = BeautifulSoup(page_data, 'html.parser')
	all_jobs_raw = page_soup.find_all('li', attrs={'class': 'ais-Hits-item'})

	print("\nFound jobs ({}) :".format(len(all_jobs_raw)))
	for jobs in all_jobs_raw:
		job_name = jobs.find('h4', attrs={'class': 'job-title'}).text.strip()
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


if __name__ == "__main__":
	main()
