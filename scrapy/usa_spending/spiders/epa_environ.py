import scrapy

import zipfile

import scrapy
from scrapy.http import FormRequest
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.common.by import By
import os

# Get the current directory
from .upload_redivis import create_dataset, create_table, filename_to_table_name, upload_file

# from upload_redivis import create_dataset
from .usa_spending import all_zip_files, all_existing_files

current_directory = os.getcwd()
parent_directory = current_directory


class EpaEnvironSpider(scrapy.Spider):
    name = "epa_environ"
    allowed_domains = ["enviro.epa.gov"]
    start_urls = [
        "https://enviro.epa.gov/enviro/P2_EF_Query.master_build_sql?FacOrParent=1&Industry_Search=null&Industry_Search=311&Chemical_Search=null&Year_Search=null&State_Search=null&pZipCity=&database_type=TRI&results2_length=10&page_no=1&pRepOption=1"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.csv_before_running = all_existing_files(extension='.csv')

        options = webdriver.ChromeOptions()
        options.add_argument("download.default_directory=./files/")
        options.add_argument("--headless")

        self.driver = webdriver.Chrome(options=options)
        # self.driver = webdriver.Chrome()

    def parse(self, response):
        self.driver.get(response.url)
        driver = self.driver
        driver.get(
            "https://enviro.epa.gov/enviro/P2_EF_Query.master_build_sql?FacOrParent=1&Industry_Search=null&Industry_Search=311&Chemical_Search=null&Year_Search=null&State_Search=null&pZipCity=&database_type=TRI&results2_length=10&page_no=1&pRepOption=1")
        driver.find_element(By.XPATH, "//div[@id='results2_wrapper']/div/div/button[2]/span").click()
        while True:
            downloaded_file = all_existing_files(extension='.csv') - self.csv_before_running
            if len(downloaded_file) > 0:
                break
            else:
                print('Waiting for file to be downloaded')
                time.sleep(30)
        print(downloaded_file)
        downloaded_file = downloaded_file.pop()

        dataset = create_dataset('environ_epa_test')
        table = create_table(dataset, "List of Facilities in TRI submitting Pollution Prevention")
        upload_file(table, downloaded_file)
        print(f'Finished Extracting {downloaded_file}')
