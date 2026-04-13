import streamlit as st
import requests
from datetime import datetime, timezone, timedelta
import time

st.set_page_config(
    page_title="Sooryavanshi's Next Match",
    page_icon="🏏",
    layout="centered",
    initial_sidebar_state="collapsed"
)

IST = timezone(timedelta(hours=5, minutes=30))

RR_SCHEDULE = [
    {"date": "2026-03-30", "time": "19:30", "opponent": "Chennai Super Kings",         "venue": "ACA Stadium, Guwahati",                    "short": "CSK",  "result": "RR won"},
    {"date": "2026-04-04", "time": "19:30", "opponent": "Gujarat Titans",              "venue": "Narendra Modi Stadium, Ahmedabad",          "short": "GT",   "result": "RR won"},
    {"date": "2026-04-07", "time": "19:30", "opponent": "Mumbai Indians",              "venue": "ACA Stadium, Guwahati",                    "short": "MI",   "result": "RR won"},
    {"date": "2026-04-10", "time": "19:30", "opponent": "Royal Challengers Bengaluru", "venue": "ACA Stadium, Guwahati",                    "short": "RCB",  "result": "RR won"},
    {"date": "2026-04-13", "time": "19:30", "opponent": "Sunrisers Hyderabad",         "venue": "Rajiv Gandhi Intl. Stadium, Hyderabad",    "short": "SRH",  "result": None},
    {"date": "2026-04-19", "time": "15:30", "opponent": "Kolkata Knight Riders",       "venue": "Eden Gardens, Kolkata",                    "short": "KKR",  "result": None},
    {"date": "2026-04-22", "time": "19:30", "opponent": "Lucknow Super Giants",        "venue": "Ekana Cricket Stadium, Lucknow",           "short": "LSG",  "result": None},
    {"date": "2026-04-25", "time": "19:30", "opponent": "Sunrisers Hyderabad",         "venue": "Sawai Mansingh Stadium, Jaipur",           "short": "SRH",  "result": None},
    {"date": "2026-04-28", "time": "19:30", "opponent": "Punjab Kings",                "venue": "New Intl. Cricket Stadium, New Chandigarh","short": "PBKS", "result": None},
    {"date": "2026-05-01", "time": "19:30", "opponent": "Delhi Capitals",              "venue": "Sawai Mansingh Stadium, Jaipur",           "short": "DC",   "result": None},
    {"date": "2026-05-09", "time": "19:30", "opponent": "Gujarat Titans",              "venue": "Sawai Mansingh Stadium, Jaipur",           "short": "GT",   "result": None},
    {"date": "2026-05-17", "time": "19:30", "opponent": "Delhi Capitals",              "venue": "Arun Jaitley Stadium, Delhi",              "short": "DC",   "result": None},
    {"date": "2026-05-19", "time": "19:30", "opponent": "Lucknow Super Giants",        "venue": "Sawai Mansingh Stadium, Jaipur",           "short": "LSG",  "result": None},
]

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
    ],
    "last_updated": "Apr 13, 2026"
}

def get_next_match():
    now_ist = datetime.now(IST)
    for match in RR_SCHEDULE:
        mdt = datetime.strptime(f"{match['date']} {match['time']}", "%Y-%m-%d %H:%M").replace(tzinfo=IST)
        if mdt >= now_ist - timedelta(hours=4):
            return match, mdt
    return None, None

def get_countdown(match_dt):
    now_ist = datetime.now(IST)
    delta = match_dt - now_ist
    if delta.total_seconds() <= 0:
        return "LIVE NOW!"
    days = delta.days
    hours, rem = divmod(delta.seconds, 3600)
    minutes, _ = divmod(rem, 60)
    if days > 0:
        return str(days) + "d " + str(hours).zfill(2) + "h " + str(minutes).zfill(2) + "m"
    return str(hours).zfill(2) + "h " + str(minutes).zfill(2) + "m"

stats = FALLBACK_STATS
next_match, match_dt = get_next_match()
now_ist = datetime.now(IST)
innings_by_match = {i['match'].replace('vs ', ''): i for i in stats['innings'] if i['balls'] > 0}

# Tetris block colors per stat
BLOCK_COLORS = ["#FF3B3B", "#FF9500", "#FFDD00", "#34C759", "#007AFF", "#AF52DE", "#FF2D55", "#5AC8FA", "#FF6B6B"]

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Nunito:wght@400;700;800;900&display=swap');

* { box-sizing: border-box; }

[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
footer, #MainMenu { display: none !important; }

[data-testid="stAppViewContainer"],
[data-testid="stMain"],
section.main {
    background: #FFFBF0 !important;
}

.block-container {
    padding: 0 !important;
    max-width: 740px !important;
    margin: 0 auto !important;
}

/* ── WRAPPER ── */
.tx {
    padding: 0 20px 80px;
    font-family: 'Nunito', sans-serif;
    background: #FFFBF0;
}

/* ── HERO ── */
.tx-hero {
    background: #FFDD00;
    border: 4px solid #1a1a1a;
    border-radius: 0px;
    padding: 36px 32px 32px;
    margin-bottom: 16px;
    position: relative;
    box-shadow: 6px 6px 0px #1a1a1a;
}
.tx-hero-eyebrow {
    font-family: 'Press Start 2P', monospace;
    font-size: 8px;
    color: #1a1a1a;
    letter-spacing: 1px;
    margin-bottom: 16px;
    opacity: 0.6;
}
.tx-hero-name {
    font-family: 'Press Start 2P', monospace;
    font-size: clamp(18px, 4.5vw, 28px);
    color: #1a1a1a;
    line-height: 1.5;
    margin-bottom: 16px;
}
.tx-hero-name span { color: #FF3B3B; }
.tx-hero-tags {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
}
.tx-tag {
    background: #1a1a1a;
    color: #FFDD00;
    font-family: 'Press Start 2P', monospace;
    font-size: 7px;
    padding: 6px 10px;
    border-radius: 0;
    letter-spacing: 0.5px;
}
.tx-bat-emoji {
    position: absolute;
    top: 24px;
    right: 28px;
    font-size: 48px;
    opacity: 0.25;
}

/* ── SECTION HEADER ── */
.tx-sec-title {
    font-family: 'Press Start 2P', monospace;
    font-size: 9px;
    color: #1a1a1a;
    letter-spacing: 1px;
    margin: 24px 0 12px;
    padding: 10px 14px;
    background: #1a1a1a;
    color: #FFDD00;
    display: inline-block;
}

/* ── NEXT MATCH CARD ── */
.tx-match-card {
    background: #007AFF;
    border: 4px solid #1a1a1a;
    padding: 28px;
    margin-bottom: 16px;
    box-shadow: 6px 6px 0px #1a1a1a;
    position: relative;
}
.tx-match-vs {
    font-family: 'Press Start 2P', monospace;
    font-size: clamp(13px, 3.5vw, 20px);
    color: #ffffff;
    line-height: 1.6;
    margin-bottom: 14px;
}
.tx-match-meta {
    font-family: 'Nunito', sans-serif;
    font-size: 14px;
    color: rgba(255,255,255,0.8);
    margin-bottom: 4px;
    font-weight: 700;
}
.tx-countdown {
    margin-top: 20px;
    background: #FFDD00;
    border: 3px solid #1a1a1a;
    padding: 14px 20px;
    display: inline-block;
}
.tx-countdown-val {
    font-family: 'Press Start 2P', monospace;
    font-size: clamp(16px, 4vw, 24px);
    color: #1a1a1a;
    letter-spacing: 2px;
}
.tx-countdown-lbl {
    font-family: 'Press Start 2P', monospace;
    font-size: 7px;
    color: #1a1a1a;
    margin-top: 6px;
    opacity: 0.6;
}
.tx-live-badge {
    display: inline-block;
    margin-top: 20px;
    background: #FF3B3B;
    border: 3px solid #1a1a1a;
    padding: 10px 18px;
    font-family: 'Press Start 2P', monospace;
    font-size: 10px;
    color: #ffffff;
    letter-spacing: 1px;
    animation: flash 0.8s step-end infinite;
}
@keyframes flash { 0%,100%{opacity:1} 50%{opacity:0.4} }

/* ── STATS TETRIS GRID ── */
.tx-tetris-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin-bottom: 16px;
}
.tx-block {
    border: 4px solid #1a1a1a;
    padding: 20px 16px;
    box-shadow: 5px 5px 0px #1a1a1a;
    text-align: center;
    position: relative;
}
.tx-block-num {
    font-family: 'Press Start 2P', monospace;
    font-size: clamp(22px, 5vw, 32px);
    color: #1a1a1a;
    line-height: 1;
    margin-bottom: 10px;
}
.tx-block-lbl {
    font-family: 'Press Start 2P', monospace;
    font-size: 7px;
    color: #1a1a1a;
    letter-spacing: 0.5px;
    opacity: 0.7;
}

/* ── INNINGS LOG ── */
.tx-innings-wrap {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-bottom: 16px;
}
.tx-innings-row {
    border: 4px solid #1a1a1a;
    padding: 16px 20px;
    display: grid;
    grid-template-columns: 56px 1fr auto auto auto;
    align-items: center;
    gap: 12px;
    box-shadow: 4px 4px 0px #1a1a1a;
}
.tx-inn-match {
    font-family: 'Press Start 2P', monospace;
    font-size: 7px;
    color: #1a1a1a;
    opacity: 0.6;
}
.tx-inn-runs {
    font-family: 'Press Start 2P', monospace;
    font-size: clamp(18px, 4vw, 26px);
    color: #1a1a1a;
    line-height: 1;
}
.tx-inn-balls {
    font-family: 'Nunito', sans-serif;
    font-size: 12px;
    color: #555;
    font-weight: 700;
}
.tx-inn-chip {
    background: #1a1a1a;
    color: #FFDD00;
    font-family: 'Press Start 2P', monospace;
    font-size: 7px;
    padding: 5px 8px;
}

/* ── RECORDS ── */
.tx-records-wrap {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-bottom: 16px;
}
.tx-record-card {
    border: 4px solid #1a1a1a;
    padding: 18px 20px;
    box-shadow: 4px 4px 0px #1a1a1a;
    display: flex;
    gap: 14px;
    align-items: flex-start;
}
.tx-record-num {
    font-family: 'Press Start 2P', monospace;
    font-size: 10px;
    color: #fff;
    background: #1a1a1a;
    width: 28px;
    height: 28px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}
.tx-record-title {
    font-family: 'Press Start 2P', monospace;
    font-size: 8px;
    color: #1a1a1a;
    line-height: 1.8;
    margin-bottom: 6px;
}
.tx-record-detail {
    font-family: 'Nunito', sans-serif;
    font-size: 13px;
    color: #555;
    font-weight: 700;
    line-height: 1.5;
}

/* ── MATCH SLIDER SECTION ── */
.tx-slider-card {
    border: 4px solid #1a1a1a;
    padding: 24px 22px;
    box-shadow: 6px 6px 0px #1a1a1a;
    margin-top: 12px;
    margin-bottom: 16px;
}
.tx-slider-title {
    font-family: 'Press Start 2P', monospace;
    font-size: clamp(11px, 3vw, 16px);
    color: #1a1a1a;
    line-height: 1.6;
    margin-bottom: 8px;
}
.tx-slider-meta {
    font-family: 'Nunito', sans-serif;
    font-size: 13px;
    color: #777;
    font-weight: 700;
    margin-bottom: 4px;
}
.tx-status-won  { display:inline-block; background:#34C759; border:3px solid #1a1a1a; color:#fff; font-family:'Press Start 2P',monospace; font-size:7px; padding:6px 12px; margin-top:12px; }
.tx-status-live { display:inline-block; background:#FF3B3B; border:3px solid #1a1a1a; color:#fff; font-family:'Press Start 2P',monospace; font-size:7px; padding:6px 12px; margin-top:12px; }
.tx-status-up   { display:inline-block; background:#8E8E93; border:3px solid #1a1a1a; color:#fff; font-family:'Press Start 2P',monospace; font-size:7px; padding:6px 12px; margin-top:12px; }

.tx-score-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 8px;
    margin-top: 18px;
}
.tx-score-cell {
    border: 3px solid #1a1a1a;
    padding: 14px 8px;
    text-align: center;
}
.tx-score-num {
    font-family: 'Press Start 2P', monospace;
    font-size: clamp(14px, 3vw, 20px);
    color: #1a1a1a;
    line-height: 1;
    margin-bottom: 8px;
}
.tx-score-lbl {
    font-family: 'Press Start 2P', monospace;
    font-size: 6px;
    color: #888;
}
.tx-nodata {
    margin-top: 16px;
    font-family: 'Press Start 2P', monospace;
    font-size: 8px;
    color: #aaa;
    letter-spacing: 1px;
}

/* ── FOOTER ── */
.tx-footer {
    margin-top: 32px;
    text-align: center;
    font-family: 'Press Start 2P', monospace;
    font-size: 7px;
    color: #aaa;
    letter-spacing: 1px;
    line-height: 2;
}

/* Slider overrides */
[data-testid="stSlider"] { padding: 8px 0 4px !important; }
div[data-baseweb="slider"] > div:first-child {
    background: #1a1a1a !important;
    height: 6px !important;
}
div[data-baseweb="slider"] > div > div[role="slider"] {
    background: #FF3B3B !important;
    border: 3px solid #1a1a1a !important;
    width: 22px !important;
    height: 22px !important;
    border-radius: 0 !important;
}
.stSlider p { color: #888 !important; font-family: 'Press Start 2P', monospace !important; font-size: 7px !important; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="tx">', unsafe_allow_html=True)

# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="tx-hero">'
    '<div class="tx-bat-emoji">🏏</div>'
    '<div class="tx-hero-eyebrow">RAJASTHAN ROYALS · IPL 2026</div>'
    '<div class="tx-hero-name">VAIBHAV<br><span>SOORY</span>AVANSHI</div>'
    '<div class="tx-hero-tags">'
    '<span class="tx-tag">AGE 15</span>'
    '<span class="tx-tag">OPENER</span>'
    '<span class="tx-tag">LEFT-HAND</span>'
    '<span class="tx-tag">BIHAR</span>'
    '</div>'
    '</div>',
    unsafe_allow_html=True
)

# ── NEXT MATCH ────────────────────────────────────────────────────────────────
st.markdown('<div class="tx-sec-title">▶ NEXT MATCH</div>', unsafe_allow_html=True)

if next_match:
    cd_str = get_countdown(match_dt)
    date_display = match_dt.strftime("%a, %d %b %Y")
    is_live = match_dt <= now_ist <= match_dt + timedelta(hours=4)

    if is_live:
        cd_html = '<div class="tx-live-badge">● LIVE NOW!</div>'
    else:
        cd_html = (
            '<div class="tx-countdown">'
            '<div class="tx-countdown-val">' + cd_str + '</div>'
            '<div class="tx-countdown-lbl">UNTIL MATCH STARTS</div>'
            '</div>'
        )

    st.markdown(
        '<div class="tx-match-card">'
        '<div class="tx-match-vs">RR vs<br>' + next_match['opponent'].upper() + '</div>'
        '<div class="tx-match-meta">📅 ' + date_display + ' · ' + next_match['time'] + ' IST</div>'
        '<div class="tx-match-meta">📍 ' + next_match['venue'] + '</div>'
        + cd_html + '</div>',
        unsafe_allow_html=True
    )

# ── SEASON STATS ──────────────────────────────────────────────────────────────
st.markdown('<div class="tx-sec-title">▶ IPL 2026 STATS</div>', unsafe_allow_html=True)

stat_data = [
    (stats['runs'], "RUNS"),
    (stats['matches'], "MATCHES"),
    (stats['highest'], "BEST"),
    (stats['strike_rate'], "STRIKE RATE"),
    (stats['sixes'], "SIXES 💥"),
    (stats['fours'], "FOURS"),
    (stats['average'], "AVERAGE"),
    (stats['fifties'], "FIFTIES"),
    (stats['hundreds'], "100s"),
]

colors = ["#FFDD00","#FF9500","#FF3B3B","#34C759","#007AFF","#AF52DE","#FF2D55","#5AC8FA","#FF6B6B"]

grid_html = '<div class="tx-tetris-grid">'
for i, (val, lbl) in enumerate(stat_data):
    bg = colors[i % len(colors)]
    grid_html += (
        '<div class="tx-block" style="background:' + bg + ';">'
        '<div class="tx-block-num">' + str(val) + '</div>'
        '<div class="tx-block-lbl">' + lbl + '</div>'
        '</div>'
    )
grid_html += '</div>'
st.markdown(grid_html, unsafe_allow_html=True)

# ── INNINGS LOG ───────────────────────────────────────────────────────────────
completed = [i for i in stats['innings'] if i['balls'] > 0]
if completed:
    st.markdown('<div class="tx-sec-title">▶ INNINGS LOG</div>', unsafe_allow_html=True)
    inn_colors = ["#FFDD00","#FF9500","#34C759","#007AFF","#AF52DE"]
    rows_html = '<div class="tx-innings-wrap">'
    for idx, inn in enumerate(completed):
        sr = round((inn['runs'] / inn['balls']) * 100, 1)
        bg = inn_colors[idx % len(inn_colors)]
        rows_html += (
            '<div class="tx-innings-row" style="background:' + bg + ';">'
            '<div class="tx-inn-match">' + inn['match'].replace('vs ','') + '</div>'
            '<div class="tx-inn-runs">' + str(inn['runs']) + '</div>'
            '<div class="tx-inn-balls">' + str(inn['balls']) + 'b<br>SR ' + str(sr) + '</div>'
            '<div class="tx-inn-chip">4s ' + str(inn['fours']) + '</div>'
            '<div class="tx-inn-chip">6s ' + str(inn['sixes']) + '</div>'
            '</div>'
        )
    rows_html += '</div>'
    st.markdown(rows_html, unsafe_allow_html=True)

# ── RECORDS ───────────────────────────────────────────────────────────────────
records = [
    ("YOUNGEST T20 CENTURION", "101 off 38 balls vs GT, IPL 2025. He was 14."),
    ("2ND FASTEST IPL CENTURY", "Off 35 deliveries. Only Chris Gayle is faster."),
    ("YOUNGEST IPL DEBUTANT", "14 years and 23 days when he walked out for RR."),
    ("U19 WC PLAYER OF TOURNAMENT", "175 off 80 balls in the final vs England U19."),
    ("ORANGE CAP HOLDER 2026", "267+ strike rate through the first four matches."),
]
rec_colors = ["#FF3B3B","#007AFF","#AF52DE","#34C759","#FF9500"]

st.markdown('<div class="tx-sec-title">▶ RECORDS</div>', unsafe_allow_html=True)
recs_html = '<div class="tx-records-wrap">'
for i, (title, detail) in enumerate(records):
    bg = rec_colors[i % len(rec_colors)]
    recs_html += (
        '<div class="tx-record-card" style="background:' + bg + '20; border-color:' + bg + ';">'
        '<div class="tx-record-num" style="background:' + bg + ';">' + str(i+1) + '</div>'
        '<div>'
        '<div class="tx-record-title">' + title + '</div>'
        '<div class="tx-record-detail">' + detail + '</div>'
        '</div>'
        '</div>'
    )
recs_html += '</div>'
st.markdown(recs_html, unsafe_allow_html=True)

# ── ALL MATCHES SLIDER ────────────────────────────────────────────────────────
st.markdown('<div class="tx-sec-title">▶ ALL MATCHES</div>', unsafe_allow_html=True)

match_labels = []
for idx, m in enumerate(RR_SCHEDULE):
    mdt = datetime.strptime(f"{m['date']} {m['time']}", "%Y-%m-%d %H:%M").replace(tzinfo=IST)
    is_past = mdt < now_ist - timedelta(hours=4)
    is_today = mdt.date() == now_ist.date()
    prefix = "✓" if is_past else ("●" if is_today else "○")
    match_labels.append(prefix + " M" + str(idx+1) + " · " + m['short'] + " (" + m['date'][5:] + ")")

selected_label = st.select_slider("match", options=match_labels, label_visibility="collapsed")
selected_idx = match_labels.index(selected_label)
sel = RR_SCHEDULE[selected_idx]
sel_dt = datetime.strptime(f"{sel['date']} {sel['time']}", "%Y-%m-%d %H:%M").replace(tzinfo=IST)
sel_is_past = sel_dt < now_ist - timedelta(hours=4)
sel_is_today = sel_dt.date() == now_ist.date()
sel_date = sel_dt.strftime("%a, %d %b %Y")
inn_data = innings_by_match.get(sel['short'], None)

slider_bg_colors = ["#FFDD00","#FF9500","#FF3B3B","#34C759","#007AFF","#AF52DE","#FF2D55","#5AC8FA","#FF6B6B","#FFDD00","#FF9500","#FF3B3B","#34C759"]
card_bg = slider_bg_colors[selected_idx % len(slider_bg_colors)]

if sel_is_today:
    pill = '<div class="tx-status-live">● LIVE TODAY</div>'
elif sel_is_past:
    pill = '<div class="tx-status-won">✓ ' + (sel.get('result') or 'PLAYED') + '</div>'
else:
    pill = '<div class="tx-status-up">UPCOMING</div>'

st.markdown(
    '<div class="tx-slider-card" style="background:' + card_bg + '30; border-color:' + card_bg + ';">'
    '<div class="tx-slider-title">RR vs<br>' + sel['opponent'].upper() + '</div>'
    '<div class="tx-slider-meta">📅 ' + sel_date + ' · ' + sel['time'] + ' IST</div>'
    '<div class="tx-slider-meta">📍 ' + sel['venue'] + '</div>'
    + pill,
    unsafe_allow_html=True
)

if inn_data:
    sr = round((inn_data['runs'] / inn_data['balls']) * 100, 1)
    score_colors = ["#FF3B3B","#FF9500","#FFDD00","#34C759","#007AFF"]
    sg = '<div class="tx-score-grid">'
    for val, lbl, sc in [
        (inn_data['runs'], "RUNS", score_colors[0]),
        (inn_data['balls'], "BALLS", score_colors[1]),
        (sr, "SR", score_colors[2]),
        (inn_data['sixes'], "SIXES", score_colors[3]),
        (inn_data['fours'], "FOURS", score_colors[4]),
    ]:
        sg += (
            '<div class="tx-score-cell" style="background:' + sc + '; border-color:#1a1a1a;">'
            '<div class="tx-score-num">' + str(val) + '</div>'
            '<div class="tx-score-lbl">' + lbl + '</div>'
            '</div>'
        )
    sg += '</div>'
    st.markdown(sg + '</div>', unsafe_allow_html=True)
elif sel_is_today:
    st.markdown('<div class="tx-nodata">MATCH IN PROGRESS...</div></div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="tx-nodata">STATS AFTER MATCH</div></div>', unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="tx-footer">'
    'IPL 2026 · RAJASTHAN ROYALS<br>'
    'UPDATED ' + stats['last_updated'] + '<br><br>'
    '🏏 WATCHING EVERY MATCH HE PLAYS'
    '</div>',
    unsafe_allow_html=True
)

st.markdown('</div>', unsafe_allow_html=True)

if next_match:
    match_date = datetime.strptime(next_match["date"], "%Y-%m-%d").date()
    if match_date == datetime.now(IST).date():
        time.sleep(1)
        st.rerun()
