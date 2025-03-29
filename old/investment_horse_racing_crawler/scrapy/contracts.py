import re
from scrapy.contracts import Contract
from scrapy.exceptions import ContractFail
from scrapy.http import Request
from scrapy import Item

from investment_horse_racing_crawler.app_logging import get_logger
from investment_horse_racing_crawler.scrapy.items import RaceInfoItem, RacePayoffItem, RaceResultItem, RaceDenmaItem, HorseItem, TrainerItem, JockeyItem, OddsWinPlaceItem, OddsBracketQuinellaItem, OddsExactaItem, OddsQuinellaItem, OddsQuinellaPlaceItem, OddsTrifectaItem, OddsTrioItem


logger = get_logger(__name__)


class ScheduleListContract(Contract):
    name = "schedule_list"

    def post_process(self, output):
        # Check requests
        requests = list(filter(lambda o: isinstance(o, Request), output))
        if len(requests) == 0:
            raise ContractFail("requests is empty")

        race_lists = list(filter(lambda r: r.url.startswith("https://keiba.yahoo.co.jp/race/list/"), requests))
        if len(race_lists) == 0:
            raise ContractFail("race_lists is empty")

        if len(requests) != len(race_lists):
            raise ContractFail("Unknown request")


class RaceListContract(Contract):
    name = "race_list"

    def post_process(self, output):
        # Check requests
        requests = list(filter(lambda o: isinstance(o, Request), output))
        if len(requests) == 0:
            raise ContractFail("requests is empty")

        race_denmas = list(filter(lambda r: r.url.startswith("https://keiba.yahoo.co.jp/race/denma/"), requests))
        if len(race_denmas) == 0:
            raise ContractFail("race_denmas is empty")

        if len(requests) != len(race_denmas):
            raise ContractFail("Unknown request")


class RaceResultContract(Contract):
    name = "race_result"

    def post_process(self, output):
        # Check items
        items = list(filter(lambda o: isinstance(o, Item), output))
        if len(items) == 0:
            raise ContractFail("items is empty")

        race_payoff_items = list(filter(lambda o: isinstance(o, RacePayoffItem), output))
        if len(race_payoff_items) == 0:
            raise ContractFail("race_payoff_items is empty")

        race_result_items = list(filter(lambda o: isinstance(o, RaceResultItem), output))
        if len(race_result_items) == 0:
            raise ContractFail("race_result_items is empty")

        if len(items) != (len(race_payoff_items) + len(race_result_items)):
            raise ContractFail("Unknown item")


class RaceDenmaContract(Contract):
    name = "race_denma"

    def post_process(self, output):
        # Check requests
        requests = list(filter(lambda o: isinstance(o, Request), output))
        if len(requests) == 0:
            raise ContractFail("requests is empty")

        horse_requests = list(filter(lambda r: r.url.startswith("https://keiba.yahoo.co.jp/directory/horse/"), requests))
        if len(horse_requests) == 0:
            raise ContractFail("horse_requests is empty")

        trainer_requests = list(filter(lambda r: r.url.startswith("https://keiba.yahoo.co.jp/directory/trainer/"), requests))
        if len(trainer_requests) == 0:
            raise ContractFail("trainer_requests is empty")

        jockey_requests = list(filter(lambda r: r.url.startswith("https://keiba.yahoo.co.jp/directory/jocky/"), requests))
        if len(jockey_requests) == 0:
            raise ContractFail("jockey_requests is empty")

        odds_requests = list(filter(lambda r: r.url.startswith("https://keiba.yahoo.co.jp/odds/tfw/"), requests))
        if len(odds_requests) != 1:
            raise ContractFail("len(odds_requests) is not 1")

        race_result_requests = list(filter(lambda r: r.url.startswith("https://keiba.yahoo.co.jp/race/result/"), requests))
        if len(race_result_requests) != 1:
            raise ContractFail("len(race_result_requests) is not 1")

        if len(requests) != (len(horse_requests) + len(trainer_requests) + len(jockey_requests) + len(odds_requests) + len(race_result_requests)):
            raise ContractFail("Unknown request")

        # Check items
        items = list(filter(lambda o: isinstance(o, Item), output))
        if len(items) == 0:
            raise ContractFail("items is empty")

        race_info_items = list(filter(lambda o: isinstance(o, RaceInfoItem), output))
        if len(race_info_items) != 1:
            raise ContractFail("len(race_info_items) is not 1")

        race_denma_items = list(filter(lambda o: isinstance(o, RaceDenmaItem), output))
        if len(race_denma_items) == 0:
            raise ContractFail("race_denma_items is empty")

        if len(items) != (len(race_info_items) + len(race_denma_items)):
            raise ContractFail("Unknown item")


class HorseContract(Contract):
    name = "horse"

    def post_process(self, output):
        # Check items
        items = list(filter(lambda o: isinstance(o, Item), output))
        if len(items) == 0:
            raise ContractFail("items is empty")

        horse_items = list(filter(lambda o: isinstance(o, HorseItem), output))
        if len(horse_items) != 1:
            raise ContractFail("len(horse_items) is not 1")

        if len(items) != len(horse_items):
            raise ContractFail("Unknown item")


class TrainerContract(Contract):
    name = "trainer"

    def post_process(self, output):
        # Check items
        items = list(filter(lambda o: isinstance(o, Item), output))
        if len(items) == 0:
            raise ContractFail("items is empty")

        trainer_items = list(filter(lambda o: isinstance(o, TrainerItem), output))
        if len(trainer_items) != 1:
            raise ContractFail("len(trainer_items) is not 1")

        if len(items) != len(trainer_items):
            raise ContractFail("Unknown item")


class JockeyContract(Contract):
    name = "jockey"

    def post_process(self, output):
        # Check items
        items = list(filter(lambda o: isinstance(o, Item), output))
        if len(items) == 0:
            raise ContractFail("items is empty")

        jockey_items = list(filter(lambda o: isinstance(o, JockeyItem), output))
        if len(jockey_items) != 1:
            raise ContractFail("len(jockey_items) is not 1")

        if len(items) != len(jockey_items):
            raise ContractFail("Unknown item")


class OddsWinPlaceContract(Contract):
    name = "odds_win_place"

    def post_process(self, output):
        # Check requests
        requests = list(filter(lambda o: isinstance(o, Request), output))
        if len(requests) == 0:
            raise ContractFail("requests is empty")

        odds_exacta_requests = list(filter(lambda r: r.url.startswith("https://keiba.yahoo.co.jp/odds/ut/"), requests))
        if len(odds_exacta_requests) != 1:
            raise ContractFail("len(odds_exacta_requests) is not 1")

        odds_quinella_requests = list(filter(lambda r: r.url.startswith("https://keiba.yahoo.co.jp/odds/ur/"), requests))
        if len(odds_quinella_requests) != 1:
            raise ContractFail("len(odds_quinella_requests) is not 1")

        odds_quinella_place_requests = list(filter(lambda r: r.url.startswith("https://keiba.yahoo.co.jp/odds/wide/"), requests))
        if len(odds_quinella_place_requests) != 1:
            raise ContractFail("len(odds_quinella_place_requests) is not 1")

        odds_trifecta_requests = list(filter(lambda r: r.url.startswith("https://keiba.yahoo.co.jp/odds/st/"), requests))
        if len(odds_trifecta_requests) != 1:
            raise ContractFail("len(odds_trifecta_requests) is not 1")

        odds_trio_requests = list(filter(lambda r: r.url.startswith("https://keiba.yahoo.co.jp/odds/sf/"), requests))
        if len(odds_trio_requests) != 1:
            raise ContractFail("len(odds_trio_requests) is not 1")

        if len(requests) != (len(odds_exacta_requests) + len(odds_quinella_requests) + len(odds_quinella_place_requests) + len(odds_trifecta_requests) + len(odds_trio_requests)):
            raise ContractFail("Unknown request")

        # Check items
        items = list(filter(lambda o: isinstance(o, Item), output))
        if len(items) == 0:
            raise ContractFail("items is empty")

        odds_win_place_items = list(filter(lambda o: isinstance(o, OddsWinPlaceItem), output))
        if len(odds_win_place_items) == 0:
            raise ContractFail("odds_win_place_items is empty")

        odds_bracket_quinella_items = list(filter(lambda o: isinstance(o, OddsBracketQuinellaItem), output))
        if len(odds_bracket_quinella_items) == 0:
            raise ContractFail("odds_bracket_quinella_items is empty")

        if len(items) != (len(odds_win_place_items) + len(odds_bracket_quinella_items)):
            raise ContractFail("Unknown item")


class OddsExactaContract(Contract):
    name = "odds_exacta"

    def post_process(self, output):
        # Check items
        items = list(filter(lambda o: isinstance(o, Item), output))
        if len(items) == 0:
            raise ContractFail("items is empty")

        odds_exacta_items = list(filter(lambda o: isinstance(o, OddsExactaItem), output))
        if len(odds_exacta_items) == 0:
            raise ContractFail("odds_exacta_items is empty")

        if len(items) != len(odds_exacta_items):
            raise ContractFail("Unknown item")


class OddsQuinellaContract(Contract):
    name = "odds_quinella"

    def post_process(self, output):
        # Check items
        items = list(filter(lambda o: isinstance(o, Item), output))
        if len(items) == 0:
            raise ContractFail("items is empty")

        odds_quinella_items = list(filter(lambda o: isinstance(o, OddsQuinellaItem), output))
        if len(odds_quinella_items) == 0:
            raise ContractFail("odds_quinella_items is empty")

        if len(items) != len(odds_quinella_items):
            raise ContractFail("Unknown item")


class OddsQuinellaPlaceContract(Contract):
    name = "odds_quinella_place"

    def post_process(self, output):
        # Check items
        items = list(filter(lambda o: isinstance(o, Item), output))
        if len(items) == 0:
            raise ContractFail("items is empty")

        odds_quinella_place_items = list(filter(lambda o: isinstance(o, OddsQuinellaPlaceItem), output))
        if len(odds_quinella_place_items) == 0:
            raise ContractFail("odds_quinella_place_items is empty")

        if len(items) != len(odds_quinella_place_items):
            raise ContractFail("Unknown item")


class OddsTrifectaContract(Contract):
    name = "odds_trifecta"

    def post_process(self, output):
        # Check requests
        requests = list(filter(lambda o: isinstance(o, Request), output))
        if len(requests) == 0:
            raise ContractFail("requests is empty")

        odds_requests = list(filter(lambda r: re.match(r"^https://keiba\.yahoo\.co\.jp/odds/st/\d+/\?umaBan=\d+$", r.url), requests))
        if len(odds_requests) == 0:
            raise ContractFail("odds_requests is empty")

        if len(requests) != len(odds_requests):
            raise ContractFail("Unknown request")

        # Check items
        items = list(filter(lambda o: isinstance(o, Item), output))
        if len(items) == 0:
            raise ContractFail("items is empty")

        odds_trifecta_items = list(filter(lambda o: isinstance(o, OddsTrifectaItem), output))
        if len(odds_trifecta_items) == 0:
            raise ContractFail("odds_trifecta_items is empty")

        if len(items) != len(odds_trifecta_items):
            raise ContractFail("Unknown item")


class OddsTrioContract(Contract):
    name = "odds_trio"

    def post_process(self, output):
        # Check items
        items = list(filter(lambda o: isinstance(o, Item), output))
        if len(items) == 0:
            raise ContractFail("items is empty")

        odds_trio_items = list(filter(lambda o: isinstance(o, OddsTrioItem), output))
        if len(odds_trio_items) == 0:
            raise ContractFail("odds_trio_items is empty")

        if len(items) != len(odds_trio_items):
            raise ContractFail("Unknown item")
