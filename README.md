# crypto_lab

Personal learning scaffold for GeckoTerminal + crypto market data exploration.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Snapshot pools into SQLite

```bash
python -m gecko.snapshot --network solana --kind trending
python -m gecko.snapshot --network solana --kind new
python -m gecko.snapshot --network base   --kind new
```

Data lands in `data/gecko.db` (gitignored).

Suggested cadence: twice a day for a week, then explore in `notebooks/explore.ipynb`.

## Explore

```bash
jupyter notebook notebooks/explore.ipynb
```

## Valid network IDs

`solana`, `eth`, `base`, `bsc`, `arbitrum`, `polygon_pos`, `avax`, and more.
Full list: `curl -s https://api.geckoterminal.com/api/v2/networks | jq '.data[].id'`
