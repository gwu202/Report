import  scrapy
from scrapy.http import Request


class GenericTableSpider(scrapy.Spider):
    name = 'ejscreen'
    start_urls = ['https://gaftp.epa.gov/EJScreen/2023/']


    def parse(self, response):
        # Extract table rows
        href_links = response.css('tr td:nth-child(2) a::attr(href)').getall()
        yield scrapy.Request(response.urljoin(href_links[-1]), callback=self.parse_second_page)

    def file_path(self, request, response=None, info=None):
        return request.url.split("/")[-1]
    def parse_second_page(self, response):
        # Extract all the file links from the second page
        file_links = response.css('tr td:nth-child(2) a::attr(href)').getall()
        file_urls = [response.urljoin(file_link) for file_link in file_links]
        files_urls = [file for file in file_urls if file.split('.')[-1] in ['zip', 'csv', 'xlsx']]
        # files_urls = [file for file in file_urls if file.split('.')[-1] in ['xlsx']]
        print('file URLS ',files_urls)
        # Download the files one by one
        for file_url in files_urls:
            print('Downloading ', file_url)
            yield {
                'file_urls': [file_url],
                'files': [file_url.split('/')[-1]]
            }

    # def download_file(self, response):
    #     # Use Scrapy's FilesPipeline to download the file
    #     print('Download Timeout ',response.meta['download_timeout'])
    #     return {
    #         'url': response.url,
    #         'path': response.meta['download_timeout'],
    #     }