import argparse
import datetime as dt
import sqlite3
from pathlib import Path

from .client import GeckoClient

SCHEMA_PATH = Path(__file__).parent / "schema.sql"
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DB_PATH = DATA_DIR / "gecko.db"


def _f(x):
    if x is None or x == "":
        return None
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def _i(x):
    if x is None:
        return None
    try:
        return int(x)
    except (TypeError, ValueError):
        return None


def _connect() -> sqlite3.Connection:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    con.executescript(SCHEMA_PATH.read_text())
    return con


def _row(ts: int, network: str, kind: str, pool: dict) -> tuple:
    a = pool.get("attributes", {}) or {}
    vol = a.get("volume_usd") or {}
    pc = a.get("price_change_percentage") or {}
    tx24 = (a.get("transactions") or {}).get("h24") or {}

    name = a.get("name") or ""
    base_sym, _, quote_sym = name.partition(" / ")

    return (
        ts,
        network,
        a.get("address"),
        kind,
        name or None,
        base_sym or None,
        quote_sym or None,
        _f(a.get("base_token_price_usd")),
        _f(a.get("reserve_in_usd")),
        _f(a.get("fdv_usd")),
        _f(a.get("market_cap_usd")),
        _f(vol.get("m5")),
        _f(vol.get("h1")),
        _f(vol.get("h24")),
        _f(pc.get("m5")),
        _f(pc.get("h1")),
        _f(pc.get("h24")),
        _i(tx24.get("buys")),
        _i(tx24.get("sells")),
        a.get("pool_created_at"),
    )


def snapshot(network: str, kind: str) -> tuple[int, int]:
    with GeckoClient() as gt:
        pools = gt.trending_pools(network) if kind == "trending" else gt.new_pools(network)

    ts = int(dt.datetime.now(dt.timezone.utc).timestamp())
    rows = [_row(ts, network, kind, p) for p in pools]

    with _connect() as con:
        con.executemany(
            "INSERT OR REPLACE INTO pool_snapshot VALUES ("
            + ",".join(["?"] * 20)
            + ")",
            rows,
        )
        con.commit()

    return len(rows), ts


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Snapshot GeckoTerminal pools into local SQLite."
    )
    parser.add_argument("--network", required=True, help="e.g. solana, eth, base, bsc")
    parser.add_argument("--kind", choices=["trending", "new"], required=True)
    args = parser.parse_args()

    n, ts = snapshot(args.network, args.kind)
    iso = dt.datetime.fromtimestamp(ts, dt.timezone.utc).isoformat()
    print(f"[{iso}] {args.network} {args.kind}: {n} pools -> {DB_PATH}")


if __name__ == "__main__":
    main()
