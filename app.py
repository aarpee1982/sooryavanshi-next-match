import streamlit as st
import requests
from bs4 import BeautifulSoup
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

@st.cache_data(ttl=300)
def fetch_live_stats():
    try:
        url = "https://www.iplt20.com/players/vaibhav-sooryavanshi/22203"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        r = requests.get(url, headers=headers, timeout=8)
        if r.status_code == 200:
            return None
    except Exception:
        return None
    return None

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
        return None, "LIVE"
    days = delta.days
    hours, rem = divmod(delta.seconds, 3600)
    minutes, _ = divmod(rem, 60)
    if days > 0:
        return delta.total_seconds(), str(days) + "D " + str(hours).zfill(2) + "H " + str(minutes).zfill(2) + "M"
    return delta.total_seconds(), str(hours).zfill(2) + "H " + str(minutes).zfill(2) + "M"

stats = fetch_live_stats() or FALLBACK_STATS
next_match, match_dt = get_next_match()
now_ist = datetime.now(IST)
innings_by_match = {i['match'].replace('vs ', ''): i for i in stats['innings'] if i['balls'] > 0}

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Oswald:wght@300;400;500;600;700&display=swap');

* { box-sizing: border-box; }

[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
footer, #MainMenu { display: none !important; }

[data-testid="stAppViewContainer"],
[data-testid="stMain"],
section.main { background: #080808 !important; }

.block-container {
    padding: 0 !important;
    max-width: 720px !important;
    margin: 0 auto !important;
}

.sv { padding: 0 28px 80px; font-family: 'Inter', sans-serif; color: #fff; background: #080808; }

.sv-hero { padding: 72px 0 56px; border-bottom: 1px solid #161616; }
.sv-tag { font-size: 10px; font-weight: 500; letter-spacing: 4px; text-transform: uppercase; color: #3a3a3a; margin-bottom: 20px; }
.sv-name { font-family: 'Oswald', sans-serif; font-size: clamp(58px, 13vw, 92px); font-weight: 700; line-height: 0.9; color: #fff; letter-spacing: -1px; margin-bottom: 22px; }
.sv-name span { color: #222; }
.sv-meta { font-size: 12px; color: #333; letter-spacing: 1px; display: flex; gap: 20px; flex-wrap: wrap; }
.sv-meta b { color: #666; font-weight: 500; }

.sv-sec { padding: 48px 0; border-bottom: 1px solid #111; }
.sv-sec-label { font-size: 10px; font-weight: 500; letter-spacing: 4px; text-transform: uppercase; color: #333; margin-bottom: 28px; }

.sv-vs { font-family: 'Oswald', sans-serif; font-size: clamp(28px, 7vw, 48px); font-weight: 600; color: #fff; line-height: 1; margin-bottom: 12px; letter-spacing: -0.5px; }
.sv-detail { font-size: 13px; color: #444; letter-spacing: 0.5px; margin-bottom: 4px; }
.sv-detail b { color: #777; font-weight: 400; }

.sv-cd { margin-top: 32px; }
.sv-cd-val { font-family: 'Oswald', sans-serif; font-size: clamp(38px, 9vw, 60px); font-weight: 300; color: #fff; letter-spacing: 4px; line-height: 1; margin-bottom: 8px; }
.sv-cd-lbl { font-size: 10px; letter-spacing: 3px; text-transform: uppercase; color: #333; }
.sv-live { display: inline-flex; align-items: center; gap: 8px; font-size: 11px; letter-spacing: 3px; text-transform: uppercase; color: #ef4444; font-weight: 500; margin-top: 32px; }
.sv-live::before { content: ''; width: 7px; height: 7px; background: #ef4444; border-radius: 50%; animation: blink 1.2s ease-in-out infinite; display: inline-block; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.15} }

.sv-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1px; background: #161616; border: 1px solid #161616; }
.sv-cell { background: #080808; padding: 30px 22px; }
.sv-cell.hi { background: #0c0c0c; }
.sv-num { font-family: 'Oswald', sans-serif; font-size: 42px; font-weight: 400; color: #fff; line-height: 1; letter-spacing: -1px; margin-bottom: 8px; }
.sv-lbl { font-size: 9px; letter-spacing: 2.5px; text-transform: uppercase; color: #2a2a2a; font-weight: 500; }

.sv-irow { display: grid; grid-template-columns: 52px 1fr 90px 56px 56px; align-items: center; padding: 18px 0; border-bottom: 1px solid #0f0f0f; gap: 8px; }
.sv-irow:last-child { border-bottom: none; }
.sv-im { font-size: 10px; letter-spacing: 2px; text-transform: uppercase; color: #2a2a2a; font-weight: 500; }
.sv-ir { font-family: 'Oswald', sans-serif; font-size: 34px; font-weight: 400; color: #fff; line-height: 1; }
.sv-ib { font-size: 12px; color: #2a2a2a; line-height: 1.6; }
.sv-it { font-size: 11px; color: #333; letter-spacing: 1px; text-align: right; }

.sv-rec { display: grid; grid-template-columns: 20px 1fr; gap: 16px; padding: 22px 0; border-bottom: 1px solid #0f0f0f; align-items: start; }
.sv-rec:last-child { border-bottom: none; }
.sv-rn { font-family: 'Oswald', sans-serif; font-size: 12px; font-weight: 300; color: #222; padding-top: 3px; letter-spacing: 1px; }
.sv-rt { font-size: 14px; color: #444; line-height: 1.6; font-weight: 300; }
.sv-rt strong { color: #bbb; font-weight: 500; display: block; margin-bottom: 3px; font-size: 15px; }

.sv-pill { display: inline-block; margin-top: 14px; padding: 4px 14px; border-radius: 2px; font-size: 10px; letter-spacing: 2px; text-transform: uppercase; font-weight: 500; }
.sv-pill.won { background: #0a1a0a; color: #4ade80; border: 1px solid #152815; }
.sv-pill.live { background: #1a0a0a; color: #ef4444; border: 1px solid #2a1010; }
.sv-pill.up { background: #111; color: #444; border: 1px solid #1c1c1c; }

.sv-sgrid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 1px; background: #161616; border: 1px solid #161616; margin-top: 22px; }
.sv-sc { background: #0c0c0c; padding: 18px 10px; text-align: center; }
.sv-sn { font-family: 'Oswald', sans-serif; font-size: 26px; font-weight: 400; color: #fff; line-height: 1; margin-bottom: 6px; }
.sv-sl { font-size: 9px; letter-spacing: 2px; text-transform: uppercase; color: #252525; font-weight: 500; }
.sv-nodata { margin-top: 22px; padding: 18px 0; font-size: 11px; color: #222; letter-spacing: 2px; text-transform: uppercase; }

.sv-footer { padding: 40px 0 20px; font-size: 10px; color: #1c1c1c; letter-spacing: 2px; text-transform: uppercase; border-top: 1px solid #0f0f0f; margin-top: 0; text-align: center; }

div[data-testid="stSlider"] { padding: 8px 0 4px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="sv">', unsafe_allow_html=True)

# HERO
st.markdown(
    '<div class="sv-hero">'
    '<div class="sv-tag">Rajasthan Royals &nbsp;&middot;&nbsp; IPL 2026</div>'
    '<div class="sv-name">VAIBHAV<br><span>SOORY</span>AVANSHI</div>'
    '<div class="sv-meta">'
    '<span><b>Age</b> 15</span>'
    '<span><b>Role</b> Opener</span>'
    '<span><b>Bats</b> Left-hand</span>'
    '<span><b>From</b> Bihar</span>'
    '</div>'
    '</div>',
    unsafe_allow_html=True
)

# NEXT MATCH
if next_match:
    _, cd_str = get_countdown(match_dt)
    date_display = match_dt.strftime("%A, %d %B %Y")
    is_live = match_dt <= now_ist <= match_dt + timedelta(hours=4)
    cd_html = '<div class="sv-live">Live now</div>' if is_live else (
        '<div class="sv-cd"><div class="sv-cd-val">' + cd_str + '</div>'
        '<div class="sv-cd-lbl">Until match starts</div></div>'
    )
    st.markdown(
        '<div class="sv-sec">'
        '<div class="sv-sec-label">Next Match</div>'
        '<div class="sv-vs">RR &nbsp;vs&nbsp; ' + next_match['opponent'] + '</div>'
        '<div class="sv-detail"><b>' + date_display + '</b></div>'
        '<div class="sv-detail">' + next_match['time'] + ' IST &nbsp;&middot;&nbsp; ' + next_match['venue'] + '</div>'
        + cd_html + '</div>',
        unsafe_allow_html=True
    )
else:
    st.markdown(
        '<div class="sv-sec"><div class="sv-sec-label">Season</div>'
        '<div class="sv-vs">League stage complete.</div>'
        '<div class="sv-detail">Watch for playoff fixtures.</div></div>',
        unsafe_allow_html=True
    )

# SEASON STATS
st.markdown('<div class="sv-sec"><div class="sv-sec-label">IPL 2026 &nbsp;&middot;&nbsp; Season Stats</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sv-grid">'
    '<div class="sv-cell hi"><div class="sv-num">' + str(stats['runs']) + '</div><div class="sv-lbl">Runs</div></div>'
    '<div class="sv-cell"><div class="sv-num">' + str(stats['matches']) + '</div><div class="sv-lbl">Matches</div></div>'
    '<div class="sv-cell"><div class="sv-num">' + str(stats['highest']) + '</div><div class="sv-lbl">Best Score</div></div>'
    '<div class="sv-cell"><div class="sv-num">' + str(stats['strike_rate']) + '</div><div class="sv-lbl">Strike Rate</div></div>'
    '<div class="sv-cell hi"><div class="sv-num">' + str(stats['sixes']) + '</div><div class="sv-lbl">Sixes</div></div>'
    '<div class="sv-cell"><div class="sv-num">' + str(stats['fours']) + '</div><div class="sv-lbl">Fours</div></div>'
    '<div class="sv-cell"><div class="sv-num">' + str(stats['average']) + '</div><div class="sv-lbl">Average</div></div>'
    '<div class="sv-cell"><div class="sv-num">' + str(stats['fifties']) + '</div><div class="sv-lbl">Fifties</div></div>'
    '<div class="sv-cell"><div class="sv-num">' + str(stats['hundreds']) + '</div><div class="sv-lbl">Hundreds</div></div>'
    '</div>',
    unsafe_allow_html=True
)
st.markdown('</div>', unsafe_allow_html=True)

# INNINGS LOG
completed = [i for i in stats['innings'] if i['balls'] > 0]
if completed:
    st.markdown('<div class="sv-sec"><div class="sv-sec-label">Innings Log</div>', unsafe_allow_html=True)
    for inn in completed:
        sr = round((inn['runs'] / inn['balls']) * 100, 1)
        st.markdown(
            '<div class="sv-irow">'
            '<div class="sv-im">' + inn['match'].replace('vs ', '') + '</div>'
            '<div class="sv-ir">' + str(inn['runs']) + '</div>'
            '<div class="sv-ib">' + str(inn['balls']) + ' balls<br><span style="color:#1e1e1e">SR ' + str(sr) + '</span></div>'
            '<div class="sv-it">4s &nbsp;' + str(inn['fours']) + '</div>'
            '<div class="sv-it">6s &nbsp;' + str(inn['sixes']) + '</div>'
            '</div>',
            unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)

# RECORDS
records = [
    ("Youngest centurion in men's T20 cricket", "101 off 38 balls vs GT, IPL 2025. He was 14."),
    ("2nd fastest century in IPL history", "Off 35 deliveries. Only Chris Gayle has done it faster."),
    ("Youngest IPL debutant ever", "14 years and 23 days when he walked out for RR in 2025."),
    ("U19 World Cup 2026 Player of the Tournament", "175 off 80 balls in the final against England U19."),
    ("Orange Cap holder, IPL 2026", "267+ strike rate through the first four matches of the season."),
]
st.markdown('<div class="sv-sec"><div class="sv-sec-label">Records</div>', unsafe_allow_html=True)
for i, (title, detail) in enumerate(records):
    st.markdown(
        '<div class="sv-rec">'
        '<div class="sv-rn">' + str(i+1).zfill(2) + '</div>'
        '<div class="sv-rt"><strong>' + title + '</strong>' + detail + '</div>'
        '</div>',
        unsafe_allow_html=True
    )
st.markdown('</div>', unsafe_allow_html=True)

# ALL MATCHES SLIDER
st.markdown('<div class="sv-sec"><div class="sv-sec-label">All Matches &mdash; Slide to Browse</div>', unsafe_allow_html=True)

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
sel_date = sel_dt.strftime("%d %B %Y")
inn_data = innings_by_match.get(sel['short'], None)

if sel_is_today:
    pill = '<span class="sv-pill live">Live Today</span>'
elif sel_is_past:
    pill = '<span class="sv-pill won">' + (sel.get('result') or 'Played') + '</span>'
else:
    pill = '<span class="sv-pill up">Upcoming</span>'

st.markdown(
    '<div style="padding-top:8px;">'
    '<div style="font-family:Oswald,sans-serif;font-size:30px;font-weight:500;color:#fff;letter-spacing:-0.5px;">RR vs ' + sel['opponent'] + '</div>'
    '<div style="font-size:12px;color:#333;letter-spacing:1px;margin-top:6px;">' + sel_date + ' &nbsp;&middot;&nbsp; ' + sel['time'] + ' IST</div>'
    '<div style="font-size:12px;color:#222;letter-spacing:0.5px;margin-top:3px;">' + sel['venue'] + '</div>'
    + pill,
    unsafe_allow_html=True
)

if inn_data:
    sr = round((inn_data['runs'] / inn_data['balls']) * 100, 1)
    st.markdown(
        '<div class="sv-sgrid">'
        '<div class="sv-sc"><div class="sv-sn">' + str(inn_data['runs']) + '</div><div class="sv-sl">Runs</div></div>'
        '<div class="sv-sc"><div class="sv-sn">' + str(inn_data['balls']) + '</div><div class="sv-sl">Balls</div></div>'
        '<div class="sv-sc"><div class="sv-sn">' + str(sr) + '</div><div class="sv-sl">SR</div></div>'
        '<div class="sv-sc"><div class="sv-sn">' + str(inn_data['sixes']) + '</div><div class="sv-sl">Sixes</div></div>'
        '<div class="sv-sc"><div class="sv-sn">' + str(inn_data['fours']) + '</div><div class="sv-sl">Fours</div></div>'
        '</div></div>',
        unsafe_allow_html=True
    )
elif sel_is_today:
    st.markdown('<div class="sv-nodata">Match in progress</div></div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="sv-nodata">Stats available after the match</div></div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# FOOTER
st.markdown(
    '<div class="sv-footer">IPL 2026 &nbsp;&middot;&nbsp; Rajasthan Royals &nbsp;&middot;&nbsp; Updated ' + stats['last_updated'] + '</div>',
    unsafe_allow_html=True
)

st.markdown('</div>', unsafe_allow_html=True)

if next_match:
    match_date = datetime.strptime(next_match["date"], "%Y-%m-%d").date()
    if match_date == datetime.now(IST).date():
        time.sleep(1)
        st.rerun()
