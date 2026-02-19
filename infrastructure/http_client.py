import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class HttpClient:

    def __init__(self):
        self.session = requests.Session()

        retries = Retry(
            total=5,
            backoff_factor=1,
            status_forcelist=[500, 502, 503, 504]
        )

        self.session.mount("https://", HTTPAdapter(max_retries=retries))

        self.headers = {
            "User-Agent": "Mozilla/5.0"
        }

    def get(self, url):
        return self.session.get(url, headers=self.headers, timeout=10)
