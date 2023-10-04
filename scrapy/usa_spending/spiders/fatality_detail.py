from io import StringIO

import scrapy
import csv
import datetime
import os


class GenericTableSpider(scrapy.Spider):
    name = 'fatality_detail'
    start_urls = ['https://www.osha.gov/ords/imis/establishment.inspection_detail?id=1674337.015']
    def parse(self, response):
        csv_output = StringIO()
        csv_writer = csv.writer(csv_output)

        # Write header row to CSV
        header = ['Inspection Nr', 'Report ID', 'Date Opened', "Site Address", "Mailing Address", "Union Status", "SIC",
                  "NAICS",
                  "Inspection Type", "Scope", "Advanced Notice", "Ownership", "Safety/Health", "Close Conference",
                  "Emphasis", "Case Closed"]

        csv_writer.writerow(header)

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
        row_data = [inspection_number, report_id, data_opened, site_address, mailing_address, union_status, sic, naics,
                    inspection_type, scope, advanced_notice,
                    ownership, safety_health, close_conference, emphasis, case_closed]
        print('Row Data', row_data)
        csv_writer.writerow(row_data)
        # Save CSV data to a file
        with open('fatality_detail.csv', 'w', newline='') as csvfile:
            csvfile.write(csv_output.getvalue())

        self.log('Saved data to output.csv')

    def get_text_after_strong(self, response, strong_text, mother_element='p'):
        return response.xpath(
            f"//{mother_element}[contains(strong,'{strong_text}')]/strong/following-sibling::text()").get()[2:]
