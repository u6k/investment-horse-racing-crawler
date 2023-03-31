import logging
import os

BOT_NAME = "horse_racing_crawler"
USER_AGENT = os.environ.get("USER_AGENT", "horse_racing_crawler/1.0 (+https://github.com/u6k/investment-horse-racing-crawler)")
CRAWL_HTTP_PROXY = os.environ.get("CRAWL_HTTP_PROXY")

SPIDER_MODULES = ["horse_racing_crawler.spiders"]
NEWSPIDER_MODULE = "horse_racing_crawler.spiders"

ROBOTSTXT_OBEY = True

CONCURRENT_REQUESTS = 1
CONCURRENT_REQUESTS_PER_DOMAIN = 1
CONCURRENT_REQUESTS_PER_IP = 0

DOWNLOAD_DELAY = 1
DOWNLOAD_TIMEOUT = 60
RETRY_TIMES = 10

HTTPCACHE_ENABLED = True
HTTPCACHE_STORAGE = "horse_racing_crawler.middlewares.S3CacheStorage"

SPIDER_CONTRACTS = {
    "horse_racing_crawler.contracts.CalendarContract": 10,
}

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

logging.getLogger("boto3").setLevel(logging.INFO)
logging.getLogger("botocore").setLevel(logging.INFO)

S3_ENDPOINT = os.environ["S3_ENDPOINT"]
S3_REGION = os.environ["S3_REGION"]
S3_ACCESS_KEY = os.environ["S3_ACCESS_KEY"]
S3_SECRET_KEY = os.environ["S3_SECRET_KEY"]
S3_BUCKET = os.environ["S3_BUCKET"]
S3_FOLDER = os.environ["S3_FOLDER"]
