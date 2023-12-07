import os
import time
import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By

# Define the URL to scrape
from .upload_redivis import upload_xlsx
from .utils import create_empty_directory, all_existing_files

current_directory = os.getcwd()

URL = 'https://www.transit.dot.gov/ntd/data-product/ts11-total-funding-time-series-2'

# Transit funding time series
class TotalFundingSpider(scrapy.Spider):
    name = "total_funding"
    allowed_domains = ["transit.dot.gov"]
    start_urls = [URL]
    download_folder = f"{current_directory}/total_funding/"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        options = webdriver.ChromeOptions()
        create_empty_directory(self.download_folder)
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        options.add_argument(f'user-agent={user_agent}')
        options.add_experimental_option("prefs", {"download.default_directory": self.download_folder})
        options.add_argument("--headless")
        self.files_before_running = all_existing_files(self.download_folder)

        self.driver = webdriver.Chrome(options=options)
        # self.driver = webdriver.Chrome()

    def parse(self, response):
        self.driver.get(response.url)
        driver = self.driver
        driver.get(URL)
        driver.find_element(By.XPATH, "//div[@id='block-fta-content']/div/article/div/div/span/a").click()
        while True:
            downloaded_file = all_existing_files(self.download_folder) - self.files_before_running
            if len(downloaded_file) > 0:
                break
            else:
                print('Waiting for file to be downloaded')
                time.sleep(30)
        print("Downloaded File " + str(downloaded_file))
        downloaded_file = downloaded_file.pop()
        print(downloaded_file)
        upload_xlsx(self.download_folder + downloaded_file, self.name)

    # def all_existing_files(self, extension='.csv'):
    #     files = [file for file in os.listdir('.') if file.endswith(extension)]
    #     return set(files)
    # Implement the create_dataset, create_table, and upload_file functions here
    # You should provide the implementations or import them from your project


# Main entry point
if __name__ == '__main__':
    # You can start the spider here if needed
    pass
