from urllib.parse import parse_qs, urlparse

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

        elif url.startswith("https://race.netkeiba.com/top/race_list_sub.html?kaisai_date="):
            self.logger.debug("#_follow: follow race_list page")
            return scrapy.Request(url, callback=self.parse_race_list, meta=meta)

        elif url.startswith("https://race.netkeiba.com/race/result.html?race_id="):
            self.logger.debug("#_follow: follow race_result page")
            return scrapy.Request(url, callback=self.parse_race_result, meta=meta)

        else:
            raise Exception("Unknown url")

    def parse_calendar(self, response):
        """Parse calendar page.

        @url https://race.netkeiba.com/top/calendar.html?year=2023&month=3
        @returns items 0 0
        @returns requests 8 8
        @calendar_contract
        """
        self.logger.info(f"#parse_calendar: start: response={response.url}")

        for a in response.xpath("//a"):
            race_list_url = urlparse(response.urljoin(a.xpath("@href").get()))
            race_list_url_qs = parse_qs(race_list_url.query)

            if race_list_url.hostname == "race.netkeiba.com" and race_list_url.path == "/top/race_list.html" and "kaisai_date" in race_list_url_qs:
                self.logger.debug(f"#parse_calendar: a={race_list_url.geturl()}")

                race_list_url = f"https://race.netkeiba.com/top/race_list_sub.html?kaisai_date={race_list_url_qs['kaisai_date'][0]}"
                yield self._follow(race_list_url)

    def parse_race_list(self, response):
        """Parse race_list page.

        @url https://race.netkeiba.com/top/race_list_sub.html?kaisai_date=20230318
        @returns items 0 0
        @returns requests 36 36
        @race_list_contract
        """
        self.logger.info(f"#parse_race_list: start: response={response.url}")

        for a in response.xpath("//a"):
            race_result_url = urlparse(response.urljoin(a.xpath("@href").get()))
            race_result_url_qs = parse_qs(race_result_url.query)

            if race_result_url.hostname == "race.netkeiba.com" and race_result_url.path == "/race/result.html" and "race_id" in race_result_url_qs:
                self.logger.debug(f"#parse_race_list: a={race_result_url.geturl()}")

                race_result_url = f"https://race.netkeiba.com/race/result.html?race_id={race_result_url_qs['race_id'][0]}"
                yield self._follow(race_result_url)

    def parse_race_result(self, response):
        """Parse race_result page."""
        self.logger.info(f"#parse_race_result: start: response={response.url}")
