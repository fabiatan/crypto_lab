CREATE TABLE IF NOT EXISTS pool_snapshot (
    ts                    INTEGER NOT NULL,
    network               TEXT    NOT NULL,
    pool_address          TEXT    NOT NULL,
    kind                  TEXT    NOT NULL,  -- 'trending' or 'new'
    name                  TEXT,
    base_symbol           TEXT,
    quote_symbol          TEXT,
    base_token_price_usd  REAL,
    reserve_in_usd        REAL,
    fdv_usd               REAL,
    market_cap_usd        REAL,
    volume_m5_usd         REAL,
    volume_h1_usd         REAL,
    volume_h24_usd        REAL,
    price_change_m5       REAL,
    price_change_h1       REAL,
    price_change_h24      REAL,
    buys_h24              INTEGER,
    sells_h24             INTEGER,
    pool_created_at       TEXT,
    PRIMARY KEY (ts, network, pool_address, kind)
);

CREATE INDEX IF NOT EXISTS idx_pool_snapshot_pool ON pool_snapshot(network, pool_address);
CREATE INDEX IF NOT EXISTS idx_pool_snapshot_ts   ON pool_snapshot(ts);
