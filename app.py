import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
import yfinance as yf
import google.generativeai as genai

st.set_page_config(page_title="AI Pro Chart Analyzer", page_icon="📈", layout="wide")

st.title("📈 AI Pro Chart Analyzer App")
st.caption("Professional Crypto & Stock Technical Analysis powered by AI")

st.sidebar.header("⚙️ Configuration")
api_key = st.sidebar.text_input("Gemini API Key (Optional for Vision AI)", type="password")

analysis_mode = st.sidebar.radio("Select Mode", ["📸 Upload Chart Image", "📊 Live Market Data Analysis"])

if api_key:
    genai.configure(api_key=api_key)

# MODE 1: Upload Chart Screenshot
if analysis_mode == "📸 Upload Chart Image":
    st.subheader("1. Upload Trading Chart Screenshot")
    uploaded_file = st.file_uploader("Choose a chart screenshot", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        col1, col2 = st.columns()

        with col1:
            st.image(image, caption="Uploaded Chart", use_container_width=True)

        with col2:
            st.subheader("🤖 AI Analysis Options")
            trade_type = st.selectbox("Trading Style", ["Swing Trading (4H/1D)", "Intraday (15M/1H)", "Scalping (1M/5M)"])
            user_notes = st.text_area("Additional Context", placeholder="e.g. BTC/USDT 1H chart...")

            if st.button("🚀 Analyze Chart with AI", type="primary"):
                if api_key:
                    try:
                        model = genai.GenerativeModel('gemini-1.5-flash')
                        prompt = f"""
                        You are an elite institutional technical analyst. Analyze the chart thoroughly:
                        1. Market Structure & Trend
                        2. Key Support & Resistance Levels
                        3. Candlestick & Chart Patterns
                        4. Bullish/Bearish Trade Setups with Entry, SL, and TP.
                        """
                        response = model.generate_content([prompt, image])
                        st.markdown(response.text)
                    except Exception as e:
                        st.error(f"Error: {e}")
                else:
                    st.warning("⚠️ Enter Gemini API Key in sidebar for Vision AI analysis.")

# MODE 2: Live Crypto Data
elif analysis_mode == "📊 Live Market Data Analysis":
    st.subheader("2. Analyze Live Crypto / Stock Symbol")
    symbol = st.text_input("Enter Ticker Symbol", value="BTC-USD")

    if st.button("📊 Fetch & Analyze", type="primary"):
        data = yf.download(symbol, period="3mo", interval="1d")
        if not data.empty:
            if isinstance(data.columns, pd.MultiIndex):
                data.columns = data.columns.get_level_values(0)

            data['EMA_20'] = data['Close'].ewm(span=20, adjust=False).mean()
            data['EMA_50'] = data['Close'].ewm(span=50, adjust=False).mean()

            latest_price = float(data['Close'].iloc[-1])
            latest_ema20 = float(data['EMA_20'].iloc[-1])

            st.metric("Current Price", f"${latest_price:,.2f}")
            st.line_chart(data[['Close', 'EMA_20']])
