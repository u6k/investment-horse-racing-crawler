import logging
import os


BOT_NAME = 'investment_horse_racing_crawler'
USER_AGENT = os.environ.get("USER_AGENT", "horse_racing_crawler/1.0 (+https://github.com/u6k/investment-horse-racing-crawler)")

SPIDER_MODULES = ['investment_horse_racing_crawler.scrapy.spiders']
NEWSPIDER_MODULE = 'investment_horse_racing_crawler.scrapy.spiders'
CRAWL_HTTP_PROXY = os.environ.get("CRAWL_HTTP_PROXY")


ROBOTSTXT_OBEY = True

CONCURRENT_REQUESTS = 1
CONCURRENT_REQUESTS_PER_DOMAIN = 1
CONCURRENT_REQUESTS_PER_IP = 0

DOWNLOAD_DELAY = 1
DOWNLOAD_TIMEOUT = 60
RETRY_TIMES = 10

ITEM_PIPELINES = {
    "investment_horse_racing_crawler.scrapy.pipelines.PostgreSQLPipeline": 300,
}

HTTPCACHE_ENABLED = True
HTTPCACHE_STORAGE = "investment_horse_racing_crawler.scrapy.middlewares.S3CacheStorage"

SPIDER_CONTRACTS = {
    "investment_horse_racing_crawler.scrapy.contracts.ScheduleListContract": 10,
    "investment_horse_racing_crawler.scrapy.contracts.RaceListContract": 10,
    "investment_horse_racing_crawler.scrapy.contracts.RaceResultContract": 10,
    "investment_horse_racing_crawler.scrapy.contracts.RaceDenmaContract": 10,
    "investment_horse_racing_crawler.scrapy.contracts.HorseContract": 10,
    "investment_horse_racing_crawler.scrapy.contracts.TrainerContract": 10,
    "investment_horse_racing_crawler.scrapy.contracts.JockeyContract": 10,
    "investment_horse_racing_crawler.scrapy.contracts.OddsWinPlaceContract": 10,
    "investment_horse_racing_crawler.scrapy.contracts.OddsExactaContract": 10,
    "investment_horse_racing_crawler.scrapy.contracts.OddsQuinellaContract": 10,
    "investment_horse_racing_crawler.scrapy.contracts.OddsQuinellaPlaceContract": 10,
    "investment_horse_racing_crawler.scrapy.contracts.OddsTrifectaContract": 10,
    "investment_horse_racing_crawler.scrapy.contracts.OddsTrioContract": 10,
}

logging.getLogger("boto3").setLevel(logging.INFO)
logging.getLogger("botocore").setLevel(logging.INFO)

S3_ENDPOINT = os.environ["S3_ENDPOINT"]
S3_REGION = os.environ["S3_REGION"]
S3_ACCESS_KEY = os.environ["S3_ACCESS_KEY"]
S3_SECRET_KEY = os.environ["S3_SECRET_KEY"]
S3_BUCKET = os.environ["S3_BUCKET"]
S3_FOLDER = os.environ["S3_FOLDER"]

DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_DATABASE = os.environ["DB_DATABASE"]
DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
