# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html


import io
from pathlib import Path

import boto3
import joblib
from botocore.exceptions import ClientError
from scrapy.http import Headers
from scrapy.responsetypes import responsetypes


class S3CacheStorage:
    def __init__(self, settings):
        # Store parameters
        self.s3_endpoint = settings["S3_ENDPOINT"]
        self.s3_region = settings["S3_REGION"]
        self.s3_access_key = settings["S3_ACCESS_KEY"]
        self.s3_secret_key = settings["S3_SECRET_KEY"]
        self.s3_bucket = settings["S3_BUCKET"]
        self.s3_folder = settings["S3_FOLDER"]

        # Setup s3 client
        self.s3_client = boto3.resource("s3", endpoint_url=self.s3_endpoint, aws_access_key_id=self.s3_access_key, aws_secret_access_key=self.s3_secret_key, region_name=self.s3_region)

        self.s3_bucket_obj = self.s3_client.Bucket(self.s3_bucket)
        if not self.s3_bucket_obj.creation_date:
            self.s3_bucket_obj.create()

    def open_spider(self, spider):
        self._fingerprinter = spider.crawler.request_fingerprinter

    def close_spider(self, spider):
        pass

    def retrieve_response(self, spider, request):
        spider.logger.debug(f"#retrieve_response: start: url={request.url}")

        # TODO: キャッシュを制御する
        # if spider.recache_race and (("/schedule/list" in request.url) or ("/race/list" in request.url) or ("/race/result" in request.url) or ("/race/denma" in request.url) or ("/odds" in request.url)):
        #     logger.debug("#retrieve_response: re-cache race")
        #     return

        # if spider.recache_horse and (("/directory/horse" in request.url) or ("/directory/trainer" in request.url) or ("/directory/jocky" in request.url)):
        #     logger.debug("#retrieve_response: re-cache horse/jockey/trainer")
        #     return

        rpath = self._get_request_path(spider, request)
        spider.logger.debug(f"#retrieve_response: cache path={rpath}")

        s3_obj = self.s3_bucket_obj.Object(rpath + ".joblib")

        try:
            with io.BytesIO(s3_obj.get()["Body"].read()) as b:
                data = joblib.load(b)
        except ClientError as err:
            if err.response["Error"]["Code"] == "404" or err.response["Error"]["Code"] == "NoSuchKey":
                spider.logger.debug("#retrieve_response: cache not found")
                return
            else:
                raise err

        url = data["response"]["url"]
        status = data["response"]["status"]
        headers = Headers(data["response"]["headers"])
        body = data["response"]["body"]
        respcls = responsetypes.from_args(headers=headers, url=url)
        response = respcls(url=url, headers=headers, status=status, body=body)

        spider.logger.debug("#retrieve_response: cache exist")

        return response

    def store_response(self, spider, request, response):
        spider.logger.debug(f"#store_response: start: url={response.url}, status={response.status}")

        rpath = self._get_request_path(spider, request)
        spider.logger.debug(f"#store_response: cache path={rpath}")

        data = {
            "request": {
                "url": request.url,
                "method": request.method,
                "headers": request.headers,
                "body": request.body,
            },
            "response": {
                "url": response.url,
                "status": response.status,
                "headers": response.headers,
                "body": response.body,
            },
        }

        with io.BytesIO() as b:
            joblib.dump(data, b, compress=True)
            self.s3_bucket_obj.Object(rpath + ".joblib").put(Body=b.getvalue())

    def _get_request_path(self, spider, request):
        key = self._fingerprinter.fingerprint(request).hex()
        path = str(Path(self.s3_folder, spider.name, key[0:2], key))

        return path
