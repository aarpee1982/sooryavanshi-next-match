import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, timezone, timedelta
from urllib.parse import quote
import base64
import time

st.set_page_config(
    page_title="Sooryavanshi's Next Match",
    page_icon="🏏",
    layout="centered",
    initial_sidebar_state="collapsed"
)

IST = timezone(timedelta(hours=5, minutes=30))
UTC = timezone.utc

RR_SCHEDULE = [
    {"date": "2026-03-30", "time": "19:30", "opponent": "Chennai Super Kings",         "venue": "ACA Stadium, Guwahati",                     "short": "CSK",  "result": "RR won", "color": "#FFD700"},
    {"date": "2026-04-04", "time": "19:30", "opponent": "Gujarat Titans",              "venue": "Narendra Modi Stadium, Ahmedabad",           "short": "GT",   "result": "RR won", "color": "#1DB954"},
    {"date": "2026-04-07", "time": "19:30", "opponent": "Mumbai Indians",              "venue": "ACA Stadium, Guwahati",                      "short": "MI",   "result": "RR won", "color": "#004BA0"},
    {"date": "2026-04-10", "time": "19:30", "opponent": "Royal Challengers Bengaluru", "venue": "ACA Stadium, Guwahati",                      "short": "RCB",  "result": "RR won", "color": "#C8102E"},
    {"date": "2026-04-13", "time": "19:30", "opponent": "Sunrisers Hyderabad",         "venue": "Rajiv Gandhi Intl. Stadium, Hyderabad",      "short": "SRH",  "result": None,     "color": "#FF6B00"},
    {"date": "2026-04-19", "time": "15:30", "opponent": "Kolkata Knight Riders",       "venue": "Eden Gardens, Kolkata",                      "short": "KKR",  "result": None,     "color": "#3A225D"},
    {"date": "2026-04-22", "time": "19:30", "opponent": "Lucknow Super Giants",        "venue": "Ekana Cricket Stadium, Lucknow",             "short": "LSG",  "result": None,     "color": "#A0C4FF"},
    {"date": "2026-04-25", "time": "19:30", "opponent": "Sunrisers Hyderabad",         "venue": "Sawai Mansingh Stadium, Jaipur",             "short": "SRH",  "result": None,     "color": "#FF6B00"},
    {"date": "2026-04-28", "time": "19:30", "opponent": "Punjab Kings",                "venue": "New Intl. Cricket Stadium, New Chandigarh",  "short": "PBKS", "result": None,     "color": "#ED1B24"},
    {"date": "2026-05-01", "time": "19:30", "opponent": "Delhi Capitals",              "venue": "Sawai Mansingh Stadium, Jaipur",             "short": "DC",   "result": None,     "color": "#0078BC"},
    {"date": "2026-05-09", "time": "19:30", "opponent": "Gujarat Titans",              "venue": "Sawai Mansingh Stadium, Jaipur",             "short": "GT",   "result": None,     "color": "#1DB954"},
    {"date": "2026-05-17", "time": "19:30", "opponent": "Delhi Capitals",              "venue": "Arun Jaitley Stadium, Delhi",                "short": "DC",   "result": None,     "color": "#0078BC"},
    {"date": "2026-05-19", "time": "19:30", "opponent": "Lucknow Super Giants",        "venue": "Sawai Mansingh Stadium, Jaipur",             "short": "LSG",  "result": None,     "color": "#A0C4FF"},
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
        {"match": "vs CSK", "runs": 52,  "balls": 17, "fours": 4, "sixes": 5},
        {"match": "vs GT",  "runs": 31,  "balls": 18, "fours": 5, "sixes": 1},
        {"match": "vs MI",  "runs": 39,  "balls": 14, "fours": 2, "sixes": 5},
        {"match": "vs RCB", "runs": 78,  "balls": 26, "fours": 5, "sixes": 8},
    ],
    "last_updated": "Apr 13, 2026"
}

stats = FALLBACK_STATS
now_ist = datetime.now(IST)
innings_by_match = {i['match'].replace('vs ', ''): i for i in stats['innings'] if i['balls'] > 0}

def get_next_match():
    for match in RR_SCHEDULE:
        mdt = datetime.strptime(f"{match['date']} {match['time']}", "%Y-%m-%d %H:%M").replace(tzinfo=IST)
        if mdt >= now_ist - timedelta(hours=4):
            return match, mdt
    return None, None

def get_countdown(match_dt):
    delta = match_dt - now_ist
    if delta.total_seconds() <= 0:
        return "Live Now"
    days = delta.days
    hours, rem = divmod(delta.seconds, 3600)
    minutes, _ = divmod(rem, 60)
    if days > 0:
        return f"{days}d {hours:02d}h {minutes:02d}m"
    return f"{hours:02d}h {minutes:02d}m"

def make_gcal_link(match):
    """Generate Google Calendar URL for a match."""
    dt = datetime.strptime(f"{match['date']} {match['time']}", "%Y-%m-%d %H:%M").replace(tzinfo=IST)
    dt_utc = dt.astimezone(UTC)
    end_utc = dt_utc + timedelta(hours=4)
    fmt = "%Y%m%dT%H%M%SZ"
    title = quote(f"RR vs {match['opponent']} — IPL 2026")
    details = quote(f"Vaibhav Sooryavanshi plays for Rajasthan Royals vs {match['opponent']}. IPL 2026.")
    location = quote(match['venue'])
    start = dt_utc.strftime(fmt)
    end = end_utc.strftime(fmt)
    return f"https://calendar.google.com/calendar/render?action=TEMPLATE&text={title}&dates={start}/{end}&details={details}&location={location}"

def make_ics_content(match):
    """Generate .ics file content for a match."""
    dt = datetime.strptime(f"{match['date']} {match['time']}", "%Y-%m-%d %H:%M").replace(tzinfo=IST)
    dt_utc = dt.astimezone(UTC)
    end_utc = dt_utc + timedelta(hours=4)
    fmt = "%Y%m%dT%H%M%SZ"
    uid = f"rr-vs-{match['short']}-{match['date']}@sooryavanshi"
    ics = "\r\n".join([
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Sooryavanshi Tracker//IPL 2026//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "BEGIN:VEVENT",
        f"UID:{uid}",
        f"DTSTART:{dt_utc.strftime(fmt)}",
        f"DTEND:{end_utc.strftime(fmt)}",
        f"SUMMARY:RR vs {match['opponent']} — IPL 2026",
        f"DESCRIPTION:Vaibhav Sooryavanshi plays for Rajasthan Royals vs {match['opponent']}. IPL 2026.",
        f"LOCATION:{match['venue']}",
        "STATUS:CONFIRMED",
        "END:VEVENT",
        "END:VCALENDAR",
    ])
    return ics

def ics_download_link(match):
    """Return an HTML anchor tag for .ics download."""
    ics = make_ics_content(match)
    b64 = base64.b64encode(ics.encode()).decode()
    fname = f"RR_vs_{match['short']}_{match['date']}.ics"
    return f'<a class="cal-btn ics" href="data:text/calendar;base64,{b64}" download="{fname}">⬇ Apple / Outlook</a>'

next_match, match_dt = get_next_match()

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=Barlow:wght@300;400;500;600;700&family=Barlow+Condensed:wght@500;600;700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

[data-testid="stHeader"],[data-testid="stToolbar"],
[data-testid="stDecoration"],footer,#MainMenu { display:none!important; }

[data-testid="stAppViewContainer"],
[data-testid="stMain"], section.main { background:#F7F4EF!important; }

.block-container { padding:0!important; max-width:780px!important; margin:0 auto!important; }

/* ROOT */
.mg { background:#F7F4EF; font-family:'Barlow',sans-serif; color:#1a1a1a; padding:0 0 80px; }

/* MASTHEAD */
.mg-top { background:#1a1a1a; padding:12px 32px; display:flex; align-items:center; justify-content:space-between; }
.mg-top-l { font-family:'Barlow Condensed',sans-serif; font-size:10px; font-weight:600; letter-spacing:4px; text-transform:uppercase; color:#F7F4EF; opacity:0.4; }
.mg-top-r { font-family:'Barlow Condensed',sans-serif; font-size:10px; font-weight:700; letter-spacing:3px; text-transform:uppercase; color:#E8411E; }

/* HERO */
.mg-hero { padding:52px 32px 44px; border-bottom:3px solid #1a1a1a; position:relative; }
.mg-hero::before { content:''; position:absolute; top:0; left:0; right:0; height:4px; background:#E8411E; }
.mg-kicker { font-family:'Barlow Condensed',sans-serif; font-size:11px; font-weight:700; letter-spacing:4px; text-transform:uppercase; color:#E8411E; margin-bottom:16px; }
.mg-name { font-family:'Playfair Display',serif; font-size:clamp(52px,11vw,86px); font-weight:900; line-height:0.92; color:#1a1a1a; margin-bottom:20px; letter-spacing:-2px; }
.mg-name em { font-style:italic; color:#E8411E; }
.mg-byline { display:flex; gap:20px; flex-wrap:wrap; align-items:center; }
.mg-byline-item { font-size:12px; font-weight:500; color:#888; letter-spacing:1px; text-transform:uppercase; }
.mg-byline-item strong { color:#1a1a1a; font-weight:700; }
.mg-dot { width:4px; height:4px; background:#E8411E; border-radius:50%; display:inline-block; }

/* NEXT MATCH BANNER */
.mg-banner { margin:32px 32px 0; background:#1a1a1a; padding:36px 36px 32px; position:relative; }
.mg-banner::after { content:''; position:absolute; bottom:0; left:0; width:72px; height:4px; background:#E8411E; }
.mg-banner-label { font-family:'Barlow Condensed',sans-serif; font-size:10px; font-weight:700; letter-spacing:4px; text-transform:uppercase; color:#E8411E; margin-bottom:16px; }
.mg-banner-vs { font-family:'Playfair Display',serif; font-size:clamp(26px,5.5vw,42px); font-weight:700; color:#fff; line-height:1.1; margin-bottom:14px; }
.mg-banner-meta { font-size:13px; font-weight:500; color:#666; margin-bottom:4px; }
.mg-banner-meta strong { color:#999; font-weight:600; }
.mg-cd { margin-top:24px; border-left:3px solid #E8411E; padding-left:16px; display:inline-flex; flex-direction:column; gap:4px; }
.mg-cd-val { font-family:'Playfair Display',serif; font-size:clamp(34px,7vw,52px); font-weight:700; color:#fff; line-height:1; letter-spacing:-1px; }
.mg-cd-lbl { font-family:'Barlow Condensed',sans-serif; font-size:10px; font-weight:600; letter-spacing:3px; text-transform:uppercase; color:#444; }
.mg-live { margin-top:20px; display:inline-flex; align-items:center; gap:10px; font-family:'Barlow Condensed',sans-serif; font-size:13px; font-weight:700; letter-spacing:3px; text-transform:uppercase; color:#E8411E; }
.mg-live::before { content:''; width:8px; height:8px; background:#E8411E; border-radius:50%; animation:pulse 1s ease-in-out infinite; display:inline-block; }
@keyframes pulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:0.2;transform:scale(0.75)} }

/* SECTION LABELS */
.mg-sec { font-family:'Barlow Condensed',sans-serif; font-size:10px; font-weight:700; letter-spacing:4px; text-transform:uppercase; color:#E8411E; padding:32px 32px 16px; }
.mg-rule { height:3px; background:#1a1a1a; margin:32px 32px 0; }
.mg-rule-thin { height:1px; background:#e0ddd8; margin:0 32px; }

/* STATS GRID */
.mg-stats { display:grid; grid-template-columns:repeat(3,1fr); margin:0 32px; border:1.5px solid #ddd; }
.mg-stat { padding:22px 18px; border-right:1.5px solid #ddd; border-bottom:1.5px solid #ddd; background:#fff; }
.mg-stat:nth-child(3n) { border-right:none; }
.mg-stat:nth-child(7),.mg-stat:nth-child(8),.mg-stat:nth-child(9) { border-bottom:none; }
.mg-stat-n { font-family:'Playfair Display',serif; font-size:clamp(28px,5vw,44px); font-weight:900; color:#1a1a1a; line-height:1; margin-bottom:6px; letter-spacing:-1px; }
.mg-stat-n.red { color:#E8411E; }
.mg-stat-l { font-family:'Barlow Condensed',sans-serif; font-size:9px; font-weight:700; letter-spacing:2px; text-transform:uppercase; color:#aaa; }

/* INNINGS */
.mg-inn-wrap { margin:0 32px; }
.mg-inn-row { display:grid; grid-template-columns:52px 1fr 80px 56px 56px; align-items:center; gap:12px; padding:16px 0; border-bottom:1px solid #e8e3db; }
.mg-inn-row:last-child { border-bottom:none; }
.mg-inn-opp { font-family:'Barlow Condensed',sans-serif; font-size:11px; font-weight:700; letter-spacing:2px; text-transform:uppercase; color:#bbb; }
.mg-inn-r { font-family:'Playfair Display',serif; font-size:clamp(26px,5vw,38px); font-weight:900; color:#1a1a1a; line-height:1; letter-spacing:-1px; }
.mg-inn-m { font-size:12px; font-weight:500; color:#aaa; line-height:1.6; }
.mg-inn-c { font-family:'Barlow Condensed',sans-serif; font-size:12px; font-weight:700; color:#555; letter-spacing:1px; text-align:right; }
.mg-inn-c span { color:#E8411E; }

/* RECORDS */
.mg-rec-wrap { margin:0 32px; }
.mg-rec { display:grid; grid-template-columns:28px 1fr; gap:16px; padding:20px 0; border-bottom:1px solid #e8e3db; align-items:start; }
.mg-rec:last-child { border-bottom:none; }
.mg-rec-n { font-family:'Barlow Condensed',sans-serif; font-size:20px; font-weight:700; color:#ddd; line-height:1; }
.mg-rec-title { font-family:'Barlow Condensed',sans-serif; font-size:15px; font-weight:700; letter-spacing:0.5px; color:#1a1a1a; text-transform:uppercase; margin-bottom:4px; }
.mg-rec-detail { font-size:13px; font-weight:400; color:#888; line-height:1.6; }

/* ── ALL MATCHES TABLE ── */
.mg-matches-wrap { margin:0 32px; }

.mg-match-card {
    background:#fff;
    border:1.5px solid #e0ddd8;
    margin-bottom:10px;
    transition:border-color 0.15s;
    position:relative;
    overflow:hidden;
}
.mg-match-card.next-up {
    border-color:#1a1a1a;
    border-width:2px;
}
.mg-match-card.played { opacity:0.75; }

.mg-match-card-top {
    display:grid;
    grid-template-columns:56px 1fr auto;
    align-items:center;
    gap:16px;
    padding:18px 20px;
}
.mg-match-num {
    font-family:'Barlow Condensed',sans-serif;
    font-size:13px;
    font-weight:700;
    letter-spacing:2px;
    color:#ccc;
    text-align:center;
    line-height:1;
}
.mg-match-num .mn { font-family:'Playfair Display',serif; font-size:28px; font-weight:900; color:#1a1a1a; display:block; letter-spacing:-1px; }
.mg-match-info {}
.mg-match-vs-text {
    font-family:'Barlow Condensed',sans-serif;
    font-size:clamp(16px,3.5vw,22px);
    font-weight:700;
    color:#1a1a1a;
    letter-spacing:0.5px;
    text-transform:uppercase;
    margin-bottom:4px;
}
.mg-match-vs-text .opp-color { font-weight:800; }
.mg-match-datetime {
    font-size:12px;
    font-weight:500;
    color:#999;
    margin-bottom:2px;
}
.mg-match-venue {
    font-size:11px;
    color:#bbb;
    font-weight:400;
}
.mg-match-right {
    text-align:right;
    min-width:80px;
}
.mg-badge-won { display:inline-block; padding:4px 10px; background:#e8f5e9; color:#2e7d32; border:1px solid #a5d6a7; font-family:'Barlow Condensed',sans-serif; font-size:9px; font-weight:700; letter-spacing:2px; text-transform:uppercase; }
.mg-badge-next { display:inline-block; padding:4px 10px; background:#1a1a1a; color:#fff; font-family:'Barlow Condensed',sans-serif; font-size:9px; font-weight:700; letter-spacing:2px; text-transform:uppercase; }
.mg-badge-up { display:inline-block; padding:4px 10px; background:#f5f5f5; color:#999; border:1px solid #ddd; font-family:'Barlow Condensed',sans-serif; font-size:9px; font-weight:700; letter-spacing:2px; text-transform:uppercase; }
.mg-badge-live { display:inline-block; padding:4px 10px; background:#fff0ee; color:#E8411E; border:1px solid #ffb4a0; font-family:'Barlow Condensed',sans-serif; font-size:9px; font-weight:700; letter-spacing:2px; text-transform:uppercase; }

/* Score strip for played matches */
.mg-match-score-strip {
    display:grid;
    grid-template-columns:repeat(5,1fr);
    border-top:1px solid #f0ede8;
    background:#faf9f7;
}
.mg-score-c { padding:10px 8px; text-align:center; border-right:1px solid #f0ede8; }
.mg-score-c:last-child { border-right:none; }
.mg-score-n { font-family:'Playfair Display',serif; font-size:20px; font-weight:900; color:#1a1a1a; line-height:1; }
.mg-score-l { font-family:'Barlow Condensed',sans-serif; font-size:8px; font-weight:700; letter-spacing:2px; text-transform:uppercase; color:#ccc; margin-top:3px; }

/* Calendar buttons */
.cal-strip {
    display:flex;
    gap:8px;
    padding:12px 20px 14px;
    border-top:1px solid #f0ede8;
    background:#f7f4ef;
    flex-wrap:wrap;
    align-items:center;
}
.cal-strip-label {
    font-family:'Barlow Condensed',sans-serif;
    font-size:10px;
    font-weight:700;
    letter-spacing:2px;
    text-transform:uppercase;
    color:#bbb;
    margin-right:4px;
    flex-shrink:0;
}
.cal-btn {
    display:inline-block;
    padding:7px 14px;
    font-family:'Barlow Condensed',sans-serif;
    font-size:11px;
    font-weight:700;
    letter-spacing:1.5px;
    text-transform:uppercase;
    text-decoration:none;
    border:1.5px solid #1a1a1a;
    color:#1a1a1a;
    background:#fff;
    cursor:pointer;
    transition:all 0.15s;
    white-space:nowrap;
}
.cal-btn:hover { background:#1a1a1a; color:#fff; }
.cal-btn.gcal { border-color:#E8411E; color:#E8411E; }
.cal-btn.gcal:hover { background:#E8411E; color:#fff; }
.cal-btn.ics { border-color:#555; color:#555; }
.cal-btn.ics:hover { background:#555; color:#fff; }

/* team color accent bar */
.mg-match-accent { position:absolute; left:0; top:0; bottom:0; width:4px; }

/* FOOTER */
.mg-footer { margin:40px 32px 0; padding:20px 0; border-top:3px solid #1a1a1a; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; }
.mg-footer-l { font-family:'Barlow Condensed',sans-serif; font-size:10px; font-weight:700; letter-spacing:3px; text-transform:uppercase; color:#bbb; }
.mg-footer-r { font-family:'Barlow Condensed',sans-serif; font-size:10px; font-weight:600; letter-spacing:2px; text-transform:uppercase; color:#E8411E; }

/* Slider */
[data-testid="stSlider"] { padding:4px 0!important; }
div[data-baseweb="slider"]>div:first-child { background:#1a1a1a!important; height:3px!important; }
div[data-baseweb="slider"]>div>div[role="slider"] { background:#E8411E!important; border:2px solid #1a1a1a!important; width:18px!important; height:18px!important; border-radius:50%!important; box-shadow:0 2px 8px rgba(232,65,30,0.35)!important; }
.stSlider p { color:#ccc!important; font-family:'Barlow Condensed',sans-serif!important; font-size:10px!important; letter-spacing:1px!important; }
</style>
""", unsafe_allow_html=True)

# ── RENDER ────────────────────────────────────────────────────────────────────
st.markdown('<div class="mg">', unsafe_allow_html=True)

# MASTHEAD
st.markdown(
    '<div class="mg-top">'
    '<div class="mg-top-l">Sooryavanshi\'s Next Match</div>'
    '<div class="mg-top-r">IPL 2026 Tracker</div>'
    '</div>',
    unsafe_allow_html=True
)

# HERO
st.markdown(
    '<div class="mg-hero">'
    '<div class="mg-kicker">Rajasthan Royals · IPL 2026</div>'
    '<div class="mg-name">Vaibhav<br><em>Soory</em>avanshi</div>'
    '<div class="mg-byline">'
    '<span class="mg-byline-item"><strong>15</strong> Years Old</span>'
    '<span class="mg-dot"></span>'
    '<span class="mg-byline-item"><strong>Opener</strong></span>'
    '<span class="mg-dot"></span>'
    '<span class="mg-byline-item"><strong>Left-hand</strong> bat</span>'
    '<span class="mg-dot"></span>'
    '<span class="mg-byline-item"><strong>Bihar</strong></span>'
    '</div>'
    '</div>',
    unsafe_allow_html=True
)

# NEXT MATCH BANNER
if next_match:
    cd_str = get_countdown(match_dt)
    date_display = match_dt.strftime("%A, %d %B %Y")
    is_live = match_dt <= now_ist <= match_dt + timedelta(hours=4)
    cd_html = '<div class="mg-live">Live Now</div>' if is_live else (
        '<div class="mg-cd"><div class="mg-cd-val">' + cd_str + '</div>'
        '<div class="mg-cd-lbl">Until match starts</div></div>'
    )
    st.markdown(
        '<div class="mg-banner">'
        '<div class="mg-banner-label">Next Match</div>'
        '<div class="mg-banner-vs">RR vs ' + next_match['opponent'] + '</div>'
        '<div class="mg-banner-meta"><strong>' + date_display + '</strong> &nbsp;·&nbsp; ' + next_match['time'] + ' IST</div>'
        '<div class="mg-banner-meta">' + next_match['venue'] + '</div>'
        + cd_html + '</div>',
        unsafe_allow_html=True
    )

# SEASON STATS
st.markdown('<div class="mg-rule"></div>', unsafe_allow_html=True)
st.markdown('<div class="mg-sec">IPL 2026 — Season Stats</div>', unsafe_allow_html=True)

stat_items = [
    (stats['runs'], "Runs", True),
    (stats['matches'], "Matches", False),
    (stats['highest'], "Best Score", False),
    (stats['strike_rate'], "Strike Rate", False),
    (stats['sixes'], "Sixes", True),
    (stats['fours'], "Fours", False),
    (stats['average'], "Average", False),
    (stats['fifties'], "Fifties", False),
    (stats['hundreds'], "Hundreds", False),
]
grid = '<div class="mg-stats">'
for val, lbl, accent in stat_items:
    cls = "mg-stat-n red" if accent else "mg-stat-n"
    grid += '<div class="mg-stat"><div class="' + cls + '">' + str(val) + '</div><div class="mg-stat-l">' + lbl + '</div></div>'
grid += '</div>'
st.markdown(grid, unsafe_allow_html=True)

# INNINGS LOG
completed = [i for i in stats['innings'] if i['balls'] > 0]
if completed:
    st.markdown('<div class="mg-rule"></div>', unsafe_allow_html=True)
    st.markdown('<div class="mg-sec">Innings Log</div>', unsafe_allow_html=True)
    st.markdown('<div class="mg-inn-wrap">', unsafe_allow_html=True)
    for inn in completed:
        sr = round((inn['runs'] / inn['balls']) * 100, 1)
        st.markdown(
            '<div class="mg-inn-row">'
            '<div class="mg-inn-opp">' + inn['match'].replace('vs ','') + '</div>'
            '<div class="mg-inn-r">' + str(inn['runs']) + '</div>'
            '<div class="mg-inn-m">' + str(inn['balls']) + ' balls<br>SR ' + str(sr) + '</div>'
            '<div class="mg-inn-c"><span>' + str(inn['fours']) + '</span> 4s</div>'
            '<div class="mg-inn-c"><span>' + str(inn['sixes']) + '</span> 6s</div>'
            '</div>',
            unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)

# RECORDS
records = [
    ("Youngest T20 centurion ever", "101 off 38 balls vs Gujarat Titans, IPL 2025. He was 14 years old."),
    ("2nd fastest century in IPL history", "Off 35 deliveries. Only Chris Gayle has done it faster."),
    ("Youngest IPL debutant ever", "14 years and 23 days when he walked out for Rajasthan Royals."),
    ("U19 World Cup 2026 Player of Tournament", "175 off 80 balls in the final against England U19."),
    ("Orange Cap holder, IPL 2026", "267+ strike rate through the opening four matches of the season."),
]
st.markdown('<div class="mg-rule"></div>', unsafe_allow_html=True)
st.markdown('<div class="mg-sec">Records</div>', unsafe_allow_html=True)
st.markdown('<div class="mg-rec-wrap">', unsafe_allow_html=True)
for i, (title, detail) in enumerate(records):
    st.markdown(
        '<div class="mg-rec">'
        '<div class="mg-rec-n">' + str(i+1).zfill(2) + '</div>'
        '<div><div class="mg-rec-title">' + title + '</div>'
        '<div class="mg-rec-detail">' + detail + '</div></div>'
        '</div>',
        unsafe_allow_html=True
    )
st.markdown('</div>', unsafe_allow_html=True)

# ── ALL MATCHES — THE USP ─────────────────────────────────────────────────────
st.markdown('<div class="mg-rule"></div>', unsafe_allow_html=True)
st.markdown('<div class="mg-sec">All 13 Matches — Add Any to Your Calendar</div>', unsafe_allow_html=True)
st.markdown('<div class="mg-matches-wrap">', unsafe_allow_html=True)

for idx, m in enumerate(RR_SCHEDULE):
    mdt = datetime.strptime(f"{m['date']} {m['time']}", "%Y-%m-%d %H:%M").replace(tzinfo=IST)
    is_past = mdt < now_ist - timedelta(hours=4)
    is_today = mdt.date() == now_ist.date()
    is_next = (not is_past) and (not is_today) and next_match and m['short'] == next_match['short'] and m['date'] == next_match['date']

    date_str = mdt.strftime("%a, %d %b")
    time_str = m['time'] + " IST"

    # Badge
    if is_today:
        badge = '<span class="mg-badge-live">● Live Today</span>'
        card_class = "mg-match-card next-up"
    elif is_past:
        badge = '<span class="mg-badge-won">✓ ' + (m.get('result') or 'Played') + '</span>'
        card_class = "mg-match-card played"
    elif is_next:
        badge = '<span class="mg-badge-next">▶ Next</span>'
        card_class = "mg-match-card next-up"
    else:
        badge = '<span class="mg-badge-up">Upcoming</span>'
        card_class = "mg-match-card"

    # Innings data
    inn = innings_by_match.get(m['short'], None)

    # Score strip for played matches
    score_strip = ""
    if inn:
        sr = round((inn['runs'] / inn['balls']) * 100, 1)
        score_strip = (
            '<div class="mg-match-score-strip">'
            '<div class="mg-score-c"><div class="mg-score-n">' + str(inn['runs']) + '</div><div class="mg-score-l">Runs</div></div>'
            '<div class="mg-score-c"><div class="mg-score-n">' + str(inn['balls']) + '</div><div class="mg-score-l">Balls</div></div>'
            '<div class="mg-score-c"><div class="mg-score-n">' + str(sr) + '</div><div class="mg-score-l">SR</div></div>'
            '<div class="mg-score-c"><div class="mg-score-n">' + str(inn['sixes']) + '</div><div class="mg-score-l">Sixes</div></div>'
            '<div class="mg-score-c"><div class="mg-score-n">' + str(inn['fours']) + '</div><div class="mg-score-l">Fours</div></div>'
            '</div>'
        )

    # Calendar buttons (only for upcoming/today)
    cal_strip = ""
    if not is_past:
        gcal_url = make_gcal_link(m)
        ics_link = ics_download_link(m)
        cal_strip = (
            '<div class="cal-strip">'
            '<span class="cal-strip-label">Add to calendar</span>'
            '<a class="cal-btn gcal" href="' + gcal_url + '" target="_blank">📅 Google Calendar</a>'
            + ics_link +
            '</div>'
        )

    accent_color = m.get('color', '#E8411E')

    card_html = (
        '<div class="' + card_class + '">'
        '<div class="mg-match-accent" style="background:' + accent_color + ';"></div>'
        '<div class="mg-match-card-top">'
        '<div class="mg-match-num"><span style="font-family:Barlow Condensed,sans-serif;font-size:11px;letter-spacing:2px;color:#ccc;">M</span><span class="mn">' + str(idx+1) + '</span></div>'
        '<div class="mg-match-info">'
        '<div class="mg-match-vs-text">RR vs <span class="opp-color" style="color:' + accent_color + ';">' + m['opponent'] + '</span></div>'
        '<div class="mg-match-datetime">' + date_str + ' &nbsp;·&nbsp; ' + time_str + '</div>'
        '<div class="mg-match-venue">' + m['venue'] + '</div>'
        '</div>'
        '<div class="mg-match-right">' + badge + '</div>'
        '</div>'
        + score_strip
        + cal_strip
        + '</div>'
    )
    st.markdown(card_html, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# FOOTER
st.markdown(
    '<div class="mg-footer">'
    '<div class="mg-footer-l">IPL 2026 · Rajasthan Royals · Updated ' + stats['last_updated'] + '</div>'
    '<div class="mg-footer-r">Watching every match he plays</div>'
    '</div>',
    unsafe_allow_html=True
)

st.markdown('</div>', unsafe_allow_html=True)

if next_match:
    match_date = datetime.strptime(next_match["date"], "%Y-%m-%d").date()
    if match_date == datetime.now(IST).date():
        time.sleep(1)
        st.rerun()
