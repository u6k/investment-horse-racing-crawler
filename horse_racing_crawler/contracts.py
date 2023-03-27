import re

from scrapy.contracts import Contract
from scrapy.exceptions import ContractFail
from scrapy.http import Request


class CalendarContract(Contract):
    name = "calendar_contract"

    def post_process(self, output):
        # Check requests
        requests = list(filter(lambda o: isinstance(o, Request), output))

        for r in requests:
            if not re.match(r"^https://race\.netkeiba\.com/top/race_list\.html\?kaisai_date=[0-9]{8}$", r.url):
                raise ContractFail(f"Unknown request: url={r.url}")
