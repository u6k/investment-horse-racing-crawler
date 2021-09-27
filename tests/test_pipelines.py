import logging
import os

from nose.tools import eq_
from scrapy.crawler import Crawler

from investment_horse_racing_crawler.scrapy.spiders.horse_racing_spider import HorseRacingSpider
from investment_horse_racing_crawler.scrapy.items import RaceInfoItem, RacePayoffItem, RaceResultItem, RaceDenmaItem, HorseItem, TrainerItem, JockeyItem, OddsWinPlaceItem, OddsBracketQuinellaItem, OddsExactaItem, OddsQuinellaItem, OddsQuinellaPlaceItem, OddsTrifectaItem, OddsTrioItem
from investment_horse_racing_crawler.scrapy.pipelines import PostgreSQLPipeline, RaceInfoData, RacePayoffData, RaceResultData, RaceDenmaData, HorseData, TrainerData, JockeyData, OddsWinPlaceData, OddsBracketQuinellaData, OddsExactaData, OddsQuinellaData, OddsQuinellaPlaceData, OddsTrifectaData, OddsTrioData


class TestPostgreSQLPipeline:
    def setup(self):
        logging.disable(logging.DEBUG)

        # Setting pipeline
        settings = {
            "DB_HOST": os.getenv("DB_HOST"),
            "DB_PORT": os.getenv("DB_PORT"),
            "DB_DATABASE": os.getenv("DB_DATABASE"),
            "DB_USERNAME": os.getenv("DB_USERNAME"),
            "DB_PASSWORD": os.getenv("DB_PASSWORD"),
        }
        crawler = Crawler(HorseRacingSpider, settings)
        self.pipeline = PostgreSQLPipeline.from_crawler(crawler)

        # Setting db
        with self.pipeline.session() as sess:
            sess.query(RaceInfoData).delete()
            sess.query(RacePayoffData).delete()
            sess.query(RaceResultData).delete()
            sess.query(RaceDenmaData).delete()
            sess.query(HorseData).delete()
            sess.query(TrainerData).delete()
            sess.query(JockeyData).delete()
            sess.query(OddsWinPlaceData).delete()
            sess.query(OddsBracketQuinellaData).delete()
            sess.query(OddsExactaData).delete()
            sess.query(OddsQuinellaData).delete()
            sess.query(OddsQuinellaPlaceData).delete()
            sess.query(OddsTrifectaData).delete()
            sess.query(OddsTrioData).delete()
            sess.commit()

        self.sess = self.pipeline.session()

    def teardown(self):
        self.sess.close()

    def test_process_race_info_item(self):
        # Setup
        item = RaceInfoItem()
        item['added_money'] = [' 本賞金：500、200、130、75、50万円 ']
        item['course_condition'] = ['良']
        item['course_type_length'] = ['ダート・右 1200m ']
        item['place_name'] = [' 5回中山2日 ']
        item['race_id'] = ['1906050201']
        item['race_name'] = ['\n2歳未勝利']
        item['race_round'] = ['1R']
        item['start_date'] = ['2019年12月1日（日） ']
        item['start_time'] = [' 9:50発走']
        item['weather'] = ['曇']

        # Before check
        records = self.sess.query(RaceInfoData).all()
        eq_(len(records), 0)

        # Execute
        self.pipeline.process_item(item, None)

        # Check db
        records = self.sess.query(RaceInfoData).all()
        eq_(len(records), 1)

        record = records[0]
        eq_(len(record.id), 64)
        eq_(record.added_money, ' 本賞金：500、200、130、75、50万円 ')
        eq_(record.course_condition, '良')
        eq_(record.course_type_length, 'ダート・右 1200m ')
        eq_(record.place_name, ' 5回中山2日 ')
        eq_(record.race_id, '1906050201')
        eq_(record.race_name, '\n2歳未勝利')
        eq_(record.race_round, '1R')
        eq_(record.start_date, '2019年12月1日（日） ')
        eq_(record.start_time, ' 9:50発走')
        eq_(record.weather, '曇')

        # Execute (2)
        self.pipeline.process_item(item, None)

        # Check db (2)
        records = self.sess.query(RaceInfoData).all()
        eq_(len(records), 1)

    def test_process_race_payoff_item(self):
        # Setup
        item = RacePayoffItem()
        item['favorite_order'] = ['4番人気']
        item['horse_number'] = ['12']
        item['odds'] = ['550円']
        item['payoff_type'] = ['単勝']
        item['race_id'] = ['1906050201']

        # Before check
        records = self.sess.query(RacePayoffData).all()
        eq_(len(records), 0)

        # Execute
        self.pipeline.process_item(item, None)

        # Check db
        records = self.sess.query(RacePayoffData).all()
        eq_(len(records), 1)

        record = records[0]
        eq_(len(record.id), 64)
        eq_(record.favorite_order, '4番人気')
        eq_(record.horse_number, '12')
        eq_(record.odds, '550円')
        eq_(record.payoff_type, '単勝')
        eq_(record.race_id, '1906050201')

        # Execute (2)
        self.pipeline.process_item(item, None)

        # Check db (2)
        records = self.sess.query(RacePayoffData).all()
        eq_(len(records), 1)

    def test_process_race_result_item(self):
        # Setup
        item = RaceResultItem()
        item['arrival_time'] = ['\n1.12.5']
        item['bracket_number'] = ['6']
        item['favorite_order'] = ['\n4    ']
        item['horse_gender_age'] = ['\n牡2/484(-2)/    ']
        item['horse_id'] = ['/directory/horse/2017103493/']
        item['horse_name'] = ['バウンティハンター']
        item['horse_number'] = ['\n12  ']
        item['horse_weight_and_diff'] = ['\n牡2/484(-2)/    ']
        item['jockey_id'] = ['/directory/jocky/01109/']
        item['jockey_name'] = ['黛 弘人']
        item['jockey_weight'] = ['55.0']
        item['odds'] = ['(5.5)']
        item['race_id'] = ['1906050201']
        item['result'] = ['\n1  ']
        item['trainer_id'] = ['/directory/trainer/00435/']
        item['trainer_name'] = ['藤原 辰雄']

        # Before check
        records = self.sess.query(RaceResultData).all()
        eq_(len(records), 0)

        # Execute
        self.pipeline.process_item(item, None)

        # Check db
        records = self.sess.query(RaceResultData).all()
        eq_(len(records), 1)

        record = records[0]
        eq_(len(record.id), 64)
        eq_(record.arrival_time, '\n1.12.5')
        eq_(record.bracket_number, '6')
        eq_(record.favorite_order, '\n4    ')
        eq_(record.horse_gender_age, '\n牡2/484(-2)/    ')
        eq_(record.horse_id, '/directory/horse/2017103493/')
        eq_(record.horse_name, 'バウンティハンター')
        eq_(record.horse_number, '\n12  ')
        eq_(record.horse_weight_and_diff, '\n牡2/484(-2)/    ')
        eq_(record.jockey_id, '/directory/jocky/01109/')
        eq_(record.jockey_name, '黛 弘人')
        eq_(record.jockey_weight, '55.0')
        eq_(record.odds, '(5.5)')
        eq_(record.race_id, '1906050201')
        eq_(record.result, '\n1  ')
        eq_(record.trainer_id, '/directory/trainer/00435/')
        eq_(record.trainer_name, '藤原 辰雄')

        # Execute (2)
        self.pipeline.process_item(item, None)

        # Check db (2)
        records = self.sess.query(RaceResultData).all()
        eq_(len(records), 1)

    def test_process_race_denma_item(self):
        # Setup
        item = RaceDenmaItem()
        item['bracket_number'] = ['1']
        item['horse_id'] = ['/directory/horse/2017101602/']
        item['horse_number'] = ['1']
        item['horse_weight_and_diff'] = ['\n518(+14)\n']
        item['jockey_id'] = ['/directory/jocky/01167/']
        item['jockey_weight'] = ['53.0 △']
        item['prize_total_money'] = ['\n0万']
        item['race_id'] = ['1906050201']
        item['trainer_id'] = ['/directory/trainer/01012/']

        # Before check
        records = self.sess.query(RaceDenmaData).all()
        eq_(len(records), 0)

        # Execute
        self.pipeline.process_item(item, None)

        # Check db
        records = self.sess.query(RaceDenmaData).all()
        eq_(len(records), 1)

        record = records[0]
        eq_(len(record.id), 64)
        eq_(record.bracket_number, '1')
        eq_(record.horse_id, '/directory/horse/2017101602/')
        eq_(record.horse_number, '1')
        eq_(record.horse_weight_and_diff, '\n518(+14)\n')
        eq_(record.jockey_id, '/directory/jocky/01167/')
        eq_(record.jockey_weight, '53.0 △')
        eq_(record.prize_total_money, '\n0万')
        eq_(record.race_id, '1906050201')
        eq_(record.trainer_id, '/directory/trainer/01012/')

        # Execute (2)
        self.pipeline.process_item(item, None)

        # Check db (2)
        records = self.sess.query(RaceDenmaData).all()
        eq_(len(records), 1)

    def test_process_horse_item(self):
        # Setup
        item = HorseItem()
        item['birthday'] = ['2017年3月31日']
        item['breeder'] = ['大栄牧場']
        item['breeding_farm'] = ['新冠町']
        item['coat_color'] = ['栗毛']
        item['gender'] = [' 牡 | 登録抹消 ']
        item['horse_id'] = ['2017101602']
        item['name'] = ['エリンクロノス']
        item['owner'] = ['田頭 勇貴']
        item['trainer_id'] = ['/directory/trainer/01012/']

        # Before check
        records = self.sess.query(HorseData).all()
        eq_(len(records), 0)

        # Execute
        self.pipeline.process_item(item, None)

        # Check db
        records = self.sess.query(HorseData).all()
        eq_(len(records), 1)

        record = records[0]
        eq_(len(record.id), 64)
        eq_(record.birthday, '2017年3月31日')
        eq_(record.breeder, '大栄牧場')
        eq_(record.breeding_farm, '新冠町')
        eq_(record.coat_color, '栗毛')
        eq_(record.gender, ' 牡 | 登録抹消 ')
        eq_(record.horse_id, '2017101602')
        eq_(record.name, 'エリンクロノス')
        eq_(record.owner, '田頭 勇貴')
        eq_(record.trainer_id, '/directory/trainer/01012/')

        # Execute (2)
        self.pipeline.process_item(item, None)

        # Check db (2)
        records = self.sess.query(HorseData).all()
        eq_(len(records), 1)

    def test_process_trainer_item(self):
        # Setup
        item = TrainerItem()
        item['belong_to'] = ['\n美浦']
        item['birthday'] = ['1953年2月13日']
        item['first_licensing_year'] = ['1996年']
        item['name'] = ['大江原 哲']
        item['name_kana'] = ['オオエハラ サトシ ']
        item['trainer_id'] = ['01012']

        # Before check
        records = self.sess.query(TrainerData).all()
        eq_(len(records), 0)

        # Execute
        self.pipeline.process_item(item, None)

        # Check db
        records = self.sess.query(TrainerData).all()
        eq_(len(records), 1)

        record = records[0]
        eq_(len(record.id), 64)
        eq_(record.belong_to, '\n美浦')
        eq_(record.birthday, '1953年2月13日')
        eq_(record.first_licensing_year, '1996年')
        eq_(record.name, '大江原 哲')
        eq_(record.name_kana, 'オオエハラ サトシ ')
        eq_(record.trainer_id, '01012')

        # Execute (2)
        self.pipeline.process_item(item, None)

        # Check db (2)
        records = self.sess.query(TrainerData).all()
        eq_(len(records), 1)

    def test_process_jockey_item(self):
        # Setup
        item = JockeyItem()
        item['belong_to'] = ['\n美浦(藤沢 和雄)']
        item['birthday'] = ['1998年9月21日']
        item['first_licensing_year'] = ['2017年（平地・障害）']
        item['jockey_id'] = ['01167']
        item['name'] = ['木幡 育也']
        item['name_kana'] = ['コワタ イクヤ ']

        # Before check
        records = self.sess.query(JockeyData).all()
        eq_(len(records), 0)

        # Execute
        self.pipeline.process_item(item, None)

        # Check db
        records = self.sess.query(JockeyData).all()
        eq_(len(records), 1)

        record = records[0]
        eq_(len(record.id), 64)
        eq_(record.belong_to, '\n美浦(藤沢 和雄)')
        eq_(record.birthday, '1998年9月21日')
        eq_(record.first_licensing_year, '2017年（平地・障害）')
        eq_(record.jockey_id, '01167')
        eq_(record.name, '木幡 育也')
        eq_(record.name_kana, 'コワタ イクヤ ')

        # Execute (2)
        self.pipeline.process_item(item, None)

        # Check db (2)
        records = self.sess.query(JockeyData).all()
        eq_(len(records), 1)

    def test_process_odds_win_place_item(self):
        # Setup
        item = OddsWinPlaceItem()
        item['horse_id'] = ['/directory/horse/2017101602/']
        item['horse_number'] = ['1']
        item['odds_place_max'] = ['43.8']
        item['odds_place_min'] = ['26.0']
        item['odds_win'] = ['161.2']
        item['race_id'] = ['1906050201']

        # Before check
        records = self.sess.query(OddsWinPlaceData).all()
        eq_(len(records), 0)

        # Execute
        self.pipeline.process_item(item, None)

        # Check db
        records = self.sess.query(OddsWinPlaceData).all()
        eq_(len(records), 1)

        record = records[0]
        eq_(len(record.id), 64)
        eq_(record.horse_id, '/directory/horse/2017101602/')
        eq_(record.horse_number, '1')
        eq_(record.odds_place_max, '43.8')
        eq_(record.odds_place_min, '26.0')
        eq_(record.odds_win, '161.2')
        eq_(record.race_id, '1906050201')

        # Execute (2)
        self.pipeline.process_item(item, None)

        # Check db (2)
        records = self.sess.query(OddsWinPlaceData).all()
        eq_(len(records), 1)

    def test_process_odds_bracket_quinella_item(self):
        # Setup
        item = OddsBracketQuinellaItem()
        item['bracket_number_1'] = ['1']
        item['bracket_number_2'] = ['1']
        item['odds'] = ['139.8']
        item['race_id'] = ['1906050201']

        # Before check
        records = self.sess.query(OddsBracketQuinellaData).all()
        eq_(len(records), 0)

        # Execute
        self.pipeline.process_item(item, None)

        # Check db
        records = self.sess.query(OddsBracketQuinellaData).all()
        eq_(len(records), 1)

        record = records[0]
        eq_(len(record.id), 64)
        eq_(record.bracket_number_1, '1')
        eq_(record.bracket_number_2, '1')
        eq_(record.odds, '139.8')
        eq_(record.race_id, '1906050201')

        # Execute (2)
        self.pipeline.process_item(item, None)

        # Check db (2)
        records = self.sess.query(OddsBracketQuinellaData).all()
        eq_(len(records), 1)

    def test_process_odds_exacta_item(self):
        # Setup
        item = OddsExactaItem()
        item['horse_number_1'] = ['1']
        item['horse_number_2'] = ['2']
        item['odds'] = ['548.0']
        item['race_id'] = ['1906050201']

        # Before check
        records = self.sess.query(OddsExactaData).all()
        eq_(len(records), 0)

        # Execute
        self.pipeline.process_item(item, None)

        # Check db
        records = self.sess.query(OddsExactaData).all()
        eq_(len(records), 1)

        record = records[0]
        eq_(len(record.id), 64)
        eq_(record.horse_number_1, '1')
        eq_(record.horse_number_2, '2')
        eq_(record.odds, '548.0')
        eq_(record.race_id, '1906050201')

        # Execute (2)
        self.pipeline.process_item(item, None)

        # Check db (2)
        records = self.sess.query(OddsExactaData).all()
        eq_(len(records), 1)

    def test_process_odds_quinella_item(self):
        # Setup
        item = OddsQuinellaItem()
        item['horse_number_1'] = ['1']
        item['horse_number_2'] = ['2']
        item['odds'] = ['170.6']
        item['race_id'] = ['1906050201']

        # Before check
        records = self.sess.query(OddsQuinellaData).all()
        eq_(len(records), 0)

        # Execute
        self.pipeline.process_item(item, None)

        # Check db
        records = self.sess.query(OddsQuinellaData).all()
        eq_(len(records), 1)

        record = records[0]
        eq_(len(record.id), 64)
        eq_(record.horse_number_1, '1')
        eq_(record.horse_number_2, '2')
        eq_(record.odds, '170.6')
        eq_(record.race_id, '1906050201')

        # Execute (2)
        self.pipeline.process_item(item, None)

        # Check db (2)
        records = self.sess.query(OddsQuinellaData).all()
        eq_(len(records), 1)

    def test_process_odds_quinella_place_item(self):
        # Setup
        item = OddsQuinellaPlaceItem()
        item['horse_number_1'] = ['1']
        item['horse_number_2'] = ['2']
        item['odds_max'] = ['54.3']
        item['odds_min'] = ['48.9']
        item['race_id'] = ['1906050201']

        # Before check
        records = self.sess.query(OddsQuinellaPlaceData).all()
        eq_(len(records), 0)

        # Execute
        self.pipeline.process_item(item, None)

        # Check db
        records = self.sess.query(OddsQuinellaPlaceData).all()
        eq_(len(records), 1)

        record = records[0]
        eq_(len(record.id), 64)
        eq_(record.horse_number_1, '1')
        eq_(record.horse_number_2, '2')
        eq_(record.odds_max, '54.3')
        eq_(record.odds_min, '48.9')
        eq_(record.race_id, '1906050201')

        # Execute (2)
        self.pipeline.process_item(item, None)

        # Check db (2)
        records = self.sess.query(OddsQuinellaPlaceData).all()
        eq_(len(records), 1)

    def test_process_odds_trifecta_item(self):
        # Setup
        item = OddsTrifectaItem()
        item['horse_number_1_2_3'] = ['1－2－3']
        item['odds'] = ['4558.0']
        item['race_id'] = ['1906050201']

        # Before check
        records = self.sess.query(OddsTrifectaData).all()
        eq_(len(records), 0)

        # Execute
        self.pipeline.process_item(item, None)

        # Check db
        records = self.sess.query(OddsTrifectaData).all()
        eq_(len(records), 1)

        record = records[0]
        eq_(len(record.id), 64)
        eq_(record.horse_number_1_2_3, '1－2－3')
        eq_(record.odds, '4558.0')
        eq_(record.race_id, '1906050201')

        # Execute (2)
        self.pipeline.process_item(item, None)

        # Check db (2)
        records = self.sess.query(OddsTrifectaData).all()
        eq_(len(records), 1)

    def test_process_odds_trio_item(self):
        # Setup
        item = OddsTrioItem()
        item['horse_number_1_2'] = ['1－2']
        item['horse_number_3'] = ['3']
        item['odds'] = ['454.8']
        item['race_id'] = ['1906050201']

        # Before check
        records = self.sess.query(OddsTrioData).all()
        eq_(len(records), 0)

        # Execute
        self.pipeline.process_item(item, None)

        # Check db
        records = self.sess.query(OddsTrioData).all()
        eq_(len(records), 1)

        record = records[0]
        eq_(len(record.id), 64)
        eq_(record.horse_number_1_2, '1－2')
        eq_(record.horse_number_3, '3')
        eq_(record.odds, '454.8')
        eq_(record.race_id, '1906050201')

        # Execute (2)
        self.pipeline.process_item(item, None)

        # Check db (2)
        records = self.sess.query(OddsTrioData).all()
        eq_(len(records), 1)
