import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests

st.title("Economic Indicator Tracker")

API_KEY = "ec3217f9afb3137e1833ddc192fa1c19"

def fetch_fred_data(series_id):
    """Fetches data for the given FRED series ID."""
    url = f"https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": series_id,
        "api_key": API_KEY,
        "file_type": "json"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        observations = data.get("observations", [])
        df = pd.DataFrame(observations)
        df["date"] = pd.to_datetime(df["date"])
        df["value"] = pd.to_numeric(df["value"], errors="coerce")
        return df[["date", "value"]]
    else:
        raise ValueError(f"Error fetching data from FRED API: {response.status_code}")

# Sidebar: Choose dataset
st.sidebar.header("Select Economic Indicator")
indicator = st.sidebar.selectbox("Choose an indicator:", ["GDP", "Unemployment Rate", "Core CPI (percent change)", "Federal Funds Rate"])


FRED_SERIES = {
    "GDP": "GDP",
    "Unemployment Rate": "UNRATE",
    "Core CPI (percent change)": "CORESTICKM159SFRBATL",
    "Federal Funds Rate": "FEDFUNDS"
}


series_id = FRED_SERIES[indicator]
try:
    data = fetch_fred_data(series_id)
    st.write(f"Live Data for {indicator}")
    st.line_chart(data.set_index("date")["value"])
except Exception as e:
    st.error(f"Error fetching data: {e}")