# How to use: 
Instructions on how to run the scrapy spiders 
## Install Requirements
Python version used is 3.7.

Run `pip install -r requirements.txt`

## Run a spider
`cd scrapy && scrapy crawl spider_name`
## Redivis Token
Insert a `.env` file under `scrapy/usa_spending/spiders` 

The `.env.` should be `TOKEN=FAKE_TOKEN`
# Spider Names:
- monthly_ridership (Transit ridership time series)
- epa_environ (Pollution Prevention Information)
- fatality (Work-related fatalities)
- LAU_data (Current Unemployment Rates for States)
- safety_security_major (Transit Safety & Security)
- total_funding (Transit funding time series)
- usa_spending (Federal Spending For EPA)