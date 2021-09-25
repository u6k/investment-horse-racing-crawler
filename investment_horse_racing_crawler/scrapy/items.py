# -*- coding: utf-8 -*-


from scrapy import Item, Field


class RaceInfoItem(Item):
    race_id = Field()
    race_round = Field()
    start_date = Field()
    start_time = Field()
    place_name = Field()
    race_name = Field()
    course_type_length = Field()
    weather = Field()
    course_condition = Field()
    added_money = Field()


class RacePayoffItem(Item):
    race_id = Field()
    payoff_type = Field()
    horse_number = Field()
    odds = Field()
    favorite_order = Field()


class RaceResultItem(Item):
    race_id = Field()
    result = Field()
    bracket_number = Field()
    horse_number = Field()
    horse_id = Field()
    horse_name = Field()
    horse_gender_age = Field()
    horse_weight_and_diff = Field()
    arrival_time = Field()
    jockey_id = Field()
    jockey_name = Field()
    jockey_weight = Field()
    favorite_order = Field()
    odds = Field()
    trainer_id = Field()
    trainer_name = Field()


class RaceDenmaItem(Item):
    race_id = Field()
    bracket_number = Field()
    horse_number = Field()
    horse_id = Field()
    trainer_id = Field()
    horse_weight_and_diff = Field()
    jockey_id = Field()
    jockey_weight = Field()
    prize_total_money = Field()


class HorseItem(Item):
    horse_id = Field()
    gender = Field()
    name = Field()
    birthday = Field()
    coat_color = Field()
    trainer_id = Field()
    owner = Field()
    breeder = Field()
    breeding_farm = Field()


class TrainerItem(Item):
    trainer_id = Field()
    name_kana = Field()
    name = Field()
    birthday = Field()
    belong_to = Field()
    first_licensing_year = Field()


class JockeyItem(Item):
    jockey_id = Field()
    name_kana = Field()
    name = Field()
    birthday = Field()
    belong_to = Field()
    first_licensing_year = Field()


class OddsWinPlaceItem(Item):
    race_id = Field()
    horse_number = Field()
    horse_id = Field()
    odds_win = Field()
    odds_place_min = Field()
    odds_place_max = Field()


class OddsBracketQuinellaItem(Item):
    race_id = Field()
    bracket_number_1 = Field()
    bracket_number_2 = Field()
    odds = Field()


class OddsExactaItem(Item):
    race_id = Field()
    horse_number_1 = Field()
    horse_number_2 = Field()
    odds = Field()


class OddsQuinellaItem(Item):
    race_id = Field()
    horse_number_1 = Field()
    horse_number_2 = Field()
    odds = Field()


class OddsQuinellaPlaceItem(Item):
    race_id = Field()
    horse_number_1 = Field()
    horse_number_2 = Field()
    odds_min = Field()
    odds_max = Field()


class OddsTrifectaItem(Item):
    race_id = Field()
    horse_number_1_2_3 = Field()
    odds = Field()


class OddsTrioItem(Item):
    race_id = Field()
    horse_number_1_2 = Field()
    horse_number_3 = Field()
    odds = Field()
