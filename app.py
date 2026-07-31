import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import pandas as pd
import numpy as np
import yfinance as yf
import google.generativeai as genai

st.set_page_config(
    page_title="Pro AI TradingView Chart Analyzer",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main { background-color: #0d1117; color: #c9d1d9; }
    .stAppHeader { background-color: #0d1117; }
    h1, h2, h3 { color: #58a6ff; }
    .stButton>button {
        background-color: #238636;
        color: white;
        font-weight: bold;
        border-radius: 6px;
    }
</style>
""", unsafe_allow_html=True)

st.title("📈 AI Pro TradingView Chart Analyzer")
st.caption("Live Real-time TradingView Candlestick Charts & Institutional AI Technical Analysis")

st.sidebar.header("⚙️ Trading Controls")
api_key = st.sidebar.text_input("Gemini API Key (Optional for Vision AI)", type="password")

analysis_mode = st.sidebar.radio(
    "Select Mode",
    ["📺 Live TradingView Real-Time Chart", "📸 Upload Chart Screenshot"]
)

if api_key:
    genai.configure(api_key=api_key)

if analysis_mode == "📺 Live TradingView Real-Time Chart":
    st.subheader("1. Live Real-Time TradingView Candlestick Chart")

    col_sym1, col_sym2, col_sym3 = st.columns([2, 1, 1])
    with col_sym1:
        pair_input = st.selectbox(
            "Select Crypto Pair / Exchange Symbol",
            [
                "BINANCE:BTCUSDT",
                "BINANCE:ETHUSDT",
                "BINANCE:SOLUSDT",
                "BINANCE:BNBUSDT",
                "BINANCE:XRPUSDT",
                "BINANCE:DOGEUSDT",
                "BINANCE:ADAUSDT",
                "COINBASE:BTCUSD"
            ],
            index=0
        )
    with col_sym2:
        interval_input = st.selectbox(
            "Select Timeframe",
            ["1", "5", "15", "60", "240", "D"],
            index=3,
            format_func=lambda x: {"1": "1m", "5": "5m", "15": "15m", "60": "1 Hour (1h)", "240": "4 Hours (4h)", "D": "1 Day (1D)"}[x]
        )
    with col_sym3:
        chart_theme = st.selectbox("Chart Theme", ["dark", "light"], index=0)

    tv_widget_html = f"""
    <div class="tradingview-widget-container" style="height:620px;width:100%">
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
        "details": true,
        "hotlist": true,
        "calendar": true,
        "studies": [
          "STD;EMA",
          "STD;RSI"
        ],
        "container_id": "tradingview_chart"
      }}
      );
      </script>
    </div>
    """
    components.html(tv_widget_html, height=640)

    st.markdown("---")
    st.subheader("🔍 Professional Institutional Analysis Checklist")

    col_a, col_b = st.columns([1, 1])

    with col_a:
        st.markdown("""
        ### 📌 Step 1: Market Structure Analysis
        * **Trend Identification**: Look at Higher Timeframe (4H/1D). Higher Highs & Higher Lows (Uptrend) vs Lower Highs & Lower Lows (Downtrend).
        * **Liquidity Sweeps**: Observe if recent swing highs or lows were swept before aggressive reversal.
        * **Market Structure Shift (MSS)**: Confirm if the last swing high/low broke with a strong body close.
        """)

    with col_b:
        st.markdown("""
        ### 🎯 Step 2: Key Levels & Trade Execution Plan
        * **Demand / Support Zone**: Identify the last down-candle before a strong rally.
        * **Supply / Resistance Zone**: Identify the last up-candle before a sharp decline.
        * **Risk-to-Reward Ratio**: Minimum 1:2 R:R.
        """)

elif analysis_mode == "📸 Upload Chart Screenshot":
    st.subheader("2. Upload Chart Screenshot for Instant AI Breakdown")
    uploaded_file = st.file_uploader("Upload chart screenshot", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        c1, c2 = st.columns([1, 1])
        with c1:
            st.image(image, caption="Uploaded Chart", use_container_width=True)
        with c2:
            st.markdown("### 🤖 Vision AI Analysis")
            user_notes = st.text_area("Notes / Questions", placeholder="e.g. BTC/USDT 1H chart, looking for Long entry...")

            if st.button("🚀 Analyze with Professional AI"):
                if api_key:
                    try:
                        model = genai.GenerativeModel('gemini-1.5-flash')
                        prompt = """
                        You are a veteran institutional price-action trader with 10+ years of experience.
                        Analyze this chart screenshot in rigorous detail:
                        1. Market Structure & Trend
                        2. Key Support & Resistance Levels
                        3. Candlestick Patterns & Liquidity Zones
                        4. Trade Setups (Long & Short scenarios with Entry, SL, TP, and R:R)
                        5. Risk Management Warning
                        """
                        response = model.generate_content([prompt, image])
                        st.markdown(response.text)
                    except Exception as e:
                        st.error(f"AI Analysis Error: {e}")
                else:
                    st.warning("⚠️ Enter Gemini API Key in sidebar for Vision AI analysis.")

