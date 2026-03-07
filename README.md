# ðŸ“ˆ Stock Analysis Dashboard â€” Setup Guide

## What's Included

| File | Purpose |
|------|---------|
| `fetch_clean_stocks.py` | Main pipeline: fetch â†’ clean â†’ engineer features â†’ export |
| `run_daily.bat` | Windows auto-scheduler |
| `setup_cron.sh` | Mac/Linux auto-scheduler |
| `powerbi_data/` | â† **Power BI reads from this folder** |

---

## âš™ï¸ Step 1 â€” Install Requirements

```bash
pip install yfinance pandas numpy openpyxl ta schedule
```

---

## â–¶ï¸ Step 2 â€” Run the Pipeline (First Time)

```bash
python fetch_clean_stocks.py
```

This will:
- Download data for **India-only NSE stocks from 2000 to today**
- Clean and validate all data
- Add **30+ technical indicators**
- Export 5 CSV files to `powerbi_data/`

Expected runtime: **3â€“7 minutes** (first run, downloading ~24 years of data)

---

## ðŸ“Š Step 3 â€” Connect Power BI

### Connect to the data folder:

1. Open **Power BI Desktop**
2. **Home â†’ Get Data â†’ Text/CSV**
3. Navigate to your `powerbi_data/` folder
4. Load these files:

| CSV File | Table Name in Power BI |
|----------|----------------------|
| `fact_stock_prices.csv` | `StockPrices` |
| `dim_date.csv` | `Calendar` |
| `dim_company.csv` | `Company` |
| `agg_sector_monthly.csv` | `SectorMonthly` |
| `snapshot_latest.csv` | `LatestSnapshot` |

### Set Relationships:
- `StockPrices[Date]` â†’ `Calendar[Date]` (Many to One)
- `StockPrices[Ticker]` â†’ `Company[Ticker]` (Many to One)

---

## ðŸŽ¨ Step 4 â€” Build Dashboard Pages

### Suggested Pages:

#### ðŸ“Œ Page 1 â€” Executive Summary
- **KPI Cards** (from `LatestSnapshot`):
  - Current Price, Daily Change %, YTD Return
  - RSI Signal, Volatility
- **Line Chart**: Close price over time (slicer by Ticker)
- **Bar Chart**: 1Y Return % by Company

#### ðŸ“Œ Page 2 â€” Technical Analysis
- **Candlestick / Line**: OHLC with SMA20, SMA50, SMA200
- **Area Chart**: Bollinger Bands (BB_Upper, BB_Middle, BB_Lower)
- **Line**: RSI_14 with 30/70 reference lines
- **Bar**: MACD Histogram

#### ðŸ“Œ Page 3 â€” Sector & Comparison
- **Clustered Bar**: Sector returns by year
- **Heat Map Matrix**: Monthly returns (Year Ã— Month)
- **Scatter**: Volatility vs Return (risk/reward)
- **Waterfall**: Cumulative return by stock

#### ðŸ“Œ Page 4 â€” Volume & Market Activity
- **Bar**: Daily Volume vs Volume_SMA20
- **Line**: Volume_Ratio over time
- **Highlight**: High_Volume_Day events

---

## ðŸ”„ Step 5 â€” Auto-Refresh Daily

### Windows (Task Scheduler):

```
1. Open Task Scheduler
2. Create Basic Task â†’ Name: "Stock Data Refresh"
3. Trigger: Daily at 7:00 AM (weekdays)
4. Action: Start a program â†’ run_daily.bat
5. Finish â†’ Enable
```

### Mac / Linux (Cron):

```bash
chmod +x setup_cron.sh
./setup_cron.sh
```

This installs a cron job that runs every weekday at 7:00 AM.

### Power BI Auto-Refresh:
- In Power BI Desktop: **Home â†’ Refresh** (manual)
- For **Power BI Service** (cloud):
  - Publish report to Power BI Service
  - Set **Scheduled Refresh** to Daily
  - Use a **gateway** to connect to your local CSV folder

---

## ðŸ“ Output Files Explained

### `fact_stock_prices.csv` â€” Main Table
| Column | Description |
|--------|-------------|
| Date, Open, High, Low, Close, Volume | OHLCV data |
| Daily_Return_% | Day over day % change |
| Return_1W/1M/3M/1Y_% | Rolling period returns |
| Cumulative_Return_% | Total return since 2000 |
| SMA_20/50/100/200 | Simple moving averages |
| EMA_20/50/100/200 | Exponential moving averages |
| RSI_14, RSI_Signal | Momentum indicator |
| MACD, MACD_Signal, MACD_Hist | Trend indicator |
| BB_Upper/Middle/Lower/Width/Position | Bollinger Bands |
| Volatility_1M/3M_% | Annualised rolling volatility |
| Volume_SMA20, Volume_Ratio | Volume analysis |
| Year, Month, Quarter, Week | Date dimensions |

---

## âž• Adding More Stocks

Edit `STOCKS` dict in `fetch_clean_stocks.py` (use `.NS` or `.BO` symbols only):

```python
STOCKS = {
    "TSLA": "Tesla",
    "BRK-B": "Berkshire Hathaway",
    "V": "Visa",
    # ... add Indian exchange tickers only (example: TATAMOTORS.NS)
}
```

Also add to `SECTOR_MAP`:
```python
SECTOR_MAP = {
    "TSLA": "Consumer Discretionary",
    "V": "Financials",
    ...
}
```

---

## ðŸ› ï¸ Troubleshooting

| Issue | Fix |
|-------|-----|
| `ModuleNotFoundError: ta` | `pip install ta` |
| Empty data for a ticker | Check ticker on finance.yahoo.com |
| Power BI won't refresh | Check file path hasn't changed |
| Cron not running | Check `crontab -l` and log file |

