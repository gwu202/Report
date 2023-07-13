import scrapy
import csv

class USASpendingSpider(scrapy.Spider):
    name = 'usaspending'
    start_urls = ['https://www.usaspending.gov/download_center/custom_account_data']

    def parse(self, response):
        download_link = response.css('.btn.btn-primary.btn-block::attr(href)').get()
        
        if download_link:
            yield scrapy.Request(url=download_link, callback=self.download_file)
        else:
            self.log("Download link not found on the page.")

    def download_file(self, response):
        # Save the file as 'custom_account_data.csv'
        filename = 'custom_account_data.csv'
        with open(filename, 'wb') as file:
            file.write(response.body)
        self.log(f"File downloaded: {filename}")
        
        # Read the CSV file and extract the data
        data = self.read_csv(filename)
        
        # Process the data as needed (e.g., print, manipulate, etc.)
        updated_data = self.process_data(data)
        
        # Save the updated data to a new CSV file
        updated_filename = 'updated_custom_account_data.csv'
        self.save_csv(updated_filename, updated_data)
        self.log(f"Updated data saved to: {updated_filename}")

    def read_csv(self, filename):
        data = []
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                data.append(row)
        return data
    
    def process_data(self, data):
        # Example: Append ' (updated)' to the first row
        updated_data = data
        updated_data[0][0] += ' (updated)'
        return updated_data
    
    def save_csv(self, filename, data):
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)
