import scrapy
from scrapy.http import FormRequest
from scrapy.selector import Selector


class USASpendingSpider(scrapy.Spider):
    name = "usaspending"
    start_urls = ["https://www.usaspending.gov/search/awards"]

    def parse(self, response):
        # Replace the specific element's HTML
        modified_response = self.replace_element(response)

        # Find the form and submit it
        form = modified_response.css("form[action='/search/awards/download/advanced/']")[0]
        print(form)
        yield FormRequest.from_response(form, clickdata={"type": "submit", "value": "Download"},
                                        callback=self.download_data)

    def replace_element(self, response):
        # Load the response into a selector
        selector = Selector(response)

        # Find the element you want to replace
        element_to_replace = selector.css("button[title='Select a Budget Function']")[0]

        # Define the new HTML content you want to use as a replacement
        new_html = """
        <button class="selected-button" title="All" aria-label="All">
            <div class="label">All</div>
            <div class="arrow-icon">
                <svg class="usa-da-icon-angle-down" viewBox="0 0 512 512" aria-label="Pick a budget function">
                    <title>Pick a budget function</title>
                    <g><path d="M77.2 143L255 303.7l179.7-160.2 71.3-.4-250.5 225.4L6 143.7"></path></g>
                </svg>
            </div>
        </button>
        """

        # Replace the element's HTML with the new HTML content
        modified_html = response.text.replace(element_to_replace.extract(), new_html)

        # Create a new response with the modified HTML content
        modified_response = response.replace(body=modified_html)

        return modified_response
    def download_data(self, response):
        # Process the downloaded data or handle the download file here
        # For now, let's just print the response content
        print(response.text)
