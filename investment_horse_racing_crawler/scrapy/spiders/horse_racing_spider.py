from distutils.util import strtobool
import re
import scrapy
from scrapy.loader import ItemLoader

from investment_horse_racing_crawler.app_logging import get_logger
from investment_horse_racing_crawler.scrapy.items import RaceInfoItem, RacePayoffItem, RaceResultItem, RaceDenmaItem, HorseItem, TrainerItem, JockeyItem, OddsWinPlaceItem, OddsBracketQuinellaItem, OddsExactaItem, OddsQuinellaItem, OddsQuinellaPlaceItem, OddsTrifectaItem, OddsTrioItem


logger = get_logger(__name__)


class HorseRacingSpider(scrapy.Spider):
    name = "horse_racing"

    def __init__(self, start_url='https://keiba.yahoo.co.jp/schedule/list/', recache_race=False, recache_horse=False, *args, **kwargs):
        logger.info(f"#__init__: start: start_url={start_url}, recache_race={recache_race}, recache_horse={recache_horse}")
        try:
            super(HorseRacingSpider, self).__init__(*args, **kwargs)

            self.start_urls = [start_url]
            self.recache_race = recache_race if type(recache_race) is bool else strtobool(recache_race)
            self.recache_horse = recache_horse if type(recache_horse) is bool else strtobool(recache_horse)
        except Exception:
            logger.exception("#__init__: fail")

    def parse(self, response):
        """ Parse start page.
        """
        logger.debug(f"#parse: start_url={response.url}")
        logger.debug(f"#parse: recache_race={self.recache_race}")
        logger.debug(f"#parse: recache_horse={self.recache_horse}")

        path = response.url[25:]
        yield self._follow_delegate(response, path)

    def parse_schedule_list(self, response):
        """ Parse schedule list page.

        @url https://keiba.yahoo.co.jp/schedule/list/2019/?month=12
        @returns items 0 0
        @returns requests 1
        @schedule_list
        """
        logger.info(f"#parse_schedule_list: start: url={response.url}")

        # Parse link
        for a in response.xpath("//a"):
            href = a.xpath("@href").get()

            if href.startswith("/race/list/"):
                logger.debug(f"#parse_schedule_list: found race list page: url={href}")
                yield self._follow_delegate(response, href)

    def parse_race_list(self, response):
        """ Parse race list page.

        @url https://keiba.yahoo.co.jp/race/list/19060502/
        @returns items 0 0
        @returns requests 1
        @race_list
        """
        logger.info(f"#parse_race_list: start: url={response.url}")

        # Parse link
        for a in response.xpath("//a"):
            race_id_re = re.match("^/race/result/([0-9]+)/$", a.xpath("@href").get())
            if race_id_re:
                race_id = race_id_re.group(1)
                yield self._follow_delegate(response, f"/race/denma/{race_id}/")

    def parse_race_result(self, response):
        """ Parse race result page.

        @url https://keiba.yahoo.co.jp/race/result/1906050201/
        @returns items 1
        @returns requests 0 0
        @race_result
        """
        logger.info(f"#parse_race_result: start: url={response.url}")

        # Parse race payoff
        logger.debug("#parse_race_result: parse race payoff")

        race_id = response.url.split("/")[-2]

        payoff_type = None
        for tr in response.xpath("//table[contains(@class, 'resultYen')]/tr"):
            payoff_type_str = tr.xpath("th/text()").get()
            if payoff_type_str is not None:
                payoff_type = payoff_type_str

            loader = ItemLoader(item=RacePayoffItem(), selector=tr)
            loader.add_value("race_id", race_id)
            loader.add_value("payoff_type", payoff_type)
            loader.add_xpath("horse_number", "td[1]/text()")
            loader.add_xpath("odds", "td[2]/text()")
            loader.add_xpath("favorite_order", "td[3]/span/text()")
            i = loader.load_item()

            logger.debug(f"#parse_race_result: race payoff={i}")
            yield i

        # Parse race result
        logger.debug("#parse_race_result: parse race result")

        for tr in response.xpath("//table[@id='raceScore']/tbody/tr"):
            loader = ItemLoader(item=RaceResultItem(), selector=tr)
            loader.add_value("race_id", race_id)
            loader.add_xpath("result", "td[1]/text()")
            loader.add_xpath("bracket_number", "td[2]/span/text()")
            loader.add_xpath("horse_number", "td[3]/text()")
            loader.add_xpath("horse_id", "td[4]/a/@href")
            loader.add_xpath("arrival_time", "td[5]/text()[1]")
            loader.add_xpath("passing_order", "td[6]/text()[1]")
            loader.add_xpath("final_600_meters_time", "td[6]/span/text()")
            loader.add_xpath("jockey_id", "td[7]/a/@href")
            loader.add_xpath("favorite_order", "td[8]/text()[1]")
            loader.add_xpath("odds", "td[8]/span/text()")
            loader.add_xpath("trainer_id", "td[9]/a/@href")
            i = loader.load_item()

            logger.debug(f"#parse_race_result: race result={i}")
            yield i

    def parse_race_denma(self, response):
        """ Parse denma page.

        @url https://keiba.yahoo.co.jp/race/denma/1906050201/
        @returns items 1
        @returns requests 1
        @race_denma
        """
        logger.info(f"#parse_race_denma: start: url={response.url}")

        # Parse race info
        logger.debug("#parse_race_denma: parse race info")

        loader = ItemLoader(item=RaceInfoItem(), response=response)
        race_id = response.url.split("/")[-2]
        loader.add_value("race_id", race_id)
        loader.add_xpath("race_round", "//td[@id='raceNo']/text()")
        loader.add_xpath("start_date", "//p[@id='raceTitDay']/text()[1]")
        loader.add_xpath("start_time", "//p[@id='raceTitDay']/text()[3]")
        loader.add_xpath("place_name", "//p[@id='raceTitDay']/text()[2]")
        loader.add_xpath("race_name", "//div[@id='raceTitName']/h1/text()")
        loader.add_xpath("course_type_length", "//p[@id='raceTitMeta']/text()[1]")
        loader.add_xpath("weather", "//p[@id='raceTitMeta']/img[1]/@alt")
        loader.add_xpath("course_condition", "//p[@id='raceTitMeta']/img[2]/@alt")
        loader.add_xpath("race_condition_1", "//p[@id='raceTitMeta']/text()[6]")
        loader.add_xpath("race_condition_2", "//p[@id='raceTitMeta']/text()[7]")
        loader.add_xpath("added_money", "//p[@id='raceTitMeta']/text()[8]")
        i = loader.load_item()

        logger.debug(f"#parse_race_denma: race info={i}")
        yield i

        # Parse race denma
        logger.debug("#parse_race_denma: parse race denma")

        for tr in response.xpath("//table[contains(@class, 'denmaLs')]/tr[position()>1]"):
            loader = ItemLoader(item=RaceDenmaItem(), selector=tr)
            loader.add_value("race_id", race_id)
            loader.add_xpath("bracket_number", "td[1]/span/text()")
            loader.add_xpath("horse_number", "td[2]/strong/text()")
            loader.add_xpath("horse_id", "td[3]/a/@href")
            loader.add_xpath("trainer_id", "td[3]/span/a/@href")
            loader.add_xpath("horse_weight_and_diff", "string(td[4])")
            loader.add_xpath("jockey_id", "td[5]/a/@href")
            loader.add_xpath("jockey_weight", "td[5]/text()")
            loader.add_xpath("prize_total_money", "td[7]/text()[3]")
            i = loader.load_item()

            logger.debug(f"#parse_race_denma: race denma={i}")
            yield i

        # Parse link
        logger.debug("#parse_race_denma: parse link")

        for a in response.xpath("//a"):
            href = a.xpath("@href").get()

            if href.startswith("/directory/horse/") \
                    or href.startswith("/directory/trainer/") \
                    or href.startswith("/directory/jocky/"):
                yield self._follow_delegate(response, href)

        yield self._follow_delegate(response, f"/odds/tfw/{race_id}/")
        yield self._follow_delegate(response, f"/race/result/{race_id}/")

    def parse_horse(self, response):
        """ Parse horse page.

        @url https://keiba.yahoo.co.jp/directory/horse/2017101602/
        @returns items 1 1
        @returns requests 0 0
        @horse
        """
        logger.info(f"#parse_horse: start: url={response.url}")

        horse_id = response.url.split("/")[-2]

        # Parse horse
        loader = ItemLoader(item=HorseItem(), response=response)
        loader.add_value("horse_id", horse_id)
        loader.add_xpath("gender", "string(//div[@id='dirTitName']/p)")
        loader.add_xpath("name", "//div[@id='dirTitName']/h1/text()")
        loader.add_xpath("birthday", "//div[@id='dirTitName']/ul/li[1]/text()")
        loader.add_xpath("coat_color", "//div[@id='dirTitName']/ul/li[2]/text()")
        loader.add_xpath("trainer_id", "//div[@id='dirTitName']/ul/li[3]/a/@href")
        loader.add_xpath("owner", "//div[@id='dirTitName']/ul/li[4]/text()")
        loader.add_xpath("breeder", "//div[@id='dirTitName']/ul/li[5]/text()")
        loader.add_xpath("breeding_farm", "//div[@id='dirTitName']/ul/li[6]/text()")

        tdBloodM = response.xpath("//table[@id='dirUmaBlood']/tr/td[@class='bloodM']/text()")
        loader.add_value("parent_horse_name_male_1", tdBloodM[0].get())
        loader.add_value("parent_horse_name_male_21", tdBloodM[1].get())
        loader.add_value("parent_horse_name_male_31", tdBloodM[2].get())
        loader.add_value("parent_horse_name_male_32", tdBloodM[3].get())
        loader.add_value("parent_horse_name_male_22", tdBloodM[4].get())
        loader.add_value("parent_horse_name_male_33", tdBloodM[5].get())
        loader.add_value("parent_horse_name_male_34", tdBloodM[6].get())

        tdBloodF = response.xpath("//table[@id='dirUmaBlood']/tr/td[@class='bloodF']/text()")
        loader.add_value("parent_horse_name_female_31", tdBloodF[0].get())
        loader.add_value("parent_horse_name_female_21", tdBloodF[1].get())
        loader.add_value("parent_horse_name_female_32", tdBloodF[2].get())
        loader.add_value("parent_horse_name_female_1", tdBloodF[3].get())
        loader.add_value("parent_horse_name_female_33", tdBloodF[4].get())
        loader.add_value("parent_horse_name_female_22", tdBloodF[5].get())
        loader.add_value("parent_horse_name_female_34", tdBloodF[6].get())
        i = loader.load_item()

        logger.debug(f"#parse_horse: horse={i}")
        yield i

    def parse_trainer(self, response):
        """ Parse trainer page.

        @url https://keiba.yahoo.co.jp/directory/trainer/01012/
        @returns items 1 1
        @returns requests 0 0
        @trainer
        """
        logger.info(f"#parse_trainer: start: url={response.url}")

        trainer_id = response.url.split("/")[-2]

        # Parse trainer
        loader = ItemLoader(item=TrainerItem(), response=response)
        loader.add_value("trainer_id", trainer_id)
        loader.add_xpath("name_kana", "//div[@id='dirTitName']/p/text()[1]")
        loader.add_xpath("name", "//div[@id='dirTitName']/h1/text()")
        loader.add_xpath("birthday", "//div[@id='dirTitName']/ul/li[1]/text()")
        loader.add_xpath("belong_to", "//div[@id='dirTitName']/ul/li[2]/text()")
        loader.add_xpath("first_licensing_year", "//div[@id='dirTitName']/ul/li[3]/text()")
        i = loader.load_item()

        logger.debug(f"#parse_trainer: trainer={i}")
        yield i

    def parse_jockey(self, response):
        """ Parse jockey page.

        @url https://keiba.yahoo.co.jp/directory/jocky/01167/
        @returns items 1 1
        @returns requests 0 0
        @jockey
        """
        logger.info(f"#parse_jockey: start: url={response.url}")

        jockey_id = response.url.split("/")[-2]

        # Parse jockey
        loader = ItemLoader(item=JockeyItem(), response=response)
        loader.add_value("jockey_id", jockey_id)
        loader.add_xpath("name_kana", "//div[@id='dirTitName']/p/text()[1]")
        loader.add_xpath("name", "//div[@id='dirTitName']/h1/text()")
        loader.add_xpath("birthday", "//div[@id='dirTitName']/ul/li[1]/text()")
        loader.add_xpath("belong_to", "//div[@id='dirTitName']/ul/li[2]/text()")
        loader.add_xpath("first_licensing_year", "//div[@id='dirTitName']/ul/li[3]/text()")
        loader.add_xpath("first_entry_day", "//div[@id='dirTitName']/ul/li[4]/text()")
        loader.add_xpath("first_win_day", "//div[@id='dirTitName']/ul/li[5]/text()")
        i = loader.load_item()

        logger.debug(f"#parse_jockey: jockey={i}")
        yield i

    def parse_odds_win_place(self, response):
        """ Parse odds win place page.

        @url https://keiba.yahoo.co.jp/odds/tfw/1906050201/?ninki=0
        @returns items 1
        @returns requests 1
        @odds_win_place
        """
        logger.info(f"#parse_odds_win_place: start: url={response.url}")

        race_id = response.url.split("/")[-2]

        # Parse odds win place
        for tr in response.xpath("//table[@class='dataLs oddTkwLs']/tbody/tr"):
            if len(tr.xpath("th")) > 0:
                continue

            loader = ItemLoader(item=OddsWinPlaceItem(), selector=tr)
            loader.add_value("race_id", race_id)
            loader.add_xpath("horse_number", "td[2]/text()")
            loader.add_xpath("horse_id", "td[3]/a/@href")
            loader.add_xpath("odds_win", "td[4]/text()")
            loader.add_xpath("odds_place_min", "td[5]/text()")
            loader.add_xpath("odds_place_max", "td[7]/text()")

            i = loader.load_item()

            logger.debug(f"#parse_odds_win_place: odds_win_place={i}")
            yield i

        # Parse odds bracket quinella
        for tr in response.xpath("//table[@class='oddsLs']/tbody/tr"):
            th = tr.xpath("th")
            if "class" in th.attrib:
                bracket_number_1 = th.xpath("div/text()").get()
            else:
                loader = ItemLoader(item=OddsBracketQuinellaItem(), selector=tr)
                loader.add_value("race_id", race_id)
                loader.add_value("bracket_number_1", bracket_number_1)
                loader.add_value("bracket_number_2", th.xpath("text()").get())
                loader.add_xpath("odds", "td/text()")

                i = loader.load_item()

                logger.debug(f"#parse_odds_win_place: odds_bracket_quinella={i}")
                yield i

        # Parse link
        logger.debug("#parse_odds_win_place: parse link")

        for a in response.xpath("//a"):
            href = a.xpath("@href").get()

            if not href:
                # hrefがNoneである場合がある
                continue

            if href.startswith("/odds/ut/") \
                    or href.startswith("/odds/ur/") \
                    or href.startswith("/odds/wide/") \
                    or href.startswith("/odds/st/") \
                    or href.startswith("/odds/sf/"):
                yield self._follow_delegate(response, href)

    def parse_odds_exacta(self, response):
        """ Parse odds exacta page.

        @url https://keiba.yahoo.co.jp/odds/ut/1906050201/?ninki=0
        @returns items 1
        @returns requests 0 0
        @odds_exacta
        """
        logger.info(f"#parse_odds_exacta: start: url={response.url}")

        race_id = response.url.split("/")[-2]

        # Parse odds exacta
        for tr in response.xpath("//table[@class='oddsLs']/tbody/tr"):
            th = tr.xpath("th")
            if "class" in th.attrib:
                horse_number_1 = th.xpath("text()").get()
            else:
                loader = ItemLoader(item=OddsExactaItem(), selector=tr)
                loader.add_value("race_id", race_id)
                loader.add_value("horse_number_1", horse_number_1)
                loader.add_value("horse_number_2", th.xpath("text()").get())
                loader.add_xpath("odds", "td/text()")

                i = loader.load_item()

                logger.debug(f"#parse_odds_exacta: odds_exacta={i}")
                yield i

    def parse_odds_quinella(self, response):
        """ Parse odds quinella page.

        @url https://keiba.yahoo.co.jp/odds/ur/1906050201/?ninki=0
        @returns items 1
        @returns requests 0 0
        @odds_quinella
        """
        logger.info(f"#parse_odds_quinella: start: url={response.url}")

        race_id = response.url.split("/")[-2]

        # Parse odds quinella
        for tr in response.xpath("//table[@class='oddsLs']/tbody/tr"):
            th = tr.xpath("th")
            if "class" in th.attrib:
                horse_number_1 = th.xpath("text()").get()
            else:
                loader = ItemLoader(item=OddsQuinellaItem(), selector=tr)
                loader.add_value("race_id", race_id)
                loader.add_value("horse_number_1", horse_number_1)
                loader.add_value("horse_number_2", th.xpath("text()").get())
                loader.add_xpath("odds", "td/text()")

                i = loader.load_item()

                logger.debug(f"#parse_odds_quinella: odds_quinella={i}")
                yield i

    def parse_odds_quinella_place(self, response):
        """ Parse odds quinella place page.

        @url https://keiba.yahoo.co.jp/odds/wide/1906050201/?ninki=0
        @returns items 1
        @returns requests 0 0
        @odds_quinella_place
        """
        logger.info(f"#parse_odds_quinella_place: start: url={response.url}")

        race_id = response.url.split("/")[-2]

        # Parse odds quinella place
        for tr in response.xpath("//table[@class='oddsWLs']/tbody/tr"):
            th = tr.xpath("th")
            if "class" in th.attrib:
                horse_number_1 = th.xpath("text()").get()
            else:
                loader = ItemLoader(item=OddsQuinellaPlaceItem(), selector=tr)
                loader.add_value("race_id", race_id)
                loader.add_value("horse_number_1", horse_number_1)
                loader.add_value("horse_number_2", th.xpath("text()").get())
                loader.add_xpath("odds_min", "td[1]/text()")
                loader.add_xpath("odds_max", "td[3]/text()")

                i = loader.load_item()

                logger.debug(f"#parse_odds_quinella_place: odds_quinella_place={i}")
                yield i

    def parse_odds_trifecta(self, response):
        """ Parse odds trifecta page.

        @url https://keiba.yahoo.co.jp/odds/st/1906050201/?umaBan=1
        @returns items 1
        @returns requests 1
        @odds_trifecta
        """
        logger.info(f"#parse_odds_trifecta: start: url={response.url}")

        race_id = response.url.split("/")[-2]

        # Parse odds trifecta
        for tr in response.xpath("//table[@class='odds3TLs']/tbody/tr"):
            if len(tr.xpath("td")) == 0:
                continue

            loader = ItemLoader(item=OddsTrifectaItem(), selector=tr)
            loader.add_value("race_id", race_id)
            loader.add_xpath("horse_number_1_2_3", "th/text()")
            loader.add_xpath("odds", "td/text()")

            i = loader.load_item()

            logger.debug(f"#parse_odds_trifecta: odds_trifecta={i}")
            yield i

        # Parse link
        for opt in response.xpath("//select[@name='umaBan']/option"):
            umaBan = opt.attrib["value"]
            href = f"/odds/st/{race_id}/?umaBan={umaBan}"
            yield self._follow_delegate(response, href)

    def parse_odds_trio(self, response):
        """ Parse odds trio page.

        @url https://keiba.yahoo.co.jp/odds/sf/1906050201/?ninki=0
        @returns items 1
        @returns requests 0 0
        @odds_trio
        """
        logger.info(f"#parse_odds_trio: start: url={response.url}")

        race_id = response.url.split("/")[-2]

        # Parse odds trio
        for tr in response.xpath("//table[@class='oddsLs']/tbody/tr"):
            th = tr.xpath("th")
            if "class" in th.attrib:
                horse_number_1_2 = th.xpath("text()").get()
            else:
                loader = ItemLoader(item=OddsTrioItem(), selector=tr)
                loader.add_value("race_id", race_id)
                loader.add_value("horse_number_1_2", horse_number_1_2)
                loader.add_value("horse_number_3", th.xpath("text()").get())
                loader.add_xpath("odds", "td/text()")

                i = loader.load_item()

                logger.debug(f"#parse_odds_trio: odds_trio={i}")
                yield i

    def _follow_delegate(self, response, path):
        logger.info(f"#_follow_delegate: start: path={path}")

        if path.startswith("/schedule/list/"):
            logger.debug("#_follow_delegate: follow schedule list page")
            return response.follow(path, callback=self.parse_schedule_list)

        elif path.startswith("/race/list/"):
            logger.debug("#_follow_delegate: follow race list page")
            return response.follow(path, callback=self.parse_race_list)

        elif path.startswith("/race/denma/"):
            logger.debug("#_follow_delegate: follow race denma page")
            return response.follow(path, callback=self.parse_race_denma)

        elif path.startswith("/race/result/"):
            logger.debug("#_follow_delegate: follow race result page")
            return response.follow(path, callback=self.parse_race_result)

        elif path.startswith("/odds/tfw/"):
            logger.debug("#_follow_delegate: follow odds win place page")
            return response.follow(path, callback=self.parse_odds_win_place)

        elif path.startswith("/odds/ut/"):
            logger.debug("#_follow_delegate: follow odds exacta page")
            return response.follow(path, callback=self.parse_odds_exacta)

        elif path.startswith("/odds/ur/"):
            logger.debug("#_follow_delegate: follow odds quinella page")
            return response.follow(path, callback=self.parse_odds_quinella)

        elif path.startswith("/odds/wide/"):
            logger.debug("#_follow_delegate: follow odds quinella place page")
            return response.follow(path, callback=self.parse_odds_quinella_place)

        elif path.startswith("/odds/st/"):
            logger.debug("#_follow_delegate: follow odds trifecta page")
            return response.follow(path, callback=self.parse_odds_trifecta)

        elif path.startswith("/odds/sf/"):
            logger.debug("#_follow_delegate: follow odds trio page")
            return response.follow(path, callback=self.parse_odds_trio)

        elif path.startswith("/directory/horse/"):
            logger.debug("#_follow_delegate: follow horse page")
            return response.follow(path, callback=self.parse_horse)

        elif path.startswith("/directory/trainer/"):
            logger.debug("#_follow_delegate: follow trainer page")
            return response.follow(path, callback=self.parse_trainer)

        elif path.startswith("/directory/jocky/"):
            logger.debug("#_follow_delegate: follow jockey page")
            return response.follow(path, callback=self.parse_jockey)

        else:
            logger.warning("#_follow_delegate: unknown path pattern")
