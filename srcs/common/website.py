from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep

from common.constants import CHROMEDRIVER_PATH, GOOGLE_CHROME_BIN


class Website:

    def __init__(self, name, url):
        self.name = name
        self.url = url


    def _get_chrome_page_data(self, url):
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
        for _ in range(100):
            driver.execute_script("window.scrollTo(0, window.scrollY + 200)")
            sleep(0.1)
        driver.implicitly_wait(3)
        page_data = driver.page_source
        driver.quit()
        return page_data


    def scrap(self):
        print("Scrap function is not implemented in website '{}'!".format(self.name))
