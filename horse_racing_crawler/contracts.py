from urllib.parse import parse_qs, urlparse

from scrapy.contracts import Contract
from scrapy.exceptions import ContractFail
from scrapy.http import Request

from horse_racing_crawler.items import HorseItem, JockeyItem, OddsItem, ParentHorseItem, RaceCornerPassingItem, RaceInfoItem, RaceLapTimeItem, RacePayoffItem, RaceResultItem, TrainerItem, TrainingItem


class CalendarContract(Contract):
    name = "calendar_contract"

    def post_process(self, output):
        # Check requests
        requests = list(filter(lambda o: isinstance(o, Request), output))

        for r in requests:
            url = urlparse(r.url)
            qs = parse_qs(url.query)

            if url.hostname == "race.netkeiba.com" and url.path == "/top/race_list_sub.html" and "kaisai_date" in qs:
                continue

            elif url.hostname == "db.netkeiba.com" and url.path.startswith("/race/sum/"):
                continue

            raise ContractFail(f"Unknown request: url={r.url}")


class RaceListContract(Contract):
    name = "race_list_contract"

    def post_process(self, output):
        # Check requests
        requests = list(filter(lambda o: isinstance(o, Request), output))

        for r in requests:
            url = urlparse(r.url)
            qs = parse_qs(url.query)

            if url.hostname == "race.netkeiba.com" and url.path == "/race/result.html" and "race_id" in qs:
                continue

            raise ContractFail(f"Unknown request: url={r.url}")


class OldRaceListContract(Contract):
    name = "old_race_list_contract"

    def post_process(self, output):
        # Check requests
        requests = list(filter(lambda o: isinstance(o, Request), output))

        for r in requests:
            if r.url.startswith("https://db.netkeiba.com/race/"):
                continue

            raise ContractFail(f"Unknown request: url={r.url}")


class RaceResultContract(Contract):
    name = "race_result_contract"

    def post_process(self, output):
        #
        # Check items
        #

        # race info
        items = list(filter(lambda o: isinstance(o, RaceInfoItem), output))

        assert len(items) == 1

        i = items[0]
        assert i["race_id"][0] == "202306020702"
        assert i["race_round"][0].strip() == "2R"
        assert i["race_name"][0].strip() == "3歳未勝利"
        assert i["race_data1"][0].strip() == "10:35発走 / ダ1800m (右)\n/ 天候:雨\n\n/ 馬場:重"
        assert i["race_data2"][0].strip() == "2回\n中山\n7日目\nサラ系３歳\n未勝利\n\xa0\xa0\xa0\xa0\xa0\n(混)[指]\n馬齢\n16頭\n\n本賞金:550,220,140,83,55万円"
        assert i["race_data3"][0].strip() == "３歳未勝利 結果・払戻 | 2023年3月18日 中山2R レース情報(JRA) - netkeiba"

        # race result
        items = list(filter(lambda o: isinstance(o, RaceResultItem), output))

        assert len(items) == 16

        i = items[0]
        assert i["arrival_margin"][0].strip() == ""
        assert i["arrival_time"][0].strip() == "1:54.1"
        assert i["bracket_number"][0].strip() == "5"
        assert i["corner_passing_order"][0].strip() == "1-1-1-1"
        assert i["favorite_order"][0].strip() == "1"
        assert i["final_600_meters_time"][0].strip() == "37.3"
        assert i["horse_id_url"][0].strip() == "https://db.netkeiba.com/horse/2020100583"
        assert i["horse_number"][0].strip() == "9"
        assert i["horse_weight_and_diff"][0].strip() == "518(+2)"
        assert i["jockey_id_url"][0].strip() == "https://db.netkeiba.com/jockey/result/recent/01075/"
        assert i["jockey_weight"][0].strip() == "56.0"
        assert i["race_id"][0].strip() == "202306020702"
        assert i["result"][0].strip() == "1"
        assert i["trainer_id_url"][0].strip() == "https://db.netkeiba.com/trainer/result/recent/01027/"

        i = items[1]
        assert i["arrival_margin"][0].strip() == "2.1/2"
        assert i["arrival_time"][0].strip() == "1:54.5"
        assert i["bracket_number"][0].strip() == "6"
        assert i["corner_passing_order"][0].strip() == "4-4-2-2"
        assert i["favorite_order"][0].strip() == "2"
        assert i["final_600_meters_time"][0].strip() == "37.6"
        assert i["horse_id_url"][0].strip() == "https://db.netkeiba.com/horse/2020103318"
        assert i["horse_number"][0].strip() == "12"
        assert i["horse_weight_and_diff"][0].strip() == "506(-8)"
        assert i["jockey_id_url"][0].strip() == "https://db.netkeiba.com/jockey/result/recent/05339/"
        assert i["jockey_weight"][0].strip() == "56.0"
        assert i["race_id"][0].strip() == "202306020702"
        assert i["result"][0].strip() == "2"
        assert i["trainer_id_url"][0].strip() == "https://db.netkeiba.com/trainer/result/recent/01081/"

        i = items[2]
        assert i["arrival_margin"][0].strip() == "4"
        assert i["arrival_time"][0].strip() == "1:55.2"
        assert i["bracket_number"][0].strip() == "3"
        assert i["corner_passing_order"][0].strip() == "5-5-5-5"
        assert i["favorite_order"][0].strip() == "6"
        assert i["final_600_meters_time"][0].strip() == "37.8"
        assert i["horse_id_url"][0].strip() == "https://db.netkeiba.com/horse/2020104355"
        assert i["horse_number"][0].strip() == "6"
        assert i["horse_weight_and_diff"][0].strip() == "484(+2)"
        assert i["jockey_id_url"][0].strip() == "https://db.netkeiba.com/jockey/result/recent/01184/"
        assert i["jockey_weight"][0].strip() == "54.0"
        assert i["race_id"][0].strip() == "202306020702"
        assert i["result"][0].strip() == "3"
        assert i["trainer_id_url"][0].strip() == "https://db.netkeiba.com/trainer/result/recent/01088/"

        i = items[3]
        assert i["arrival_margin"][0].strip() == "1/2"
        assert i["arrival_time"][0].strip() == "1:55.3"
        assert i["bracket_number"][0].strip() == "7"
        assert i["corner_passing_order"][0].strip() == "11-11-7-7"
        assert i["favorite_order"][0].strip() == "3"
        assert i["final_600_meters_time"][0].strip() == "37.7"
        assert i["horse_id_url"][0].strip() == "https://db.netkeiba.com/horse/2020110020"
        assert i["horse_number"][0].strip() == "14"
        assert i["horse_weight_and_diff"][0].strip() == "474(-2)"
        assert i["jockey_id_url"][0].strip() == "https://db.netkeiba.com/jockey/result/recent/00733/"
        assert i["jockey_weight"][0].strip() == "56.0"
        assert i["race_id"][0].strip() == "202306020702"
        assert i["result"][0].strip() == "4"
        assert i["trainer_id_url"][0].strip() == "https://db.netkeiba.com/trainer/result/recent/01054/"

        i = items[4]
        assert i["arrival_margin"][0].strip() == "アタマ"
        assert i["arrival_time"][0].strip() == "1:55.3"
        assert i["bracket_number"][0].strip() == "1"
        assert i["corner_passing_order"][0].strip() == "12-12-12-11"
        assert i["favorite_order"][0].strip() == "4"
        assert i["final_600_meters_time"][0].strip() == "37.3"
        assert i["horse_id_url"][0].strip() == "https://db.netkeiba.com/horse/2020105372"
        assert i["horse_number"][0].strip() == "2"
        assert i["horse_weight_and_diff"][0].strip() == "492(-2)"
        assert i["jockey_id_url"][0].strip() == "https://db.netkeiba.com/jockey/result/recent/00422/"
        assert i["jockey_weight"][0].strip() == "56.0"
        assert i["race_id"][0].strip() == "202306020702"
        assert i["result"][0].strip() == "5"
        assert i["trainer_id_url"][0].strip() == "https://db.netkeiba.com/trainer/result/recent/01089/"

        i = items[5]
        assert i["arrival_margin"][0].strip() == "クビ"
        assert i["arrival_time"][0].strip() == "1:55.3"
        assert i["bracket_number"][0].strip() == "2"
        assert i["corner_passing_order"][0].strip() == "14-14-9-8"
        assert i["favorite_order"][0].strip() == "11"
        assert i["final_600_meters_time"][0].strip() == "37.4"
        assert i["horse_id_url"][0].strip() == "https://db.netkeiba.com/horse/2020104495"
        assert i["horse_number"][0].strip() == "4"
        assert i["horse_weight_and_diff"][0].strip() == "486(0)"
        assert i["jockey_id_url"][0].strip() == "https://db.netkeiba.com/jockey/result/recent/01117/"
        assert i["jockey_weight"][0].strip() == "56.0"
        assert i["race_id"][0].strip() == "202306020702"
        assert i["result"][0].strip() == "6"
        assert i["trainer_id_url"][0].strip() == "https://db.netkeiba.com/trainer/result/recent/00420/"

        i = items[6]
        assert i["arrival_margin"][0].strip() == "1"
        assert i["arrival_time"][0].strip() == "1:55.5"
        assert i["bracket_number"][0].strip() == "3"
        assert i["corner_passing_order"][0].strip() == "5-5-6-5"
        assert i["favorite_order"][0].strip() == "9"
        assert i["final_600_meters_time"][0].strip() == "38.0"
        assert i["horse_id_url"][0].strip() == "https://db.netkeiba.com/horse/2020100397"
        assert i["horse_number"][0].strip() == "5"
        assert i["horse_weight_and_diff"][0].strip() == "452(+4)"
        assert i["jockey_id_url"][0].strip() == "https://db.netkeiba.com/jockey/result/recent/01192/"
        assert i["jockey_weight"][0].strip() == "54.0"
        assert i["race_id"][0].strip() == "202306020702"
        assert i["result"][0].strip() == "7"
        assert i["trainer_id_url"][0].strip() == "https://db.netkeiba.com/trainer/result/recent/01020/"

        i = items[7]
        assert i["arrival_margin"][0].strip() == "ハナ"
        assert i["arrival_time"][0].strip() == "1:55.5"
        assert i["bracket_number"][0].strip() == "1"
        assert i["corner_passing_order"][0].strip() == "2-2-4-3"
        assert i["favorite_order"][0].strip() == "5"
        assert i["final_600_meters_time"][0].strip() == "38.3"
        assert i["horse_id_url"][0].strip() == "https://db.netkeiba.com/horse/2020110080"
        assert i["horse_number"][0].strip() == "1"
        assert i["horse_weight_and_diff"][0].strip() == "472(-2)"
        assert i["jockey_id_url"][0].strip() == "https://db.netkeiba.com/jockey/result/recent/01170/"
        assert i["jockey_weight"][0].strip() == "54.0"
        assert i["race_id"][0].strip() == "202306020702"
        assert i["result"][0].strip() == "8"
        assert i["trainer_id_url"][0].strip() == "https://db.netkeiba.com/trainer/result/recent/01147/"

        i = items[8]
        assert i["arrival_margin"][0].strip() == "2.1/2"
        assert i["arrival_time"][0].strip() == "1:55.9"
        assert i["bracket_number"][0].strip() == "6"
        assert i["corner_passing_order"][0].strip() == "15-15-14-14"
        assert i["favorite_order"][0].strip() == "12"
        assert i["final_600_meters_time"][0].strip() == "37.0"
        assert i["horse_id_url"][0].strip() == "https://db.netkeiba.com/horse/2020104452"
        assert i["horse_number"][0].strip() == "11"
        assert i["horse_weight_and_diff"][0].strip() == "460(0)"
        assert i["jockey_id_url"][0].strip() == "https://db.netkeiba.com/jockey/result/recent/01206/"
        assert i["jockey_weight"][0].strip() == "52.0"
        assert i["race_id"][0].strip() == "202306020702"
        assert i["result"][0].strip() == "9"
        assert i["trainer_id_url"][0].strip() == "https://db.netkeiba.com/trainer/result/recent/01010/"

        i = items[9]
        assert i["arrival_margin"][0].strip() == "1/2"
        assert i["arrival_time"][0].strip() == "1:56.0"
        assert i["bracket_number"][0].strip() == "4"
        assert i["corner_passing_order"][0].strip() == "9-9-13-11"
        assert i["favorite_order"][0].strip() == "10"
        assert i["final_600_meters_time"][0].strip() == "37.9"
        assert i["horse_id_url"][0].strip() == "https://db.netkeiba.com/horse/2020100274"
        assert i["horse_number"][0].strip() == "8"
        assert i["horse_weight_and_diff"][0].strip() == "424(-10)"
        assert i["jockey_id_url"][0].strip() == "https://db.netkeiba.com/jockey/result/recent/01096/"
        assert i["jockey_weight"][0].strip() == "56.0"
        assert i["race_id"][0].strip() == "202306020702"
        assert i["result"][0].strip() == "10"
        assert i["trainer_id_url"][0].strip() == "https://db.netkeiba.com/trainer/result/recent/01100/"

        i = items[10]
        assert i["arrival_margin"][0].strip() == "1.1/4"
        assert i["arrival_time"][0].strip() == "1:56.2"
        assert i["bracket_number"][0].strip() == "8"
        assert i["corner_passing_order"][0].strip() == "9-9-9-10"
        assert i["favorite_order"][0].strip() == "14"
        assert i["final_600_meters_time"][0].strip() == "38.3"
        assert i["horse_id_url"][0].strip() == "https://db.netkeiba.com/horse/2020101092"
        assert i["horse_number"][0].strip() == "15"
        assert i["horse_weight_and_diff"][0].strip() == "468(-6)"
        assert i["jockey_id_url"][0].strip() == "https://db.netkeiba.com/jockey/result/recent/01162/"
        assert i["jockey_weight"][0].strip() == "56.0"
        assert i["race_id"][0].strip() == "202306020702"
        assert i["result"][0].strip() == "11"
        assert i["trainer_id_url"][0].strip() == "https://db.netkeiba.com/trainer/result/recent/00423/"

        i = items[11]
        assert i["arrival_margin"][0].strip() == "1.3/4"
        assert i["arrival_time"][0].strip() == "1:56.5"
        assert i["bracket_number"][0].strip() == "4"
        assert i["corner_passing_order"][0].strip() == "7-8-9-11"
        assert i["favorite_order"][0].strip() == "7"
        assert i["final_600_meters_time"][0].strip() == "38.6"
        assert i["horse_id_url"][0].strip() == "https://db.netkeiba.com/horse/2020109101"
        assert i["horse_number"][0].strip() == "7"
        assert i["horse_weight_and_diff"][0].strip() == "458(-8)"
        assert i["jockey_id_url"][0].strip() == "https://db.netkeiba.com/jockey/result/recent/01092/"
        assert i["jockey_weight"][0].strip() == "56.0"
        assert i["race_id"][0].strip() == "202306020702"
        assert i["result"][0].strip() == "12"
        assert i["trainer_id_url"][0].strip() == "https://db.netkeiba.com/trainer/result/recent/01086/"

        i = items[12]
        assert i["arrival_margin"][0].strip() == "1/2"
        assert i["arrival_time"][0].strip() == "1:56.6"
        assert i["bracket_number"][0].strip() == "8"
        assert i["corner_passing_order"][0].strip() == "2-2-2-3"
        assert i["favorite_order"][0].strip() == "8"
        assert i["final_600_meters_time"][0].strip() == "39.7"
        assert i["horse_id_url"][0].strip() == "https://db.netkeiba.com/horse/2020109130"
        assert i["horse_number"][0].strip() == "16"
        assert i["horse_weight_and_diff"][0].strip() == "470(+4)"
        assert i["jockey_id_url"][0].strip() == "https://db.netkeiba.com/jockey/result/recent/01161/"
        assert i["jockey_weight"][0].strip() == "56.0"
        assert i["race_id"][0].strip() == "202306020702"
        assert i["result"][0].strip() == "13"
        assert i["trainer_id_url"][0].strip() == "https://db.netkeiba.com/trainer/result/recent/01115/"

        i = items[13]
        assert i["arrival_margin"][0].strip() == "クビ"
        assert i["arrival_time"][0].strip() == "1:56.6"
        assert i["bracket_number"][0].strip() == "5"
        assert i["corner_passing_order"][0].strip() == "7-7-8-8"
        assert i["favorite_order"][0].strip() == "13"
        assert i["final_600_meters_time"][0].strip() == "38.8"
        assert i["horse_id_url"][0].strip() == "https://db.netkeiba.com/horse/2020106142"
        assert i["horse_number"][0].strip() == "10"
        assert i["horse_weight_and_diff"][0].strip() == "516(0)"
        assert i["jockey_id_url"][0].strip() == "https://db.netkeiba.com/jockey/result/recent/01009/"
        assert i["jockey_weight"][0].strip() == "56.0"
        assert i["race_id"][0].strip() == "202306020702"
        assert i["result"][0].strip() == "14"
        assert i["trainer_id_url"][0].strip() == "https://db.netkeiba.com/trainer/result/recent/01143/"

        i = items[14]
        assert i["arrival_margin"][0].strip() == "大"
        assert i["arrival_time"][0].strip() == "1:59.7"
        assert i["bracket_number"][0].strip() == "2"
        assert i["corner_passing_order"][0].strip() == "16-16-16-15"
        assert i["favorite_order"][0].strip() == "15"
        assert i["final_600_meters_time"][0].strip() == "39.6"
        assert i["horse_id_url"][0].strip() == "https://db.netkeiba.com/horse/2020103272"
        assert i["horse_number"][0].strip() == "3"
        assert i["horse_weight_and_diff"][0].strip() == "484(0)"
        assert i["jockey_id_url"][0].strip() == "https://db.netkeiba.com/jockey/result/recent/01169/"
        assert i["jockey_weight"][0].strip() == "56.0"
        assert i["race_id"][0].strip() == "202306020702"
        assert i["result"][0].strip() == "15"
        assert i["trainer_id_url"][0].strip() == "https://db.netkeiba.com/trainer/result/recent/00420/"

        i = items[15]
        assert i["arrival_margin"][0].strip() == "6"
        assert i["arrival_time"][0].strip() == "2:00.7"
        assert i["bracket_number"][0].strip() == "7"
        assert i["corner_passing_order"][0].strip() == "12-13-15-16"
        assert i["favorite_order"][0].strip() == "16"
        assert i["final_600_meters_time"][0].strip() == "40.7"
        assert i["horse_id_url"][0].strip() == "https://db.netkeiba.com/horse/2020100043"
        assert i["horse_number"][0].strip() == "13"
        assert i["horse_weight_and_diff"][0].strip() == "468(0)"
        assert i["jockey_id_url"][0].strip() == "https://db.netkeiba.com/jockey/result/recent/01177/"
        assert i["jockey_weight"][0].strip() == "54.0"
        assert i["race_id"][0].strip() == "202306020702"
        assert i["result"][0].strip() == "16"
        assert i["trainer_id_url"][0].strip() == "https://db.netkeiba.com/trainer/result/recent/01026/"

        # race payoff
        items = list(filter(lambda o: isinstance(o, RacePayoffItem), output))

        assert len(items) == 8

        i = items[0]
        assert i["betting_type"] == ["単勝"]
        assert i["horse_numbers"] == ["9"]
        assert i["payoff"] == ["120円"]
        assert i["race_id"] == ["202306020702"]

        i = items[1]
        assert i["betting_type"] == ["複勝"]
        assert i["horse_numbers"] == ["9", "12", "6"]
        assert i["payoff"] == ["100円", "110円", "220円"]
        assert i["race_id"] == ["202306020702"]

        i = items[2]
        assert i["betting_type"] == ["枠連"]
        assert i["horse_numbers"] == ["5", "6"]
        assert i["payoff"] == ["180円"]
        assert i["race_id"] == ["202306020702"]

        i = items[3]
        assert i["betting_type"] == ["馬連"]
        assert i["horse_numbers"] == ["9", "12"]
        assert i["payoff"] == ["170円"]
        assert i["race_id"] == ["202306020702"]

        i = items[4]
        assert i["betting_type"] == ["ワイド"]
        assert i["horse_numbers"] == ["9", "12", "6", "9", "6", "12"]
        assert i["payoff"] == ["130円", "360円", "740円"]
        assert i["race_id"] == ["202306020702"]

        i = items[5]
        assert i["betting_type"] == ["馬単"]
        assert i["horse_numbers"] == ["9", "12"]
        assert i["payoff"] == ["250円"]
        assert i["race_id"] == ["202306020702"]

        i = items[6]
        assert i["betting_type"] == ["3連複"]
        assert i["horse_numbers"] == ["6", "9", "12"]
        assert i["payoff"] == ["880円"]
        assert i["race_id"] == ["202306020702"]

        i = items[7]
        assert i["betting_type"] == ["3連単"]
        assert i["horse_numbers"] == ["9", "12", "6"]
        assert i["payoff"] == ["1,900円"]
        assert i["race_id"] == ["202306020702"]

        # race corner passing
        items = list(filter(lambda o: isinstance(o, RaceCornerPassingItem), output))

        assert len(items) == 1

        i = items[0]
        assert i["corner_name"] == ["<th><strong>1</strong>コーナー</th>", "<th><strong>2</strong>コーナー</th>", "<th><strong>3</strong>コーナー</th>", "<th><strong>4</strong>コーナー</th>"]
        assert i["passing_order"] == ['<td><span class="fwB Corner_Num01">9</span>(1,16)<span class="fwB Corner_Num02">12</span>(5,<span class="fwB Corner_Num03">6</span>)(7,10)(8,15)14(2,13)4-11=3</td>', '<td><span class="fwB Corner_Num01">9</span>(1,16)<span class="fwB Corner_Num02">12</span>(5,<span class="fwB Corner_Num03">6</span>)10,7(8,15)14,2,13,4-11=3</td>', '<td><span class="fwB Corner_Num01">9</span>(16,<span class="fwB Corner_Num02">12</span>)1,<span class="fwB Corner_Num03">6</span>,5,14,10(7,15,4)2,8-11=13,3</td>', '<td><span class="fwB Corner_Num01">9</span>,<span class="fwB Corner_Num02">12</span>(1,16)(5,<span class="fwB Corner_Num03">6</span>)14(10,4)15(7,8,2)-11=3,13</td>']
        assert i["race_id"] == ["202306020702"]

        # race lap time
        items = list(filter(lambda o: isinstance(o, RaceLapTimeItem), output))

        assert len(items) == 1

        i = items[0]
        assert i["length"] == ["200m", "400m", "600m", "800m", "1000m", "1200m", "1400m", "1600m", "1800m"]
        assert i["race_id"] == ["202306020702"]
        assert i["time1"] == ["12.8", "25.3", "38.5", "52.0", "1:04.6", "1:16.8", "1:29.3", "1:41.6", "1:54.1"]
        assert i["time2"] == ["12.8", "12.5", "13.2", "13.5", "12.6", "12.2", "12.5", "12.3", "12.5"]

        #
        # Check requests
        #
        requests = list(filter(lambda o: isinstance(o, Request), output))

        # odds page
        odds_page_links = list(filter(lambda r: r.url.startswith("https://race.netkeiba.com/api/api_get_jra_odds.html?type="), requests))

        assert len(odds_page_links) == 7

        # training page
        training_page_links = list(filter(lambda r: r.url.startswith("https://race.netkeiba.com/race/oikiri.html?race_id="), requests))

        assert len(training_page_links) == 1

        # horse page
        horse_page_links = list(filter(lambda r: r.url.startswith("https://db.netkeiba.com/v1.1/?pid=api_db_horse_info_simple"), requests))

        assert len(horse_page_links) == 16

        # parent horse page
        parent_horse_page_links = list(filter(lambda r: r.url.startswith("https://db.netkeiba.com/horse/ped/"), requests))

        assert len(parent_horse_page_links) == 16

        # jockey page
        jockey_page_links = list(filter(lambda r: r.url.startswith("https://db.netkeiba.com/jockey/"), requests))

        assert len(jockey_page_links) == 16

        # trainer page
        trainer_page_links = list(filter(lambda r: r.url.startswith("https://db.netkeiba.com/trainer/"), requests))

        assert len(trainer_page_links) == 16


class OddsWinPlaceContract(Contract):
    name = "odds_win_place_contract"

    def post_process(self, output):
        #
        # Check items
        #

        odds_items = list(filter(lambda o: isinstance(o, OddsItem), output))

        assert len(odds_items) == 32

        # win odds
        items = list(filter(lambda i: i["odds_type"] == [1], odds_items))

        assert len(items) == 16

        i = items[0]
        assert i["favorite_order"] == ["5"]
        assert i["horse_number"] == ["01"]
        assert i["odds1"] == ["32.8"]
        assert i["odds2"] == [""]
        assert i["odds_type"] == [1]
        assert i["race_id"] == ["202306020702"]

        i = items[1]
        assert i["favorite_order"] == ["4"]
        assert i["horse_number"] == ["02"]
        assert i["odds1"] == ["27.9"]
        assert i["odds2"] == [""]
        assert i["odds_type"] == [1]
        assert i["race_id"] == ["202306020702"]

        i = items[2]
        assert i["favorite_order"] == ["15"]
        assert i["horse_number"] == ["03"]
        assert i["odds1"] == ["274.1"]
        assert i["odds2"] == [""]
        assert i["odds_type"] == [1]
        assert i["race_id"] == ["202306020702"]

        i = items[3]
        assert i["favorite_order"] == ["11"]
        assert i["horse_number"] == ["04"]
        assert i["odds1"] == ["154.6"]
        assert i["odds2"] == [""]
        assert i["odds_type"] == [1]
        assert i["race_id"] == ["202306020702"]

        i = items[4]
        assert i["favorite_order"] == ["9"]
        assert i["horse_number"] == ["05"]
        assert i["odds1"] == ["113.5"]
        assert i["odds2"] == [""]
        assert i["odds_type"] == [1]
        assert i["race_id"] == ["202306020702"]

        i = items[5]
        assert i["favorite_order"] == ["6"]
        assert i["horse_number"] == ["06"]
        assert i["odds1"] == ["36.7"]
        assert i["odds2"] == [""]
        assert i["odds_type"] == [1]
        assert i["race_id"] == ["202306020702"]

        i = items[6]
        assert i["favorite_order"] == ["7"]
        assert i["horse_number"] == ["07"]
        assert i["odds1"] == ["66.0"]
        assert i["odds2"] == [""]
        assert i["odds_type"] == [1]
        assert i["race_id"] == ["202306020702"]

        i = items[7]
        assert i["favorite_order"] == ["10"]
        assert i["horse_number"] == ["08"]
        assert i["odds1"] == ["140.9"]
        assert i["odds2"] == [""]
        assert i["odds_type"] == [1]
        assert i["race_id"] == ["202306020702"]

        i = items[8]
        assert i["favorite_order"] == ["1"]
        assert i["horse_number"] == ["09"]
        assert i["odds1"] == ["1.2"]
        assert i["odds2"] == [""]
        assert i["odds_type"] == [1]
        assert i["race_id"] == ["202306020702"]

        i = items[9]
        assert i["favorite_order"] == ["13"]
        assert i["horse_number"] == ["10"]
        assert i["odds1"] == ["254.1"]
        assert i["odds2"] == [""]
        assert i["odds_type"] == [1]
        assert i["race_id"] == ["202306020702"]

        i = items[10]
        assert i["favorite_order"] == ["12"]
        assert i["horse_number"] == ["11"]
        assert i["odds1"] == ["187.3"]
        assert i["odds2"] == [""]
        assert i["odds_type"] == [1]
        assert i["race_id"] == ["202306020702"]

        i = items[11]
        assert i["favorite_order"] == ["2"]
        assert i["horse_number"] == ["12"]
        assert i["odds1"] == ["4.0"]
        assert i["odds2"] == [""]
        assert i["odds_type"] == [1]
        assert i["race_id"] == ["202306020702"]

        i = items[12]
        assert i["favorite_order"] == ["16"]
        assert i["horse_number"] == ["13"]
        assert i["odds1"] == ["700.7"]
        assert i["odds2"] == [""]
        assert i["odds_type"] == [1]
        assert i["race_id"] == ["202306020702"]

        i = items[13]
        assert i["favorite_order"] == ["3"]
        assert i["horse_number"] == ["14"]
        assert i["odds1"] == ["22.4"]
        assert i["odds2"] == [""]
        assert i["odds_type"] == [1]
        assert i["race_id"] == ["202306020702"]

        i = items[14]
        assert i["favorite_order"] == ["14"]
        assert i["horse_number"] == ["15"]
        assert i["odds1"] == ["258.0"]
        assert i["odds2"] == [""]
        assert i["odds_type"] == [1]
        assert i["race_id"] == ["202306020702"]

        i = items[15]
        assert i["favorite_order"] == ["8"]
        assert i["horse_number"] == ["16"]
        assert i["odds1"] == ["76.6"]
        assert i["odds2"] == [""]
        assert i["odds_type"] == [1]
        assert i["race_id"] == ["202306020702"]

        # place odds
        items = list(filter(lambda i: i["odds_type"] == [2], odds_items))

        assert len(items) == 16

        i = items[0]
        assert i["favorite_order"] == ["6"]
        assert i["horse_number"] == ["01"]
        assert i["odds1"] == ["3.2"]
        assert i["odds2"] == ["24.2"]
        assert i["odds_type"] == [2]
        assert i["race_id"] == ["202306020702"]

        i = items[1]
        assert i["favorite_order"] == ["3"]
        assert i["horse_number"] == ["02"]
        assert i["odds1"] == ["1.6"]
        assert i["odds2"] == ["10.5"]
        assert i["odds_type"] == [2]
        assert i["race_id"] == ["202306020702"]

        i = items[2]
        assert i["favorite_order"] == ["15"]
        assert i["horse_number"] == ["03"]
        assert i["odds1"] == ["21.6"]
        assert i["odds2"] == ["186.5"]
        assert i["odds_type"] == [2]
        assert i["race_id"] == ["202306020702"]

        i = items[3]
        assert i["favorite_order"] == ["12"]
        assert i["horse_number"] == ["04"]
        assert i["odds1"] == ["15.5"]
        assert i["odds2"] == ["132.1"]
        assert i["odds_type"] == [2]
        assert i["race_id"] == ["202306020702"]

        i = items[4]
        assert i["favorite_order"] == ["10"]
        assert i["horse_number"] == ["05"]
        assert i["odds1"] == ["7.4"]
        assert i["odds2"] == ["61.5"]
        assert i["odds_type"] == [2]
        assert i["race_id"] == ["202306020702"]

        i = items[5]
        assert i["favorite_order"] == ["5"]
        assert i["horse_number"] == ["06"]
        assert i["odds1"] == ["2.2"]
        assert i["odds2"] == ["15.5"]
        assert i["odds_type"] == [2]
        assert i["race_id"] == ["202306020702"]

        i = items[6]
        assert i["favorite_order"] == ["7"]
        assert i["horse_number"] == ["07"]
        assert i["odds1"] == ["4.0"]
        assert i["odds2"] == ["31.4"]
        assert i["odds_type"] == [2]
        assert i["race_id"] == ["202306020702"]

        i = items[7]
        assert i["favorite_order"] == ["9"]
        assert i["horse_number"] == ["08"]
        assert i["odds1"] == ["5.5"]
        assert i["odds2"] == ["45.0"]
        assert i["odds_type"] == [2]
        assert i["race_id"] == ["202306020702"]

        i = items[8]
        assert i["favorite_order"] == ["1"]
        assert i["horse_number"] == ["09"]
        assert i["odds1"] == ["1.0"]
        assert i["odds2"] == ["1.1"]
        assert i["odds_type"] == [2]
        assert i["race_id"] == ["202306020702"]

        i = items[9]
        assert i["favorite_order"] == ["14"]
        assert i["horse_number"] == ["10"]
        assert i["odds1"] == ["19.9"]
        assert i["odds2"] == ["171.5"]
        assert i["odds_type"] == [2]
        assert i["race_id"] == ["202306020702"]

        i = items[10]
        assert i["favorite_order"] == ["11"]
        assert i["horse_number"] == ["11"]
        assert i["odds1"] == ["10.2"]
        assert i["odds2"] == ["86.1"]
        assert i["odds_type"] == [2]
        assert i["race_id"] == ["202306020702"]

        i = items[11]
        assert i["favorite_order"] == ["2"]
        assert i["horse_number"] == ["12"]
        assert i["odds1"] == ["1.1"]
        assert i["odds2"] == ["4.6"]
        assert i["odds_type"] == [2]
        assert i["race_id"] == ["202306020702"]

        i = items[12]
        assert i["favorite_order"] == ["16"]
        assert i["horse_number"] == ["13"]
        assert i["odds1"] == ["47.7"]
        assert i["odds2"] == ["415.7"]
        assert i["odds_type"] == [2]
        assert i["race_id"] == ["202306020702"]

        i = items[13]
        assert i["favorite_order"] == ["4"]
        assert i["horse_number"] == ["14"]
        assert i["odds1"] == ["1.9"]
        assert i["odds2"] == ["12.9"]
        assert i["odds_type"] == [2]
        assert i["race_id"] == ["202306020702"]

        i = items[14]
        assert i["favorite_order"] == ["13"]
        assert i["horse_number"] == ["15"]
        assert i["odds1"] == ["19.8"]
        assert i["odds2"] == ["170.1"]
        assert i["odds_type"] == [2]
        assert i["race_id"] == ["202306020702"]

        i = items[15]
        assert i["favorite_order"] == ["8"]
        assert i["horse_number"] == ["16"]
        assert i["odds1"] == ["4.6"]
        assert i["odds2"] == ["36.8"]
        assert i["odds_type"] == [2]
        assert i["race_id"] == ["202306020702"]


class OddsBracketQuinellaContract(Contract):
    name = "odds_bracket_quinella_contract"

    def post_process(self, output):
        #
        # Check items
        #

        odds_items = list(filter(lambda o: isinstance(o, OddsItem), output))

        items = list(filter(lambda i: i["odds_type"] == [3], odds_items))

        assert len(odds_items) == len(items)

        i = items[0]
        assert i["favorite_order"] == ["20"]
        assert i["horse_number"] == ["0101"]
        assert i["odds1"] == ["154.3"]
        assert i["odds2"] == [""]
        assert i["odds_type"] == [3]
        assert i["race_id"] == ["202306020702"]

        i = items[1]
        assert i["favorite_order"] == ["22"]
        assert i["horse_number"] == ["0102"]
        assert i["odds1"] == ["186.4"]
        assert i["odds2"] == [""]
        assert i["odds_type"] == [3]
        assert i["race_id"] == ["202306020702"]

        i = items[34]
        assert i["favorite_order"] == ["23"]
        assert i["horse_number"] == ["0708"]
        assert i["odds1"] == ["193.0"]
        assert i["odds2"] == [""]
        assert i["odds_type"] == [3]
        assert i["race_id"] == ["202306020702"]

        i = items[35]
        assert i["favorite_order"] == ["35"]
        assert i["horse_number"] == ["0808"]
        assert i["odds1"] == ["1717.1"]
        assert i["odds2"] == [""]
        assert i["odds_type"] == [3]
        assert i["race_id"] == ["202306020702"]


class OddsQuinellaContract(Contract):
    name = "odds_quinella_contract"

    def post_process(self, output):
        #
        # Check items
        #

        odds_items = list(filter(lambda o: isinstance(o, OddsItem), output))

        items = list(filter(lambda i: i["odds_type"] == [4], odds_items))

        assert len(odds_items) == len(items)

        i = items[0]
        assert i["favorite_order"] == ["21"]
        assert i["horse_number"] == ["0102"]
        assert i["odds1"] == ["140.4"]
        assert i["odds2"] == [""]
        assert i["odds_type"] == [4]
        assert i["race_id"] == ["202306020702"]

        i = items[1]
        assert i["favorite_order"] == ["69"]
        assert i["horse_number"] == ["0103"]
        assert i["odds1"] == ["1767.9"]
        assert i["odds2"] == [""]
        assert i["odds_type"] == [4]
        assert i["race_id"] == ["202306020702"]

        i = items[118]
        assert i["favorite_order"] == ["40"]
        assert i["horse_number"] == ["1416"]
        assert i["odds1"] == ["530.8"]
        assert i["odds2"] == [""]
        assert i["odds_type"] == [4]
        assert i["race_id"] == ["202306020702"]

        i = items[119]
        assert i["favorite_order"] == ["96"]
        assert i["horse_number"] == ["1516"]
        assert i["odds1"] == ["4362.2"]
        assert i["odds2"] == [""]
        assert i["odds_type"] == [4]
        assert i["race_id"] == ["202306020702"]


class OddsQuinellaPlaceContract(Contract):
    name = "odds_quinella_place_contract"

    def post_process(self, output):
        #
        # Check items
        #

        odds_items = list(filter(lambda o: isinstance(o, OddsItem), output))

        items = list(filter(lambda i: i["odds_type"] == [5], odds_items))

        assert len(odds_items) == len(items)

        i = items[0]
        assert i["favorite_order"] == ["22"]
        assert i["horse_number"] == ["0102"]
        assert i["odds1"] == ["24.1"]
        assert i["odds2"] == ["26.9"]
        assert i["odds_type"] == [5]
        assert i["race_id"] == ["202306020702"]

        i = items[1]
        assert i["favorite_order"] == ["79"]
        assert i["horse_number"] == ["0103"]
        assert i["odds1"] == ["331.2"]
        assert i["odds2"] == ["349.0"]
        assert i["odds_type"] == [5]
        assert i["race_id"] == ["202306020702"]

        i = items[118]
        assert i["favorite_order"] == ["31"]
        assert i["horse_number"] == ["1416"]
        assert i["odds1"] == ["45.5"]
        assert i["odds2"] == ["51.6"]
        assert i["odds_type"] == [5]
        assert i["race_id"] == ["202306020702"]

        i = items[119]
        assert i["favorite_order"] == ["85"]
        assert i["horse_number"] == ["1516"]
        assert i["odds1"] == ["450.4"]
        assert i["odds2"] == ["468.1"]
        assert i["odds_type"] == [5]
        assert i["race_id"] == ["202306020702"]


class OddsExactaContract(Contract):
    name = "odds_exacta_contract"

    def post_process(self, output):
        #
        # Check items
        #

        odds_items = list(filter(lambda o: isinstance(o, OddsItem), output))

        items = list(filter(lambda i: i["odds_type"] == [6], odds_items))

        assert len(odds_items) == len(items)

        i = items[0]
        assert i["favorite_order"] == ["44"]
        assert i["horse_number"] == ["0102"]
        assert i["odds1"] == ["391.5"]
        assert i["odds2"] == [""]
        assert i["odds_type"] == [6]
        assert i["race_id"] == ["202306020702"]

        i = items[1]
        assert i["favorite_order"] == ["139"]
        assert i["horse_number"] == ["0103"]
        assert i["odds1"] == ["4791.5"]
        assert i["odds2"] == [""]
        assert i["odds_type"] == [6]
        assert i["race_id"] == ["202306020702"]

        i = items[238]
        assert i["favorite_order"] == ["76"]
        assert i["horse_number"] == ["1614"]
        assert i["odds1"] == ["1121.4"]
        assert i["odds2"] == [""]
        assert i["odds_type"] == [6]
        assert i["race_id"] == ["202306020702"]

        i = items[239]
        assert i["favorite_order"] == ["195"]
        assert i["horse_number"] == ["1615"]
        assert i["odds1"] == ["13870.3"]
        assert i["odds2"] == [""]
        assert i["odds_type"] == [6]
        assert i["race_id"] == ["202306020702"]


class OddsTrioContract(Contract):
    name = "odds_trio_contract"

    def post_process(self, output):
        #
        # Check items
        #

        odds_items = list(filter(lambda o: isinstance(o, OddsItem), output))

        items = list(filter(lambda i: i["odds_type"] == [7], odds_items))

        assert len(odds_items) == len(items)

        i = items[0]
        assert i["favorite_order"] == ["154"]
        assert i["horse_number"] == ["010203"]
        assert i["odds1"] == ["2028.6"]
        assert i["odds2"] == [""]
        assert i["odds_type"] == [7]
        assert i["race_id"] == ["202306020702"]

        i = items[1]
        assert i["favorite_order"] == ["167"]
        assert i["horse_number"] == ["010204"]
        assert i["odds1"] == ["2302.1"]
        assert i["odds2"] == [""]
        assert i["odds_type"] == [7]
        assert i["race_id"] == ["202306020702"]

        i = items[558]
        assert i["favorite_order"] == ["364"]
        assert i["horse_number"] == ["131516"]
        assert i["odds1"] == ["17074.3"]
        assert i["odds2"] == [""]
        assert i["odds_type"] == [7]
        assert i["race_id"] == ["202306020702"]

        i = items[559]
        assert i["favorite_order"] == ["245"]
        assert i["horse_number"] == ["141516"]
        assert i["odds1"] == ["5744.6"]
        assert i["odds2"] == [""]
        assert i["odds_type"] == [7]
        assert i["race_id"] == ["202306020702"]


class OddsTrifectaContract(Contract):
    name = "odds_trifecta_contract"

    def post_process(self, output):
        #
        # Check items
        #

        odds_items = list(filter(lambda o: isinstance(o, OddsItem), output))

        items = list(filter(lambda i: i["odds_type"] == [8], odds_items))

        assert len(odds_items) == len(items)

        i = items[0]
        assert i["favorite_order"] == ["805"]
        assert i["horse_number"] == ["010203"]
        assert i["odds1"] == ["14182.1"]
        assert i["odds2"] == [""]
        assert i["odds_type"] == [8]
        assert i["race_id"] == ["202306020702"]

        i = items[1]
        assert i["favorite_order"] == ["998"]
        assert i["horse_number"] == ["010204"]
        assert i["odds1"] == ["23273.2"]
        assert i["odds2"] == [""]
        assert i["odds_type"] == [8]
        assert i["race_id"] == ["202306020702"]

        i = items[3358]
        assert i["favorite_order"] == ["2632"]
        assert i["horse_number"] == ["161513"]
        assert i["odds1"] == ["302552.1"]
        assert i["odds2"] == [""]
        assert i["odds_type"] == [8]
        assert i["race_id"] == ["202306020702"]

        i = items[3359]
        assert i["favorite_order"] == ["2139"]
        assert i["horse_number"] == ["161514"]
        assert i["odds1"] == ["151276.0"]
        assert i["odds2"] == [""]
        assert i["odds_type"] == [8]
        assert i["race_id"] == ["202306020702"]


class TrainingContract(Contract):
    name = "training_contract"

    def post_process(self, output):
        #
        # Check items
        #

        items = list(filter(lambda i: isinstance(i, TrainingItem), output))

        i = items[0]
        assert i["evaluation_rank"] == ["B"]
        assert i["evaluation_text"] == ["変身十分"]
        assert i["horse_id_url"] == ["https://db.netkeiba.com/horse/2020110080"]
        assert i["horse_number"] == ["1"]
        assert i["race_id"] == ["202306020702"]

        i = items[1]
        assert i["evaluation_rank"] == ["B"]
        assert i["evaluation_text"] == ["動き良化"]
        assert i["horse_id_url"] == ["https://db.netkeiba.com/horse/2020105372"]
        assert i["horse_number"] == ["1"]
        assert i["race_id"] == ["202306020702"]

        i = items[2]
        assert i["evaluation_rank"] == ["D"]
        assert i["evaluation_text"] == ["動き平凡"]
        assert i["horse_id_url"] == ["https://db.netkeiba.com/horse/2020103272"]
        assert i["horse_number"] == ["2"]
        assert i["race_id"] == ["202306020702"]

        i = items[3]
        assert i["evaluation_rank"] == ["C"]
        assert i["evaluation_text"] == ["仕上十分"]
        assert i["horse_id_url"] == ["https://db.netkeiba.com/horse/2020104495"]
        assert i["horse_number"] == ["2"]
        assert i["race_id"] == ["202306020702"]

        i = items[4]
        assert i["evaluation_rank"] == ["B"]
        assert i["evaluation_text"] == ["動き良化"]
        assert i["horse_id_url"] == ["https://db.netkeiba.com/horse/2020100397"]
        assert i["horse_number"] == ["3"]
        assert i["race_id"] == ["202306020702"]

        i = items[5]
        assert i["evaluation_rank"] == ["C"]
        assert i["evaluation_text"] == ["多少良化"]
        assert i["horse_id_url"] == ["https://db.netkeiba.com/horse/2020104355"]
        assert i["horse_number"] == ["3"]
        assert i["race_id"] == ["202306020702"]

        i = items[6]
        assert i["evaluation_rank"] == ["C"]
        assert i["evaluation_text"] == ["まずまず"]
        assert i["horse_id_url"] == ["https://db.netkeiba.com/horse/2020109101"]
        assert i["horse_number"] == ["4"]
        assert i["race_id"] == ["202306020702"]

        i = items[7]
        assert i["evaluation_rank"] == ["C"]
        assert i["evaluation_text"] == ["反応平凡"]
        assert i["horse_id_url"] == ["https://db.netkeiba.com/horse/2020100274"]
        assert i["horse_number"] == ["4"]
        assert i["race_id"] == ["202306020702"]

        i = items[8]
        assert i["evaluation_rank"] == ["B"]
        assert i["evaluation_text"] == ["好調子"]
        assert i["horse_id_url"] == ["https://db.netkeiba.com/horse/2020100583"]
        assert i["horse_number"] == ["5"]
        assert i["race_id"] == ["202306020702"]

        i = items[9]
        assert i["evaluation_rank"] == ["C"]
        assert i["evaluation_text"] == ["気配平凡"]
        assert i["horse_id_url"] == ["https://db.netkeiba.com/horse/2020106142"]
        assert i["horse_number"] == ["5"]
        assert i["race_id"] == ["202306020702"]

        i = items[10]
        assert i["evaluation_rank"] == ["B"]
        assert i["evaluation_text"] == ["動き上々"]
        assert i["horse_id_url"] == ["https://db.netkeiba.com/horse/2020104452"]
        assert i["horse_number"] == ["6"]
        assert i["race_id"] == ["202306020702"]

        i = items[11]
        assert i["evaluation_rank"] == ["B"]
        assert i["evaluation_text"] == ["力強い"]
        assert i["horse_id_url"] == ["https://db.netkeiba.com/horse/2020103318"]
        assert i["horse_number"] == ["6"]
        assert i["race_id"] == ["202306020702"]

        i = items[12]
        assert i["evaluation_rank"] == ["C"]
        assert i["evaluation_text"] == ["目立たず"]
        assert i["horse_id_url"] == ["https://db.netkeiba.com/horse/2020100043"]
        assert i["horse_number"] == ["7"]
        assert i["race_id"] == ["202306020702"]

        i = items[13]
        assert i["evaluation_rank"] == ["B"]
        assert i["evaluation_text"] == ["好調持続"]
        assert i["horse_id_url"] == ["https://db.netkeiba.com/horse/2020110020"]
        assert i["horse_number"] == ["7"]
        assert i["race_id"] == ["202306020702"]

        i = items[14]
        assert i["evaluation_rank"] == ["B"]
        assert i["evaluation_text"] == ["力強い"]
        assert i["horse_id_url"] == ["https://db.netkeiba.com/horse/2020101092"]
        assert i["horse_number"] == ["8"]
        assert i["race_id"] == ["202306020702"]

        i = items[15]
        assert i["evaluation_rank"] == ["B"]
        assert i["evaluation_text"] == ["好気配"]
        assert i["horse_id_url"] == ["https://db.netkeiba.com/horse/2020109130"]
        assert i["horse_number"] == ["8"]
        assert i["race_id"] == ["202306020702"]


class HorseContract(Contract):
    name = "horse_contract"

    def post_process(self, output):
        #
        # Check items
        #

        items = list(filter(lambda i: isinstance(i, HorseItem), output))

        i = items[0]
        assert i["birthday"] == ["2020-04-24"]
        assert i["breeder_id"] == ["510045"]
        assert i["coat_color"] == ["03"]
        assert i["farm"] == ["浦河町"]
        assert i["gender"] == ["3"]
        assert i["horse_id"] == ["2020100583"]
        assert i["horse_name"] == ["レイズカイザー"]
        assert i["kigo"] == ["00"]
        assert i["owner_id"] == ["652031"]
        assert i["seri_name"] == ["2021年 北海道セレクションセール"]
        assert i["seri_price"] == ["31900000"]
        assert i["tozai"] == ["1"]
        assert i["trainer_id"] == ["01027"]


class ParentHorseContract(Contract):
    name = "parent_horse_contract"

    def post_process(self, output):
        #
        # Check items
        #

        items = list(filter(lambda i: isinstance(i, ParentHorseItem), output))

        i = items[0]
        assert i["parent_horse_id"] == ["/horse/ped/2020100583/"]
        assert i["parent1_id"] == [
            "/horse/000a011155/",
            "/horse/2013102789/",
        ]
        assert i["parent2_id"] == [
            "/horse/000a000178/",
            "/horse/000a01117d/",
            "/horse/000a010542/",
            "/horse/2005101307/",
        ]
        assert i["parent3_id"] == [
            "/horse/000a001a98/",
            "/horse/000a00a104/",
            "/horse/000a001c0e/",
            "/horse/000a009e3b/",
            "/horse/000a001cd0/",
            "/horse/000a01008f/",
            "/horse/1995108676/",
            "/horse/1992100605/",
        ]
        assert i["parent4_id"] == [
            "/horse/000a0016d4/",
            "/horse/000a008e05/",
            "/horse/000a0010d6/",
            "/horse/000a009f23/",
            "/horse/000a00184d/",
            "/horse/000a0092dd/",
            "/horse/000a001db6/",
            "/horse/000a009e3a/",
            "/horse/000a001702/",
            "/horse/000a00902d/",
            "/horse/000a0019da/",
            "/horse/000a008a92/",
            "/horse/000a0019b4/",
            "/horse/000a00a4b9/",
            "/horse/000a0003bd/",
            "/horse/1980101974/",
        ]
        assert i["parent5_id"] == [
            "/horse/000a000e04/",
            "/horse/000a00834c/",
            "/horse/000a000ded/",
            "/horse/000a008e04/",
            "/horse/000a001236/",
            "/horse/000a007525/",
            "/horse/000a001ee1/",
            "/horse/000a009f22/",
            "/horse/000a00180b/",
            "/horse/000a0086de/",
            "/horse/000a000e46/",
            "/horse/000a0092dc/",
            "/horse/000a000dbc/",
            "/horse/000a009a0c/",
            "/horse/000a001eaf/",
            "/horse/000a009e39/",
            "/horse/000a001607/",
            "/horse/000a0083e3/",
            "/horse/000a000e44/",
            "/horse/000a00902c/",
            "/horse/000a000e04/",
            "/horse/000a008298/",
            "/horse/000a0010e2/",
            "/horse/000a008a91/",
            "/horse/000a0012cb/",
            "/horse/000a008c0e/",
            "/horse/000a0000d3/",
            "/horse/000a00a4b8/",
            "/horse/000a000dfe/",
            "/horse/000a0002fd/",
            "/horse/000a000444/",
            "/horse/1966100143/",
        ]


class JockeyContract(Contract):
    name = "jockey_contract"

    def post_process(self, output):
        #
        # Check items
        #

        items = list(filter(lambda i: isinstance(i, JockeyItem), output))

        i = items[0]
        assert i["birth_place"] == ["福島県/A型"]
        assert i["debut_year"] == ["2002年(24年目)"]
        assert i["jockey_id"] == ["/jockey/01075/"]
        assert i["jockey_name"][0].strip() == "田辺裕信\xa0\n          \n          (タナベヒロノブ)"
        assert i["jockey_text"][0].strip() == "1984/02/12\n            \n            \n            [美浦]フリー"


class TrainerContract(Contract):
    name = "trainer_contract"

    def post_process(self, output):
        #
        # Check items
        #

        items = list(filter(lambda i: isinstance(i, TrainerItem), output))

        i = items[0]
        assert i["birth_place"] == ["千葉県"]
        assert i["debut_year"] == ["1997年(29年目)"]
        assert i["trainer_id"] == ["/trainer/01027/"]
        assert i["trainer_name"][0].strip() == "田村康仁\xa0\n                \n                (タムラヤスヒト)"
        assert i["trainer_text"][0].strip() == "1963/03/30\n                \n                美浦"
