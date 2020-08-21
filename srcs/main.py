from time import sleep

from websites.stationf import StationF
from websites.wttj import WTTJ

SLEEP_TIME = 900
WEBSITES_TO_SCRAP = [WTTJ()]


def main():
    """
    Main function of the program.
    Looping every $SLEEP_TIME seconds on the websites to scrap, and send notifications on Discord
    when a new job is found.
    """

    print("Starting Developer Job Scrapper..")

    while True:

        print("Running another iteration..")
        for website in WEBSITES_TO_SCRAP:
            print("== SCRAPING {} ===".format(website.name))
            website.scrap()
            print("SCRAP OF {} FINISHED!\n".format(website.name))
        
        sleep(SLEEP_TIME)
      


if __name__ == "__main__":
    import sys
    sys.path.append("..")
    main()
