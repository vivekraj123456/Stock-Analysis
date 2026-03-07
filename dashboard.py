"""
========================================================
  STOCK INTELLIGENCE DASHBOARD - Premium Edition
  pip install dash dash-bootstrap-components plotly pandas
  python dashboard.py -> http://localhost:8050
========================================================
"""
import os, warnings, json, time
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from dash import Dash, dcc, html, Input, Output, State, callback_context, no_update, MATCH
import dash_bootstrap_components as dbc
from datetime import datetime, timedelta, timezone

try:
    import yfinance as yf
except Exception:
    yf = None

# ÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚Â
#  DATA
# ÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚Â
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "powerbi_data")

prices   = pd.read_csv(os.path.join(BASE,"fact_stock_prices.csv"),  parse_dates=["Date"], low_memory=False)
snapshot = pd.read_csv(os.path.join(BASE,"snapshot_latest.csv"),    parse_dates=["Date"], low_memory=False)
company  = pd.read_csv(os.path.join(BASE,"dim_company.csv"),        low_memory=False)

# INR-native display (no FX conversion).
def fmt_inr(val, compact=False):
    """Format value as Indian Rupees."""
    if pd.isna(val) or val is None: return "-"
    if compact:
        if abs(val) >= 1e7:  return f"INR {val/1e7:.2f}Cr"
        if abs(val) >= 1e5:  return f"INR {val/1e5:.2f}L"
        if abs(val) >= 1000: return f"INR {val/1000:.1f}K"
    return f"INR {val:,.2f}"

def is_indian_symbol(ticker):
    if not isinstance(ticker, str):
        return False
    return ticker.endswith(".NS") or ticker.endswith(".BO")

prices = prices[prices["Ticker"].map(is_indian_symbol)].copy()
snapshot = snapshot[snapshot["Ticker"].map(is_indian_symbol)].copy()
company = company[company["Ticker"].map(is_indian_symbol)].copy()

prices["Sector"] = prices["Ticker"].map(company.set_index("Ticker")["Sector"])
snapshot = snapshot.merge(company[["Ticker","Sector","Company"]], on="Ticker", how="left", suffixes=("","_c"))

TICKERS = sorted(prices["Ticker"].unique())
MIN_DATE = prices["Date"].min()
MAX_DATE = prices["Date"].max()
DEFAULT_T = [
    t for t in ["RELIANCE.NS","TCS.NS","HDFCBANK.NS","ICICIBANK.NS","INFY.NS"]
    if t in TICKERS
][:5]

IST = timezone(timedelta(hours=5, minutes=30))
LIVE_CACHE_TTL_SECONDS = int(os.getenv("LIVE_CACHE_TTL_SECONDS", "60"))
_LIVE_QUOTE_CACHE = {}

def _to_float(value):
    """Best-effort float conversion for external quote fields."""
    try:
        if value is None:
            return None
        if isinstance(value, float) and np.isnan(value):
            return None
        return float(value)
    except Exception:
        return None

def _as_utc_timestamp(value):
    if value is None:
        return pd.NaT
    try:
        if isinstance(value, (int, float, np.integer, np.floating)):
            if isinstance(value, float) and np.isnan(value):
                return pd.NaT
            v = float(value)
            if v > 1e14:
                return pd.to_datetime(v, unit="ns", utc=True, errors="coerce")
            if v > 1e11:
                return pd.to_datetime(v, unit="ms", utc=True, errors="coerce")
            return pd.to_datetime(v, unit="s", utc=True, errors="coerce")
        return pd.to_datetime(value, errors="coerce", utc=True)
    except Exception:
        return pd.NaT

def _fast_info_get(fast_info, key):
    try:
        if isinstance(fast_info, dict):
            return fast_info.get(key)
        if hasattr(fast_info, "get"):
            return fast_info.get(key)
        return fast_info[key]
    except Exception:
        return None

def _fetch_single_live_quote(ticker):
    if yf is None:
        return None

    tk = yf.Ticker(ticker)
    fast_info = {}
    try:
        fast_info = tk.fast_info or {}
    except Exception:
        fast_info = {}

    price = _to_float(_fast_info_get(fast_info, "last_price"))
    prev_close = _to_float(_fast_info_get(fast_info, "previous_close"))
    volume = _to_float(_fast_info_get(fast_info, "last_volume"))
    as_of = _as_utc_timestamp(_fast_info_get(fast_info, "last_price_time"))

    # Fallback to recent daily candles when fast quote fields are missing.
    if price is None or prev_close is None:
        try:
            hist = tk.history(period="5d", interval="1d", auto_adjust=False, timeout=8)
        except TypeError:
            # Older yfinance versions do not support timeout argument here.
            hist = tk.history(period="5d", interval="1d", auto_adjust=False)
        except Exception:
            hist = pd.DataFrame()
        if not hist.empty:
            if price is None and "Close" in hist.columns:
                price = _to_float(hist["Close"].iloc[-1])
            if prev_close is None and "Close" in hist.columns:
                if len(hist) > 1:
                    prev_close = _to_float(hist["Close"].iloc[-2])
                else:
                    prev_close = _to_float(hist["Close"].iloc[-1])
            if pd.isna(as_of):
                as_of = _as_utc_timestamp(hist.index[-1])

    if price is None:
        return None

    chg_pct = None
    if prev_close and prev_close != 0:
        chg_pct = ((price / prev_close) - 1) * 100

    return {
        "price": price,
        "daily_change_pct": chg_pct,
        "volume": volume,
        "as_of": as_of if not pd.isna(as_of) else pd.NaT,
    }

def get_live_quotes(tickers):
    now = time.time()
    live = {}

    for ticker in sorted({t for t in tickers if isinstance(t, str) and t.strip()}):
        cached = _LIVE_QUOTE_CACHE.get(ticker)
        if cached and now - cached["ts"] <= LIVE_CACHE_TTL_SECONDS:
            live[ticker] = cached["quote"]
            continue

        quote = None
        try:
            quote = _fetch_single_live_quote(ticker)
        except Exception:
            quote = None

        if quote is not None:
            _LIVE_QUOTE_CACHE[ticker] = {"ts": now, "quote": quote}
            live[ticker] = quote
        elif cached:
            live[ticker] = cached["quote"]

    return live

def with_live_quotes(snap_df):
    if snap_df.empty:
        return snap_df

    out = snap_df.copy()
    out["Price_Source"] = "EOD"
    out["Price_As_Of"] = out.get("Date")
    out["Price_As_Of"] = out["Price_As_Of"].astype("object")

    live = get_live_quotes(out["Ticker"].dropna().astype(str).tolist())
    if not live:
        return out

    for idx, row in out.iterrows():
        quote = live.get(row.get("Ticker"))
        if quote is None:
            continue

        out.at[idx, "Close"] = quote["price"]
        if quote.get("daily_change_pct") is not None:
            out.at[idx, "Daily_Return_%"] = quote["daily_change_pct"]
        out.at[idx, "Price_Source"] = "LIVE"
        out.at[idx, "Price_As_Of"] = quote.get("as_of")

    return out

def fmt_quote_timestamp(ts):
    stamp = pd.to_datetime(ts, errors="coerce", utc=True)
    if pd.isna(stamp):
        return "Time unavailable"
    return stamp.tz_convert(IST).strftime("%d %b %Y %I:%M %p IST")

# ÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚Â
#  DESIGN SYSTEM ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Luxury Dark Financial Theme
# ÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚Â
# Deep navy-black base, gold accents, electric teal highlights
# Typography: Outfit (display) + DM Mono (numbers)

BG0    = "#03060f"   # deepest background
BG1    = "#060d1a"   # page bg
BG2    = "#0a1628"   # card bg
BG3    = "#0e1e35"   # elevated card
GLASS  = "rgba(14,30,53,0.7)"
BORDER = "rgba(255,255,255,0.06)"
BORDER2= "rgba(255,255,255,0.12)"

GOLD   = "#f5c842"   # primary accent - gold
TEAL   = "#00e5cc"   # secondary accent - teal
BLUE   = "#4d9fff"   # info
GREEN  = "#00d68f"   # positive
RED    = "#ff4d6d"   # negative
AMBER  = "#ffb84d"   # warning
PURPLE = "#9b72ff"   # special
PINK   = "#ff72b8"   # highlight

TEXT   = "#f0f4ff"
TEXT2  = "#8899bb"
TEXT3  = "#4a5878"
DIM    = "#1a2a44"

COLORS = [TEAL, GOLD, BLUE, GREEN, AMBER, PURPLE, PINK, RED,
          "#00b4d8","#90e0ef","#f77f00","#d62828"]

def gl(**kw):
    base = dict(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="'DM Mono',monospace", color=TEXT2, size=11),
        margin=dict(l=0,r=0,t=40,b=0),
        legend=dict(bgcolor="rgba(0,0,0,0)", font_size=10,
                    orientation="h", yanchor="bottom", y=1.02,
                    xanchor="left", x=0, font_color=TEXT2),
        xaxis=dict(gridcolor=DIM, zerolinecolor=DIM, color=TEXT3,
                   gridwidth=0.5, showgrid=True, tickfont_size=10),
        yaxis=dict(gridcolor=DIM, zerolinecolor=DIM, color=TEXT3,
                   gridwidth=0.5, showgrid=True, tickfont_size=10),
        hoverlabel=dict(bgcolor=BG3, font_color=TEXT, bordercolor=BORDER2,
                        font_family="'DM Mono',monospace", font_size=12),
        hovermode="x unified",
    )
    base.update(kw)
    return base

# ÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚Â
#  COMPONENTS
# ÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚Â
def card(children, glow=None, style=None, pad="20px"):
    glow_css = f"box-shadow: 0 0 40px {glow}22, 0 8px 32px rgba(0,0,0,0.5);" if glow else "box-shadow: 0 4px 24px rgba(0,0,0,0.4);"
    s = {
        "background": BG2,
        "border": f"1px solid {BORDER}",
        "borderRadius": "16px",
        "padding": pad,
        "marginBottom": "16px",
        "backdropFilter": "blur(12px)",
        "position": "relative",
        "overflow": "hidden",
    }
    if style: s.update(style)
    return html.Div(children, style=s)

def G(fig, h=None, gid=None):
    s = {"width":"100%"}
    if h: s["height"] = f"{h}px"
    props = {
        "figure": fig,
        "config": {
            "displayModeBar": True,
            "modeBarButtonsToRemove": ["lasso2d","select2d","autoScale2d"],
            "displaylogo": False,
            "toImageButtonOptions": {"format":"png","scale":2},
        },
        "style": s,
    }
    if gid is not None:
        props["id"] = gid
    return dcc.Graph(**props)

def badge(text, color=TEAL):
    return html.Span(text, style={
        "background": f"{color}18", "color": color,
        "border": f"1px solid {color}40",
        "borderRadius": "6px", "padding": "3px 10px",
        "fontSize": "10px", "fontWeight": "600", "letterSpacing": "1px",
        "textTransform": "uppercase", "fontFamily": "'DM Mono',monospace",
    })

def lbl(text):
    return html.Div(text, style={
        "fontSize": "10px", "color": TEXT3, "letterSpacing": "2px",
        "textTransform": "uppercase", "marginBottom": "6px",
        "fontFamily": "'Outfit',sans-serif", "fontWeight": "500"
    })

def divider():
    return html.Div(style={"height":"1px","background":f"linear-gradient(90deg,transparent,{BORDER2},transparent)","margin":"4px 0"})


def ticker_opts():
    cm = company.set_index("Ticker")
    return [{"label": f"{t} | {cm.loc[t,'Company'] if t in cm.index else t}", "value": t}
            for t in TICKERS]

MONTH_LABELS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
MONTH_NAME_TO_NUM = {m: i + 1 for i, m in enumerate(MONTH_LABELS)}
MONTH_NUM_TO_NAME = {i + 1: m for i, m in enumerate(MONTH_LABELS)}

def hex_to_rgba(hex_color, alpha=0.15):
    h = str(hex_color).lstrip("#")
    if len(h) != 6:
        return f"rgba(255,255,255,{alpha})"
    return f"rgba({int(h[0:2],16)},{int(h[2:4],16)},{int(h[4:6],16)},{alpha})"

def build_month_wave_figure(sub, ticker, year=None, month=None):
    inr_prefix = fmt_inr(0).replace("0.00", "")
    empty_fig = go.Figure()
    empty_fig.update_layout(**gl(height=320, title="",
        xaxis=dict(gridcolor=DIM, color=TEXT3),
        yaxis=dict(gridcolor=DIM, color=TEXT3)))

    if sub is None or sub.empty:
        empty_fig.add_annotation(text="No data in selected range", showarrow=False,
            font=dict(color=TEXT3, size=12))
        return empty_fig, f"{ticker} | No data in selected range"

    sub = sub.sort_values("Date").copy()
    if "Daily_Return_%" not in sub.columns:
        sub["Daily_Return_%"] = sub["Close"].pct_change() * 100
    sub["Daily_Return_%"] = sub["Daily_Return_%"].fillna(0)
    sub["Daily_Change_INR"] = sub["Close"].diff().fillna(0)

    if year is None or month is None:
        latest = sub["Date"].max()
        year, month = int(latest.year), int(latest.month)
    year, month = int(year), int(month)

    sel = sub[(sub["Date"].dt.year == year) & (sub["Date"].dt.month == month)].copy()
    if sel.empty:
        mlabel = MONTH_NUM_TO_NAME.get(month, str(month))
        empty_fig.add_annotation(text=f"No trading data for {mlabel} {year}", showarrow=False,
            font=dict(color=TEXT3, size=12))
        return empty_fig, f"{ticker} | {mlabel} {year} | No trading data"

    start_p = float(sel["Close"].iloc[0])
    end_p = float(sel["Close"].iloc[-1])
    change = end_p - start_p
    ret = (end_p / start_p - 1) * 100 if start_p else 0
    color = GREEN if change >= 0 else RED

    wf = go.Figure(go.Scatter(
        x=sel["Date"], y=sel["Close"], mode="lines+markers", name=ticker,
        line=dict(color=color, width=3, shape="spline"),
        marker=dict(size=5, color=color),
        fill="tozeroy", fillcolor=hex_to_rgba(color, 0.15),
        customdata=np.column_stack([sel["Daily_Change_INR"], sel["Daily_Return_%"]]),
        hovertemplate=(
            "<b>%{x|%d %b %Y}</b><br>"
            f"Close: {inr_prefix}%{{y:,.2f}}<br>"
            f"Daily Change: {inr_prefix}%{{customdata[0]:+,.2f}}<br>"
            "Daily Return: %{customdata[1]:+.2f}%<extra></extra>"
        ),
    ))
    wf.update_layout(**gl(height=320, title="", hovermode="x unified",
        yaxis=dict(gridcolor=DIM, color=TEXT3, tickprefix=inr_prefix, tickformat=",.0f"),
        xaxis=dict(gridcolor=DIM, color=TEXT3)))

    caption = (
        f"{ticker} | {MONTH_NUM_TO_NAME.get(month, str(month))} {year} | "
        f"{inr_prefix}{change:+,.2f} ({ret:+.2f}%)"
    )
    return wf, caption

def build_month_daily_table_figure(sub, ticker, year=None, month=None):
    tf = go.Figure()
    tf.update_layout(**gl(height=260, title=""))

    if sub is None or sub.empty:
        tf.add_annotation(text=f"{ticker}: no data in selected range", showarrow=False,
            font=dict(color=TEXT3, size=11))
        return tf

    sub = sub.sort_values("Date").copy()
    if "Daily_Return_%" not in sub.columns:
        sub["Daily_Return_%"] = sub["Close"].pct_change() * 100
    sub["Daily_Return_%"] = sub["Daily_Return_%"].fillna(0)

    if year is None or month is None:
        latest = sub["Date"].max()
        year, month = int(latest.year), int(latest.month)
    year, month = int(year), int(month)

    sel = sub[(sub["Date"].dt.year == year) & (sub["Date"].dt.month == month)].copy()
    if sel.empty:
        mlabel = MONTH_NUM_TO_NAME.get(month, str(month))
        tf.add_annotation(text=f"{ticker}: no daily rows for {mlabel} {year}", showarrow=False,
            font=dict(color=TEXT3, size=11))
        return tf

    rows = pd.DataFrame()
    rows["Date"] = sel["Date"].dt.strftime("%d %b %Y")
    if "Open" in sel.columns:
        rows["Open"] = sel["Open"].map(lambda v: f"{v:,.2f}")
    if "High" in sel.columns:
        rows["High"] = sel["High"].map(lambda v: f"{v:,.2f}")
    if "Low" in sel.columns:
        rows["Low"] = sel["Low"].map(lambda v: f"{v:,.2f}")
    if "Close" in sel.columns:
        rows["Close"] = sel["Close"].map(lambda v: f"{v:,.2f}")
    if "Volume" in sel.columns:
        rows["Volume"] = sel["Volume"].fillna(0).map(lambda v: f"{int(v):,}")
    rows["Daily Return %"] = sel["Daily_Return_%"].map(lambda v: f"{v:+.2f}%")

    tf = go.Figure(go.Table(
        header=dict(
            values=[f"<b>{c}</b>" for c in rows.columns.tolist()],
            fill_color=DIM, font=dict(color=GOLD, size=11, family="'DM Mono',monospace"),
            align="left", height=36, line_color=BG0
        ),
        cells=dict(
            values=[rows[c].tolist() for c in rows.columns.tolist()],
            fill_color=[[BG3 if i % 2 == 0 else BG2 for i in range(len(rows))]],
            font=dict(color=TEXT, size=10, family="'DM Mono',monospace"),
            align="left", height=28, line_color=BG0
        )
    ))
    tf.update_layout(**gl(height=max(260, min(760, len(rows) * 28 + 95)), title=""))
    return tf

# ÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚Â
#  APP
# ÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚Â
app = Dash(__name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=DM+Mono:wght@300;400;500&display=swap",
    ],
    suppress_callback_exceptions=True,
    meta_tags=[{"name":"viewport","content":"width=device-width, initial-scale=1"}]
)
app.title = "Stock Intelligence"

NAV = [
    ("overview",    "overview",    "Market Overview",   "O"),
    ("price",       "price",       "Price & Volume",    "P"),
    ("technicals",  "technicals",  "Technicals",        "T"),
    ("compare",     "compare",     "Compare",           "C"),
    ("sector",      "sector",      "Sectors",           "S"),
    ("risk",        "risk",        "Risk & Vol",        "R"),
    ("screener",    "screener",    "Screener",          "F"),
    ("heatmap",     "heatmap",     "Heat Map",          "H"),
]

# ÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚Â
#  LAYOUT
# ÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚Â
app.layout = html.Div([
    dcc.Store(id="active-page", data="overview"),
    dcc.Interval(id="clock", interval=60000, n_intervals=0),

    html.Div(style={
        "display": "flex", "minHeight": "100vh",
        "background": BG1, "fontFamily": "'Outfit',sans-serif",
        "color": TEXT,
    }, children=[

        # ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ SIDEBAR ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬
        html.Div(style={
            "width": "240px", "minWidth": "240px",
            "background": f"linear-gradient(180deg, {BG2} 0%, {BG0} 100%)",
            "borderRight": f"1px solid {BORDER}",
            "height": "100vh", "position": "sticky", "top": "0",
            "display": "flex", "flexDirection": "column",
            "overflow": "hidden",
        }, children=[

            # Logo
            html.Div(style={
                "padding": "28px 24px 24px",
                "borderBottom": f"1px solid {BORDER}",
                "position": "relative",
            }, children=[
                html.Div(style={"display":"flex","alignItems":"center","gap":"12px"}, children=[
                    html.Div("SI", style={
                        "fontSize": "26px", "color": GOLD,
                        "filter": f"drop-shadow(0 0 8px {GOLD}88)",
                        "lineHeight": "1",
                    }),
                    html.Div([
                        html.Div("STOCK", style={"fontSize":"15px","fontWeight":"800",
                            "color":TEXT,"letterSpacing":"3px","lineHeight":"1"}),
                        html.Div("INTELLIGENCE", style={"fontSize":"8px","color":GOLD,
                            "letterSpacing":"4px","marginTop":"2px","fontWeight":"600"}),
                    ]),
                ]),
                html.Div(style={
                    "marginTop":"16px","display":"flex","gap":"6px","flexWrap":"wrap"
                }, children=[
                    badge("INDIA", GOLD),
                    badge("INR", TEAL),
                    badge("LIVE", GREEN),
                ]),
            ]),

            # Nav links
            html.Div(style={"flex":"1","padding":"12px 8px","overflowY":"auto"}, children=[
                html.Div(id=f"nav-{page}", children=[
                    html.Span(icon, style={
                        "fontSize": "16px", "width": "24px", "display":"inline-block",
                        "textAlign": "center", "marginRight": "10px",
                    }),
                    html.Span(name, style={"fontSize":"13px","fontWeight":"500"}),
                ], n_clicks=0, style={"cursor":"pointer"})
                for page, _, name, icon in NAV
            ]),

            # Data info
            html.Div(style={
                "padding":"16px 20px",
                "borderTop": f"1px solid {BORDER}",
                "background": f"rgba(0,0,0,0.3)",
            }, children=[
                html.Div(id="data-meta"),
                html.Div("Data Source: Yahoo Finance (NSE/BSE, INR)", style={
                    "fontSize":"10px","color":AMBER,"marginTop":"8px",
                    "fontFamily":"'DM Mono',monospace",
                }),
            ]),
        ]),

        # ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ MAIN CONTENT ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬
        html.Div(style={"flex":"1","display":"flex","flexDirection":"column","minWidth":"0"}, children=[

            # Top bar
            html.Div(style={
                "background": f"linear-gradient(90deg,{BG2},{BG0})",
                "borderBottom": f"1px solid {BORDER}",
                "padding": "0 28px",
                "display": "flex", "alignItems": "center",
                "justifyContent": "space-between",
                "height": "60px", "position": "sticky", "top": "0", "zIndex": "100",
            }, children=[
                html.Div(id="page-title", style={
                    "fontSize":"16px","fontWeight":"700","color":TEXT,
                    "letterSpacing":"0.5px",
                }),
                html.Div(style={"display":"flex","alignItems":"center","gap":"16px"}, children=[
                    html.Div(id="live-time", style={
                        "fontSize":"12px","color":TEXT3,
                        "fontFamily":"'DM Mono',monospace",
                    }),
                    html.Div([
                        html.Span("*", style={"color":GREEN,"fontSize":"10px","marginRight":"5px",
                            "animation":"pulse 2s infinite"}),
                        html.Span("NSE / BSE", style={"fontSize":"11px","color":TEXT3}),
                    ]),
                ]),
            ]),

            # Controls bar
            html.Div(style={
                "background": BG2,
                "borderBottom": f"1px solid {BORDER}",
                "padding": "14px 28px",
            }, children=[
                html.Div(style={
                    "display":"grid",
                    "gridTemplateColumns":"2.5fr 1.4fr 0.7fr 0.7fr",
                    "gap":"16px","alignItems":"end"
                }, children=[
                    html.Div([
                        lbl("Select Stocks"),
                        dcc.Dropdown(id="g-tickers", options=ticker_opts(),
                            value=DEFAULT_T, multi=True, clearable=False,
                            className="ctrl-dd",
                            style={"fontSize":"12px"}),
                    ]),
                    html.Div([
                        lbl("Date Range"),
                        dcc.DatePickerRange(id="g-dates",
                            min_date_allowed=MIN_DATE, max_date_allowed=MAX_DATE,
                            start_date=(MAX_DATE-timedelta(days=365*3)).strftime("%Y-%m-%d"),
                            end_date=MAX_DATE.strftime("%Y-%m-%d"),
                            className="ctrl-date",
                            display_format="DD MMM YYYY"),
                    ]),
                    html.Div([
                        lbl("Chart"),
                        dcc.Dropdown(id="g-ctype",
                            options=[{"label":"Line","value":"line"},
                                     {"label":"Candle","value":"candle"},
                                     {"label":"Area","value":"area"},
                                     {"label":"OHLC","value":"ohlc"}],
                            value="line", clearable=False, className="ctrl-dd"),
                    ]),
                    html.Div([
                        lbl("Scale"),
                        dcc.Dropdown(id="g-scale",
                            options=[{"label":"Linear","value":"linear"},
                                     {"label":"Log","value":"log"}],
                            value="linear", clearable=False, className="ctrl-dd"),
                    ]),
                ]),
                # Period buttons
                html.Div(style={"display":"flex","alignItems":"center","gap":"6px","marginTop":"12px"}, children=[
                    html.Span("Period:", style={"fontSize":"10px","color":TEXT3,"marginRight":"4px",
                        "letterSpacing":"1px","textTransform":"uppercase"}),
                    *[html.Button(p, id=f"btn-{p}", n_clicks=0, className="period-btn")
                      for p in ["1W","1M","3M","6M","1Y","3Y","5Y","10Y","MAX"]],
                ]),
            ]),

            # Page content
            html.Div(id="page-content", style={"padding":"24px 28px","flex":"1"}),
        ]),
    ]),
], style={"background":BG1})


# ÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚Â
#  CALLBACKS ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â ROUTING
# ÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚Â
@app.callback(Output("active-page","data"),
    [Input(f"nav-{p}","n_clicks") for p,_,__,___ in NAV],
    prevent_initial_call=True)
def set_page(*args):
    ctx = callback_context
    if not ctx.triggered: return "overview"
    return ctx.triggered[0]["prop_id"].split(".")[0].replace("nav-","")

for page, _, name, icon in NAV:
    @app.callback(Output(f"nav-{page}","style"), Input("active-page","data"))
    def nav_style(active, p=page):
        on = active == p
        return {
            "padding": "11px 16px", "cursor": "pointer",
            "borderRadius": "10px", "margin": "2px 0",
            "display": "flex", "alignItems": "center",
            "transition": "all 0.2s ease",
            "background": f"linear-gradient(90deg,{GOLD}15,{GOLD}05)" if on else "transparent",
            "color": GOLD if on else TEXT3,
            "borderLeft": f"2px solid {GOLD}" if on else "2px solid transparent",
            "fontWeight": "600" if on else "400",
        }

@app.callback(Output("page-title","children"), Input("active-page","data"))
def page_title(active):
    for p,_,name,icon in NAV:
        if p == active: return f"{icon}  {name}"
    return ""

@app.callback(Output("live-time","children"), Input("clock","n_intervals"))
def update_time(_):
    return datetime.now().strftime("%d %b %Y | %H:%M IST")

@app.callback(Output("data-meta","children"), Input("clock","n_intervals"))
def update_meta(_):
    try:
        m = pd.read_csv(os.path.join(BASE,"meta_refresh.csv")).iloc[0]
        return html.Div([
            html.Div(f"Stocks: {int(m['Stocks_Count'])}", style={"fontSize":"11px","color":TEXT3}),
            html.Div(f"Records: {int(m['Total_Rows']):,}", style={"fontSize":"11px","color":TEXT3}),
            html.Div("Updated:", style={"fontSize":"10px","color":TEXT3,"marginTop":"4px"}),
            html.Div(str(m['Last_Refresh'])[:16], style={"fontSize":"10px","color":GREEN,"fontFamily":"'DM Mono',monospace"}),
        ])
    except: return ""

@app.callback(Output("g-dates","start_date"),
    [Input(f"btn-{p}","n_clicks") for p in ["1W","1M","3M","6M","1Y","3Y","5Y","10Y","MAX"]],
    prevent_initial_call=True)
def quick_dates(*args):
    ctx = callback_context
    if not ctx.triggered: return no_update
    p = ctx.triggered[0]["prop_id"].split(".")[0].replace("btn-","")
    d = {"1W":7,"1M":30,"3M":90,"6M":180,"1Y":365,"3Y":1095,"5Y":1825,"10Y":3650}
    return MIN_DATE.strftime("%Y-%m-%d") if p=="MAX" else (MAX_DATE-timedelta(days=d[p])).strftime("%Y-%m-%d")

@app.callback(
    Output("price-month-wave", "figure"),
    Output("price-month-caption", "children"),
    Input("price-month-heatmap", "clickData"),
    State("g-tickers", "value"),
    State("g-dates", "start_date"),
    State("g-dates", "end_date"),
    prevent_initial_call=True
)
def month_heatmap_click(click_data, tickers, start_date, end_date):
    if not click_data or not tickers:
        return no_update, no_update

    ticker = tickers[0] if isinstance(tickers, list) else tickers
    points = click_data.get("points", [])
    if not points:
        return no_update, no_update

    month_name = str(points[0].get("x", ""))
    year_value = points[0].get("y", "")
    month = MONTH_NAME_TO_NUM.get(month_name)
    try:
        year = int(year_value)
    except (TypeError, ValueError):
        year = None

    if month is None or year is None:
        return no_update, no_update

    s = pd.to_datetime(start_date) if start_date else MIN_DATE
    e = pd.to_datetime(end_date) if end_date else MAX_DATE
    sub = prices[(prices["Ticker"] == ticker) & (prices["Date"] >= s) & (prices["Date"] <= e)].copy()
    wave_fig, wave_caption = build_month_wave_figure(sub, ticker, year, month)
    return wave_fig, wave_caption

# ÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚Â
#  MAIN RENDERER
# ÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚Â
@app.callback(
    Output({"type": "heatmap-month-detail-wave", "ticker": MATCH}, "figure"),
    Output({"type": "heatmap-month-detail-caption", "ticker": MATCH}, "children"),
    Output({"type": "heatmap-month-detail-table", "ticker": MATCH}, "figure"),
    Input({"type": "heatmap-month", "ticker": MATCH}, "clickData"),
    State({"type": "heatmap-month", "ticker": MATCH}, "id"),
    State("g-dates", "start_date"),
    State("g-dates", "end_date"),
    prevent_initial_call=True
)
def heatmap_page_month_click(click_data, heatmap_id, start_date, end_date):
    if not click_data or not isinstance(heatmap_id, dict):
        return no_update, no_update, no_update

    ticker = heatmap_id.get("ticker")
    if not ticker:
        return no_update, no_update, no_update

    points = click_data.get("points", [])
    if not points:
        return no_update, no_update, no_update

    month_name = str(points[0].get("x", ""))
    year_value = points[0].get("y", "")
    month = MONTH_NAME_TO_NUM.get(month_name)
    try:
        year = int(float(year_value))
    except (TypeError, ValueError):
        year = None

    if month is None or year is None:
        return no_update, no_update, no_update

    s = pd.to_datetime(start_date) if start_date else MIN_DATE
    e = pd.to_datetime(end_date) if end_date else MAX_DATE
    sub = prices[(prices["Ticker"] == ticker) & (prices["Date"] >= s) & (prices["Date"] <= e)].copy()
    wave_fig, wave_caption = build_month_wave_figure(sub, ticker, year, month)
    table_fig = build_month_daily_table_figure(sub, ticker, year, month)
    return wave_fig, wave_caption, table_fig

@app.callback(Output("page-content","children"),
    Input("active-page","data"), Input("g-tickers","value"),
    Input("g-dates","start_date"), Input("g-dates","end_date"),
    Input("g-ctype","value"), Input("g-scale","value"),
    Input("clock","n_intervals"))
def render(page, tickers, start, end, ctype, scale, _clock_tick):
    if not tickers: tickers = DEFAULT_T
    if isinstance(tickers, str): tickers = [tickers]
    s,e = pd.to_datetime(start), pd.to_datetime(end)
    df   = prices[(prices["Ticker"].isin(tickers))&(prices["Date"]>=s)&(prices["Date"]<=e)].copy()
    snap = snapshot[snapshot["Ticker"].isin(tickers)].copy()
    snap = with_live_quotes(snap)
    fns  = {"overview":pg_overview,"price":pg_price,"technicals":pg_technicals,
            "compare":pg_compare,"sector":pg_sector,"risk":pg_risk,
            "screener":pg_screener,"heatmap":pg_heatmap}
    return fns.get(page, pg_overview)(df, snap, tickers, ctype, scale)


# ÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚Â
#  PAGE 1 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â MARKET OVERVIEW
# ÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚Â
def pg_overview(df, snap, tickers, ctype, scale):
    # ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ KPI Cards ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬
    kpis = []
    for _, row in snap.iterrows():
        chg   = row.get("Daily_Return_%", 0) or 0
        y1    = row.get("Return_1Y_%", 0) or 0
        rsi   = row.get("RSI_14", 50) or 50
        price = row.get("Close", 0) or 0
        price_source = str(row.get("Price_Source", "EOD")).upper()
        price_as_of = row.get("Price_As_Of", row.get("Date"))
        up    = chg >= 0
        rsi_c = RED if rsi>70 else (GREEN if rsi<30 else AMBER)
        spark_data = df[df["Ticker"]==row["Ticker"]]["Close"].tail(30).tolist()

        if price_source == "LIVE":
            price_stamp = f"LIVE | {fmt_quote_timestamp(price_as_of)}"
        else:
            eod_date = pd.to_datetime(row.get("Date"), errors="coerce")
            eod_label = eod_date.strftime("%d %b %Y") if not pd.isna(eod_date) else "Date unavailable"
            price_stamp = f"EOD CLOSE | {eod_label}"

        kpis.append(html.Div([
            # Glow border top
            html.Div(style={
                "position":"absolute","top":"0","left":"0","right":"0","height":"2px",
                "background": f"linear-gradient(90deg,transparent,{GREEN if up else RED},transparent)",
            }),
            html.Div(style={"display":"flex","justifyContent":"space-between","alignItems":"flex-start","marginBottom":"12px"}, children=[
                html.Div([
                    html.Div(row["Ticker"], style={"fontSize":"15px","fontWeight":"800","color":TEXT,"letterSpacing":"1px"}),
                    html.Div(row.get("Company","")[:18] if pd.notna(row.get("Company","")) else "", style={"fontSize":"10px","color":TEXT3,"marginTop":"2px"}),
                ]),
                html.Div(f"{row.get('Sector','')[:10]}", style={
                    "fontSize":"9px","color":GOLD,"background":f"{GOLD}12",
                    "border":f"1px solid {GOLD}30","borderRadius":"5px",
                    "padding":"3px 7px","letterSpacing":"0.5px",
                }),
            ]),
            html.Div(fmt_inr(price), style={
                "fontSize":"26px","fontWeight":"700","color":TEXT,
                "fontFamily":"'DM Mono',monospace","letterSpacing":"-0.5px","marginBottom":"8px",
            }),
            html.Div(style={"display":"flex","gap":"8px","alignItems":"center","marginBottom":"12px"}, children=[
                html.Div(f"{'UP' if up else 'DOWN'} {abs(chg):.2f}%", style={
                    "fontSize":"12px","fontWeight":"600",
                    "color": GREEN if up else RED,
                    "background": f"{GREEN}15" if up else f"{RED}15",
                    "border": f"1px solid {GREEN}30" if up else f"1px solid {RED}30",
                    "borderRadius":"6px","padding":"3px 10px",
                }),
                html.Div(f"1Y: {y1:+.1f}%", style={"fontSize":"11px","color":GREEN if y1>=0 else RED}),
            ]),
            html.Div(style={"display":"grid","gridTemplateColumns":"1fr 1fr","gap":"8px","fontSize":"10px"}, children=[
                html.Div([html.Span("RSI  ",style={"color":TEXT3}), html.Span(f"{rsi:.0f}",style={"color":rsi_c,"fontWeight":"700","fontFamily":"'DM Mono',monospace"})]),
                html.Div([html.Span("Vol  ",style={"color":TEXT3}), html.Span(f"{row.get('Volatility_1M_%',0) or 0:.1f}%",style={"color":AMBER,"fontFamily":"'DM Mono',monospace"})]),
            ]),
            html.Div(price_stamp, style={
                "marginTop":"10px","fontSize":"9px","letterSpacing":"0.4px",
                "color": GREEN if price_source == "LIVE" else TEXT3,
                "fontFamily":"'DM Mono',monospace",
            }),
        ], style={
            "background": f"linear-gradient(135deg,{BG3} 0%,{BG2} 100%)",
            "border": f"1px solid {BORDER}",
            "borderRadius": "16px", "padding": "18px",
            "flex":"1","minWidth":"180px","position":"relative","overflow":"hidden",
            "transition":"transform 0.2s,box-shadow 0.2s",
        }))

    # ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Price Chart with Volume ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬
    pf = make_subplots(rows=2,cols=1,shared_xaxes=True,
        row_heights=[0.75,0.25],vertical_spacing=0.02)
    for i,t in enumerate(tickers):
        sub = df[df["Ticker"]==t].sort_values("Date")
        c = COLORS[i % len(COLORS)]
        if ctype=="candle":
            pf.add_trace(go.Candlestick(x=sub["Date"],open=sub["Open"],high=sub["High"],
                low=sub["Low"],close=sub["Close"],name=t,
                increasing_line_color=GREEN,decreasing_line_color=RED,
                increasing_fillcolor=f"{GREEN}80",decreasing_fillcolor=f"{RED}80"),row=1,col=1)
        elif ctype=="area":
            pf.add_trace(go.Scatter(x=sub["Date"],y=sub["Close"],name=t,
                fill="tozeroy",line=dict(color=c,width=2),
                fillcolor=f"rgba({int(c[1:3],16)},{int(c[3:5],16)},{int(c[5:7],16)},0.08)"),row=1,col=1)
        else:
            pf.add_trace(go.Scatter(x=sub["Date"],y=sub["Close"],name=t,
                line=dict(color=c,width=2.5),
                hovertemplate=f"<b>{t}</b><br>%{{x|%d %b %Y}}<br>{fmt_inr(0).replace('0.00','')}%{{y:,.0f}}<extra></extra>"),row=1,col=1)
        vc = [GREEN if r>=0 else RED for r in sub["Daily_Return_%"].fillna(0)]
        pf.add_trace(go.Bar(x=sub["Date"],y=sub["Volume"],name=f"{t} Vol",
            marker_color=vc,opacity=0.45,showlegend=False),row=2,col=1)
    pf.update_layout(**gl(height=480,title="",yaxis_type=scale,
        xaxis_rangeslider_visible=False,
        yaxis=dict(gridcolor=DIM,color=TEXT3,tickprefix="INR ",tickformat=",.0f"),
        yaxis2=dict(gridcolor=DIM,color=TEXT3),
        xaxis2=dict(gridcolor=DIM,color=TEXT3)))

    # ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Cumulative Return ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬
    cf = go.Figure()
    for i,t in enumerate(tickers):
        sub = df[df["Ticker"]==t].copy().sort_values("Date")
        if not len(sub): continue
        sub["cum"] = (sub["Close"]/sub["Close"].iloc[0]-1)*100
        cf.add_trace(go.Scatter(x=sub["Date"],y=sub["cum"],name=t,
            line=dict(color=COLORS[i%len(COLORS)],width=2.5),
            hovertemplate=f"<b>{t}</b><br>%{{x|%d %b %Y}}<br>Return: %{{y:+.2f}}%<extra></extra>",
            fill="tozeroy" if len(tickers)==1 else None,
            fillcolor=f"rgba({int(COLORS[0][1:3],16)},{int(COLORS[0][3:5],16)},{int(COLORS[0][5:7],16)},0.06)" if len(tickers)==1 else None))
    cf.add_hline(y=0,line_dash="dot",line_color=DIM,line_width=1.5)
    cf.update_layout(**gl(height=260,title="",
        yaxis=dict(gridcolor=DIM,color=TEXT3,ticksuffix="%")))

    # ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ 1Y Return Bar ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬
    bd = snap.sort_values("Return_1Y_%")
    bf = go.Figure(go.Bar(
        x=bd["Ticker"],y=bd["Return_1Y_%"],
        marker=dict(color=[GREEN if v>=0 else RED for v in bd["Return_1Y_%"]],
            cornerradius=6),
        text=[f"{v:+.1f}%" for v in bd["Return_1Y_%"]],
        textposition="outside",textfont=dict(size=11,color=TEXT2),
        hovertemplate="<b>%{x}</b><br>1Y Return: %{y:+.2f}%<extra></extra>",
    ))
    bf.add_hline(y=0,line_color=DIM,line_width=1)
    bf.update_layout(**gl(height=260,title="",hovermode="x",
        yaxis=dict(gridcolor=DIM,color=TEXT3,ticksuffix="%"),
        bargap=0.35))

    def section_title(t, sub=None):
        return html.Div(style={"marginBottom":"12px"}, children=[
            html.Span(t, style={"fontSize":"15px","fontWeight":"700","color":TEXT,"letterSpacing":"0.3px"}),
            html.Span(f"  {sub}", style={"fontSize":"11px","color":TEXT3,"marginLeft":"8px"}) if sub else "",
        ])

    return html.Div([
        html.Div(kpis,style={"display":"flex","gap":"14px","flexWrap":"wrap","marginBottom":"20px"}),
        card([
            section_title("Price History", f"INR | {ctype.capitalize()} Chart"),
            G(pf),
        ]),
        html.Div(style={"display":"grid","gridTemplateColumns":"1fr 1fr","gap":"16px"},children=[
            card([section_title("Cumulative Return"), G(cf)]),
            card([section_title("1-Year Return"), G(bf)]),
        ]),
    ])


# ÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚Â
#  PAGE 2 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â PRICE & VOLUME
# ÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚Â
def pg_price(df, snap, tickers, ctype, scale):
    t = tickers[0]
    sub = df[df["Ticker"] == t].sort_values("Date").copy()

    if not len(sub):
        return card(html.Div(f"No price data found for {t} in the selected date range.", style={"color": TEXT3}))

    inr_prefix = fmt_inr(0).replace("0.00", "")
    if "Daily_Return_%" not in sub.columns:
        sub["Daily_Return_%"] = sub["Close"].pct_change() * 100
    sub["Daily_Return_%"] = sub["Daily_Return_%"].fillna(0)
    sub["Daily_Change_INR"] = sub["Close"].diff().fillna(0)

    fig = make_subplots(rows=3, cols=1, shared_xaxes=True,
        row_heights=[0.6, 0.22, 0.18], vertical_spacing=0.02)

    if ctype == "candle":
        fig.add_trace(go.Candlestick(x=sub["Date"], open=sub["Open"], high=sub["High"],
            low=sub["Low"], close=sub["Close"], name=t,
            increasing_line_color=GREEN, decreasing_line_color=RED), row=1, col=1)
    else:
        fig.add_trace(go.Scatter(x=sub["Date"], y=sub["Close"], name="Price",
            line=dict(color=TEAL, width=2.5),
            hovertemplate=f"{inr_prefix}%{{y:,.2f}}<extra></extra>"), row=1, col=1)
    for ma, c, d in [("SMA_20", GOLD, "dot"), ("SMA_50", PURPLE, "dot"), ("SMA_200", RED, "dash")]:
        if ma in sub.columns:
            fig.add_trace(go.Scatter(x=sub["Date"], y=sub[ma], name=ma,
                line=dict(color=c, width=1.3, dash=d), opacity=0.85), row=1, col=1)
    if "BB_Upper" in sub.columns:
        fig.add_trace(go.Scatter(x=sub["Date"], y=sub["BB_Upper"], name="BB+",
            line=dict(color=TEXT3, width=0.8, dash="dash"), opacity=0.5), row=1, col=1)
        fig.add_trace(go.Scatter(x=sub["Date"], y=sub["BB_Lower"], name="BB-",
            line=dict(color=TEXT3, width=0.8, dash="dash"), opacity=0.5,
            fill="tonexty", fillcolor="rgba(100,116,139,0.04)"), row=1, col=1)

    vc = [GREEN if r >= 0 else RED for r in sub["Daily_Return_%"]]
    fig.add_trace(go.Bar(x=sub["Date"], y=sub["Volume"], marker_color=vc,
        name="Volume", opacity=0.6), row=2, col=1)
    if "Volume_SMA20" in sub.columns:
        fig.add_trace(go.Scatter(x=sub["Date"], y=sub["Volume_SMA20"],
            line=dict(color=TEAL, width=1.5, dash="dot"), name="Vol MA20"), row=2, col=1)
    ret_c = [GREEN if r >= 0 else RED for r in sub["Daily_Return_%"]]
    fig.add_trace(go.Bar(x=sub["Date"], y=sub["Daily_Return_%"],
        marker_color=ret_c, name="Daily Return %", opacity=0.75), row=3, col=1)
    fig.add_hline(y=0, line_color=DIM, line_width=1, row=3, col=1)

    fig.update_layout(**gl(height=660, title="", yaxis_type=scale,
        xaxis_rangeslider_visible=False,
        yaxis=dict(gridcolor=DIM, color=TEXT3, tickprefix=inr_prefix, tickformat=",.0f"),
        yaxis2=dict(gridcolor=DIM, color=TEXT3),
        yaxis3=dict(gridcolor=DIM, color=TEXT3, ticksuffix="%"),
        xaxis3=dict(gridcolor=DIM, color=TEXT3)))

    # Stats
    yr = sub[sub["Date"] >= sub["Date"].max() - timedelta(days=365)]
    def stat_card(label, value, color=TEAL):
        return html.Div([
            html.Div(label, style={"fontSize":"9px","color":TEXT3,"letterSpacing":"1.5px","textTransform":"uppercase","marginBottom":"5px"}),
            html.Div(value, style={"fontSize":"18px","fontWeight":"700","color":color,"fontFamily":"'DM Mono',monospace"}),
        ], style={"background":BG3,"border":f"1px solid {BORDER}","borderRadius":"10px","padding":"14px","textAlign":"center"})

    stats = html.Div([
        stat_card("52W High", fmt_inr(yr["High"].max()), GREEN),
        stat_card("52W Low", fmt_inr(yr["Low"].min()), RED),
        stat_card("Avg Volume", f"{yr['Volume'].mean()/1e6:.1f}M", BLUE),
        stat_card("Daily Range", f"{yr['Daily_Range_%'].mean():.2f}%", AMBER),
        stat_card("Best Day", f"{yr['Daily_Return_%'].max():+.2f}%", GREEN),
        stat_card("Worst Day", f"{yr['Daily_Return_%'].min():+.2f}%", RED),
        stat_card("Up Days", str((yr["Daily_Return_%"] > 0).sum()), GREEN),
        stat_card("Down Days", str((yr["Daily_Return_%"] < 0).sum()), RED),
    ], style={"display":"grid","gridTemplateColumns":"repeat(8,1fr)","gap":"10px","marginBottom":"16px"})

    # Monthly return timeline (first vs last trading day each month)
    mret = (sub.assign(Year=sub["Date"].dt.year, Month=sub["Date"].dt.month)
              .groupby(["Year", "Month"], as_index=False)
              .agg(Start_Close=("Close", "first"), End_Close=("Close", "last")))
    mret["Return_%"] = (mret["End_Close"] / mret["Start_Close"] - 1) * 100
    mret["Change_INR"] = mret["End_Close"] - mret["Start_Close"]
    mret["YM"] = mret["Year"].astype(str) + "-" + mret["Month"].astype(str).str.zfill(2)

    mf = go.Figure(go.Bar(
        x=mret["YM"], y=mret["Return_%"],
        marker=dict(color=[GREEN if v >= 0 else RED for v in mret["Return_%"]], cornerradius=3),
        customdata=np.column_stack([mret["Change_INR"], mret["Start_Close"], mret["End_Close"]]),
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Monthly Return: %{y:+.2f}%<br>"
            f"Monthly Change: {inr_prefix}%{{customdata[0]:+,.2f}}<br>"
            f"Start: {inr_prefix}%{{customdata[1]:,.2f}}<br>"
            f"End: {inr_prefix}%{{customdata[2]:,.2f}}<extra></extra>"
        )
    ))
    mf.add_hline(y=0, line_color=DIM)
    mf.update_layout(**gl(height=240, title="",
        yaxis=dict(gridcolor=DIM, color=TEXT3, ticksuffix="%"),
        xaxis=dict(gridcolor=DIM, color=TEXT3, tickangle=-45, tickfont_size=9)))

    # Yearly performance
    yret = (sub.assign(Year=sub["Date"].dt.year)
              .groupby("Year", as_index=False)
              .agg(Start_Date=("Date", "min"), End_Date=("Date", "max"),
                   Start_Close=("Close", "first"), End_Close=("Close", "last")))
    yret["Return_%"] = (yret["End_Close"] / yret["Start_Close"] - 1) * 100
    yret["Change_INR"] = yret["End_Close"] - yret["Start_Close"]
    yf = go.Figure(go.Bar(
        x=yret["Year"].astype(str), y=yret["Return_%"],
        marker=dict(color=[GREEN if v >= 0 else RED for v in yret["Return_%"]], cornerradius=5),
        text=[f"{v:+.1f}%" for v in yret["Return_%"]],
        textposition="outside",
        customdata=np.column_stack([
            yret["Change_INR"],
            yret["Start_Close"],
            yret["End_Close"],
            yret["Start_Date"].dt.strftime("%d %b %Y"),
            yret["End_Date"].dt.strftime("%d %b %Y"),
        ]),
        hovertemplate=(
            "<b>%{x}</b><br>"
            "%{customdata[3]} to %{customdata[4]}<br>"
            "Return: %{y:+.2f}%<br>"
            f"Change: {inr_prefix}%{{customdata[0]:+,.2f}}<br>"
            f"Start: {inr_prefix}%{{customdata[1]:,.2f}}<br>"
            f"End: {inr_prefix}%{{customdata[2]:,.2f}}<extra></extra>"
        )
    ))
    yf.add_hline(y=0, line_color=DIM, line_width=1)
    yf.update_layout(**gl(height=280, title="",
        yaxis=dict(gridcolor=DIM, color=TEXT3, ticksuffix="%"),
        xaxis=dict(gridcolor=DIM, color=TEXT3)))

    # Monthly heatmap (year x month)
    months = MONTH_LABELS
    hp = (mret.pivot(index="Year", columns="Month", values="Return_%")
             .reindex(columns=range(1, 13))
             .sort_index(ascending=False))
    zvals = hp.values
    htext = [[("" if pd.isna(v) else f"{v:+.1f}%") for v in row] for row in zvals]
    hm = go.Figure(go.Heatmap(
        z=zvals,
        x=months,
        y=[str(v) for v in hp.index.tolist()],
        colorscale=[[0, RED], [0.5, BG3], [1, GREEN]],
        zmid=0,
        text=htext,
        texttemplate="%{text}",
        textfont_size=9,
        hovertemplate="<b>%{y} %{x}</b><br>Monthly Return: %{z:+.2f}%<extra></extra>",
        colorbar=dict(title=dict(text="Return %", font=dict(color=TEXT3)), tickfont=dict(color=TEXT3))
    ))
    hm.update_layout(**gl(
        height=max(280, len(hp) * 24 + 110),
        title="",
        hovermode="closest",
        xaxis=dict(gridcolor="rgba(0,0,0,0)", color=TEXT3, side="top"),
        yaxis=dict(gridcolor=DIM, color=TEXT3)
    ))

    latest_dt = sub["Date"].max()
    wave_fig, wave_caption = build_month_wave_figure(sub, t, int(latest_dt.year), int(latest_dt.month))

    return html.Div([
        html.Div(style={"display":"flex","justifyContent":"space-between","alignItems":"center","marginBottom":"12px"}, children=[
            html.Div(f"Deep Dive: {t}", style={"fontSize":"16px","fontWeight":"700","color":TEXT}),
            badge(f"First Selected Ticker", BLUE),
        ]),
        stats,
        card([G(fig)]),
        card([html.Div("Monthly Returns", style={"fontSize":"14px","fontWeight":"600","color":TEXT,"marginBottom":"10px"}), G(mf)]),
        html.Div(style={"display":"grid","gridTemplateColumns":"1fr 1fr","gap":"16px"}, children=[
            card([html.Div("Yearly Increase / Decrease", style={"fontSize":"14px","fontWeight":"600","color":TEXT,"marginBottom":"10px"}), G(yf)]),
            card([html.Div("Monthly Return Heatmap (Year x Month)", style={"fontSize":"14px","fontWeight":"600","color":TEXT,"marginBottom":"10px"}),
                  html.Div("Click any month cell to see date-wise wave trend below.", style={"fontSize":"11px","color":TEXT3,"marginBottom":"8px"}),
                  G(hm, gid="price-month-heatmap")]),
        ]),
        card([
            html.Div("Month Drilldown: Date-wise Wave", style={"fontSize":"14px","fontWeight":"600","color":TEXT,"marginBottom":"8px"}),
            html.Div(id="price-month-caption", children=wave_caption, style={"fontSize":"11px","color":TEXT3,"marginBottom":"8px","fontFamily":"'DM Mono',monospace"}),
            G(wave_fig, gid="price-month-wave")
        ]),
    ])

def pg_technicals(df, snap, tickers, ctype, scale):
    t = tickers[0]
    sub = df[df["Ticker"]==t].sort_values("Date")
    latest = sub.iloc[-1] if len(sub) else pd.Series()

    tech = make_subplots(rows=4,cols=1,shared_xaxes=True,
        row_heights=[0.45,0.2,0.2,0.15],vertical_spacing=0.015)

    if ctype=="candle":
        tech.add_trace(go.Candlestick(x=sub["Date"],open=sub["Open"],high=sub["High"],
            low=sub["Low"],close=sub["Close"],name=t,
            increasing_line_color=GREEN,decreasing_line_color=RED),row=1,col=1)
    else:
        tech.add_trace(go.Scatter(x=sub["Date"],y=sub["Close"],name="Price",
            line=dict(color=TEAL,width=2.5)),row=1,col=1)

    for ma,c in [("SMA_20",GOLD),("SMA_50",PURPLE),("SMA_200",RED)]:
        if ma in sub.columns:
            tech.add_trace(go.Scatter(x=sub["Date"],y=sub[ma],name=ma,
                line=dict(color=c,width=1.2,dash="dot"),opacity=0.9),row=1,col=1)
    if "BB_Upper" in sub.columns:
        tech.add_trace(go.Scatter(x=sub["Date"],y=sub["BB_Upper"],name="BB Upper",
            line=dict(color=TEXT3,width=0.8,dash="dash"),opacity=0.5),row=1,col=1)
        tech.add_trace(go.Scatter(x=sub["Date"],y=sub["BB_Lower"],name="BB Lower",
            line=dict(color=TEXT3,width=0.8,dash="dash"),opacity=0.5,
            fill="tonexty",fillcolor="rgba(100,116,139,0.05)"),row=1,col=1)

    if "RSI_14" in sub.columns:
        tech.add_trace(go.Scatter(x=sub["Date"],y=sub["RSI_14"],name="RSI",
            line=dict(color=AMBER,width=2),
            hovertemplate="RSI: %{y:.1f}<extra></extra>"),row=2,col=1)
        tech.add_hline(y=70,line_dash="dash",line_color=RED,  line_width=1,row=2,col=1)
        tech.add_hline(y=30,line_dash="dash",line_color=GREEN,line_width=1,row=2,col=1)
        tech.add_hrect(y0=70,y1=100,fillcolor=RED,  opacity=0.05,row=2,col=1)
        tech.add_hrect(y0=0, y1=30, fillcolor=GREEN,opacity=0.05,row=2,col=1)

    if all(c in sub.columns for c in ["MACD","MACD_Signal","MACD_Hist"]):
        tech.add_trace(go.Scatter(x=sub["Date"],y=sub["MACD"],name="MACD",
            line=dict(color=TEAL,width=2)),row=3,col=1)
        tech.add_trace(go.Scatter(x=sub["Date"],y=sub["MACD_Signal"],name="Signal",
            line=dict(color=GOLD,width=1.5)),row=3,col=1)
        hc=[GREEN if v>=0 else RED for v in sub["MACD_Hist"].fillna(0)]
        tech.add_trace(go.Bar(x=sub["Date"],y=sub["MACD_Hist"],marker_color=hc,
            name="Hist",opacity=0.7),row=3,col=1)

    if "BB_Width_%" in sub.columns:
        tech.add_trace(go.Scatter(x=sub["Date"],y=sub["BB_Width_%"],name="BB Width%",
            line=dict(color=PINK,width=1.5),fill="tozeroy",
            fillcolor="rgba(255,114,184,0.06)"),row=4,col=1)

    tech.update_layout(**gl(height=700,title="",yaxis_type=scale,
        xaxis_rangeslider_visible=False,
        yaxis=dict(gridcolor=DIM,color=TEXT3,tickprefix="INR ",tickformat=",.0f"),
        yaxis2=dict(gridcolor=DIM,color=TEXT3,range=[0,100]),
        yaxis3=dict(gridcolor=DIM,color=TEXT3),
        yaxis4=dict(gridcolor=DIM,color=TEXT3),
        xaxis4=dict(gridcolor=DIM,color=TEXT3)))

    # Signal cards
    def sig_card(indicator, value, signal, sig_color, icon=""):
        return html.Div([
            html.Div(indicator,style={"fontSize":"9px","color":TEXT3,"letterSpacing":"2px","textTransform":"uppercase","marginBottom":"6px"}),
            html.Div(value,style={"fontSize":"20px","fontWeight":"700","color":TEXT,"fontFamily":"'DM Mono',monospace","marginBottom":"4px"}),
            html.Div(style={"display":"flex","alignItems":"center","gap":"6px"},children=[
                html.Div(f"{icon} {signal}",style={
                    "fontSize":"10px","fontWeight":"600","color":sig_color,
                    "background":f"{sig_color}15","border":f"1px solid {sig_color}30",
                    "borderRadius":"5px","padding":"3px 9px",
                }),
            ]),
        ],style={
            "background":f"linear-gradient(135deg,{BG3},{BG2})",
            "border":f"1px solid {sig_color}25",
            "borderRadius":"12px","padding":"16px",
            "flex":"1","minWidth":"130px",
            "boxShadow":f"0 4px 20px {sig_color}12",
        })

    rsi = latest.get("RSI_14",50) or 50
    rsi_s = ("OVERBOUGHT","UP",RED) if rsi>70 else (("OVERSOLD","DOWN",GREEN) if rsi<30 else ("NEUTRAL","-",AMBER))
    bb  = latest.get("BB_Position",0.5) or 0.5
    bb_s = ("UPPER BAND","UP",RED) if bb>0.8 else (("LOWER BAND","DOWN",GREEN) if bb<0.2 else ("MID BAND","-",AMBER))
    macd_v = latest.get("MACD",0) or 0; sig_v = latest.get("MACD_Signal",0) or 0
    macd_s = ("BULLISH","UP",GREEN) if macd_v>sig_v else ("BEARISH","DOWN",RED)
    a200 = latest.get("Above_SMA200",0)
    sma_s = ("ABOVE SMA200","UP",GREEN) if a200 else ("BELOW SMA200","DOWN",RED)

    signals = html.Div([
        sig_card("RSI (14)",   f"{rsi:.1f}",         rsi_s[0],  rsi_s[2],  rsi_s[1]),
        sig_card("BB Position",f"{bb:.2f}",           bb_s[0],   bb_s[2],   bb_s[1]),
        sig_card("MACD",       f"{macd_v:.3f}",       macd_s[0], macd_s[2], macd_s[1]),
        sig_card("vs SMA 200", "ABOVE" if a200 else "BELOW", sma_s[0], sma_s[2], sma_s[1]),
        sig_card("SMA 20",     fmt_inr(latest.get("SMA_20",0)), "Moving Avg", TEAL, ""),
        sig_card("SMA 50",     fmt_inr(latest.get("SMA_50",0)), "Moving Avg", PURPLE, ""),
        sig_card("SMA 200",    fmt_inr(latest.get("SMA_200",0)),"Long Term",  RED, ""),
        sig_card("Vol Ratio",  f"{latest.get('Volume_Ratio',1) or 1:.2f}x",
                 "HIGH VOL" if (latest.get("Volume_Ratio",1) or 1)>1.5 else "NORMAL", AMBER, ""),
    ],style={"display":"flex","gap":"10px","flexWrap":"wrap","marginBottom":"16px"})

    return html.Div([
        html.Div(style={"display":"flex","justifyContent":"space-between","alignItems":"center","marginBottom":"12px"},children=[
            html.Div(f"Technical Analysis: {t}",style={"fontSize":"16px","fontWeight":"700","color":TEXT}),
            badge("Live Signals", GREEN),
        ]),
        signals,
        card([G(tech)]),
    ])


# ÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚Â
#  PAGE 4 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â COMPARE
# ÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚Â
def pg_compare(df, snap, tickers, ctype, scale):
    nf = go.Figure()
    for i,t in enumerate(tickers):
        sub = df[df["Ticker"]==t].sort_values("Date")
        if not len(sub): continue
        sub["n"] = sub["Close"]/sub["Close"].iloc[0]*100
        nf.add_trace(go.Scatter(x=sub["Date"],y=sub["n"],name=t,
            line=dict(color=COLORS[i%len(COLORS)],width=2.5),
            hovertemplate=f"<b>{t}</b><br>%{{x|%d %b %Y}}<br>Rebased: %{{y:.1f}}<extra></extra>"))
    nf.add_hline(y=100,line_dash="dot",line_color=DIM,line_width=1.5)
    nf.update_layout(**gl(height=340,title="",yaxis_type=scale,
        yaxis=dict(gridcolor=DIM,color=TEXT3)))

    piv = df.pivot_table(index="Date",columns="Ticker",values="Daily_Return_%")
    corr = piv.corr().round(3)
    cvals = corr.values
    cf2 = go.Figure(go.Heatmap(
        z=cvals,x=corr.columns.tolist(),y=corr.index.tolist(),
        colorscale=[[0,RED],[0.5,BG3],[1,GREEN]],
        zmin=-1,zmax=1,zmid=0,
        text=np.round(cvals,2),texttemplate="<b>%{text}</b>",textfont_size=12,
        hovertemplate="<b>%{x} vs %{y}</b><br>Correlation: %{z:.3f}<extra></extra>",
        colorbar=dict(tickcolor=TEXT3,tickfont_color=TEXT3,tickfont_size=10,
                      title=dict(text="Corr",font_color=TEXT3))))
    cf2.update_layout(**gl(height=340,title="",hovermode="closest",
        xaxis=dict(gridcolor="rgba(0,0,0,0)",color=TEXT3),
        yaxis=dict(gridcolor="rgba(0,0,0,0)",color=TEXT3)))

    periods={"1W":"Return_1W_%","1M":"Return_1M_%","3M":"Return_3M_%","1Y":"Return_1Y_%"}
    av={k:v for k,v in periods.items() if v in snapshot.columns}
    bar_data = snap[snap["Ticker"].isin(tickers)]
    mf = go.Figure()
    for k,col in av.items():
        mf.add_trace(go.Bar(name=k,x=bar_data["Ticker"],y=bar_data[col],
            text=[f"{v:+.1f}%" for v in bar_data[col].fillna(0)],
            textposition="outside",
            hovertemplate=f"<b>%{{x}}</b><br>{k}: %{{y:+.2f}}%<extra></extra>"))
    mf.add_hline(y=0,line_color=DIM)
    mf.update_layout(**gl(height=300,title="",barmode="group",
        yaxis=dict(gridcolor=DIM,color=TEXT3,ticksuffix="%"),
        bargap=0.2,bargroupgap=0.05))

    return html.Div([
        html.Div(style={"display":"grid","gridTemplateColumns":"1fr 1fr","gap":"16px"},children=[
            card([html.Div("Rebased Price Comparison (Base = 100)",style={"fontSize":"14px","fontWeight":"600","color":TEXT,"marginBottom":"10px"}), G(nf)]),
            card([html.Div("Return Correlation Matrix",style={"fontSize":"14px","fontWeight":"600","color":TEXT,"marginBottom":"10px"}), G(cf2)]),
        ]),
        card([html.Div("Multi-Period Return Comparison",style={"fontSize":"14px","fontWeight":"600","color":TEXT,"marginBottom":"10px"}), G(mf)]),
    ])


# ÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚Â
#  PAGE 5 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â SECTOR
# ÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚Â
def pg_sector(df, snap, tickers, ctype, scale):
    ap = prices.copy(); ap["Year"] = ap["Date"].dt.year
    annual = ap.groupby(["Sector","Year"])["Daily_Return_%"].sum().reset_index().dropna()

    hf = go.Figure(go.Heatmap(
        z=annual.pivot_table(index="Sector",columns="Year",values="Daily_Return_%").values,
        x=annual.pivot_table(index="Sector",columns="Year",values="Daily_Return_%").columns.tolist(),
        y=annual.pivot_table(index="Sector",columns="Year",values="Daily_Return_%").index.tolist(),
        colorscale=[[0,RED],[0.45,BG3],[1,GREEN]],zmid=0,
        colorbar=dict(tickcolor=TEXT3,tickfont_color=TEXT3),
        hovertemplate="<b>%{y}</b><br>%{x}<br>Return: %{z:.1f}%<extra></extra>"))
    hf.update_layout(**gl(height=320,title="",hovermode="closest",
        xaxis=dict(gridcolor="rgba(0,0,0,0)",color=TEXT3),
        yaxis=dict(gridcolor="rgba(0,0,0,0)",color=TEXT3)))

    s2 = snapshot.copy(); s2["abs_r"]=s2["Return_1Y_%"].abs().clip(0.5); s2=s2.dropna(subset=["Sector"])
    tf = px.treemap(s2,path=["Sector","Ticker"],values="abs_r",
        color="Return_1Y_%",color_continuous_scale=[[0,RED],[0.5,BG3],[1,GREEN]],
        color_continuous_midpoint=0,custom_data=["Return_1Y_%","Company"])
    tf.update_traces(textinfo="label+percent parent",
        hovertemplate="<b>%{label}</b><br>1Y: %{customdata[0]:.1f}%<extra></extra>",
        marker_line_width=0.5,marker_line_color=BG0)
    tf.update_layout(**gl(height=380,title="",hovermode="closest"))

    ytd = ap[ap["Date"]>=f"{datetime.now().year}-01-01"]
    yr = ytd.groupby("Sector")["Daily_Return_%"].sum().reset_index().dropna().sort_values("Daily_Return_%")
    yf = go.Figure(go.Bar(x=yr["Daily_Return_%"],y=yr["Sector"],orientation="h",
        marker=dict(color=[GREEN if v>=0 else RED for v in yr["Daily_Return_%"]],cornerradius=4),
        text=[f"{v:+.1f}%" for v in yr["Daily_Return_%"]],textposition="outside",
        hovertemplate="<b>%{y}</b><br>YTD: %{x:+.1f}%<extra></extra>"))
    yf.update_layout(**gl(height=300,title="",hovermode="y unified",
        xaxis=dict(gridcolor=DIM,color=TEXT3,ticksuffix="%"),
        yaxis=dict(gridcolor=DIM,color=TEXT3)))

    return html.Div([
        html.Div(style={"display":"grid","gridTemplateColumns":"1fr 1fr","gap":"16px"},children=[
            card([html.Div("Annual Return Heatmap by Sector",style={"fontSize":"14px","fontWeight":"600","color":TEXT,"marginBottom":"10px"}), G(hf)]),
            card([html.Div("YTD Return by Sector",style={"fontSize":"14px","fontWeight":"600","color":TEXT,"marginBottom":"10px"}), G(yf)]),
        ]),
        card([html.Div("1-Year Return Treemap",style={"fontSize":"14px","fontWeight":"600","color":TEXT,"marginBottom":"10px"}), G(tf)]),
    ])


# ÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚Â
#  PAGE 6 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â RISK
# ÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚Â
def pg_risk(df, snap, tickers, ctype, scale):
    vf = go.Figure()
    for i,t in enumerate(tickers):
        sub = df[df["Ticker"]==t]
        if "Volatility_1M_%" in sub.columns:
            vf.add_trace(go.Scatter(x=sub["Date"],y=sub["Volatility_1M_%"],name=t,
                line=dict(color=COLORS[i%len(COLORS)],width=2),
                hovertemplate=f"<b>{t}</b><br>%{{x|%d %b %Y}}<br>Vol: %{{y:.2f}}%<extra></extra>",
                fill="tozeroy" if i==0 and len(tickers)==1 else None))
    vf.update_layout(**gl(height=280,title="",
        yaxis=dict(gridcolor=DIM,color=TEXT3,ticksuffix="%")))

    df2 = go.Figure()
    for i,t in enumerate(tickers):
        sub = df[df["Ticker"]==t].sort_values("Date")
        pk = sub["Close"].cummax(); dd = (sub["Close"]-pk)/pk*100
        df2.add_trace(go.Scatter(x=sub["Date"],y=dd,name=t,
            fill="tozeroy",fillcolor="rgba(255,77,109,0.06)",
            line=dict(color=COLORS[i%len(COLORS)],width=2),
            hovertemplate=f"<b>{t}</b><br>%{{x|%d %b %Y}}<br>Drawdown: %{{y:.2f}}%<extra></extra>"))
    df2.add_hline(y=0,line_color=DIM,line_width=1)
    df2.update_layout(**gl(height=260,title="",
        yaxis=dict(gridcolor=DIM,color=TEXT3,ticksuffix="%")))

    mets=[]
    for t in tickers:
        sub=df[df["Ticker"]==t]
        if len(sub)<30: continue
        ar=sub["Daily_Return_%"].mean()*252; av=sub["Daily_Return_%"].std()*np.sqrt(252)
        sh=ar/av if av>0 else 0; md=((sub["Close"]/sub["Close"].cummax()-1)*100).min()
        mets.append({"Ticker":t,"Return":round(ar,2),"Vol":round(av,2),"Sharpe":round(sh,2),"MaxDD":round(md,2)})
    mdf=pd.DataFrame(mets)

    sf=go.Figure()
    if len(mdf):
        sf.add_trace(go.Scatter(x=mdf["Vol"],y=mdf["Return"],mode="markers+text",
            text=mdf["Ticker"],textposition="top center",
            marker=dict(size=mdf["Sharpe"].clip(0)*10+12,
                color=[GREEN if v>0 else RED for v in mdf["Return"]],
                opacity=0.85,line=dict(width=2,color=BG2),
                symbol="circle"),
            hovertemplate="<b>%{text}</b><br>Return: %{y:+.2f}%<br>Vol: %{x:.2f}%<extra></extra>"))
    sf.add_hline(y=0,line_dash="dot",line_color=DIM)
    sf.update_layout(**gl(height=300,title="",hovermode="closest",showlegend=False,
        xaxis=dict(gridcolor=DIM,color=TEXT3,title="Volatility %",ticksuffix="%"),
        yaxis=dict(gridcolor=DIM,color=TEXT3,title="Annual Return %",ticksuffix="%")))

    hf=go.Figure()
    for i,t in enumerate(tickers):
        sub=df[df["Ticker"]==t]["Daily_Return_%"].dropna()
        hf.add_trace(go.Histogram(x=sub,name=t,nbinsx=80,opacity=0.6,
            marker_color=COLORS[i%len(COLORS)],
            hovertemplate=f"<b>{t}</b><br>%{{x:.2f}}%: %{{y}}<extra></extra>"))
    hf.add_vline(x=0,line_dash="dot",line_color=DIM)
    hf.update_layout(**gl(height=260,title="",barmode="overlay",
        xaxis=dict(gridcolor=DIM,color=TEXT3,ticksuffix="%"),
        yaxis=dict(gridcolor=DIM,color=TEXT3)))

    if len(mdf):
        tf=go.Figure(go.Table(
            columnwidth=[60,80,80,70,80],
            header=dict(values=["<b>Ticker</b>","<b>Ann. Return</b>","<b>Volatility</b>","<b>Sharpe</b>","<b>Max Drawdown</b>"],
                fill_color=DIM,font=dict(color=GOLD,size=11,family="'DM Mono',monospace"),align="center",height=38,line_color=BG0),
            cells=dict(
                values=[mdf["Ticker"],mdf["Return"].map(lambda x:f"{x:+.2f}%"),
                        mdf["Vol"].map(lambda x:f"{x:.2f}%"),mdf["Sharpe"].map(lambda x:f"{x:.2f}"),
                        mdf["MaxDD"].map(lambda x:f"{x:.2f}%")],
                fill_color=[[BG3 if i%2==0 else BG2 for i in range(len(mdf))]],
                font=dict(color=[TEXT,[GREEN if v>0 else RED for v in mdf["Return"]],TEXT,
                    [GREEN if v>1 else (AMBER if v>0 else RED) for v in mdf["Sharpe"]],[RED]*len(mdf)],
                    size=12,family="'DM Mono',monospace"),
                align="center",height=34,line_color=BG0)
        ))
        tf.update_layout(**gl(height=max(160,len(mdf)*36+90),title=""))
        tbl_s = card([html.Div("Risk Metrics",style={"fontSize":"14px","fontWeight":"600","color":TEXT,"marginBottom":"10px"}),G(tf)])
    else: tbl_s=html.Div()

    return html.Div([
        html.Div(style={"display":"grid","gridTemplateColumns":"1fr 1fr","gap":"16px"},children=[
            card([html.Div("Rolling Volatility (1M Annualised)",style={"fontSize":"14px","fontWeight":"600","color":TEXT,"marginBottom":"10px"}),G(vf)]),
            card([html.Div("Drawdown from Peak",style={"fontSize":"14px","fontWeight":"600","color":TEXT,"marginBottom":"10px"}),G(df2)]),
        ]),
        html.Div(style={"display":"grid","gridTemplateColumns":"1fr 1fr","gap":"16px"},children=[
            card([html.Div("Risk vs Return (Bubble = Sharpe)",style={"fontSize":"14px","fontWeight":"600","color":TEXT,"marginBottom":"10px"}),G(sf)]),
            card([html.Div("Return Distribution",style={"fontSize":"14px","fontWeight":"600","color":TEXT,"marginBottom":"10px"}),G(hf)]),
        ]),
        tbl_s,
    ])


# ÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚Â
#  PAGE 7 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â SCREENER
# ÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚Â
def pg_screener(df, snap, tickers, ctype, scale):
    all_s = snapshot.copy()
    all_s["Close_INR"] = all_s["Close"]

    def fmt_cell(col, val):
        if pd.isna(val): return "-"
        if col == "Close_INR": return fmt_inr(val)
        if col in ["Daily_Return_%","Return_1M_%","Return_1Y_%"]: return f"{val:+.2f}%"
        if col == "RSI_14": return f"{val:.1f}"
        if col == "BB_Position": return f"{val:.2f}"
        if col == "Volatility_1M_%": return f"{val:.1f}%"
        if col == "Above_SMA200": return "YES" if val==1 else "NO"
        return str(val)

    disp_cols = ["Ticker","Company","Sector","Close_INR","Daily_Return_%",
                 "Return_1M_%","Return_1Y_%","RSI_14","Volatility_1M_%","BB_Position","Above_SMA200"]
    disp_cols = [c for c in disp_cols if c in all_s.columns]
    hdrs = {"Close_INR":"Price (INR)","Daily_Return_%":"Day %","Return_1M_%":"1M %",
            "Return_1Y_%":"1Y %","RSI_14":"RSI","Volatility_1M_%":"Vol%",
            "BB_Position":"BB Pos","Above_SMA200":">SMA200"}

    rows = all_s[disp_cols]
    cell_vals = [[fmt_cell(c, v) for v in rows[c]] for c in disp_cols]

    def ccol(col, vals):
        if col in ["Daily_Return_%","Return_1M_%","Return_1Y_%"]:
            return [GREEN if "+" in str(v) else (RED if "-" in str(v) else TEXT3) for v in vals]
        if col == "Above_SMA200": return [GREEN if "YES" in str(v) else RED for v in vals]
        return [TEXT]*len(vals)

    tf = go.Figure(go.Table(
        header=dict(
            values=[f"<b>{hdrs.get(c,c)}</b>" for c in disp_cols],
            fill_color=DIM, font=dict(color=GOLD,size=11,family="'DM Mono',monospace"),
            align="left", height=40, line_color=BG0),
        cells=dict(
            values=cell_vals,
            fill_color=[[BG3 if i%2==0 else BG2 for i in range(len(rows))]],
            font=dict(color=[ccol(c, cell_vals[i]) for i,c in enumerate(disp_cols)],
                size=11,family="'DM Mono',monospace"),
            align="left", height=34, line_color=BG0)
    ))
    tf.update_layout(**gl(height=max(400,len(rows)*36+90),title=""))

    rsi_d = all_s[["Ticker","RSI_14"]].dropna().sort_values("RSI_14")
    rf = go.Figure(go.Bar(x=rsi_d["Ticker"],y=rsi_d["RSI_14"],
        marker=dict(color=[RED if v>70 else (GREEN if v<30 else TEAL) for v in rsi_d["RSI_14"]],cornerradius=4),
        text=[f"{v:.0f}" for v in rsi_d["RSI_14"]],textposition="outside",
        hovertemplate="<b>%{x}</b><br>RSI: %{y:.1f}<extra></extra>"))
    rf.add_hline(y=70,line_dash="dash",line_color=RED,line_width=1.5,
        annotation_text="Overbought 70",annotation_font_color=RED)
    rf.add_hline(y=30,line_dash="dash",line_color=GREEN,line_width=1.5,
        annotation_text="Oversold 30",annotation_font_color=GREEN)
    rf.add_hrect(y0=70,y1=100,fillcolor=RED,opacity=0.05)
    rf.add_hrect(y0=0,y1=30,fillcolor=GREEN,opacity=0.05)
    rf.update_layout(**gl(height=280,title="",yaxis=dict(gridcolor=DIM,color=TEXT3,range=[0,100])))

    return html.Div([
        card([html.Div(f"Stock Screener - {len(rows)} Stocks",style={"fontSize":"14px","fontWeight":"600","color":TEXT,"marginBottom":"10px"}),G(tf)]),
        card([html.Div("RSI Signal Overview",style={"fontSize":"14px","fontWeight":"600","color":TEXT,"marginBottom":"10px"}),G(rf)]),
    ])


# ÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚Â
#  PAGE 8 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â HEATMAP
# ÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚Â
def pg_heatmap(df, snap, tickers, ctype, scale):
    figs = []

    for t in tickers:
        sub = df[df["Ticker"] == t].copy().sort_values("Date")

        if sub.empty:
            hm = go.Figure()
            hm.update_layout(**gl(height=240, title="", hovermode="closest",
                xaxis=dict(gridcolor="rgba(0,0,0,0)", color=TEXT3, side="top"),
                yaxis=dict(gridcolor=DIM, color=TEXT3, autorange="reversed")))
            hm.add_annotation(text="No data in selected range", showarrow=False,
                font=dict(color=TEXT3, size=11))
            init_wave, init_caption = build_month_wave_figure(pd.DataFrame(), t)
            init_table = build_month_daily_table_figure(pd.DataFrame(), t)
        else:
            sub["Year"] = sub["Date"].dt.year
            sub["Month"] = sub["Date"].dt.month
            mret = (sub.groupby(["Year", "Month"], as_index=False)
                      .agg(Start_Close=("Close", "first"), End_Close=("Close", "last")))
            mret["Return_%"] = (mret["End_Close"] / mret["Start_Close"] - 1) * 100

            piv = (mret.pivot(index="Year", columns="Month", values="Return_%")
                     .reindex(columns=range(1, 13))
                     .sort_index(ascending=False))
            zvals = piv.values
            cell_text = [[("" if pd.isna(v) else f"{v:+.1f}%") for v in row] for row in zvals]
            hover_vals = [[("No data" if pd.isna(v) else f"{v:+.2f}%") for v in row] for row in zvals]

            hm = go.Figure(go.Heatmap(
                z=zvals,
                x=MONTH_LABELS,
                y=[str(v) for v in piv.index.tolist()],
                colorscale=[[0, RED], [0.45, BG3], [1, GREEN]],
                zmid=0,
                text=cell_text,
                texttemplate="%{text}",
                textfont_size=9,
                customdata=hover_vals,
                hovertemplate=f"<b>{t}</b><br>%{{y}} %{{x}}<br>Return: %{{customdata}}<extra></extra>",
                hoverongaps=False,
                colorbar=dict(tickcolor=TEXT3, tickfont_color=TEXT3, tickfont_size=9)
            ))
            hm.update_layout(**gl(height=max(240, len(piv) * 26 + 80), title="", hovermode="closest",
                xaxis=dict(gridcolor="rgba(0,0,0,0)", color=TEXT3, side="top"),
                yaxis=dict(gridcolor=DIM, color=TEXT3, autorange="reversed")))

            latest_dt = sub["Date"].max()
            init_wave, init_caption = build_month_wave_figure(sub, t, int(latest_dt.year), int(latest_dt.month))
            init_table = build_month_daily_table_figure(sub, t, int(latest_dt.year), int(latest_dt.month))

        figs.append(card([
            html.Div(f"{t} - Monthly Return Heatmap", style={"fontSize":"14px","fontWeight":"600","color":TEXT,"marginBottom":"10px"}),
            html.Div("Click a cell to load date-wise data for that month.", style={"fontSize":"11px","color":TEXT3,"marginBottom":"8px"}),
            G(hm, gid={"type": "heatmap-month", "ticker": t}),
            html.Div("Selected Month: Date-wise Wave", style={"fontSize":"13px","fontWeight":"600","color":TEXT,"marginTop":"12px","marginBottom":"6px"}),
            html.Div(id={"type":"heatmap-month-detail-caption","ticker":t}, children=init_caption,
                style={"fontSize":"11px","color":TEXT3,"marginBottom":"8px","fontFamily":"'DM Mono',monospace"}),
            G(init_wave, gid={"type":"heatmap-month-detail-wave","ticker":t}),
            html.Div("Selected Month: Date-wise Data", style={"fontSize":"13px","fontWeight":"600","color":TEXT,"marginTop":"10px","marginBottom":"6px"}),
            G(init_table, gid={"type":"heatmap-month-detail-table","ticker":t}),
        ]))

    wf = go.Figure()
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    for i, t in enumerate(tickers):
        sub = df[df["Ticker"] == t].copy()
        sub["DOW"] = sub["Date"].dt.day_name()
        wd = sub.groupby("DOW")["Daily_Return_%"].mean().reindex(days)
        wf.add_trace(go.Bar(name=t, x=days, y=wd.values,
            marker=dict(color=COLORS[i % len(COLORS)], cornerradius=4), opacity=0.85,
            hovertemplate=f"<b>{t}</b><br>%{{x}}<br>Avg: %{{y:+.3f}}%<extra></extra>"))
    wf.add_hline(y=0, line_color=DIM)
    wf.update_layout(**gl(height=260, title="", barmode="group",
        yaxis=dict(gridcolor=DIM, color=TEXT3, ticksuffix="%")))

    return html.Div([
        *figs,
        card([html.Div("Average Return by Day of Week", style={"fontSize":"14px","fontWeight":"600","color":TEXT,"marginBottom":"10px"}), G(wf)]),
    ])


# ÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚Â
#  RUN
# ÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚ÂÃƒÂ¢Ã¢â‚¬Â¢Ã‚Â
if __name__=="__main__":
    print("\n"+"="*56)
    print("  STOCK INTELLIGENCE DASHBOARD")
    print("  http://localhost:8050")
    print("  Prices in Indian Rupees (INR)")
    print("  Ctrl+C to stop")
    print("="*56+"\n")
    app.run(debug=False, port=8050, host="0.0.0.0")









