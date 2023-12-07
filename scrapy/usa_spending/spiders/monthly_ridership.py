import os
from .utils import create_empty_directory, all_existing_files

cd = os.getcwd()
md = cd



import scrapy
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import os

# Get the current directory
from .upload_redivis import create_dataset, create_table, filename_to_table_name, upload_file, upload_xlsx

# from upload_redivis import create_dataset

current_directory = os.getcwd()
URL = 'https://www.transit.dot.gov/ntd/data-product/monthly-module-adjusted-data-release'


# Transit ridership time series
class EpaEnvironSpider(scrapy.Spider):
    name = "monthly_ridership"
    allowed_domains = ["enviro.epa.gov"]
    start_urls = [URL]
    download_folder = f"{current_directory}/monthly_ridership/"

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
                time.sleep(20)
        print("Downloaded File " + str(downloaded_file))
        downloaded_file = downloaded_file.pop()
        print(downloaded_file)
        upload_xlsx(self.download_folder + downloaded_file, self.name)

# browser

# time.sleep(25)
'''
while True:
    time.sleep(3000)

if __name__ == '__main__':
    pass
'''
