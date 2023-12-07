import scrapy
#from scrapy.spiders import CrawlSpider, Rule
#from scrapy.linkextractors import LinkExtractor
import csv
import datetime

class GenericTableSpider(scrapy.Spider):
    name = 'generic_table'
    start_urls = ['https://www.bls.gov/lau/tables.htm']


    def parse(self, response):
        # Extract all the links on the page
        links = response.xpath('//a/@href').getall()

        # Loop through each link and yield a new request
        for link in links:
            if link.startswith('http'):  # Check if the link leads to a web page
                yield scrapy.Request(response.urljoin(link), callback=self.parse_table)

    count = 0

    def parse_table(self, response):
        # Extract the header names from the first row of the table
        headers = []
        for header in response.xpath('//table[@class="regular"]//tr'):
            headers.append(header.xpath('th[1]//text()').get())

        # Loop through each row of the table
        for i, row in enumerate(response.xpath('//table[@class="regular"]//tr')):
            # Skip the header row
            if i == 0:
                continue

            # Extract the data from each column of the row
            data = {}
            for j, cell in enumerate(row.xpath('td')):
                data[headers[j]] = cell.xpath('.//text()').get()

            yield data

        self.logger.info('Finished scraping')

        # Write the data to a CSV file
        self.count += 1
        filename = f'file{self.count}.csv'
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            for data in response.xpath('//table[@class="regular"]//tr[position()>1]'):
                writer.writerow({headers[j]: cell.xpath('.//text()').get() for j, cell in enumerate(data.xpath('td'))})

        self.logger.info(f'Saved data to {filename}')
