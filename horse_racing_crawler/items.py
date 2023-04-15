# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class RaceInfoItem(Item):
    race_id = Field()
    race_round = Field()
    race_name = Field()
    race_data1 = Field()
    race_data2 = Field()


class RaceResultItem(Item):
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
    race_id = Field()
    betting_type = Field()
    horse_numbers = Field()
    payoff = Field()


class RaceCornerPassingItem(Item):
    race_id = Field()
    corner_name = Field()
    passing_order = Field()


class RaceLapTimeItem(Item):
    race_id = Field()
    length = Field()
    time1 = Field()
    time2 = Field()


class OddsItem(Item):
    race_id = Field()
    odds_type = Field()
    horse_number = Field()
    odds1 = Field()
    odds2 = Field()
    favorite_order = Field()


class TrainingItem(Item):
    race_id = Field()
    horse_number = Field()
    horse_id_url = Field()
    evaluation_text = Field()
    evaluation_rank = Field()
