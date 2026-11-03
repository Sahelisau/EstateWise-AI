from html import escape

import streamlit as st


def brand():
    st.markdown("""
    <div class="ew-brand">
      <div class="ew-mark">E</div>
      <div><div class="ew-brand-name">ESTATEWISE AI</div><div class="ew-brand-sub">Property intelligence</div></div>
    </div>
    """, unsafe_allow_html=True)


def hero(title, copy, kicker="ESTATEWISE AI"):
    st.markdown(
        f'<section class="ew-hero"><div class="ew-kicker">{escape(kicker)}</div>'
        f'<h1 class="ew-title">{escape(title)}</h1><p class="ew-copy">{escape(copy)}</p></section>',
        unsafe_allow_html=True,
    )


def section(title, copy=""):
    st.markdown(
        f'<div class="ew-section"><div class="ew-section-title">{escape(title)}</div>'
        f'<div class="ew-section-copy">{escape(copy)}</div></div>',
        unsafe_allow_html=True,
    )


def metric_card(label, value, note=""):
    st.markdown(
        f'<div class="ew-card"><div class="ew-metric-label">{escape(str(label))}</div>'
        f'<div class="ew-metric-value">{escape(str(value))}</div>'
        f'<div class="ew-metric-note">{escape(str(note))}</div></div>',
        unsafe_allow_html=True,
    )


def inr(value, compact=True):
    value = float(value)
    if compact and abs(value) >= 10_000_000:
        return f"₹{value / 10_000_000:,.2f} Cr"
    if compact and abs(value) >= 100_000:
        return f"₹{value / 100_000:,.2f} L"
    return f"₹{value:,.0f}"


def empty_state(title, copy, tone="info"):
    getattr(st, tone)(f"**{title}**  \n{copy}")


def footer():
    st.markdown('<div class="ew-footer">EstateWise AI &nbsp;·&nbsp; Intelligent Real Estate Analytics<br>Built with Python, Machine Learning and Data Science.</div>', unsafe_allow_html=True)


def navigate_button(label, page, key):
    if st.button(label, key=key, use_container_width=True):
        st.session_state["_next_page"] = page
        st.rerun()
