sc# Web Scraping Project - U.S. Bureau of Labor Statistics

This project utilizes Python Scrapy to scrape data from the U.S. Bureau of Labor Statistics (LAUS) website (https://www.bls.gov/lau/tables.htm). The goal is to automate the extraction of data from the websites without API or Download access. 

## Project Scripts

### 1) LAU_Data.py

This script is the starting point of the project. It scrapes a specific table from the BLS website, using the following URL: https://www.bls.gov/web/laus/lauhsthl.htm. To run this script, follow the instructions below:
Use the command: scrapy runspider LAU_Data.py -o fileName.csv
Replace `fileName.csv` with the desired name for the output CSV file.

### 2) LAU_tables.py

This script is an enhanced version of the previous script, providing more flexibility. It allows you to scrape any table data from the LAUS website by providing the URL of the desired table as input. To run this script, follow the instructions below: 
Use the command: scrapy runspider LAU_tables.py
After executing the command, input the URL of the desired table when prompted from this list of tables (https://www.bls.gov/lau/tables.htm).

### 3) LAU_Auto.py

This script is an improved version of the previous script. When executed, it automatically scrapes all tables available on the LAUS website. To run this script, follow the instructions below: 
Use command: scrapy runspider LAU_Auto.py

## Prerequisites

To run these scripts, you need to have Python and Scrapy installed on your system. You can install Scrapy using pip: pip install scrapy

Make sure to cd to the spider folder befor running the commands.

## Output

The output of the scraping process will be saved in CSV format. The resulting CSV file will contain the extracted data from the respective tables.
