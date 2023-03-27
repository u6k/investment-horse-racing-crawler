import scrapy


class NetkeibaSpiderSpider(scrapy.Spider):
    name = "netkeiba_spider"
    allowed_domains = ["race.netkeiba.com"]
    start_urls = ["https://race.netkeiba.com/"]

    def parse(self, response):
        print(response.url)
