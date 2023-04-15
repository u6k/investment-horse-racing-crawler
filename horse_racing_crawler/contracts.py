from urllib.parse import parse_qs, urlparse

from scrapy.contracts import Contract
from scrapy.exceptions import ContractFail
from scrapy.http import Request

from horse_racing_crawler.items import OddsItem, RaceCornerPassingItem, RaceInfoItem, RaceLapTimeItem, RacePayoffItem, RaceResultItem


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
        horse_page_links = list(filter(lambda r: r.url.startswith("https://db.netkeiba.com/horse/"), requests))

        assert len(horse_page_links) == 16

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
        items = list(filter(lambda i: i["odds_type"] == 1, odds_items))

        assert len(items) == 16

        i = items[0]
        assert i["favorite_order"] == "5"
        assert i["horse_number"] == "01"
        assert i["odds1"] == "32.8"
        assert i["odds2"] == ""
        assert i["odds_type"] == 1
        assert i["race_id"] == ["202306020702"]

        i = items[1]
        assert i["favorite_order"] == "4"
        assert i["horse_number"] == "02"
        assert i["odds1"] == "27.9"
        assert i["odds2"] == ""
        assert i["odds_type"] == 1
        assert i["race_id"] == ["202306020702"]

        i = items[2]
        assert i["favorite_order"] == "15"
        assert i["horse_number"] == "03"
        assert i["odds1"] == "274.1"
        assert i["odds2"] == ""
        assert i["odds_type"] == 1
        assert i["race_id"] == ["202306020702"]

        i = items[3]
        assert i["favorite_order"] == "11"
        assert i["horse_number"] == "04"
        assert i["odds1"] == "154.6"
        assert i["odds2"] == ""
        assert i["odds_type"] == 1
        assert i["race_id"] == ["202306020702"]

        i = items[4]
        assert i["favorite_order"] == "9"
        assert i["horse_number"] == "05"
        assert i["odds1"] == "113.5"
        assert i["odds2"] == ""
        assert i["odds_type"] == 1
        assert i["race_id"] == ["202306020702"]

        i = items[5]
        assert i["favorite_order"] == "6"
        assert i["horse_number"] == "06"
        assert i["odds1"] == "36.7"
        assert i["odds2"] == ""
        assert i["odds_type"] == 1
        assert i["race_id"] == ["202306020702"]

        i = items[6]
        assert i["favorite_order"] == "7"
        assert i["horse_number"] == "07"
        assert i["odds1"] == "66.0"
        assert i["odds2"] == ""
        assert i["odds_type"] == 1
        assert i["race_id"] == ["202306020702"]

        i = items[7]
        assert i["favorite_order"] == "10"
        assert i["horse_number"] == "08"
        assert i["odds1"] == "140.9"
        assert i["odds2"] == ""
        assert i["odds_type"] == 1
        assert i["race_id"] == ["202306020702"]

        i = items[8]
        assert i["favorite_order"] == "1"
        assert i["horse_number"] == "09"
        assert i["odds1"] == "1.2"
        assert i["odds2"] == ""
        assert i["odds_type"] == 1
        assert i["race_id"] == ["202306020702"]

        i = items[9]
        assert i["favorite_order"] == "13"
        assert i["horse_number"] == "10"
        assert i["odds1"] == "254.1"
        assert i["odds2"] == ""
        assert i["odds_type"] == 1
        assert i["race_id"] == ["202306020702"]

        i = items[10]
        assert i["favorite_order"] == "12"
        assert i["horse_number"] == "11"
        assert i["odds1"] == "187.3"
        assert i["odds2"] == ""
        assert i["odds_type"] == 1
        assert i["race_id"] == ["202306020702"]

        i = items[11]
        assert i["favorite_order"] == "2"
        assert i["horse_number"] == "12"
        assert i["odds1"] == "4.0"
        assert i["odds2"] == ""
        assert i["odds_type"] == 1
        assert i["race_id"] == ["202306020702"]

        i = items[12]
        assert i["favorite_order"] == "16"
        assert i["horse_number"] == "13"
        assert i["odds1"] == "700.7"
        assert i["odds2"] == ""
        assert i["odds_type"] == 1
        assert i["race_id"] == ["202306020702"]

        i = items[13]
        assert i["favorite_order"] == "3"
        assert i["horse_number"] == "14"
        assert i["odds1"] == "22.4"
        assert i["odds2"] == ""
        assert i["odds_type"] == 1
        assert i["race_id"] == ["202306020702"]

        i = items[14]
        assert i["favorite_order"] == "14"
        assert i["horse_number"] == "15"
        assert i["odds1"] == "258.0"
        assert i["odds2"] == ""
        assert i["odds_type"] == 1
        assert i["race_id"] == ["202306020702"]

        i = items[15]
        assert i["favorite_order"] == "8"
        assert i["horse_number"] == "16"
        assert i["odds1"] == "76.6"
        assert i["odds2"] == ""
        assert i["odds_type"] == 1
        assert i["race_id"] == ["202306020702"]

        # place odds
        items = list(filter(lambda i: i["odds_type"] == 2, odds_items))

        assert len(items) == 16

        i = items[0]
        assert i["favorite_order"] == "6"
        assert i["horse_number"] == "01"
        assert i["odds1"] == "3.2"
        assert i["odds2"] == "24.2"
        assert i["odds_type"] == 2
        assert i["race_id"] == ["202306020702"]

        i = items[1]
        assert i["favorite_order"] == "3"
        assert i["horse_number"] == "02"
        assert i["odds1"] == "1.6"
        assert i["odds2"] == "10.5"
        assert i["odds_type"] == 2
        assert i["race_id"] == ["202306020702"]

        i = items[2]
        assert i["favorite_order"] == "15"
        assert i["horse_number"] == "03"
        assert i["odds1"] == "21.6"
        assert i["odds2"] == "186.5"
        assert i["odds_type"] == 2
        assert i["race_id"] == ["202306020702"]

        i = items[3]
        assert i["favorite_order"] == "12"
        assert i["horse_number"] == "04"
        assert i["odds1"] == "15.5"
        assert i["odds2"] == "132.1"
        assert i["odds_type"] == 2
        assert i["race_id"] == ["202306020702"]

        i = items[4]
        assert i["favorite_order"] == "10"
        assert i["horse_number"] == "05"
        assert i["odds1"] == "7.4"
        assert i["odds2"] == "61.5"
        assert i["odds_type"] == 2
        assert i["race_id"] == ["202306020702"]

        i = items[5]
        assert i["favorite_order"] == "5"
        assert i["horse_number"] == "06"
        assert i["odds1"] == "2.2"
        assert i["odds2"] == "15.5"
        assert i["odds_type"] == 2
        assert i["race_id"] == ["202306020702"]

        i = items[6]
        assert i["favorite_order"] == "7"
        assert i["horse_number"] == "07"
        assert i["odds1"] == "4.0"
        assert i["odds2"] == "31.4"
        assert i["odds_type"] == 2
        assert i["race_id"] == ["202306020702"]

        i = items[7]
        assert i["favorite_order"] == "9"
        assert i["horse_number"] == "08"
        assert i["odds1"] == "5.5"
        assert i["odds2"] == "45.0"
        assert i["odds_type"] == 2
        assert i["race_id"] == ["202306020702"]

        i = items[8]
        assert i["favorite_order"] == "1"
        assert i["horse_number"] == "09"
        assert i["odds1"] == "1.0"
        assert i["odds2"] == "1.1"
        assert i["odds_type"] == 2
        assert i["race_id"] == ["202306020702"]

        i = items[9]
        assert i["favorite_order"] == "14"
        assert i["horse_number"] == "10"
        assert i["odds1"] == "19.9"
        assert i["odds2"] == "171.5"
        assert i["odds_type"] == 2
        assert i["race_id"] == ["202306020702"]

        i = items[10]
        assert i["favorite_order"] == "11"
        assert i["horse_number"] == "11"
        assert i["odds1"] == "10.2"
        assert i["odds2"] == "86.1"
        assert i["odds_type"] == 2
        assert i["race_id"] == ["202306020702"]

        i = items[11]
        assert i["favorite_order"] == "2"
        assert i["horse_number"] == "12"
        assert i["odds1"] == "1.1"
        assert i["odds2"] == "4.6"
        assert i["odds_type"] == 2
        assert i["race_id"] == ["202306020702"]

        i = items[12]
        assert i["favorite_order"] == "16"
        assert i["horse_number"] == "13"
        assert i["odds1"] == "47.7"
        assert i["odds2"] == "415.7"
        assert i["odds_type"] == 2
        assert i["race_id"] == ["202306020702"]

        i = items[13]
        assert i["favorite_order"] == "4"
        assert i["horse_number"] == "14"
        assert i["odds1"] == "1.9"
        assert i["odds2"] == "12.9"
        assert i["odds_type"] == 2
        assert i["race_id"] == ["202306020702"]

        i = items[14]
        assert i["favorite_order"] == "13"
        assert i["horse_number"] == "15"
        assert i["odds1"] == "19.8"
        assert i["odds2"] == "170.1"
        assert i["odds_type"] == 2
        assert i["race_id"] == ["202306020702"]

        i = items[15]
        assert i["favorite_order"] == "8"
        assert i["horse_number"] == "16"
        assert i["odds1"] == "4.6"
        assert i["odds2"] == "36.8"
        assert i["odds_type"] == 2
        assert i["race_id"] == ["202306020702"]


class OddsBracketQuinellaContract(Contract):
    name = "odds_bracket_quinella_contract"

    def post_process(self, output):
        #
        # Check items
        #

        odds_items = list(filter(lambda o: isinstance(o, OddsItem), output))

        items = list(filter(lambda i: i["odds_type"] == 3, odds_items))

        assert len(odds_items) == len(items)

        i = items[0]
        assert i["favorite_order"] == "20"
        assert i["horse_number"] == "0101"
        assert i["odds1"] == "154.3"
        assert i["odds2"] == ""
        assert i["odds_type"] == 3
        assert i["race_id"] == ["202306020702"]

        i = items[1]
        assert i["favorite_order"] == "22"
        assert i["horse_number"] == "0102"
        assert i["odds1"] == "186.4"
        assert i["odds2"] == ""
        assert i["odds_type"] == 3
        assert i["race_id"] == ["202306020702"]

        i = items[34]
        assert i["favorite_order"] == "23"
        assert i["horse_number"] == "0708"
        assert i["odds1"] == "193.0"
        assert i["odds2"] == ""
        assert i["odds_type"] == 3
        assert i["race_id"] == ["202306020702"]

        i = items[35]
        assert i["favorite_order"] == "35"
        assert i["horse_number"] == "0808"
        assert i["odds1"] == "1717.1"
        assert i["odds2"] == ""
        assert i["odds_type"] == 3
        assert i["race_id"] == ["202306020702"]


class OddsQuinellaContract(Contract):
    name = "odds_quinella_contract"

    def post_process(self, output):
        #
        # Check items
        #

        odds_items = list(filter(lambda o: isinstance(o, OddsItem), output))

        items = list(filter(lambda i: i["odds_type"] == 4, odds_items))

        assert len(odds_items) == len(items)

        i = items[0]
        assert i["favorite_order"] == "21"
        assert i["horse_number"] == "0102"
        assert i["odds1"] == "140.4"
        assert i["odds2"] == ""
        assert i["odds_type"] == 4
        assert i["race_id"] == ["202306020702"]

        i = items[1]
        assert i["favorite_order"] == "69"
        assert i["horse_number"] == "0103"
        assert i["odds1"] == "1767.9"
        assert i["odds2"] == ""
        assert i["odds_type"] == 4
        assert i["race_id"] == ["202306020702"]

        i = items[118]
        assert i["favorite_order"] == "40"
        assert i["horse_number"] == "1416"
        assert i["odds1"] == "530.8"
        assert i["odds2"] == ""
        assert i["odds_type"] == 4
        assert i["race_id"] == ["202306020702"]

        i = items[119]
        assert i["favorite_order"] == "96"
        assert i["horse_number"] == "1516"
        assert i["odds1"] == "4362.2"
        assert i["odds2"] == ""
        assert i["odds_type"] == 4
        assert i["race_id"] == ["202306020702"]
