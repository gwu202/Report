from io import StringIO

import scrapy
import csv
import datetime
import os


class GenericTableSpider(scrapy.Spider):
    name = 'fatality'
    start_urls = ['https://www.osha.gov/fatalities#&sort%5B%23incSum%5D=0-1-1-0&sort%5B%23incSum%5D=0-1-1-0']

    def parse(self, response):
        # Extract table rows
        rows = response.xpath('//table[@id="incSum"]//tbody//tr')

        # Create a CSV output
        csv_output = StringIO()
        csv_writer = csv.writer(csv_output)

        # Write header row to CSV
        header = ["Date", "City", "State", "Hazard Description", "Inspection Number", "Federal or State Plan",
                  "Citation Issued Related to Fatality"]
        csv_writer.writerow(header)

        for row in rows:
            # Extract data from each row
            date = row.xpath('td[1]/text()').get()
            city = row.xpath('td[2]/text()').get()
            state = row.xpath('td[3]/text()').get()
            hazard_description = row.xpath('td[4]/text()').get()
            inspection_number = row.xpath('td[5]/a/text()').get()
            inspection_link = row.xpath('td[5]/a/@href').get()  # Get the hyperlink

            federal_state_plan = row.xpath('td[6]/text()').get()
            citation_issued = row.xpath('td[7]/text()').get()

            # Write row data to CSV
            csv_writer.writerow(
                [date, city, state, hazard_description,
                 '=HYPERLINK( "' + inspection_link + '"; "' + inspection_number + '")',
                 federal_state_plan, citation_issued])

        # Save CSV data to a file
        with open('output.csv', 'w', newline='') as csvfile:
            csvfile.write(csv_output.getvalue())

        self.log('Saved data to output.csv')
