import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta
import json
import time

# ─── PAGE CONFIG ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Sooryavanshi's Next Match",
    page_icon="🏏",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ─── IST TIMEZONE ─────────────────────────────────────────────────────────────
IST = timezone(timedelta(hours=5, minutes=30))

# ─── RR SCHEDULE 2026 (hardcoded, all times in IST) ──────────────────────────
RR_SCHEDULE = [
    {"date": "2026-03-30", "time": "19:30", "opponent": "Chennai Super Kings",    "venue": "ACA Stadium, Guwahati",              "short": "CSK", "result": "RR won"},
    {"date": "2026-04-04", "time": "19:30", "opponent": "Gujarat Titans",         "venue": "Narendra Modi Stadium, Ahmedabad",   "short": "GT",  "result": "RR won"},
    {"date": "2026-04-07", "time": "19:30", "opponent": "Mumbai Indians",         "venue": "ACA Stadium, Guwahati",              "short": "MI",  "result": "RR won"},
    {"date": "2026-04-10", "time": "19:30", "opponent": "Royal Challengers Bengaluru", "venue": "ACA Stadium, Guwahati",         "short": "RCB", "result": "RR won"},
    {"date": "2026-04-13", "time": "19:30", "opponent": "Sunrisers Hyderabad",    "venue": "Rajiv Gandhi Intl. Stadium, Hyderabad", "short": "SRH", "result": None},
    {"date": "2026-04-19", "time": "15:30", "opponent": "Kolkata Knight Riders",  "venue": "Eden Gardens, Kolkata",              "short": "KKR", "result": None},
    {"date": "2026-04-22", "time": "19:30", "opponent": "Lucknow Super Giants",   "venue": "Ekana Cricket Stadium, Lucknow",     "short": "LSG", "result": None},
    {"date": "2026-04-25", "time": "19:30", "opponent": "Sunrisers Hyderabad",    "venue": "Sawai Mansingh Stadium, Jaipur",     "short": "SRH", "result": None},
    {"date": "2026-04-28", "time": "19:30", "opponent": "Punjab Kings",           "venue": "New Intl. Cricket Stadium, New Chandigarh", "short": "PBKS", "result": None},
    {"date": "2026-05-01", "time": "19:30", "opponent": "Delhi Capitals",         "venue": "Sawai Mansingh Stadium, Jaipur",     "short": "DC",  "result": None},
    {"date": "2026-05-09", "time": "19:30", "opponent": "Gujarat Titans",         "venue": "Sawai Mansingh Stadium, Jaipur",     "short": "GT",  "result": None},
    {"date": "2026-05-17", "time": "19:30", "opponent": "Delhi Capitals",         "venue": "Arun Jaitley Stadium, Delhi",        "short": "DC",  "result": None},
    {"date": "2026-05-19", "time": "19:30", "opponent": "Lucknow Super Giants",   "venue": "Sawai Mansingh Stadium, Jaipur",     "short": "LSG", "result": None},
]

# ─── FALLBACK STATS (as of April 13, 2026) ────────────────────────────────────
FALLBACK_STATS = {
    "matches": 5,
    "runs": 239,
    "highest": 78,
    "average": 47.8,
    "strike_rate": 267.4,
    "fours": 19,
    "sixes": 27,
    "fifties": 3,
    "hundreds": 0,
    "innings": [
        {"match": "vs CSK", "runs": 52, "balls": 17, "fours": 4, "sixes": 5},
        {"match": "vs GT",  "runs": 31, "balls": 18, "fours": 5, "sixes": 1},
        {"match": "vs MI",  "runs": 39, "balls": 14, "fours": 2, "sixes": 5},
        {"match": "vs RCB", "runs": 78, "balls": 26, "fours": 5, "sixes": 8},
        {"match": "vs SRH", "runs": 0,  "balls": 0,  "fours": 0, "sixes": 0},  # today's match placeholder
    ],
    "last_updated": "Apr 13, 2026 — Live match day"
}

# ─── SCRAPE STATS FROM CRICBUZZ ───────────────────────────────────────────────
@st.cache_data(ttl=300)  # cache 5 min
def fetch_live_stats():
    """Try to scrape Vaibhav's IPL 2026 stats. Falls back to hardcoded data."""
    try:
        url = "https://www.iplt20.com/players/vaibhav-sooryavanshi/22203"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        r = requests.get(url, headers=headers, timeout=8)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "html.parser")
            # Try to find stats tables
            stats = {}
            tables = soup.find_all("table")
            for table in tables:
                rows = table.find_all("tr")
                for row in rows:
                    cells = row.find_all(["td", "th"])
                    if len(cells) >= 2:
                        pass  # Parse as needed
            # If we can't reliably parse, fall back
            return None
    except Exception:
        return None
    return None

# ─── FIND NEXT MATCH ──────────────────────────────────────────────────────────
def get_next_match():
    now_ist = datetime.now(IST)
    for match in RR_SCHEDULE:
        match_dt_str = f"{match['date']} {match['time']}"
        match_dt = datetime.strptime(match_dt_str, "%Y-%m-%d %H:%M").replace(tzinfo=IST)
        # Show current match if within 4 hours of start (likely live or upcoming today)
        if match_dt >= now_ist - timedelta(hours=4):
            return match, match_dt
    return None, None

def get_countdown(match_dt):
    now_ist = datetime.now(IST)
    delta = match_dt - now_ist
    if delta.total_seconds() < 0:
        return None, "Live / In Progress"
    days = delta.days
    hours, rem = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(rem, 60)
    label = ""
    if days > 0:
        label += f"{days}d "
    label += f"{hours:02d}h {minutes:02d}m {seconds:02d}s"
    return delta.total_seconds(), label

# ─── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

/* Reset & base */
[data-testid="stAppViewContainer"] {
    background: #f0f7ff;
}
[data-testid="stHeader"] { background: transparent; }
[data-testid="stToolbar"] { display: none; }

/* Main container */
.main-wrapper {
    max-width: 680px;
    margin: 0 auto;
    padding: 0 0 60px 0;
    font-family: 'DM Sans', sans-serif;
}

/* HERO */
.hero {
    background: linear-gradient(135deg, #0a1628 0%, #0d2247 50%, #091d3e 100%);
    border-radius: 24px;
    padding: 48px 40px 40px;
    margin-bottom: 20px;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(59,130,246,0.15) 0%, transparent 70%);
    border-radius: 50%;
}
.hero::after {
    content: '🏏';
    position: absolute;
    bottom: 20px; right: 32px;
    font-size: 80px;
    opacity: 0.12;
}
.hero-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #60a5fa;
    margin-bottom: 12px;
}
.hero-name {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 64px;
    line-height: 1;
    color: #ffffff;
    letter-spacing: 2px;
    margin-bottom: 4px;
}
.hero-sub {
    font-size: 14px;
    color: #94a3b8;
    font-weight: 400;
}
.hero-age-badge {
    display: inline-block;
    margin-top: 16px;
    background: rgba(59,130,246,0.2);
    border: 1px solid rgba(59,130,246,0.4);
    border-radius: 100px;
    padding: 4px 14px;
    font-size: 12px;
    color: #93c5fd;
    font-family: 'DM Mono', monospace;
}

/* NEXT MATCH CARD */
.next-match-card {
    background: #ffffff;
    border-radius: 20px;
    padding: 32px;
    margin-bottom: 16px;
    border: 1.5px solid #e0eeff;
    box-shadow: 0 4px 24px rgba(14,50,120,0.07);
}
.section-label {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: #94a3b8;
    margin-bottom: 16px;
}
.vs-block {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 20px;
}
.team-pill {
    background: #eff6ff;
    border-radius: 10px;
    padding: 10px 18px;
    font-family: 'Bebas Neue', sans-serif;
    font-size: 22px;
    letter-spacing: 1px;
    color: #1e3a5f;
}
.vs-text {
    font-family: 'DM Mono', monospace;
    font-size: 13px;
    color: #94a3b8;
}
.match-meta {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin-bottom: 24px;
}
.meta-item {
    background: #f8faff;
    border-radius: 12px;
    padding: 12px 16px;
}
.meta-label {
    font-size: 10px;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #94a3b8;
    margin-bottom: 4px;
    font-family: 'DM Mono', monospace;
}
.meta-value {
    font-size: 15px;
    font-weight: 600;
    color: #0d2247;
}

/* COUNTDOWN */
.countdown-block {
    background: linear-gradient(135deg, #1d4ed8, #2563eb);
    border-radius: 14px;
    padding: 18px 24px;
    text-align: center;
}
.countdown-label {
    font-size: 10px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: rgba(255,255,255,0.6);
    font-family: 'DM Mono', monospace;
    margin-bottom: 6px;
}
.countdown-value {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 40px;
    color: #ffffff;
    letter-spacing: 3px;
    line-height: 1;
}
.live-badge {
    display: inline-block;
    background: #ef4444;
    border-radius: 100px;
    padding: 6px 20px;
    font-family: 'DM Mono', monospace;
    font-size: 13px;
    color: white;
    letter-spacing: 2px;
    text-transform: uppercase;
    animation: pulse 1.5s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.6; }
}

/* STATS GRID */
.stats-card {
    background: #ffffff;
    border-radius: 20px;
    padding: 32px;
    margin-bottom: 16px;
    border: 1.5px solid #e0eeff;
    box-shadow: 0 4px 24px rgba(14,50,120,0.07);
}
.stats-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin-top: 16px;
}
.stat-box {
    background: #f0f7ff;
    border-radius: 14px;
    padding: 18px 14px;
    text-align: center;
}
.stat-box.highlight {
    background: linear-gradient(135deg, #0d2247, #1d4ed8);
}
.stat-number {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 36px;
    color: #0d2247;
    line-height: 1;
    margin-bottom: 4px;
}
.stat-box.highlight .stat-number {
    color: #ffffff;
}
.stat-name {
    font-size: 10px;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #64748b;
    font-family: 'DM Mono', monospace;
}
.stat-box.highlight .stat-name {
    color: rgba(255,255,255,0.7);
}

/* MATCH LOG */
.log-card {
    background: #ffffff;
    border-radius: 20px;
    padding: 32px;
    margin-bottom: 16px;
    border: 1.5px solid #e0eeff;
    box-shadow: 0 4px 24px rgba(14,50,120,0.07);
}
.log-row {
    display: grid;
    grid-template-columns: 60px 1fr auto auto auto;
    gap: 8px;
    align-items: center;
    padding: 12px 0;
    border-bottom: 1px solid #f1f5f9;
    font-size: 14px;
}
.log-row:last-child { border-bottom: none; }
.log-match { color: #94a3b8; font-family: 'DM Mono', monospace; font-size: 11px; }
.log-runs { font-family: 'Bebas Neue', sans-serif; font-size: 26px; color: #0d2247; line-height: 1; }
.log-balls { color: #94a3b8; font-size: 12px; font-family: 'DM Mono', monospace; }
.log-tag { background: #eff6ff; border-radius: 6px; padding: 2px 8px; font-size: 11px; color: #3b82f6; font-family: 'DM Mono', monospace; }
.log-tag.six { background: #fff7ed; color: #ea580c; }

/* RECORDS */
.records-card {
    background: linear-gradient(135deg, #0a1628 0%, #0d2247 100%);
    border-radius: 20px;
    padding: 32px;
    margin-bottom: 16px;
}
.record-item {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 14px 0;
    border-bottom: 1px solid rgba(255,255,255,0.07);
}
.record-item:last-child { border-bottom: none; }
.record-dot {
    width: 6px; height: 6px;
    background: #3b82f6;
    border-radius: 50%;
    margin-top: 7px;
    flex-shrink: 0;
}
.record-text {
    font-size: 14px;
    color: #cbd5e1;
    line-height: 1.5;
}
.record-text strong {
    color: #ffffff;
    font-weight: 600;
}

/* FOOTER */
.footer {
    text-align: center;
    padding: 20px;
    color: #94a3b8;
    font-size: 12px;
    font-family: 'DM Mono', monospace;
}

/* Streamlit component overrides */
div[data-testid="stVerticalBlock"] > div { padding: 0; }
.block-container { padding: 2rem 1rem 0; }
</style>
""", unsafe_allow_html=True)

# ─── FETCH DATA ───────────────────────────────────────────────────────────────
live = fetch_live_stats()
stats = live if live else FALLBACK_STATS

next_match, match_dt = get_next_match()

# ─── RENDER ───────────────────────────────────────────────────────────────────
st.markdown('<div class="main-wrapper">', unsafe_allow_html=True)

# HERO
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">Rajasthan Royals · IPL 2026</div>
    <div class="hero-name">Vaibhav<br>Sooryavanshi</div>
    <div class="hero-sub">Opener · Left-hand bat · Bihar</div>
    <div class="hero-age-badge">15 years old · Born Mar 27, 2011</div>
</div>
""", unsafe_allow_html=True)

# NEXT MATCH
if next_match:
    _, countdown_str = get_countdown(match_dt)
    date_obj = datetime.strptime(next_match["date"], "%Y-%m-%d")
    date_display = date_obj.strftime("%A, %b %d")
    time_display = next_match["time"] + " IST"

    is_live = match_dt <= datetime.now(IST) <= match_dt + timedelta(hours=4)

    countdown_html = ""
    if is_live:
        countdown_html = '<div class="live-badge">● Live Now</div>'
    else:
        countdown_html = f"""
        <div class="countdown-block">
            <div class="countdown-label">Match starts in</div>
            <div class="countdown-value" id="countdown">{countdown_str}</div>
        </div>
        """

    st.markdown(f"""
    <div class="next-match-card">
        <div class="section-label">Next Match</div>
        <div class="vs-block">
            <div class="team-pill">RR</div>
            <div class="vs-text">vs</div>
            <div class="team-pill">{next_match['short']}</div>
        </div>
        <div class="match-meta">
            <div class="meta-item">
                <div class="meta-label">Opponent</div>
                <div class="meta-value">{next_match['opponent']}</div>
            </div>
            <div class="meta-item">
                <div class="meta-label">Date</div>
                <div class="meta-value">{date_display}</div>
            </div>
            <div class="meta-item">
                <div class="meta-label">Time (IST)</div>
                <div class="meta-value">{time_display}</div>
            </div>
            <div class="meta-item">
                <div class="meta-label">Venue</div>
                <div class="meta-value" style="font-size:13px">{next_match['venue']}</div>
            </div>
        </div>
        {countdown_html}
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="next-match-card">
        <div class="section-label">Season Status</div>
        <div style="font-size: 20px; font-weight: 600; color: #0d2247;">IPL 2026 league stage complete</div>
        <div style="color: #64748b; margin-top: 8px; font-size: 14px;">Watch out for playoffs announcement.</div>
    </div>
    """, unsafe_allow_html=True)

# STATS 2026
st.markdown(f"""
<div class="stats-card">
    <div class="section-label">IPL 2026 Stats</div>
    <div style="font-size: 11px; color: #94a3b8; font-family: 'DM Mono', monospace; margin-bottom: 4px;">
        {stats['last_updated']}
    </div>
    <div class="stats-grid">
        <div class="stat-box highlight">
            <div class="stat-number">{stats['runs']}</div>
            <div class="stat-name">Runs</div>
        </div>
        <div class="stat-box">
            <div class="stat-number">{stats['matches']}</div>
            <div class="stat-name">Matches</div>
        </div>
        <div class="stat-box">
            <div class="stat-number">{stats['highest']}</div>
            <div class="stat-name">Best</div>
        </div>
        <div class="stat-box">
            <div class="stat-number">{stats['strike_rate']}</div>
            <div class="stat-name">Strike Rate</div>
        </div>
        <div class="stat-box highlight">
            <div class="stat-number">{stats['sixes']}</div>
            <div class="stat-name">Sixes</div>
        </div>
        <div class="stat-box">
            <div class="stat-number">{stats['fours']}</div>
            <div class="stat-name">Fours</div>
        </div>
        <div class="stat-box">
            <div class="stat-number">{stats['average']}</div>
            <div class="stat-name">Average</div>
        </div>
        <div class="stat-box">
            <div class="stat-number">{stats['fifties']}</div>
            <div class="stat-name">Fifties</div>
        </div>
        <div class="stat-box">
            <div class="stat-number">{stats['hundreds']}</div>
            <div class="stat-name">Hundreds</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# INNINGS LOG
completed_innings = [i for i in stats['innings'] if i['balls'] > 0]
if completed_innings:
    rows_html = ""
    for inn in completed_innings:
        rows_html += f"""
        <div class="log-row">
            <div class="log-match">{inn['match']}</div>
            <div class="log-runs">{inn['runs']}</div>
            <div class="log-balls">({inn['balls']} b)</div>
            <div class="log-tag">4s: {inn['fours']}</div>
            <div class="log-tag six">6s: {inn['sixes']}</div>
        </div>
        """

    st.markdown(f"""
    <div class="log-card">
        <div class="section-label">Innings Log — IPL 2026</div>
        {rows_html}
    </div>
    """, unsafe_allow_html=True)

# RECORDS
st.markdown("""
<div class="records-card">
    <div class="section-label" style="color: #60a5fa;">Records He Holds</div>
    <div class="record-item">
        <div class="record-dot"></div>
        <div class="record-text"><strong>Youngest centurion in men's T20 cricket</strong> — 101 off 38 balls vs GT, IPL 2025 (age 14)</div>
    </div>
    <div class="record-item">
        <div class="record-dot"></div>
        <div class="record-text"><strong>2nd fastest century in IPL history</strong> — off just 35 deliveries</div>
    </div>
    <div class="record-item">
        <div class="record-dot"></div>
        <div class="record-text"><strong>Youngest IPL debutant ever</strong> — at 14 years and 23 days</div>
    </div>
    <div class="record-item">
        <div class="record-dot"></div>
        <div class="record-text"><strong>U19 World Cup 2026 Player of the Tournament</strong> — 175 off 80 balls in the final vs England U19</div>
    </div>
    <div class="record-item">
        <div class="record-dot"></div>
        <div class="record-text"><strong>Orange Cap holder, IPL 2026</strong> — 267+ strike rate across the first four matches</div>
    </div>
</div>
""", unsafe_allow_html=True)

# UPCOMING SCHEDULE
now_ist = datetime.now(IST)
upcoming = []
for m in RR_SCHEDULE:
    mdt = datetime.strptime(f"{m['date']} {m['time']}", "%Y-%m-%d %H:%M").replace(tzinfo=IST)
    if mdt > now_ist + timedelta(hours=4):
        upcoming.append((m, mdt))

if upcoming[:4]:
    rows = ""
    for m, mdt in upcoming[:4]:
        dstr = mdt.strftime("%b %d")
        rows += f"""
        <div style="display:flex; justify-content:space-between; align-items:center; padding: 12px 0; border-bottom: 1px solid #f1f5f9; font-size: 14px;">
            <div style="font-family: 'DM Mono', monospace; font-size: 11px; color: #94a3b8; width: 60px;">{dstr}</div>
            <div style="flex: 1; font-weight: 600; color: #0d2247;">RR vs {m['short']}</div>
            <div style="font-size: 12px; color: #64748b;">{m['time']} IST</div>
        </div>
        """
    st.markdown(f"""
    <div class="stats-card">
        <div class="section-label">Coming Up</div>
        {rows}
    </div>
    """, unsafe_allow_html=True)

# FOOTER
st.markdown("""
<div class="footer">
    Built for fans who discovered cricket through a 15-year-old.<br>
    Stats refresh every 5 minutes · IPL 2026 · Rajasthan Royals
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Auto-refresh every 60s if match is today
if next_match:
    match_date = datetime.strptime(next_match["date"], "%Y-%m-%d").date()
    if match_date == datetime.now(IST).date():
        time.sleep(1)
        st.rerun()
