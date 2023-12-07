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

current_directory = os.getcwd()
parent_directory = current_directory
# Move two directories above
# parent_directory = os.path.abspath(os.path.join(current_directory, "..", ".."))

def all_existing_files(extension='.zip') -> set:
    all_files = [file for file in os.listdir(parent_directory) if file.endswith(extension)]
    return set(all_files)
def all_zip_files() -> set:

    # List all zip files in the parent directory
    return  all_existing_files()


def extract_zip_file(first_zip_file):
    zip_file_path = os.path.join(parent_directory, first_zip_file)

    # Extract the contents of the first zip file
    extraction_directory = os.path.join(parent_directory, "extracted_contents")
    os.makedirs(extraction_directory, exist_ok=True)

    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extraction_directory)
    return extraction_directory


class USASpendingSpider(scrapy.Spider):
    name = "usa_spending"
    start_urls = ["https://www.usaspending.gov/download_center/custom_account_data"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.zip_before_running = all_zip_files()

        options = webdriver.ChromeOptions()

        options.add_argument("download.default_directory=./files/")
        options.add_argument("--headless")

        self.driver = webdriver.Chrome(options=options)
        # self.driver = webdriver.Chrome()

    def parse(self, response):
        # print(current_directory)
        # print(self.zip_before_running)
        self.driver.get(response.url)
        driver = self.driver
        driver.find_element(By.XPATH,
                            "//main[@id='main-content']/div/div[2]/div/div/div[2]/div/div/div/div/div/button/div").click()
        driver.find_element(By.NAME, "All").click()
        driver.find_element(By.XPATH,
                            "(.//*[normalize-space(text()) and normalize-space(.)='All'])[4]/following::*[name()='svg'][1]").click()
        driver.find_element(By.NAME, "Environmental Protection Agency").click()
        driver.find_element(By.XPATH,
                            "//main[@id='main-content']/div/div[2]/div/div/div[2]/div[4]/div/div[2]/input").click()
        driver.find_element(By.XPATH,
                            "//main[@id='main-content']/div/div[2]/div/div/div[2]/div[4]/div/div[3]/input").click()
        driver.find_element(By.XPATH, "//input[@value='Download']").click()

        while True:
            downloaded_file = all_zip_files() - self.zip_before_running
            if len(downloaded_file) > 0:
                break
            else:
                print('Waiting for file to be downloaded')
                time.sleep(30)
        print(downloaded_file)
        downloaded_file = downloaded_file.pop()
        extract_zip_file(downloaded_file)
        extracted_files = os.listdir("extracted_contents")
        print(extracted_files)
        # create_dataset_upload(downloaded_file, 'usaspending')
        dataset = create_dataset('usa_spending_test')
        for extracted_file in extracted_files:

            table_name = filename_to_table_name(extracted_file)
            table = create_table(dataset, table_name)
            upload_file(table, "extracted_contents/" + extracted_file)
            print(f'Finished Extracting {extracted_file}')


if __name__ == '__main__':
    pass

    # extract_zip_file('FY2023P01-P09_All_FA_AccountData_2023-08-19_H04M37S47926722.zip')
