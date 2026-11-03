import streamlit as st


def apply_theme():
    st.markdown("""
    <style>
    :root { color-scheme: light; --ew-bg:#F7F8FA; --ew-white:#fff; --ew-ink:#17202E; --ew-muted:#647184; --ew-green:#087F5B; --ew-green-soft:#E8F5EF; --ew-blue:#547BA8; --ew-border:#E5E9ED; --ew-shadow:0 8px 24px rgba(23,32,46,.045); }
    html, body, [class*="css"] { font-family: Inter, "Plus Jakarta Sans", "Segoe UI", sans-serif; }
    .stApp { background:var(--ew-bg); color:var(--ew-ink); }
    [data-testid="stHeader"] { background:rgba(247,248,250,.9); }
    [data-testid="stSidebar"] { background:#fff; border-right:1px solid var(--ew-border); }
    [data-testid="stSidebar"] > div:first-child { padding:1.2rem .9rem; }
    [data-testid="stMainBlockContainer"] { max-width:1440px; padding:1.45rem 2.4rem 3rem; }
    h1,h2,h3,h4,p,label,span,div { color:inherit; }
    h1,h2,h3 { letter-spacing:-.035em; }
    h1 { font-weight:730; }
    [data-testid="stCaptionContainer"] p, .stCaption { color:var(--ew-muted); }
    [data-testid="stVerticalBlockBorderWrapper"] { background:var(--ew-white); border:1px solid var(--ew-border); border-radius:16px; box-shadow:var(--ew-shadow); }
    div[data-testid="stMetric"] { background:#fff; padding:1rem 1.1rem; border:1px solid var(--ew-border); border-radius:14px; box-shadow:var(--ew-shadow); }
    div[data-testid="stMetricLabel"] { color:var(--ew-muted); font-size:.77rem; }
    div[data-testid="stMetricValue"] { color:var(--ew-ink); font-weight:720; letter-spacing:-.035em; }
    .stButton > button, .stFormSubmitButton > button { min-height:2.75rem; border-radius:10px; font-weight:650; border:1px solid var(--ew-border); transition:transform .15s ease, box-shadow .15s ease; }
    .stButton > button:hover, .stFormSubmitButton > button:hover { transform:translateY(-1px); box-shadow:0 5px 14px rgba(8,127,91,.12); border-color:#A6D4C3; }
    button[kind="primary"], .stFormSubmitButton button[kind="primary"] { background:var(--ew-green); border-color:var(--ew-green); color:white; }
    button[kind="primary"] p { color:#fff; }
    [data-baseweb="select"] > div, [data-baseweb="input"] > div, [data-baseweb="textarea"] > div { border-radius:9px; border-color:#DCE2E7; background:#fff; }
    [data-testid="stDataFrame"] { border:1px solid var(--ew-border); border-radius:12px; overflow:hidden; }
    [data-testid="stAlert"] { border-radius:12px; }
    .ew-brand { display:flex; align-items:center; gap:11px; padding:.25rem .4rem 1.25rem; }
    .ew-mark { width:36px; height:36px; display:grid; place-items:center; border-radius:11px; background:var(--ew-green); color:white; font-size:18px; font-weight:800; box-shadow:0 5px 12px rgba(8,127,91,.18); }
    .ew-brand-name { color:var(--ew-ink); font-size:14px; font-weight:780; letter-spacing:.025em; }
    .ew-brand-sub { color:var(--ew-muted); font-size:10px; letter-spacing:.08em; margin-top:2px; text-transform:uppercase; }
    .ew-topbar { min-height:48px; display:flex; align-items:center; justify-content:space-between; gap:14px; padding:0 0 14px; margin-bottom:22px; border-bottom:1px solid var(--ew-border); }
    .ew-breadcrumb { font-size:12px; color:var(--ew-muted); }
    .ew-status { display:inline-flex; align-items:center; gap:7px; padding:6px 10px; background:#fff; border:1px solid var(--ew-border); border-radius:999px; color:var(--ew-muted); font-size:11px; white-space:nowrap; }
    .ew-status-dot { width:7px; height:7px; border-radius:50%; background:#15A36F; }
    .ew-status-dot.off { background:#D19A39; }
    .ew-page-header { margin:0 0 24px; }
    .ew-kicker { color:var(--ew-green); font-size:10px; font-weight:750; letter-spacing:.14em; text-transform:uppercase; margin:0 0 8px; }
    .ew-title { color:var(--ew-ink); font-size:clamp(25px,3vw,34px); line-height:1.13; font-weight:740; letter-spacing:-.045em; margin:0 0 8px; }
    .ew-copy { color:var(--ew-muted); font-size:13px; line-height:1.65; max-width:780px; margin:0; }
    .ew-overview-hero { position:relative; overflow:hidden; display:flex; align-items:center; justify-content:space-between; gap:22px; min-height:208px; padding:30px 34px; margin-bottom:22px; background:linear-gradient(115deg,#fff 0%,#F1F8F4 68%,#E7F4EE 100%); border:1px solid #DDECE4; border-radius:20px; box-shadow:var(--ew-shadow); }
    .ew-overview-hero:after { content:""; position:absolute; width:240px; height:240px; right:-72px; top:-96px; border:1px solid rgba(8,127,91,.12); border-radius:50%; box-shadow:0 0 0 24px rgba(8,127,91,.025),0 0 0 50px rgba(8,127,91,.02); pointer-events:none; }
    .ew-overview-hero .ew-title { font-size:clamp(30px,3.4vw,44px); max-width:650px; }
    .ew-overview-hero .ew-copy { font-size:14px; max-width:620px; }
    .ew-section { margin:25px 0 12px; }
    .ew-section-title { color:var(--ew-ink); font-size:16px; font-weight:680; margin:0 0 4px; }
    .ew-section-copy { color:var(--ew-muted); font-size:12px; line-height:1.5; margin:0; }
    .ew-card { height:100%; background:var(--ew-white); border:1px solid var(--ew-border); border-radius:14px; padding:16px 17px; box-shadow:var(--ew-shadow); transition:border-color .16s ease,transform .16s ease; }
    .ew-card:hover { border-color:#B9DCCB; transform:translateY(-1px); }
    .ew-metric-label { color:var(--ew-muted); font-size:10px; font-weight:650; letter-spacing:.07em; text-transform:uppercase; }
    .ew-metric-value { color:var(--ew-ink); font-size:23px; line-height:1.25; font-weight:740; letter-spacing:-.035em; margin-top:8px; font-variant-numeric:tabular-nums; }
    .ew-metric-note { color:var(--ew-muted); font-size:10px; line-height:1.45; margin-top:5px; }
    .ew-result { background:linear-gradient(145deg,#EAF6F0,#fff 75%); border:1px solid #BDDFCF; border-radius:16px; padding:22px; }
    .ew-result-value { color:var(--ew-green); font-size:clamp(29px,3vw,38px); font-weight:780; letter-spacing:-.04em; margin:7px 0; font-variant-numeric:tabular-nums; }
    .ew-muted { color:var(--ew-muted); font-size:12px; line-height:1.65; }
    .ew-divider { height:1px; background:var(--ew-border); margin:16px 0; }
    .ew-pill { display:inline-block; color:var(--ew-green); background:var(--ew-green-soft); border:1px solid #D0EBDD; border-radius:999px; padding:5px 10px; font-size:10px; font-weight:670; letter-spacing:.025em; }
    .ew-insight { padding:13px 15px; border-left:3px solid var(--ew-green); background:#fff; border-radius:0 10px 10px 0; color:var(--ew-muted); font-size:12px; line-height:1.6; }
    .ew-footer { color:var(--ew-muted); font-size:10px; border-top:1px solid var(--ew-border); padding-top:14px; margin-top:34px; }
    div[role="radiogroup"] { gap:3px; }
    div[role="radiogroup"] label { padding:9px 11px; border-radius:9px; color:#526071; font-size:13px; }
    div[role="radiogroup"] label:hover { background:#F2F6F4; }
    div[role="radiogroup"] label:has(input:checked) { background:#EAF6F0; color:var(--ew-green); font-weight:680; }
    div[role="radiogroup"] label:has(input:checked) p { color:var(--ew-green); }
    @media(max-width:900px) { [data-testid="stMainBlockContainer"] { padding:1.1rem 1.2rem 2rem; } .ew-overview-hero { padding:25px; } }
    @media(max-width:640px) { .ew-overview-hero { align-items:flex-start; flex-direction:column; padding:22px 20px; } .ew-topbar { margin-bottom:18px; } }
    @media(prefers-reduced-motion:reduce) { *,*:before,*:after { scroll-behavior:auto !important; transition:none !important; animation:none !important; } }
    </style>
    """, unsafe_allow_html=True)
