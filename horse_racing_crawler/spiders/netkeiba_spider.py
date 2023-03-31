import scrapy


class NetkeibaSpider(scrapy.Spider):
    name = "netkeiba_spider"
    allowed_domains = ["race.netkeiba.com"]

    def __init__(self, start_url="https://race.netkeiba.com/top/calendar.html", *args, **kwargs):
        super(NetkeibaSpider, self).__init__(*args, **kwargs)

        self.start_urls = [start_url]

    def parse(self, response):
        """Parse start_url."""
        self.logger.info(f"#parse: start: response={response.url}")

        yield self._follow(self.start_urls[0])

    def _follow(self, url):
        self.logger.debug(f"#_follow: start: url={url}")

        meta = {}
        if self.settings["CRAWL_HTTP_PROXY"]:
            meta["proxy"] = self.settings["CRAWL_HTTP_PROXY"]
        self.logger.debug(f"#_follow: start: meta={meta}")

        if url.startswith("https://race.netkeiba.com/top/calendar.html"):
            self.logger.debug("#_follow: follow calendar page")
            return scrapy.Request(url, callback=self.parse_calendar, meta=meta)

        if url.startswith("https://race.netkeiba.com/top/race_list.html?kaisai_date="):
            self.logger.debug("#_follow: follow race_list page")
            return scrapy.Request(url, callback=self.parse_race_list, meta=meta)

    def parse_calendar(self, response):
        """Parse calendar page.

        @url https://race.netkeiba.com/top/calendar.html?year=2023&month=3
        @returns items 0 0
        @returns requests 8 8
        @calendar_contract
        """
        self.logger.info(f"#parse_calendar: start: response={response.url}")

        for a in response.xpath("//a"):
            race_list_url = response.urljoin(a.xpath("@href").get())

            if race_list_url.startswith("https://race.netkeiba.com/top/race_list.html?kaisai_date="):
                self.logger.debug(f"#parse_calendar: a={race_list_url}")
                yield self._follow(race_list_url)

    def parse_race_list(self, response):
        """Parse race_list page."""
        self.logger.info(f"#parse_race_list: start: response={response.url}")
