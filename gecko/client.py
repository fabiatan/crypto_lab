import time

import httpx

BASE_URL = "https://api.geckoterminal.com/api/v2"
DEFAULT_MIN_INTERVAL = 2.2  # ~27 calls/min, safely under GT's 30/min limit


class GeckoClient:
    def __init__(self, min_interval: float = DEFAULT_MIN_INTERVAL, timeout: float = 20.0):
        self.client = httpx.Client(
            timeout=timeout,
            headers={"accept": "application/json"},
        )
        self.min_interval = min_interval
        self._last_call = 0.0

    def _throttle(self) -> None:
        elapsed = time.monotonic() - self._last_call
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self._last_call = time.monotonic()

    def get(self, path: str, **params) -> dict:
        self._throttle()
        r = self.client.get(f"{BASE_URL}{path}", params=params or None)
        r.raise_for_status()
        return r.json()

    def networks(self) -> list:
        return self.get("/networks")["data"]

    def dexes(self, network: str) -> list:
        return self.get(f"/networks/{network}/dexes")["data"]

    def trending_pools(self, network: str) -> list:
        return self.get(f"/networks/{network}/trending_pools")["data"]

    def new_pools(self, network: str) -> list:
        return self.get(f"/networks/{network}/new_pools")["data"]

    def pool(self, network: str, address: str) -> dict:
        return self.get(f"/networks/{network}/pools/{address}")["data"]

    def ohlcv(
        self,
        network: str,
        pool_address: str,
        timeframe: str = "hour",
        limit: int = 100,
    ) -> list:
        path = f"/networks/{network}/pools/{pool_address}/ohlcv/{timeframe}"
        return self.get(path, limit=limit)["data"]["attributes"]["ohlcv_list"]

    def close(self) -> None:
        self.client.close()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()
