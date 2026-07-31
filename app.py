import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import pandas as pd
import numpy as np
import yfinance as yf
import google.generativeai as genai

st.set_page_config(
    page_title="AI Pro Trading Analysis Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main { background-color: #0f172a; color: #f8fafc; }
    .stAppHeader { background-color: #0f172a; }
    h1, h2, h3, h4 { color: #38bdf8; }
    .stButton>button {
        background-color: #10b981;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px 24px;
        font-size: 16px;
    }
</style>
""", unsafe_allow_html=True)

st.title("⚡ AI Pro Chart & Signal Analysis System")
st.caption("Live Real-time TradingView Charts + Custom AI Signal Analysis Popup Layout")

st.sidebar.header("⚙️ Control Panel")
api_key = st.sidebar.text_input("Gemini API Key (Optional for Vision AI)", type="password")

analysis_mode = st.sidebar.radio(
    "Select Mode",
    ["📺 Live TradingView Real-Time Chart", "📸 Upload Chart Screenshot"]
)

if api_key:
    genai.configure(api_key=api_key)

def render_analysis_popup(
    pair="BTC/USDT",
    timeframe="1H",
    conf_score="88%",
    signal_type="BUY / LONG",
    entry_zone="$63,800 - $64,100",
    tp1="$65,200",
    tp2="$66,400",
    sl="$63,150",
    rr="1 : 2.85 R:R",
    demand_zone="$63,000 - $63,400",
    supply_zone="$65,500 - $66,200",
    pattern_notes="Bullish Liquidity Sweep at $63,800 with 1H Market Structure Shift (MSS). Strong buyer volume surge.",
    news_notes="• Federal Reserve Interest Rate Decision upcoming; dovish market sentiment.<br>• On-chain exchange outflows indicate whale accumulation.",
    psychology_notes="• <b>Rule #1:</b> Do NOT risk more than 1.5% of total capital.<br>• <b>Rule #2:</b> Do NOT chase price if it passes $64,400.<br>• <b>Rule #3:</b> Move SL to Breakeven after TP1.",
    metrics_notes="• <b>RSI (14):</b> 52.4 (Bullish Divergence)<br>• <b>EMA 20/50:</b> Golden Cross on 15M<br>• <b>Funding Rate:</b> Neutral (0.01%)"
):
    st.markdown("## 📊 ⚡ AI ANALYSIS SIGNAL POPUP MODAL")
    st.markdown(f"**Symbol:** `{pair}` | **Timeframe:** `{timeframe}`")

    # TOP ROW MATCHING HAND-DRAWN WIREFRAME
    col_tl, col_center, col_tr = st.columns([1.3, 2.4, 1.1])

    with col_tl:
        # Top Left Box 1: Confirmation Score
        st.markdown(f"""
        <div style="background-color:#1e293b; padding:15px; border-radius:10px; border-left:5px solid #10b981; margin-bottom:12px;">
            <h4 style="margin:0; color:#10b981;">✅ Confirmation Score</h4>
            <h2 style="margin:5px 0; color:#ffffff; font-size:32px;">{conf_score}</h2>
            <span style="color:#94a3b8; font-size:12px;">High Probability Signal</span>
        </div>
        """, unsafe_allow_html=True)

        # Bottom Left Box 2: Entry / Exit Parameters
        st.markdown(f"""
        <div style="background-color:#1e293b; padding:15px; border-radius:10px; border:1px solid #334155;">
            <h4 style="margin:0 0 10px 0; color:#38bdf8;">🎯 Entry & Exit Points</h4>
            <p style="margin:4px 0; font-size:13px;"><b>Entry Zone:</b> <span style="color:#f8fafc;">{entry_zone}</span></p>
            <p style="margin:4px 0; font-size:13px; color:#10b981;"><b>Take Profit 1:</b> {tp1}</p>
            <p style="margin:4px 0; font-size:13px; color:#10b981;"><b>Take Profit 2:</b> {tp2}</p>
            <p style="margin:4px 0; font-size:13px; color:#ef4444;"><b>Stop Loss:</b> {sl}</p>
            <p style="margin:4px 0; font-size:13px; color:#f59e0b;"><b>Risk/Reward:</b> {rr}</p>
        </div>
        """, unsafe_allow_html=True)

    with col_center:
        # Center Large Box: Supply / Demand Zone & Technical Analysis
        st.markdown(f"""
        <div style="background-color:#1e293b; padding:18px; border-radius:10px; border:1px solid #334155; min-height:280px;">
            <h3 style="margin:0 0 12px 0; color:#f59e0b;">📊 Zone & Market Structure Analysis</h3>
            <p style="font-size:14px; margin:6px 0;">🟢 <b>Demand Zone (Support):</b> {demand_zone}</p>
            <p style="font-size:14px; margin:6px 0;">🔴 <b>Supply Zone (Resistance):</b> {supply_zone}</p>
            <p style="font-size:14px; margin:6px 0;">🔎 <b>Market Breakdown & Price Action:</b></p>
            <p style="font-size:13px; color:#cbd5e1; background:#0f172a; padding:10px; border-radius:6px; border-left:3px solid #f59e0b;">
            {pattern_notes}
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_tr:
        # Top Right Circle: Signal Circle Gauge
        border_color = "#10b981" if "BUY" in signal_type else "#ef4444"
        st.markdown(f"""
        <div style="background-color:#1e293b; padding:20px; border-radius:10px; border:1px solid #334155; text-align:center;">
            <h4 style="margin:0; color:#a855f7;">⭕ Signal Rating</h4>
            <div style="width:115px; height:115px; border-radius:50%; border:8px solid {border_color}; margin:15px auto; display:flex; align-items:center; justify-content:center; background:#0f172a;">
                <h2 style="margin:0; color:#ffffff; font-size:28px;">{conf_score}</h2>
            </div>
            <p style="margin:0; color:{border_color}; font-weight:bold; font-size:16px;">{signal_type}</p>
        </div>
        """, unsafe_allow_html=True)

    # BOTTOM ROW MATCHING HAND-DRAWN WIREFRAME (3 COLUMNS)
    st.markdown("<br>", unsafe_allow_html=True)
    col_b1, col_b2, col_b3 = st.columns([1, 1, 1])

    with col_b1:
        st.markdown(f"""
        <div style="background-color:#1e293b; padding:15px; border-radius:10px; border:1px solid #334155; min-height:160px;">
            <h4 style="margin:0 0 10px 0; color:#38bdf8;">📰 News & Macro Drivers</h4>
            <p style="font-size:13px; color:#cbd5e1; margin:0;">{news_notes}</p>
        </div>
        """, unsafe_allow_html=True)

    with col_b2:
        st.markdown(f"""
        <div style="background-color:#1e293b; padding:15px; border-radius:10px; border:1px solid #334155; min-height:160px;">
            <h4 style="margin:0 0 10px 0; color:#ec4899;">🧠 Trading Psychology & Rules</h4>
            <p style="font-size:13px; color:#cbd5e1; margin:0;">{psychology_notes}</p>
        </div>
        """, unsafe_allow_html=True)

    with col_b3:
        st.markdown(f"""
        <div style="background-color:#1e293b; padding:15px; border-radius:10px; border:1px solid #334155; min-height:160px;">
            <h4 style="margin:0 0 10px 0; color:#f59e0b;">📈 Technical Confirmations</h4>
            <p style="font-size:13px; color:#cbd5e1; margin:0;">{metrics_notes}</p>
        </div>
        """, unsafe_allow_html=True)


if analysis_mode == "📺 Live TradingView Real-Time Chart":
    st.subheader("1. Live TradingView Real-Time Chart")

    c_s1, c_s2, c_s3 = st.columns([2, 1, 1])
    with c_s1:
        pair_input = st.selectbox(
            "Select Crypto Pair",
            ["BINANCE:BTCUSDT", "BINANCE:ETHUSDT", "BINANCE:SOLUSDT", "BINANCE:BNBUSDT", "BINANCE:XRPUSDT", "BINANCE:DOGEUSDT"],
            index=0
        )
    with c_s2:
        interval_input = st.selectbox(
            "Timeframe",
            ["1", "5", "15", "60", "240", "D"],
            index=3,
            format_func=lambda x: {"1": "1m", "5": "5m", "15": "15m", "60": "1 Hour (1h)", "240": "4 Hours (4h)", "D": "1 Day (1D)"}[x]
        )
    with c_s3:
        chart_theme = st.selectbox("Chart Theme", ["dark", "light"], index=0)

    tv_widget_html = f"""
    <div class="tradingview-widget-container" style="height:550px;width:100%">
      <div id="tradingview_chart" style="height:calc(100% - 32px);width:100%"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget(
      {{
        "autosize": true,
        "symbol": "{pair_input}",
        "interval": "{interval_input}",
        "timezone": "Etc/UTC",
        "theme": "{chart_theme}",
        "style": "1",
        "locale": "en",
        "toolbar_bg": "#f1f3f6",
        "enable_publishing": false,
        "allow_symbol_change": true,
        "studies": ["STD;EMA", "STD;RSI"],
        "container_id": "tradingview_chart"
      }}
      );
      </script>
    </div>
    """
    components.html(tv_widget_html, height=570)

    st.markdown("---")
    
    if st.button("⚡ OPEN PRO AI SIGNAL & ANALYSIS POPUP", type="primary"):
        render_analysis_popup(
            pair=pair_input.replace("BINANCE:", ""),
            timeframe=f"{interval_input}m" if interval_input in ["1","5","15"] else ("1H" if interval_input=="60" else ("4H" if interval_input=="240" else "1D")),
            conf_score="88%",
            signal_type="BUY / LONG",
            entry_zone="$63,800 - $64,100",
            tp1="$65,200",
            tp2="$66,400",
            sl="$63,150",
            rr="1 : 2.85 R:R",
            demand_zone="$63,000 - $63,400 (Strong Buying Interest)",
            supply_zone="$65,500 - $66,200 (Heavy Seller Resistance)",
            pattern_notes="Bullish Liquidity Sweep at $63,800 with 1H Market Structure Shift (MSS). Confirmed volume expansion on breakout candle.",
            news_notes="• Federal Reserve Interest Rate Decision coming up; dovish market pricing.<br>• On-chain exchange outflows show whale accumulation.",
            psychology_notes="• <b>Rule #1:</b> Do NOT risk more than 1.5% of total capital.<br>• <b>Rule #2:</b> Do NOT chase price past $64,400.<br>• <b>Rule #3:</b> Move SL to Breakeven after TP1 is hit.",
            metrics_notes="• <b>RSI (14):</b> 52.4 (Bullish Divergence)<br>• <b>EMA 20/50:</b> Golden Cross on 15M<br>• <b>Funding Rate:</b> Neutral (0.01%)"
        )

