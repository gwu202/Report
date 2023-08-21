install_dependencies:
	pip install -r requirements.txt
hello_world:
	@echo "Hello"
usa_spending: hello_world
	cd usa_spending && scrapy crawl usaspending
