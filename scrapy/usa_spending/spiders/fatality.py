import time
from io import StringIO

import scrapy
import csv
import datetime
import os

# Create a CSV output



header = ["Date", "City", "State", "Hazard Description", "Inspection Number", "Federal or State Plan",
          "Citation Issued Related to Fatality", 'Report ID', 'Date Opened', "Site Address", "Mailing Address",
          "Union Status", "SIC",
          "NAICS",
          "Inspection Type", "Scope", "Advanced Notice", "Ownership", "Safety/Health", "Close Conference",
          "Emphasis", "Case Closed"]

with open('fatality.csv', 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(header)
class GenericTableSpider(scrapy.Spider):
    name = 'fatality'
    start_urls = ['https://www.osha.gov/fatalities#&sort%5B%23incSum%5D=0-1-1-0&sort%5B%23incSum%5D=0-1-1-0']


    def parse(self, response):
        # Extract table rows
        rows = response.xpath('//table[@id="incSum"]//tbody//tr')
        print(len(rows))
        self.result = []
        for row in rows:
            time.sleep(1)
            # Extract data from each row
            date = row.xpath('td[1]/text()').get()
            city = row.xpath('td[2]/text()').get()
            state = row.xpath('td[3]/text()').get()
            hazard_description = row.xpath('td[4]/text()').get()
            inspection_number = row.xpath('td[5]/a/text()').get()
            inspection_link = row.xpath('td[5]/a/@href').get()  # Get the hyperlink

            federal_state_plan = row.xpath('td[6]/text()').get()
            citation_issued = row.xpath('td[7]/text()').get()
            yield scrapy.Request(inspection_link, callback=self.parse_inspection_details,
                                 meta={"date": date, "city": city, "state": state,
                                       "hazard_description": hazard_description,
                                       "inspection_number": inspection_number,
                                       "federal_state_plan": federal_state_plan,
                                       "citation_issued": citation_issued,
                                       "inspection_link": inspection_link,
                                       'result': self.result},
                                 dont_filter=True)
            # Save CSV data to a file

        self.log('Saved data to output.csv')

    def parse_inspection_details(self, response):
        print('in Parse inspection')
        # Extract details from the inspection link
        date = response.meta.get("date")
        city = response.meta.get("city")
        state = response.meta.get("state")
        result = response.meta.get("result")
        hazard_description = response.meta.get("hazard_description")
        inspection_link = response.meta.get("inspection_link")
        federal_state_plan = response.meta.get("federal_state_plan")
        citation_issued = response.meta.get("citation_issued")
        # Extract New Data

        inspection_number = self.get_text_after_strong(response, 'Inspection Nr', 'div')
        report_id = self.get_text_after_strong(response, 'Report ID', 'div')
        data_opened = self.get_text_after_strong(response, 'Date Opened', 'div')

        site_address = response.xpath("//p[contains(strong,'Site Address')]/br/following-sibling::text()").getall()
        site_address = ', '.join(element.strip() for element in site_address)

        print('Site Address', site_address)
        mailing_address = response.xpath(
            '//p[contains(strong,"Mailing Address")]/br/following-sibling::text()').getall()
        mailing_address = ', '.join(element.strip() for element in mailing_address)
        print('Mailing Address', mailing_address)

        # mailing_address = " ".join(mailing_address).strip()
        #
        union_status = self.get_text_after_strong(response, "Union Status")

        self.get_text_after_strong(response, '')
        sic = self.get_text_after_strong(response, 'SIC')
        naics = self.get_text_after_strong(response, 'NAICS')
        inspection_type = self.get_text_after_strong(response, 'Inspection Type')
        scope = self.get_text_after_strong(response, 'Scope')
        advanced_notice = self.get_text_after_strong(response, 'Advanced Notice')
        ownership = self.get_text_after_strong(response, 'Ownership')
        safety_health = self.get_text_after_strong(response, 'Safety/Health')
        close_conference = self.get_text_after_strong(response, 'Close Conference')
        emphasis = self.get_text_after_strong(response, 'Emphasis')
        case_closed = self.get_text_after_strong(response, 'Case Closed')

        # Write row data to CSV
        row_data = [date, city, state, hazard_description,
                    '=HYPERLINK( "' + inspection_link + '"; "' + inspection_number + '")', federal_state_plan
            , citation_issued, report_id, data_opened, site_address, mailing_address, union_status, sic, naics,
                    inspection_type, scope, advanced_notice,
                    ownership, safety_health, close_conference, emphasis, case_closed]
        self.log('Row Data '+ str(row_data))
        with open('fatality.csv', 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(row_data)
        self.result.append(row_data)

        result.append(row_data)
        self.log('Saved data to output.csv')

        yield None

    def get_text_after_strong(self, response, strong_text, mother_element='p'):
        return response.xpath(
            f"//{mother_element}[contains(strong,'{strong_text}')]/strong/following-sibling::text()").get()[2:]
