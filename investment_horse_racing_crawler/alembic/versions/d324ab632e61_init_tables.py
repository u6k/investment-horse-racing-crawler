"""Init tables

Revision ID: d324ab632e61
Revises:
Create Date: 2020-01-24 03:35:45.011606

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd324ab632e61'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "race_info",
        sa.Column("id", sa.String(255), primary_key=True),
        sa.Column("race_id", sa.String(255), nullable=True),
        sa.Column("race_round", sa.String(255), nullable=True),
        sa.Column("start_date", sa.String(255), nullable=True),
        sa.Column("start_time", sa.String(255), nullable=True),
        sa.Column("place_name", sa.String(255), nullable=True),
        sa.Column("race_name", sa.String(255), nullable=True),
        sa.Column("course_type_length", sa.String(255), nullable=True),
        sa.Column("weather", sa.String(255), nullable=True),
        sa.Column("course_condition", sa.String(255), nullable=True),
        sa.Column("added_money", sa.String(255), nullable=True),
    )

    op.create_table(
        "race_payoff",
        sa.Column("id", sa.String(255), primary_key=True),
        sa.Column("race_id", sa.String(255), nullable=True),
        sa.Column("payoff_type", sa.String(255), nullable=True),
        sa.Column("horse_number", sa.String(255), nullable=True),
        sa.Column("odds", sa.String(255), nullable=True),
        sa.Column("favorite_order", sa.String(255), nullable=True),
    )

    op.create_table(
        "race_result",
        sa.Column("id", sa.String(255), primary_key=True),
        sa.Column("race_id", sa.String(255), nullable=True),
        sa.Column("result", sa.String(255), nullable=True),
        sa.Column("bracket_number", sa.String(255), nullable=True),
        sa.Column("horse_number", sa.String(255), nullable=True),
        sa.Column("horse_id", sa.String(255), nullable=True),
        sa.Column("horse_name", sa.String(255), nullable=True),
        sa.Column("horse_gender_age", sa.String(255), nullable=True),
        sa.Column("horse_weight_and_diff", sa.String(255), nullable=True),
        sa.Column("arrival_time", sa.String(255), nullable=True),
        sa.Column("jockey_id", sa.String(255), nullable=True),
        sa.Column("jockey_name", sa.String(255), nullable=True),
        sa.Column("jockey_weight", sa.String(255), nullable=True),
        sa.Column("favorite_order", sa.String(255), nullable=True),
        sa.Column("odds", sa.String(255), nullable=True),
        sa.Column("trainer_id", sa.String(255), nullable=True),
        sa.Column("trainer_name", sa.String(255), nullable=True),
    )

    op.create_table(
        "race_denma",
        sa.Column("id", sa.String(255), primary_key=True),
        sa.Column("race_id", sa.String(255), nullable=True),
        sa.Column("bracket_number", sa.String(255), nullable=True),
        sa.Column("horse_number", sa.String(255), nullable=True),
        sa.Column("horse_id", sa.String(255), nullable=True),
        sa.Column("trainer_id", sa.String(255), nullable=True),
        sa.Column("horse_weight_and_diff", sa.String(255), nullable=True),
        sa.Column("jockey_id", sa.String(255), nullable=True),
        sa.Column("jockey_weight", sa.String(255), nullable=True),
        sa.Column("prize_total_money", sa.String(255), nullable=True),
    )

    op.create_table(
        "horse",
        sa.Column("id", sa.String(255), primary_key=True),
        sa.Column("horse_id", sa.String(255), nullable=True),
        sa.Column("gender", sa.String(255), nullable=True),
        sa.Column("name", sa.String(255), nullable=True),
        sa.Column("birthday", sa.String(255), nullable=True),
        sa.Column("coat_color", sa.String(255), nullable=True),
        sa.Column("trainer_id", sa.String(255), nullable=True),
        sa.Column("owner", sa.String(255), nullable=True),
        sa.Column("breeder", sa.String(255), nullable=True),
        sa.Column("breeding_farm", sa.String(255), nullable=True),
    )

    op.create_table(
        "trainer",
        sa.Column("id", sa.String(255), primary_key=True),
        sa.Column("trainer_id", sa.String(255), nullable=True),
        sa.Column("name_kana", sa.String(255), nullable=True),
        sa.Column("name", sa.String(255), nullable=True),
        sa.Column("birthday", sa.String(255), nullable=True),
        sa.Column("belong_to", sa.String(255), nullable=True),
        sa.Column("first_licensing_year", sa.String(255), nullable=True),
    ),

    op.create_table(
        "jockey",
        sa.Column("id", sa.String(255), primary_key=True),
        sa.Column("jockey_id", sa.String(255), nullable=True),
        sa.Column("name_kana", sa.String(255), nullable=True),
        sa.Column("name", sa.String(255), nullable=True),
        sa.Column("birthday", sa.String(255), nullable=True),
        sa.Column("belong_to", sa.String(255), nullable=True),
        sa.Column("first_licensing_year", sa.String(255), nullable=True),
    )

    op.create_table(
        "odds_win_place",
        sa.Column("id", sa.String(255), primary_key=True),
        sa.Column("race_id", sa.String(255), nullable=True),
        sa.Column("horse_number", sa.String(255), nullable=True),
        sa.Column("horse_id", sa.String(255), nullable=True),
        sa.Column("odds_win", sa.String(255), nullable=True),
        sa.Column("odds_place_min", sa.String(255), nullable=True),
        sa.Column("odds_place_max", sa.String(255), nullable=True),
    )

    op.create_table(
        "odds_bracket_quinella",
        sa.Column("id", sa.String(255), primary_key=True),
        sa.Column("race_id", sa.String(255), nullable=True),
        sa.Column("bracket_number_1", sa.String(255), nullable=True),
        sa.Column("bracket_number_2", sa.String(255), nullable=True),
        sa.Column("odds", sa.String(255), nullable=True),
    )

    op.create_table(
        "odds_exacta",
        sa.Column("id", sa.String(255), primary_key=True),
        sa.Column("race_id", sa.String(255), nullable=True),
        sa.Column("horse_number_1", sa.String(255), nullable=True),
        sa.Column("horse_number_2", sa.String(255), nullable=True),
        sa.Column("odds", sa.String(255), nullable=True),
    )

    op.create_table(
        "odds_quinella",
        sa.Column("id", sa.String(255), primary_key=True),
        sa.Column("race_id", sa.String(255), nullable=True),
        sa.Column("horse_number_1", sa.String(255), nullable=True),
        sa.Column("horse_number_2", sa.String(255), nullable=True),
        sa.Column("odds", sa.String(255), nullable=True),
    )

    op.create_table(
        "odds_quinella_place",
        sa.Column("id", sa.String(255), primary_key=True),
        sa.Column("race_id", sa.String(255), nullable=True),
        sa.Column("horse_number_1", sa.String(255), nullable=True),
        sa.Column("horse_number_2", sa.String(255), nullable=True),
        sa.Column("odds_min", sa.String(255), nullable=True),
        sa.Column("odds_max", sa.String(255), nullable=True),
    )

    op.create_table(
        "odds_trifecta",
        sa.Column("id", sa.String(255), primary_key=True),
        sa.Column("race_id", sa.String(255), nullable=True),
        sa.Column("horse_number_1_2_3", sa.String(255), nullable=True),
        sa.Column("odds", sa.String(255), nullable=True),
    )

    op.create_table(
        "odds_trio",
        sa.Column("id", sa.String(255), primary_key=True),
        sa.Column("race_id", sa.String(255), nullable=True),
        sa.Column("horse_number_1_2", sa.String(255), nullable=True),
        sa.Column("horse_number_3", sa.String(255), nullable=True),
        sa.Column("odds", sa.String(255), nullable=True),
    )


def downgrade():
    pass
