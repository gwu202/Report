import scrapy
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import os

# Get the current directory
from .upload_redivis import create_dataset, create_table, filename_to_table_name, upload_file

from .utils import create_empty_directory, all_existing_files

current_directory = os.getcwd()
parent_directory = current_directory

URL = "https://enviro.epa.gov/enviro/P2_EF_Query.master_build_sql?FacOrParent=1&Industry_Search=null&Industry_Search=311&Chemical_Search=null&Year_Search=null&State_Search=null&pZipCity=&database_type=TRI&results2_length=10&page_no=1&pRepOption=1"

# List of Facilities in TRI submitting Pollution Prevention Information for Selected Criteria:#

class EpaEnvironSpider(scrapy.Spider):
    name = "epa_environ"
    allowed_domains = ["enviro.epa.gov"]
    start_urls = [URL]
    download_folder = f"{current_directory}/epa_environ/"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        create_empty_directory(self.download_folder)
        options = webdriver.ChromeOptions()
        options.add_experimental_option("prefs", {"download.default_directory": self.download_folder})
        options.add_argument("--headless")
        self.files_before_running = all_existing_files(self.download_folder)
        print("Existing files")
        print(self.files_before_running)
        self.driver = webdriver.Chrome(options=options)

    def parse(self, response):
        self.driver.get(response.url)
        driver = self.driver
        driver.get(URL)
        driver.find_element(By.XPATH, "//div[@id='results2_wrapper']/div/div/button[2]/span").click()
        while True:
            downloaded_file = all_existing_files(self.download_folder) - self.files_before_running
            print(list(downloaded_file))

            if len(downloaded_file) > 0:
                break
            else:
                print('Waiting for file to be downloaded')
                time.sleep(10)
        print(downloaded_file)
        downloaded_file = downloaded_file.pop()
        dataset = create_dataset('environ_epa_test')
        table = create_table(dataset, "List of Facilities in TRI submitting Pollution Prevention")
        upload_file(table, self.download_folder + downloaded_file)
        print(f'Finished Extracting {downloaded_file}')
