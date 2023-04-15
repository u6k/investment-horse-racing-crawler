import json
import re
import time
from urllib.parse import parse_qs, urlparse

import scrapy
from scrapy.loader import ItemLoader

from horse_racing_crawler.items import OddsItem, RaceCornerPassingItem, RaceInfoItem, RaceLapTimeItem, RacePayoffItem, RaceResultItem, TrainingItem


class NetkeibaSpider(scrapy.Spider):
    name = "netkeiba_spider"

    def __init__(self, start_url="https://race.netkeiba.com/top/calendar.html", *args, **kwargs):
        super(NetkeibaSpider, self).__init__(*args, **kwargs)

        self.start_urls = [start_url]

    def parse(self, response):
        """Parse start_url."""
        self.logger.info(f"#parse: start: response={response.url}")

        yield self._follow(self.start_urls[0])

    def _follow(self, url):
        self.logger.debug(f"#_follow: start: url={url}")

        # Setting http proxy
        meta = {}
        if self.settings["CRAWL_HTTP_PROXY"]:
            meta["proxy"] = self.settings["CRAWL_HTTP_PROXY"]
        self.logger.debug(f"#_follow: start: meta={meta}")

        # Build request
        if url.startswith("https://race.netkeiba.com/top/calendar.html"):
            self.logger.debug("#_follow: follow calendar page")
            return scrapy.Request(url, callback=self.parse_calendar, meta=meta)

        elif url.startswith("https://race.netkeiba.com/top/race_list_sub.html?kaisai_date="):
            self.logger.debug("#_follow: follow race_list page")
            return scrapy.Request(url, callback=self.parse_race_list, meta=meta)

        elif url.startswith("https://race.netkeiba.com/race/result.html?race_id="):
            self.logger.debug("#_follow: follow race_result page")
            return scrapy.Request(url, callback=self.parse_race_result, meta=meta)

        elif url.startswith("https://race.netkeiba.com/api/api_get_jra_odds.html?type=1&race_id="):
            self.logger.debug("#_follow: follow race_odds_win_place page")
            return scrapy.Request(url, callback=self.parse_race_odds_win_place, meta=meta)

        elif url.startswith("https://race.netkeiba.com/api/api_get_jra_odds.html?type=3&race_id="):
            self.logger.debug("#_follow: follow race_odds_bracket_quinella page")
            return scrapy.Request(url, callback=self.parse_race_odds_bracket_quinella, meta=meta)

        elif url.startswith("https://race.netkeiba.com/api/api_get_jra_odds.html?type=4&race_id="):
            self.logger.debug("#_follow: follow race_odds_quinella page")
            return scrapy.Request(url, callback=self.parse_race_odds_quinella, meta=meta)

        elif url.startswith("https://race.netkeiba.com/api/api_get_jra_odds.html?type=5&race_id="):
            self.logger.debug("#_follow: follow race_odds_win_quinella_place page")
            return scrapy.Request(url, callback=self.parse_race_odds_quinella_place, meta=meta)

        elif url.startswith("https://race.netkeiba.com/api/api_get_jra_odds.html?type=6&race_id="):
            self.logger.debug("#_follow: follow race_odds_exacta page")
            return scrapy.Request(url, callback=self.parse_race_odds_exacta, meta=meta)

        elif url.startswith("https://race.netkeiba.com/api/api_get_jra_odds.html?type=7&race_id="):
            self.logger.debug("#_follow: follow race_odds_trio page")
            return scrapy.Request(url, callback=self.parse_race_odds_trio, meta=meta)

        elif url.startswith("https://race.netkeiba.com/api/api_get_jra_odds.html?type=8&race_id="):
            self.logger.debug("#_follow: follow race_odds_trifecta page")
            return scrapy.Request(url, callback=self.parse_race_odds_trifecta, meta=meta)

        elif url.startswith("https://race.netkeiba.com/race/oikiri.html?race_id="):
            self.logger.debug("#_follow: follow training page")
            return scrapy.Request(url, callback=self.parse_training, meta=meta)

        elif url.startswith("https://db.netkeiba.com/horse/"):
            self.logger.debug("#_follow: follow horse page")
            return scrapy.Request(url, callback=self.parse_horse, meta=meta)

        elif url.startswith("https://db.netkeiba.com/jockey/"):
            self.logger.debug("#_follow: follow jockey page")
            return scrapy.Request(url, callback=self.parse_jockey, meta=meta)

        elif url.startswith("https://db.netkeiba.com/trainer/"):
            self.logger.debug("#_follow: follow trainer page")
            return scrapy.Request(url, callback=self.parse_trainer, meta=meta)

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

        # Parse link
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

        # Parse link
        for a in response.xpath("//a"):
            race_result_url = urlparse(response.urljoin(a.xpath("@href").get()))
            race_result_url_qs = parse_qs(race_result_url.query)

            if race_result_url.hostname == "race.netkeiba.com" and race_result_url.path == "/race/result.html" and "race_id" in race_result_url_qs:
                self.logger.debug(f"#parse_race_list: a={race_result_url.geturl()}")

                race_result_url = f"https://race.netkeiba.com/race/result.html?race_id={race_result_url_qs['race_id'][0]}"
                yield self._follow(race_result_url)

    def parse_race_result(self, response):
        """Parse race_result page.

        @url https://race.netkeiba.com/race/result.html?race_id=202306020702
        @returns items 27 27
        @returns requests 56 56
        @race_result_contract
        """
        self.logger.info(f"#parse_race_result: start: response={response.url}")

        race_result_url = urlparse(response.url)
        race_result_url_qs = parse_qs(race_result_url.query)

        # Parse race info
        self.logger.info("#parse_race_result: parse race info")

        loader = ItemLoader(item=RaceInfoItem(), response=response)
        loader.add_value("race_id", race_result_url_qs["race_id"])
        loader.add_xpath("race_round", "string(//span[@class='RaceNum'])")
        loader.add_xpath("race_name", "string(//div[@class='RaceName'])")
        loader.add_xpath("race_data1", "string(//div[@class='RaceData01'])")
        loader.add_xpath("race_data2", "string(//div[@class='RaceData02'])")
        i = loader.load_item()

        self.logger.info(f"#parse_race_result: race_info={i}")
        yield i

        # Parse race result
        self.logger.info("#parse_race_result: parse race result")

        tr = response.xpath("//table[@id='All_Result_Table']/thead/tr[@class='Header']")
        assert tr.xpath("string(th[1])").extract_first() == "着順", tr.xpath("string(th[1])").extract_first()
        assert tr.xpath("string(th[2])").extract_first() == "枠", tr.xpath("string(th[2])").extract_first()
        assert tr.xpath("string(th[3])").extract_first() == "馬番", tr.xpath("string(th[3])").extract_first()
        assert tr.xpath("string(th[4])").extract_first().strip() == "馬名", tr.xpath("string(th[4])").extract_first()
        assert tr.xpath("string(th[5])").extract_first() == "性齢", tr.xpath("string(th[5])").extract_first()
        assert tr.xpath("string(th[6])").extract_first() == "斤量", tr.xpath("string(th[6])").extract_first()
        assert tr.xpath("string(th[7])").extract_first() == "騎手", tr.xpath("string(th[7])").extract_first()
        assert tr.xpath("string(th[8])").extract_first() == "タイム", tr.xpath("string(th[8])").extract_first()
        assert tr.xpath("string(th[9])").extract_first() == "着差", tr.xpath("string(th[9])").extract_first()
        assert tr.xpath("string(th[10])").extract_first() == "人気", tr.xpath("string(th[10])").extract_first()
        assert tr.xpath("string(th[11])").extract_first() == "単勝オッズ", tr.xpath("string(th[11])").extract_first()
        assert tr.xpath("string(th[12])").extract_first() == "後3F", tr.xpath("string(th[12])").extract_first()
        assert tr.xpath("string(th[13])").extract_first() == "コーナー通過順", tr.xpath("string(th[13])").extract_first()
        assert tr.xpath("string(th[14])").extract_first() == "厩舎", tr.xpath("string(th[14])").extract_first()
        assert tr.xpath("string(th[15])").extract_first() == "馬体重(増減)", tr.xpath("string(th[15])").extract_first()

        horse_number = 0
        for tr in response.xpath("//table[@id='All_Result_Table']/tbody/tr"):
            loader = ItemLoader(item=RaceResultItem(), selector=tr)
            loader.add_value("race_id", race_result_url_qs["race_id"])
            loader.add_xpath("result", "string(td[1])")
            loader.add_xpath("bracket_number", "string(td[2])")
            loader.add_xpath("horse_number", "string(td[3])")
            loader.add_xpath("horse_id_url", "td[4]/span/a/@href")
            loader.add_xpath("jockey_weight", "string(td[6])")
            loader.add_xpath("jockey_id_url", "td[7]/a/@href")
            loader.add_xpath("arrival_time", "string(td[8])")
            loader.add_xpath("arrival_margin", "string(td[9])")
            loader.add_xpath("favorite_order", "string(td[10])")
            loader.add_xpath("final_600_meters_time", "string(td[12])")
            loader.add_xpath("corner_passing_order", "string(td[13])")
            loader.add_xpath("trainer_id_url", "td[14]/a/@href")
            loader.add_xpath("horse_weight_and_diff", "string(td[15])")
            i = loader.load_item()

            self.logger.info(f"#parse_race_result: race_result={i}")
            yield i

            horse_number += 1

        # Parse race payoff
        self.logger.info("#parse_race_result: parse race payoff")

        tr = response.xpath("//table[@class='Payout_Detail_Table'][1]/tbody/tr[@class='Tansho']")
        loader = ItemLoader(item=RacePayoffItem(), selector=tr)
        loader.add_value("race_id", race_result_url_qs["race_id"])
        loader.add_xpath("betting_type", "th/text()")
        loader.add_xpath("horse_numbers", "td[@class='Result']/div[1]/span/text()")
        loader.add_xpath("payoff", "td[@class='Payout']/span/text()")
        i = loader.load_item()
        assert i["betting_type"][0] == "単勝", i["betting_type"][0]

        self.logger.info(f"#parse_race_result: race_payoff={i}")
        yield i

        tr = response.xpath("//table[@class='Payout_Detail_Table'][1]/tbody/tr[@class='Fukusho']")
        loader = ItemLoader(item=RacePayoffItem(), selector=tr)
        loader.add_value("race_id", race_result_url_qs["race_id"])
        loader.add_xpath("betting_type", "th/text()")
        loader.add_xpath("horse_numbers", "td[@class='Result']/div/span/text()")
        loader.add_xpath("payoff", "td[@class='Payout']/span/text()")
        i = loader.load_item()
        assert i["betting_type"][0] == "複勝", i["betting_type"][0]

        self.logger.info(f"#parse_race_result: race_payoff={i}")
        yield i

        def load_item_ren(tr):
            loader = ItemLoader(item=RacePayoffItem(), selector=tr)
            loader.add_value("race_id", race_result_url_qs["race_id"])
            loader.add_xpath("betting_type", "th/text()")
            loader.add_xpath("horse_numbers", "td[@class='Result']/ul/li/span/text()")
            loader.add_xpath("payoff", "td[@class='Payout']/span/text()")
            return loader.load_item()

        tr = response.xpath("//table[@class='Payout_Detail_Table'][1]/tbody/tr[@class='Wakuren']")
        i = load_item_ren(tr)
        assert i["betting_type"][0] == "枠連", i["betting_type"][0]

        self.logger.info(f"#parse_race_result: race_payoff={i}")
        yield i

        tr = response.xpath("//table[@class='Payout_Detail_Table'][1]/tbody/tr[@class='Umaren']")
        i = load_item_ren(tr)
        assert i["betting_type"][0] == "馬連", i["betting_type"][0]

        self.logger.info(f"#parse_race_result: race_payoff={i}")
        yield i

        tr = response.xpath("//table[@class='Payout_Detail_Table'][2]/tbody/tr[@class='Wide']")
        i = load_item_ren(tr)
        assert i["betting_type"][0] == "ワイド", i["betting_type"][0]

        self.logger.info(f"#parse_race_result: race_payoff={i}")
        yield i

        tr = response.xpath("//table[@class='Payout_Detail_Table'][2]/tbody/tr[@class='Umatan']")
        i = load_item_ren(tr)
        assert i["betting_type"][0] == "馬単", i["betting_type"][0]

        self.logger.info(f"#parse_race_result: race_payoff={i}")
        yield i

        tr = response.xpath("//table[@class='Payout_Detail_Table'][2]/tbody/tr[@class='Fuku3']")
        i = load_item_ren(tr)
        assert i["betting_type"][0] == "3連複", i["betting_type"][0]

        self.logger.info(f"#parse_race_result: race_payoff={i}")
        yield i

        tr = response.xpath("//table[@class='Payout_Detail_Table'][2]/tbody/tr[@class='Tan3']")
        i = load_item_ren(tr)
        assert i["betting_type"][0] == "3連単", i["betting_type"][0]

        self.logger.info(f"#parse_race_result: race_payoff={i}")
        yield i

        # Parse corner passing
        tbody = response.xpath("//table[contains(@class, 'Corner_Num')]/tbody")
        loader = ItemLoader(item=RaceCornerPassingItem(), selector=tbody)
        loader.add_value("race_id", race_result_url_qs["race_id"])
        loader.add_xpath("corner_name", "tr/th")
        loader.add_xpath("passing_order", "tr/td")
        i = loader.load_item()

        self.logger.info(f"#parse_race_result: race_corner_passing={i}")
        yield i

        # Parse lap time
        tbody = response.xpath("//table[contains(@class, 'Race_HaronTime')]/tbody")
        loader = ItemLoader(item=RaceLapTimeItem(), selector=tbody)
        loader.add_value("race_id", race_result_url_qs["race_id"])
        loader.add_xpath("length", "tr[1]/th/text()")
        loader.add_xpath("time1", "tr[2]/td/text()")
        loader.add_xpath("time2", "tr[3]/td/text()")
        i = loader.load_item()

        self.logger.info(f"#parse_race_result: race_lap_time={i}")
        yield i

        # Parse link
        self.logger.info("#parse_race_result: parse link")

        for a in response.xpath("//a"):
            url = urlparse(response.urljoin(a.xpath("@href").get()))
            url_qs = parse_qs(url.query)

            if url.hostname == "race.netkeiba.com" and url.path == "/odds/index.html" and "race_id" in url_qs:
                self.logger.info(f"#parse_race_result: odds top page link. a={url.geturl()}")

                t = int(time.time())  # キャッシュ回避のため、リクエストに付与する現在時刻

                # 単勝・複勝
                race_odds_url = f"https://race.netkeiba.com/api/api_get_jra_odds.html?type=1&race_id={url_qs['race_id'][0]}&_={t}"
                yield self._follow(race_odds_url)

                # 枠連
                race_odds_url = f"https://race.netkeiba.com/api/api_get_jra_odds.html?type=3&race_id={url_qs['race_id'][0]}&_={t}"
                yield self._follow(race_odds_url)

                # 馬連
                race_odds_url = f"https://race.netkeiba.com/api/api_get_jra_odds.html?type=4&race_id={url_qs['race_id'][0]}&_={t}"
                yield self._follow(race_odds_url)

                # ワイド
                race_odds_url = f"https://race.netkeiba.com/api/api_get_jra_odds.html?type=5&race_id={url_qs['race_id'][0]}&_={t}"
                yield self._follow(race_odds_url)

                # 馬単
                race_odds_url = f"https://race.netkeiba.com/api/api_get_jra_odds.html?type=6&race_id={url_qs['race_id'][0]}&_={t}"
                yield self._follow(race_odds_url)

                # 3連複
                race_odds_url = f"https://race.netkeiba.com/api/api_get_jra_odds.html?type=7&race_id={url_qs['race_id'][0]}&_={t}"
                yield self._follow(race_odds_url)

                # 3連単
                race_odds_url = f"https://race.netkeiba.com/api/api_get_jra_odds.html?type=8&race_id={url_qs['race_id'][0]}&_={t}"
                yield self._follow(race_odds_url)

            elif url.hostname == "race.netkeiba.com" and url.path == "/race/oikiri.html" and "race_id" in url_qs:
                self.logger.info(f"#parse_race_result: training page link. a={url.geturl()}")

                race_training_url = f"https://race.netkeiba.com/race/oikiri.html?race_id={url_qs['race_id'][0]}"
                yield self._follow(race_training_url)

            elif url.hostname == "db.netkeiba.com" and url.path.startswith("/horse/"):
                self.logger.info(f"#parse_race_result: horse page link. a={url.geturl()}")

                horse_id_re = re.match("^/horse/([0-9]+)$", url.path)
                horse_url = f"https://db.netkeiba.com/horse/{horse_id_re.group(1)}"

                yield self._follow(horse_url)

            elif url.hostname == "db.netkeiba.com" and url.path.startswith("/jockey/result/recent/"):
                self.logger.info(f"#parse_race_result: jockey page link. a={url.geturl()}")

                jockey_id_re = re.match("^/jockey/result/recent/([0-9]+)/$", url.path)
                jockey_url = f"https://db.netkeiba.com/jockey/{jockey_id_re.group(1)}"

                yield self._follow(jockey_url)

            elif url.hostname == "db.netkeiba.com" and url.path.startswith("/trainer/result/recent/"):
                self.logger.info(f"#parse_race_result: trainer page link. a={url.geturl()}")

                trainer_id_re = re.match("^/trainer/result/recent/([0-9]+)/$", url.path)
                trainer_url = f"https://db.netkeiba.com/trainer/{trainer_id_re.group(1)}"

                yield self._follow(trainer_url)

    def parse_race_odds_win_place(self, response):
        """Parse odds_win_place page.

        @url https://race.netkeiba.com/api/api_get_jra_odds.html?type=1&race_id=202306020702
        @returns items 32 32
        @returns requests 0 0
        @odds_win_place_contract
        """
        self.logger.info(f"#parse_race_odds_win_place: start: response={response.url}")

        odds_url = urlparse(response.url)
        odds_qs = parse_qs(odds_url.query)

        # Assertion
        json_odds = json.loads(response.text)

        assert json_odds["status"] == "result"
        assert json_odds["data"]["official_datetime"] is not None

        # Parse win odds
        for horse_number, odds in json_odds["data"]["odds"]["1"].items():
            item = OddsItem(race_id=odds_qs["race_id"], odds_type=1, horse_number=horse_number, odds1=odds[0], odds2=odds[1], favorite_order=odds[2])

            self.logger.debug(f"#parse_race_odds_win_place: odds={item}")
            yield item

        # Parse place odds
        for horse_number, odds in json_odds["data"]["odds"]["2"].items():
            item = OddsItem(race_id=odds_qs["race_id"], odds_type=2, horse_number=horse_number, odds1=odds[0], odds2=odds[1], favorite_order=odds[2])

            self.logger.debug(f"#parse_race_odds_win_place: odds={item}")
            yield item

    def parse_race_odds_bracket_quinella(self, response):
        """Parse odds_bracket_quinella page.

        @url https://race.netkeiba.com/api/api_get_jra_odds.html?type=3&race_id=202306020702
        @returns items 36 36
        @returns requests 0 0
        @odds_bracket_quinella_contract
        """
        self.logger.info(f"#parse_race_odds_bracket_quinella: start: response={response.url}")

        odds_url = urlparse(response.url)
        odds_qs = parse_qs(odds_url.query)

        # Assertion
        json_odds = json.loads(response.text)

        assert json_odds["status"] == "result"
        assert json_odds["data"]["official_datetime"] is not None

        # Parse bracket_quinella odds
        for horse_number, odds in json_odds["data"]["odds"]["3"].items():
            item = OddsItem(race_id=odds_qs["race_id"], odds_type=3, horse_number=horse_number, odds1=odds[0], odds2=odds[1], favorite_order=odds[2])

            self.logger.debug(f"#parse_race_odds_bracket_quinella: odds={item}")
            yield item

    def parse_race_odds_quinella(self, response):
        """Parse odds_quinella page.

        @url https://race.netkeiba.com/api/api_get_jra_odds.html?type=4&race_id=202306020702
        @returns items 120 120
        @returns requests 0 0
        @odds_quinella_contract
        """
        self.logger.info(f"#parse_race_odds_quinella: start: response={response.url}")

        odds_url = urlparse(response.url)
        odds_qs = parse_qs(odds_url.query)

        # Assertion
        json_odds = json.loads(response.text)

        assert json_odds["status"] == "result"
        assert json_odds["data"]["official_datetime"] is not None

        # Parse quinella odds
        for horse_number, odds in json_odds["data"]["odds"]["4"].items():
            item = OddsItem(race_id=odds_qs["race_id"], odds_type=4, horse_number=horse_number, odds1=odds[0], odds2=odds[1], favorite_order=odds[2])

            self.logger.debug(f"#parse_race_odds_quinella: odds={item}")
            yield item

    def parse_race_odds_quinella_place(self, response):
        """Parse odds_quinella_place page.

        @url https://race.netkeiba.com/api/api_get_jra_odds.html?type=5&race_id=202306020702
        @returns items 120 120
        @returns requests 0 0
        @odds_quinella_place_contract
        """
        self.logger.info(f"#parse_race_odds_quinella_place: start: response={response.url}")

        odds_url = urlparse(response.url)
        odds_qs = parse_qs(odds_url.query)

        # Assertion
        json_odds = json.loads(response.text)

        assert json_odds["status"] == "result"
        assert json_odds["data"]["official_datetime"] is not None

        # Parse quinella_place odds
        for horse_number, odds in json_odds["data"]["odds"]["5"].items():
            item = OddsItem(race_id=odds_qs["race_id"], odds_type=5, horse_number=horse_number, odds1=odds[0], odds2=odds[1], favorite_order=odds[2])

            self.logger.debug(f"#parse_race_odds_quinella_place: odds={item}")
            yield item

    def parse_race_odds_exacta(self, response):
        """Parse odds_exacta page.

        @url https://race.netkeiba.com/api/api_get_jra_odds.html?type=6&race_id=202306020702
        @returns items 240 240
        @returns requests 0 0
        @odds_exacta_contract
        """
        self.logger.info(f"#parse_race_odds_exacta: start: response={response.url}")

        odds_url = urlparse(response.url)
        odds_qs = parse_qs(odds_url.query)

        # Assertion
        json_odds = json.loads(response.text)

        assert json_odds["status"] == "result"
        assert json_odds["data"]["official_datetime"] is not None

        # Parse exacta odds
        for horse_number, odds in json_odds["data"]["odds"]["6"].items():
            item = OddsItem(race_id=odds_qs["race_id"], odds_type=6, horse_number=horse_number, odds1=odds[0], odds2=odds[1], favorite_order=odds[2])

            self.logger.debug(f"#parse_race_odds_exacta: odds={item}")
            yield item

    def parse_race_odds_trio(self, response):
        """Parse odds_trio page.

        @url https://race.netkeiba.com/api/api_get_jra_odds.html?type=7&race_id=202306020702
        @returns items 560 560
        @returns requests 0 0
        @odds_trio_contract
        """
        self.logger.info(f"#parse_race_odds_trio: start: response={response.url}")

        odds_url = urlparse(response.url)
        odds_qs = parse_qs(odds_url.query)

        # Assertion
        json_odds = json.loads(response.text)

        assert json_odds["status"] == "result"
        assert json_odds["data"]["official_datetime"] is not None

        # Parse trio odds
        for horse_number, odds in json_odds["data"]["odds"]["7"].items():
            item = OddsItem(race_id=odds_qs["race_id"], odds_type=7, horse_number=horse_number, odds1=odds[0], odds2=odds[1], favorite_order=odds[2])

            self.logger.debug(f"#parse_race_odds_trio: odds={item}")
            yield item

    def parse_race_odds_trifecta(self, response):
        """Parse odds_trifecta page.

        @url https://race.netkeiba.com/api/api_get_jra_odds.html?type=8&race_id=202306020702
        @returns items 3360 3360
        @returns requests 0 0
        @odds_trifecta_contract
        """
        self.logger.info(f"#parse_race_odds_trifecta: start: response={response.url}")

        odds_url = urlparse(response.url)
        odds_qs = parse_qs(odds_url.query)

        # Assertion
        json_odds = json.loads(response.text)

        assert json_odds["status"] == "result"
        assert json_odds["data"]["official_datetime"] is not None

        # Parse trifecta odds
        for horse_number, odds in json_odds["data"]["odds"]["8"].items():
            item = OddsItem(race_id=odds_qs["race_id"], odds_type=8, horse_number=horse_number, odds1=odds[0], odds2=odds[1], favorite_order=odds[2])

            self.logger.debug(f"#parse_race_odds_trifecta: odds={item}")
            yield item

    def parse_training(self, response):
        """Parse training page.

        @url https://race.netkeiba.com/race/oikiri.html?race_id=202306020702
        @returns items 16 16
        @returns requests 0 0
        @training_contract
        """
        self.logger.info(f"#parse_training: start: response={response.url}")

        training_url = urlparse(response.url)
        training_url_qs = parse_qs(training_url.query)

        # Parse training
        for i, tr in enumerate(response.xpath("//table[@id='All_Oikiri_Table']/tr")):
            if i == 0:
                assert tr.xpath("string(th[1])").extract_first() == "枠", tr.xpath("string(th[1])").extract_first()
                assert tr.xpath("string(th[2])").extract_first() == "馬番", tr.xpath("string(th[2])").extract_first()
                assert tr.xpath("string(th[3])").extract_first().strip() == "印", tr.xpath("string(th[3])").extract_first()
                assert tr.xpath("string(th[4])").extract_first() == "馬名", tr.xpath("string(th[4])").extract_first()
                assert tr.xpath("string(th[5])").extract_first() == "評価", tr.xpath("string(th[5])").extract_first()

            else:
                loader = ItemLoader(item=TrainingItem(), selector=tr)
                loader.add_value("race_id", training_url_qs["race_id"])
                loader.add_xpath("horse_number", "string(td[1])")
                loader.add_xpath("horse_id_url", "td[4]/div[@class='Horse_Name']/a/@href")
                loader.add_xpath("evaluation_text", "string(td[5])")
                loader.add_xpath("evaluation_rank", "string(td[6])")
                i = loader.load_item()

                self.logger.info(f"#parse_training: training={i}")
                yield i

    def parse_horse(self, response):
        self.logger.info(f"#parse_horse: start: response={response.url}")

    def parse_jockey(self, response):
        self.logger.info(f"#parse_jockey: start: response={response.url}")

    def parse_trainer(self, response):
        self.logger.info(f"#parse_trainer: start: response={response.url}")
