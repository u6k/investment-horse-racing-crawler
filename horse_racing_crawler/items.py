# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class RaceInfoItem(Item):
    type = Field()
    race_id = Field()
    race_round = Field()
    race_name = Field()
    race_data1 = Field()
    race_data2 = Field()
    race_data3 = Field()


class RaceResultItem(Item):
    type = Field()
    race_id = Field()
    result = Field()
    bracket_number = Field()
    horse_number = Field()
    horse_id_url = Field()
    jockey_weight = Field()
    jockey_id_url = Field()
    arrival_time = Field()
    arrival_margin = Field()
    favorite_order = Field()
    final_600_meters_time = Field()
    corner_passing_order = Field()
    trainer_id_url = Field()
    horse_weight_and_diff = Field()


class RacePayoffItem(Item):
    type = Field()
    race_id = Field()
    betting_type = Field()
    horse_numbers = Field()
    payoff = Field()


class RaceCornerPassingItem(Item):
    type = Field()
    race_id = Field()
    corner_name = Field()
    passing_order = Field()


class RaceLapTimeItem(Item):
    type = Field()
    race_id = Field()
    length = Field()
    time1 = Field()
    time2 = Field()


class OddsItem(Item):
    type = Field()
    race_id = Field()
    odds_type = Field()
    horse_number = Field()
    odds1 = Field()
    odds2 = Field()
    favorite_order = Field()


class TrainingItem(Item):
    type = Field()
    race_id = Field()
    horse_number = Field()
    horse_id_url = Field()
    evaluation_text = Field()
    evaluation_rank = Field()


class HorseItem(Item):
    type = Field()
    horse_id = Field()
    horse_name = Field()
    gender = Field()
    birthday = Field()
    coat_color = Field()
    kigo = Field()
    tozai = Field()
    farm = Field()
    seri_name = Field()
    seri_price = Field()
    trainer_id = Field()
    breeder_id = Field()
    owner_id = Field()


class JockeyItem(Item):
    type = Field()
    jockey_id = Field()
    jockey_name = Field()
    jockey_text = Field()
    birth_place = Field()
    debut_year = Field()


class TrainerItem(Item):
    type = Field()
    trainer_id = Field()
    trainer_name = Field()
    trainer_text = Field()
    birth_place = Field()
    debut_year = Field()


class ParentHorseItem(Item):
    type = Field()
    parent_horse_id = Field()
    parent1_id = Field()
    parent2_id = Field()
    parent3_id = Field()
    parent4_id = Field()
    parent5_id = Field()
