import scrapy

class LAUDataSpider(scrapy.Spider):
    name = 'LAU_data'
    start_urls = ['https://www.bls.gov/web/laus/lauhsthl.htm']

    def parse(self, response):
        self.logger.debug(response.text)  # print the page source to check if it's correct
        table_rows = response.xpath('//table[@id="lauhsthl"]/tbody/tr')

        for row in table_rows:
            state = row.xpath('.//th[1]//text()').get()
            current_rate = row.xpath('.//td[1]//span/text()').get()
            historical_high_date = row.xpath('.//td[2]//span/text()').get()
            historical_high_rate = row.xpath('.//td[3]//span/text()').get()
            historical_low_date = row.xpath('.//td[4]//span/text()').get()
            historical_low_rate = row.xpath('.//td[5]//span/text()').get()

            yield {
                'State': state,
                'Current Rate': current_rate,
                'Historical High Date': historical_high_date,
                'Historical High Rate': historical_high_rate,
                'Historical Low Date': historical_low_date,
                'Historical Low Rate': historical_low_rate
            }

        self.logger.info('Finished scraping')  # log when the spider is finished
