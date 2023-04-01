from urllib.parse import parse_qs, urlparse

from scrapy.contracts import Contract
from scrapy.exceptions import ContractFail
from scrapy.http import Request


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

            if url.hostname == "race.netkeiba.com" and url.path == "/top/race_list_sub.html" and "kaisai_date" in qs:
                continue

            raise ContractFail(f"Unknown request: url={r.url}")
