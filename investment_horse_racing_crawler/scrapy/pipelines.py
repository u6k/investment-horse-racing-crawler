import hashlib

from scrapy.exceptions import DropItem
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

from investment_horse_racing_crawler.app_logging import get_logger
from investment_horse_racing_crawler.scrapy.items import RaceInfoItem, RacePayoffItem, RaceResultItem, RaceDenmaItem, HorseItem, TrainerItem, JockeyItem, OddsWinPlaceItem, OddsBracketQuinellaItem, OddsExactaItem, OddsQuinellaItem, OddsQuinellaPlaceItem, OddsTrifectaItem, OddsTrioItem


logger = get_logger(__name__)


Base = declarative_base()


class RaceInfoData(Base):
    __tablename__ = "race_info"
    id = sa.Column(sa.String(), primary_key=True)
    race_id = sa.Column(sa.String())
    race_round = sa.Column(sa.String())
    start_date = sa.Column(sa.String())
    start_time = sa.Column(sa.String())
    place_name = sa.Column(sa.String())
    race_name = sa.Column(sa.String())
    course_type_length = sa.Column(sa.String())
    weather = sa.Column(sa.String())
    course_condition = sa.Column(sa.String())
    race_condition_1 = sa.Column(sa.String())
    race_condition_2 = sa.Column(sa.String())
    added_money = sa.Column(sa.String())

    @classmethod
    def from_item(cls, item):
        race_id = item["race_id"][0]
        id = hashlib.sha256(race_id.encode()).hexdigest()

        d = cls(
            id=id,
            race_id=race_id,
            race_round=item["race_round"][0] if "race_round" in item else None,
            start_date=item["start_date"][0] if "start_date" in item else None,
            start_time=item["start_time"][0] if "start_time" in item else None,
            place_name=item["place_name"][0] if "place_name" in item else None,
            race_name=item["race_name"][0] if "race_name" in item else None,
            course_type_length=item["course_type_length"][0] if "course_type_length" in item else None,
            weather=item["weather"][0] if "weather" in item else None,
            course_condition=item["course_condition"][0] if "course_condition" in item else None,
            race_condition_1=item["race_condition_1"][0] if "race_condition_1" in item else None,
            race_condition_2=item["race_condition_2"][0] if "race_condition_2" in item else None,
            added_money=item["added_money"][0] if "added_money" in item else None,
        )

        return d


class RacePayoffData(Base):
    __tablename__ = "race_payoff"
    id = sa.Column(sa.String(), primary_key=True)
    race_id = sa.Column(sa.String())
    payoff_type = sa.Column(sa.String())
    horse_number = sa.Column(sa.String())
    odds = sa.Column(sa.String())
    favorite_order = sa.Column(sa.String())

    @classmethod
    def from_item(cls, item):
        race_id = item["race_id"][0]
        horse_number = item["horse_number"][0]
        id = hashlib.sha256((race_id + "." + horse_number).encode()).hexdigest()

        d = cls(
            id=id,
            race_id=race_id,
            horse_number=horse_number,
            payoff_type=item["payoff_type"][0] if "payoff_type" in item else None,
            odds=item["odds"][0] if "odds" in item else None,
            favorite_order=item["favorite_order"][0] if "favorite_order" in item else None,
        )

        return d


class RaceResultData(Base):
    __tablename__ = "race_result"
    id = sa.Column(sa.String(), primary_key=True)
    race_id = sa.Column(sa.String())
    result = sa.Column(sa.String())
    bracket_number = sa.Column(sa.String())
    horse_number = sa.Column(sa.String())
    horse_id = sa.Column(sa.String())
    arrival_time = sa.Column(sa.String())
    arrival_margin = sa.Column(sa.String())
    passing_order = sa.Column(sa.String())
    final_600_meters_time = sa.Column(sa.String())
    jockey_id = sa.Column(sa.String())
    favorite_order = sa.Column(sa.String())
    odds = sa.Column(sa.String())
    trainer_id = sa.Column(sa.String())

    @classmethod
    def from_item(cls, item):
        race_id = item["race_id"][0]
        horse_number = item["horse_number"][0]
        id = hashlib.sha256((race_id + "." + horse_number).encode()).hexdigest()

        d = cls(
            id=id,
            race_id=race_id,
            horse_number=horse_number,
            result=item["result"][0] if "result" in item else None,
            bracket_number=item["bracket_number"][0] if "bracket_number" in item else None,
            horse_id=item["horse_id"][0] if "horse_id" in item else None,
            arrival_time=item["arrival_time"][0] if "arrival_time" in item else None,
            arrival_margin=item["arrival_margin"][0] if "arrival_margin" in item else None,
            passing_order=item["passing_order"][0] if "passing_order" in item else None,
            final_600_meters_time=item["final_600_meters_time"][0] if "final_600_meters_time" in item else None,
            jockey_id=item["jockey_id"][0] if "jockey_id" in item else None,
            favorite_order=item["favorite_order"][0] if "favorite_order" in item else None,
            odds=item["odds"][0] if "odds" in item else None,
            trainer_id=item["trainer_id"][0] if "trainer_id" in item else None,
        )

        return d


class RaceDenmaData(Base):
    __tablename__ = "race_denma"
    id = sa.Column(sa.String(), primary_key=True)
    race_id = sa.Column(sa.String())
    bracket_number = sa.Column(sa.String())
    horse_number = sa.Column(sa.String())
    horse_id = sa.Column(sa.String())
    trainer_id = sa.Column(sa.String())
    horse_weight_and_diff = sa.Column(sa.String())
    jockey_id = sa.Column(sa.String())
    jockey_weight = sa.Column(sa.String())
    prize_total_money = sa.Column(sa.String())

    @classmethod
    def from_item(cls, item):
        race_id = item["race_id"][0]
        horse_number = item["horse_number"][0]
        id = hashlib.sha256((race_id + "." + horse_number).encode()).hexdigest()

        d = cls(
            id=id,
            race_id=race_id,
            horse_number=horse_number,
            bracket_number=item["bracket_number"][0] if "bracket_number" in item else None,
            horse_id=item["horse_id"][0] if "horse_id" in item else None,
            trainer_id=item["trainer_id"][0] if "trainer_id" in item else None,
            horse_weight_and_diff=item["horse_weight_and_diff"][0] if "horse_weight_and_diff" in item else None,
            jockey_id=item["jockey_id"][0] if "jockey_id" in item else None,
            jockey_weight=item["jockey_weight"][0] if "jockey_weight" in item else None,
            prize_total_money=item["prize_total_money"][0] if "prize_total_money" in item else None,
        )

        return d


class HorseData(Base):
    __tablename__ = "horse"
    id = sa.Column(sa.String(), primary_key=True)
    horse_id = sa.Column(sa.String())
    gender = sa.Column(sa.String())
    name = sa.Column(sa.String())
    birthday = sa.Column(sa.String())
    coat_color = sa.Column(sa.String())
    trainer_id = sa.Column(sa.String())
    owner = sa.Column(sa.String())
    breeder = sa.Column(sa.String())
    breeding_farm = sa.Column(sa.String())
    parent_horse_name_male_1 = sa.Column(sa.String())
    parent_horse_name_male_21 = sa.Column(sa.String())
    parent_horse_name_male_22 = sa.Column(sa.String())
    parent_horse_name_male_31 = sa.Column(sa.String())
    parent_horse_name_male_32 = sa.Column(sa.String())
    parent_horse_name_male_33 = sa.Column(sa.String())
    parent_horse_name_male_34 = sa.Column(sa.String())
    parent_horse_name_female_1 = sa.Column(sa.String())
    parent_horse_name_female_21 = sa.Column(sa.String())
    parent_horse_name_female_22 = sa.Column(sa.String())
    parent_horse_name_female_31 = sa.Column(sa.String())
    parent_horse_name_female_32 = sa.Column(sa.String())
    parent_horse_name_female_33 = sa.Column(sa.String())
    parent_horse_name_female_34 = sa.Column(sa.String())

    @classmethod
    def from_item(cls, item):
        horse_id = item["horse_id"][0]
        id = hashlib.sha256(horse_id.encode()).hexdigest()

        d = cls(
            id=id,
            horse_id=horse_id,
            gender=item["gender"][0] if "gender" in item else None,
            name=item["name"][0] if "name" in item else None,
            birthday=item["birthday"][0] if "birthday" in item else None,
            coat_color=item["coat_color"][0] if "coat_color" in item else None,
            trainer_id=item["trainer_id"][0] if "trainer_id" in item else None,
            owner=item["owner"][0] if "owner" in item else None,
            breeder=item["breeder"][0] if "breeder" in item else None,
            breeding_farm=item["breeding_farm"][0] if "breeding_farm" in item else None,
            parent_horse_name_male_1=item["parent_horse_name_male_1"][0] if "parent_horse_name_male_1" in item else None,
            parent_horse_name_male_21=item["parent_horse_name_male_21"][0] if "parent_horse_name_male_21" in item else None,
            parent_horse_name_male_22=item["parent_horse_name_male_22"][0] if "parent_horse_name_male_22" in item else None,
            parent_horse_name_male_31=item["parent_horse_name_male_31"][0] if "parent_horse_name_male_31" in item else None,
            parent_horse_name_male_32=item["parent_horse_name_male_32"][0] if "parent_horse_name_male_32" in item else None,
            parent_horse_name_male_33=item["parent_horse_name_male_33"][0] if "parent_horse_name_male_33" in item else None,
            parent_horse_name_male_34=item["parent_horse_name_male_34"][0] if "parent_horse_name_male_34" in item else None,
            parent_horse_name_female_1=item["parent_horse_name_female_1"][0] if "parent_horse_name_female_1" in item else None,
            parent_horse_name_female_21=item["parent_horse_name_female_21"][0] if "parent_horse_name_female_21" in item else None,
            parent_horse_name_female_22=item["parent_horse_name_female_22"][0] if "parent_horse_name_female_22" in item else None,
            parent_horse_name_female_31=item["parent_horse_name_female_31"][0] if "parent_horse_name_female_31" in item else None,
            parent_horse_name_female_32=item["parent_horse_name_female_32"][0] if "parent_horse_name_female_32" in item else None,
            parent_horse_name_female_33=item["parent_horse_name_female_33"][0] if "parent_horse_name_female_33" in item else None,
            parent_horse_name_female_34=item["parent_horse_name_female_34"][0] if "parent_horse_name_female_34" in item else None,
        )

        return d


class TrainerData(Base):
    __tablename__ = "trainer"
    id = sa.Column(sa.String(), primary_key=True)
    trainer_id = sa.Column(sa.String())
    name_kana = sa.Column(sa.String())
    name = sa.Column(sa.String())
    birthday = sa.Column(sa.String())
    belong_to = sa.Column(sa.String())
    first_licensing_year = sa.Column(sa.String())

    @classmethod
    def from_item(cls, item):
        trainer_id = item["trainer_id"][0]
        id = hashlib.sha256(trainer_id.encode()).hexdigest()

        d = cls(
            id=id,
            trainer_id=trainer_id,
            name_kana=item["name_kana"][0] if "name_kana" in item else None,
            name=item["name"][0] if "name" in item else None,
            birthday=item["birthday"][0] if "birthday" in item else None,
            belong_to=item["belong_to"][0] if "belong_to" in item else None,
            first_licensing_year=item["first_licensing_year"][0] if "first_licensing_year" in item else None,
        )

        return d


class JockeyData(Base):
    __tablename__ = "jockey"
    id = sa.Column(sa.String(), primary_key=True)
    jockey_id = sa.Column(sa.String())
    name_kana = sa.Column(sa.String())
    name = sa.Column(sa.String())
    birthday = sa.Column(sa.String())
    belong_to = sa.Column(sa.String())
    first_licensing_year = sa.Column(sa.String())
    first_entry_day = sa.Column(sa.String())
    first_win_day = sa.Column(sa.String())

    @classmethod
    def from_item(cls, item):
        jockey_id = item["jockey_id"][0]
        id = hashlib.sha256(jockey_id.encode()).hexdigest()

        d = cls(
            id=id,
            jockey_id=jockey_id,
            name_kana=item["name_kana"][0] if "name_kana" in item else None,
            name=item["name"][0] if "name" in item else None,
            birthday=item["birthday"][0] if "birthday" in item else None,
            belong_to=item["belong_to"][0] if "belong_to" in item else None,
            first_licensing_year=item["first_licensing_year"][0] if "first_licensing_year" in item else None,
            first_entry_day=item["first_entry_day"][0] if "first_entry_day" in item else None,
            first_win_day=item["first_win_day"][0] if "first_win_day" in item else None,
        )

        return d


class OddsWinPlaceData(Base):
    __tablename__ = "odds_win_place"
    id = sa.Column(sa.String(), primary_key=True)
    race_id = sa.Column(sa.String())
    horse_number = sa.Column(sa.String())
    horse_id = sa.Column(sa.String())
    odds_win = sa.Column(sa.String())
    odds_place_min = sa.Column(sa.String())
    odds_place_max = sa.Column(sa.String())

    @classmethod
    def from_item(cls, item):
        race_id = item["race_id"][0]
        horse_number = item["horse_number"][0]
        id = hashlib.sha256((race_id + "." + horse_number).encode()).hexdigest()

        d = cls(
            id=id,
            race_id=race_id,
            horse_number=horse_number,
            horse_id=item["horse_id"][0] if "horse_id" in item else None,
            odds_win=item["odds_win"][0] if "odds_win" in item else None,
            odds_place_min=item["odds_place_min"][0] if "odds_place_min" in item else None,
            odds_place_max=item["odds_place_max"][0] if "odds_place_max" in item else None,
        )

        return d


class OddsBracketQuinellaData(Base):
    __tablename__ = "odds_bracket_quinella"
    id = sa.Column(sa.String(), primary_key=True)
    race_id = sa.Column(sa.String())
    bracket_number_1 = sa.Column(sa.String())
    bracket_number_2 = sa.Column(sa.String())
    odds = sa.Column(sa.String())

    @classmethod
    def from_item(cls, item):
        race_id = item["race_id"][0]
        bracket_number_1 = item["bracket_number_1"][0]
        bracket_number_2 = item["bracket_number_2"][0]
        id = hashlib.sha256((race_id + "." + bracket_number_1 + "." + bracket_number_2).encode()).hexdigest()

        d = cls(
            id=id,
            race_id=race_id,
            bracket_number_1=bracket_number_1,
            bracket_number_2=bracket_number_2,
            odds=item["odds"][0] if "odds" in item else None,
        )

        return d


class OddsExactaData(Base):
    __tablename__ = "odds_exacta"
    id = sa.Column(sa.String(), primary_key=True)
    race_id = sa.Column(sa.String())
    horse_number_1 = sa.Column(sa.String())
    horse_number_2 = sa.Column(sa.String())
    odds = sa.Column(sa.String())

    @classmethod
    def from_item(cls, item):
        race_id = item["race_id"][0]
        horse_number_1 = item["horse_number_1"][0]
        horse_number_2 = item["horse_number_2"][0]
        id = hashlib.sha256((race_id + "." + horse_number_1 + "." + horse_number_2).encode()).hexdigest()

        d = cls(
            id=id,
            race_id=race_id,
            horse_number_1=horse_number_1,
            horse_number_2=horse_number_2,
            odds=item["odds"][0] if "odds" in item else None,
        )

        return d


class OddsQuinellaData(Base):
    __tablename__ = "odds_quinella"
    id = sa.Column(sa.String(), primary_key=True)
    race_id = sa.Column(sa.String())
    horse_number_1 = sa.Column(sa.String())
    horse_number_2 = sa.Column(sa.String())
    odds = sa.Column(sa.String())

    @classmethod
    def from_item(cls, item):
        race_id = item["race_id"][0]
        horse_number_1 = item["horse_number_1"][0]
        horse_number_2 = item["horse_number_2"][0]
        id = hashlib.sha256((race_id + "." + horse_number_1 + "." + horse_number_2).encode()).hexdigest()

        d = cls(
            id=id,
            race_id=race_id,
            horse_number_1=horse_number_1,
            horse_number_2=horse_number_2,
            odds=item["odds"][0] if "odds" in item else None,
        )

        return d


class OddsQuinellaPlaceData(Base):
    __tablename__ = "odds_quinella_place"
    id = sa.Column(sa.String(), primary_key=True)
    race_id = sa.Column(sa.String())
    horse_number_1 = sa.Column(sa.String())
    horse_number_2 = sa.Column(sa.String())
    odds_min = sa.Column(sa.String())
    odds_max = sa.Column(sa.String())

    @classmethod
    def from_item(cls, item):
        race_id = item["race_id"][0]
        horse_number_1 = item["horse_number_1"][0]
        horse_number_2 = item["horse_number_2"][0]
        id = hashlib.sha256((race_id + "." + horse_number_1 + "." + horse_number_2).encode()).hexdigest()

        d = cls(
            id=id,
            race_id=race_id,
            horse_number_1=horse_number_1,
            horse_number_2=horse_number_2,
            odds_min=item["odds_min"][0] if "odds_min" in item else None,
            odds_max=item["odds_max"][0] if "odds_max" in item else None,
        )

        return d


class OddsTrifectaData(Base):
    __tablename__ = "odds_trifecta"
    id = sa.Column(sa.String(), primary_key=True)
    race_id = sa.Column(sa.String())
    horse_number_1_2_3 = sa.Column(sa.String())
    odds = sa.Column(sa.String())

    @classmethod
    def from_item(cls, item):
        race_id = item["race_id"][0]
        horse_number_1_2_3 = item["horse_number_1_2_3"][0]
        id = hashlib.sha256((race_id + "." + horse_number_1_2_3).encode()).hexdigest()

        d = cls(
            id=id,
            race_id=race_id,
            horse_number_1_2_3=horse_number_1_2_3,
            odds=item["odds"][0] if "odds" in item else None,
        )

        return d


class OddsTrioData(Base):
    __tablename__ = "odds_trio"
    id = sa.Column(sa.String(), primary_key=True)
    race_id = sa.Column(sa.String())
    horse_number_1_2 = sa.Column(sa.String())
    horse_number_3 = sa.Column(sa.String())
    odds = sa.Column(sa.String())

    @classmethod
    def from_item(cls, item):
        race_id = item["race_id"][0]
        horse_number_1_2 = item["horse_number_1_2"][0]
        horse_number_3 = item["horse_number_3"][0]
        id = hashlib.sha256((race_id + "." + horse_number_1_2 + "." + horse_number_3).encode()).hexdigest()

        d = cls(
            id=id,
            race_id=race_id,
            horse_number_1_2=horse_number_1_2,
            horse_number_3=horse_number_3,
            odds=item["odds"][0] if "odds" in item else None,
        )

        return d


class PostgreSQLPipeline(object):
    def __init__(self, db_host, db_port, db_database, db_username, db_password):
        logger.debug(f"#init: start: db_host={db_host}, db_port={db_port}, db_database={db_database}, db_username={db_username}")

        engine = sa.create_engine(f"postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_database}")
        self.session = sa.orm.sessionmaker(bind=engine, autocommit=False, autoflush=False)

    @classmethod
    def from_crawler(cls, crawler):
        logger.debug("#from_crawler")

        return cls(
            db_host=crawler.settings.get("DB_HOST"),
            db_port=crawler.settings.get("DB_PORT"),
            db_database=crawler.settings.get("DB_DATABASE"),
            db_username=crawler.settings.get("DB_USERNAME"),
            db_password=crawler.settings.get("DB_PASSWORD")
        )

    def process_item(self, item, spider):
        logger.debug(f"#process_item: start: item={item}")

        with self.session() as sess:
            try:
                # Build query
                if isinstance(item, RaceInfoItem):
                    d = RaceInfoData.from_item(item)
                    q = sess.query(RaceInfoData).filter(RaceInfoData.id == d.id)
                elif isinstance(item, RacePayoffItem):
                    d = RacePayoffData.from_item(item)
                    q = sess.query(RacePayoffData).filter(RacePayoffData.id == d.id)
                elif isinstance(item, RaceResultItem):
                    d = RaceResultData.from_item(item)
                    q = sess.query(RaceResultData).filter(RaceResultData.id == d.id)
                elif isinstance(item, RaceDenmaItem):
                    d = RaceDenmaData.from_item(item)
                    q = sess.query(RaceDenmaData).filter(RaceDenmaData.id == d.id)
                elif isinstance(item, HorseItem):
                    d = HorseData.from_item(item)
                    q = sess.query(HorseData).filter(HorseData.id == d.id)
                elif isinstance(item, TrainerItem):
                    d = TrainerData.from_item(item)
                    q = sess.query(TrainerData).filter(TrainerData.id == d.id)
                elif isinstance(item, JockeyItem):
                    d = JockeyData.from_item(item)
                    q = sess.query(JockeyData).filter(JockeyData.id == d.id)
                elif isinstance(item, OddsWinPlaceItem):
                    d = OddsWinPlaceData.from_item(item)
                    q = sess.query(OddsWinPlaceData).filter(OddsWinPlaceData.id == d.id)
                elif isinstance(item, OddsBracketQuinellaItem):
                    d = OddsBracketQuinellaData.from_item(item)
                    q = sess.query(OddsBracketQuinellaData).filter(OddsBracketQuinellaData.id == d.id)
                elif isinstance(item, OddsExactaItem):
                    d = OddsExactaData.from_item(item)
                    q = sess.query(OddsExactaData).filter(OddsExactaData.id == d.id)
                elif isinstance(item, OddsQuinellaItem):
                    d = OddsQuinellaData.from_item(item)
                    q = sess.query(OddsQuinellaData).filter(OddsQuinellaData.id == d.id)
                elif isinstance(item, OddsQuinellaPlaceItem):
                    d = OddsQuinellaPlaceData.from_item(item)
                    q = sess.query(OddsQuinellaPlaceData).filter(OddsQuinellaPlaceData.id == d.id)
                elif isinstance(item, OddsTrifectaItem):
                    d = OddsTrifectaData.from_item(item)
                    q = sess.query(OddsTrifectaData).filter(OddsTrifectaData.id == d.id)
                elif isinstance(item, OddsTrioItem):
                    d = OddsTrioData.from_item(item)
                    q = sess.query(OddsTrioData).filter(OddsTrioData.id == d.id)
                else:
                    raise DropItem("Unknown item type")

                # Delete data
                logger.debug(f"#process_item: delete: id={d.id}")
                q.delete()

                # Insert data
                logger.debug(f"#process_item: insert: data={d.__dict__}")
                sess.add(d)
                sess.commit()
            except Exception as e:
                logger.exception("except Exception")
                raise DropItem("except Exception") from e
