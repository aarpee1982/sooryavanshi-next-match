# Sooryavanshi's Next Match 🏏

A Streamlit app tracking Vaibhav Sooryavanshi's IPL 2026 journey — his next match, live stats, innings log, and records.

## What it shows
- **Next match** — opponent, date, time in IST, venue
- **Live countdown** to match start
- **IPL 2026 stats** — runs, matches, best score, strike rate, sixes, fours, average, fifties, hundreds
- **Innings log** — ball-by-ball runs, fours, sixes per match
- **Records he holds** — youngest centurion, fastest century, etc.
- **Upcoming schedule** — next 4 RR matches

## How data works
- **Schedule**: Hardcoded from official RR 2026 fixtures. Next match auto-detected by date.
- **Stats**: Attempts live scrape from iplt20.com. Falls back to manually maintained stats.
- **Auto-refresh**: On match day, the app refreshes every 60 seconds.

## Keeping stats updated
When Vaibhav plays a match, update the `FALLBACK_STATS` dict in `app.py`:

```python
FALLBACK_STATS = {
    "matches": 6,         # increment
    "runs": 278,          # add latest innings runs
    "highest": 78,        # update if he sets a new best
    "average": 46.3,      # recalculate
    "strike_rate": 265.0, # recalculate
    "fours": 22,          # add fours from latest innings
    "sixes": 30,          # add sixes from latest innings
    "fifties": 3,
    "hundreds": 0,
    "innings": [
        # add a new dict for each completed innings
        {"match": "vs SRH", "runs": 39, "balls": 15, "fours": 3, "sixes": 3},
    ],
    "last_updated": "Apr 14, 2026 — after RR vs SRH"
}
```

## Setup locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy to Streamlit Cloud (free)
1. Push to a GitHub repo
2. Go to share.streamlit.io
3. Connect your repo → select `app.py`
4. Deploy

Takes under 2 minutes. Share the public URL on LinkedIn.

## Notes
- The schedule covers all 13 RR league matches. Playoff matches will need to be added manually once announced (likely late May 2026).
- The auto-refresh on match day causes continuous reloads. If it feels aggressive, remove the `st.rerun()` block at the bottom and users can refresh manually.
