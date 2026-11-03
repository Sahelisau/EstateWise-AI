import streamlit as st


def apply_theme():
    st.markdown("""
    <style>
    :root {
      --ew-bg: #0b1220;
      --ew-panel: #111c2e;
      --ew-card: #152238;
      --ew-accent: #36c9a5;
      --ew-blue: #78a9ff;
      --ew-text: #f4f7fc;
      --ew-muted: #9aaac0;
      --ew-border: rgba(151, 174, 204, .16);
    }
    body { font-family: Inter, "Segoe UI", sans-serif; }
    h1, h2, h3 { color: var(--ew-text); letter-spacing: -.025em; }
    .ew-brand { display:flex; align-items:center; gap:11px; margin: .2rem 0 1.5rem; }
    .ew-mark { width:36px; height:36px; display:grid; place-items:center; border:1px solid rgba(54,201,165,.42); border-radius:10px; background:rgba(54,201,165,.08); color:var(--ew-accent); font-size:19px; font-weight:800; }
    .ew-brand-name { color:var(--ew-text); font-size:15px; font-weight:750; letter-spacing:.08em; }
    .ew-brand-sub { color:var(--ew-muted); font-size:10px; letter-spacing:.17em; margin-top:2px; text-transform:uppercase; }
    .ew-hero { position:relative; overflow:hidden; padding:30px 32px; border:1px solid var(--ew-border); border-radius:18px; background:linear-gradient(112deg, #152238 0%, #111c2e 72%); margin-bottom:22px; }
    .ew-hero:after { content:""; position:absolute; width:280px; height:280px; right:-105px; top:-135px; border:1px solid rgba(120,169,255,.2); border-radius:50%; box-shadow:0 0 0 28px rgba(120,169,255,.025), 0 0 0 58px rgba(120,169,255,.02); pointer-events:none; }
    .ew-kicker { color:var(--ew-accent); font-size:11px; font-weight:700; letter-spacing:.17em; text-transform:uppercase; margin-bottom:10px; }
    .ew-title { color:var(--ew-text); font-size:clamp(25px, 3vw, 38px); line-height:1.12; font-weight:720; letter-spacing:-.04em; margin:0 0 10px; }
    .ew-copy { color:var(--ew-muted); font-size:14px; line-height:1.65; max-width:770px; margin:0; }
    .ew-section { margin:24px 0 12px; }
    .ew-section-title { color:var(--ew-text); font-size:17px; font-weight:650; margin:0 0 4px; }
    .ew-section-copy { color:var(--ew-muted); font-size:12px; margin:0; }
    .ew-card { height:100%; background:var(--ew-card); border:1px solid var(--ew-border); border-radius:13px; padding:17px 18px; transition:border-color .18s ease, transform .18s ease; }
    .ew-card:hover { border-color:rgba(120,169,255,.38); transform:translateY(-2px); }
    .ew-metric-label { color:var(--ew-muted); font-size:11px; font-weight:600; letter-spacing:.08em; text-transform:uppercase; }
    .ew-metric-value { color:var(--ew-text); font-size:24px; line-height:1.25; font-weight:720; margin-top:8px; font-variant-numeric:tabular-nums; }
    .ew-metric-note { color:var(--ew-muted); font-size:11px; margin-top:6px; }
    .ew-result { background:linear-gradient(145deg, rgba(54,201,165,.10), rgba(21,34,56,.94) 58%); border:1px solid rgba(54,201,165,.32); border-radius:16px; padding:22px; }
    .ew-result-value { color:var(--ew-accent); font-size:34px; font-weight:760; letter-spacing:-.03em; font-variant-numeric:tabular-nums; margin:7px 0; }
    .ew-muted { color:var(--ew-muted); font-size:12px; line-height:1.6; }
    .ew-divider { height:1px; background:var(--ew-border); margin:18px 0; }
    .ew-pill { display:inline-block; color:var(--ew-accent); background:rgba(54,201,165,.09); border:1px solid rgba(54,201,165,.2); border-radius:999px; padding:4px 9px; font-size:10px; font-weight:650; letter-spacing:.05em; }
    .ew-footer { color:var(--ew-muted); font-size:11px; border-top:1px solid var(--ew-border); padding-top:15px; margin-top:35px; }
    @media (max-width: 700px) { .ew-hero { padding:23px 20px; } .ew-metric-value { font-size:21px; } }
    @media (prefers-reduced-motion: reduce) { *, *:before, *:after { scroll-behavior:auto !important; transition:none !important; animation:none !important; } }
    </style>
    """, unsafe_allow_html=True)
