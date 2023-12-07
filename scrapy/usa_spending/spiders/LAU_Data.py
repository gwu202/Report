import csv

import scrapy
from .upload_redivis import create_dataset, create_table, upload_file

# LAUS
class LAUDataSpider(scrapy.Spider):
    name = 'LAU_data'
    start_urls = ['https://www.bls.gov/web/laus/lauhsthl.htm']
    file_name = 'lau_data.csv'
    def parse(self, response):
        self.logger.debug(response.text)  # print the page source to check if it's correct
        table_rows = response.xpath('//table[@id="lauhsthl"]/tbody/tr')
        with open(self.file_name, 'w', newline='', encoding='utf-8') as csvfile:
            # Create a CSV writer object
            csv_writer = csv.writer(csvfile)

            # Write header row
            csv_writer.writerow(['State', 'Current Rate', 'Historical High Date', 'Historical High Rate',
                                 'Historical Low Date', 'Historical Low Rate'])

            for row in table_rows:
                state = row.xpath('.//th[1]//text()').get()
                current_rate = row.xpath('.//td[1]//span/text()').get()
                historical_high_date = row.xpath('.//td[2]//span/text()').get()
                historical_high_rate = row.xpath('.//td[3]//span/text()').get()
                historical_low_date = row.xpath('.//td[4]//span/text()').get()
                historical_low_rate = row.xpath('.//td[5]//span/text()').get()

                # Write data to CSV
                csv_writer.writerow([state, current_rate, historical_high_date, historical_high_rate,
                                     historical_low_date, historical_low_rate])

        dataset = create_dataset('lau_data_test')
        table = create_table(dataset, "Local Area Unemployment Statistics")
        upload_file(table, self.file_name)
        print(f'Finished Extracting {self.file_name}')

        self.logger.info('Finished scraping')  # log when the spider is finished