import csv

import scrapy

class LAUDataSpider(scrapy.Spider):
    name = 'LAU_data'
    start_urls = ['https://www.bls.gov/web/laus/lauhsthl.htm']

    def parse(self, response):
        self.logger.debug(response.text)  # print the page source to check if it's correct
        table_rows = response.xpath('//table[@id="lauhsthl"]/tbody/tr')
        with open('output.csv', 'w', newline='', encoding='utf-8') as csvfile:
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


                yield {
                    'State': state,
                    'Current Rate': current_rate,
                    'Historical High Date': historical_high_date,
                    'Historical High Rate': historical_high_rate,
                    'Historical Low Date': historical_low_date,
                    'Historical Low Rate': historical_low_rate
                }

        self.logger.info('Finished scraping')  # log when the spider is finished