"""
extract_macro.py — Giai đoạn 1 [E] Extract
Lấy dữ liệu kinh tế vĩ mô từ:
  - World Bank API (GDP, lạm phát, thất nghiệp...)
  - FRED API (lãi suất Fed Funds, M2, CPI Mỹ...)

Dữ liệu được lưu vào data/raw/macro/ dạng CSV.

Cách chạy:
  python extract/extract_macro.py
"""

import os
import sys
from pathlib import Path

# Ensure UTF-8 output encoding on Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

import pandas as pd
import requests
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")

MACRO_DIR = ROOT_DIR / "data" / "raw" / "macro"

# -----------------------------------------------------------
# Cấu hình dữ liệu cần lấy
# -----------------------------------------------------------

# Mã quốc gia World Bank
# Home Credit hoạt động chủ yếu ở Nga, Ukraine, Czech Republic, Hungary...
WB_COUNTRIES = ["RU", "UA", "CZ", "HU", "PL", "KZ", "VN"]

# Chỉ số World Bank cần lấy
# Xem danh sách đầy đủ tại: https://data.worldbank.org/indicator
WB_INDICATORS = {
    "NY.GDP.MKTP.KD.ZG": "gdp_growth_pct",           # Tăng trưởng GDP (%)
    "FP.CPI.TOTL.ZG":    "inflation_cpi_pct",         # Lạm phát (CPI, %)
    "SL.UEM.TOTL.ZS":    "unemployment_rate_pct",      # Tỷ lệ thất nghiệp (%)
    "FS.AST.DOMS.GD.ZS": "domestic_credit_gdp_pct",   # Tín dụng nội địa / GDP (%)
    "NY.GDP.PCAP.CD":    "gni_per_capita_usd",         # GDP per capita USD (thay cho GNI)
}

# Năm lấy dữ liệu (Home Credit dataset chủ yếu 2015–2017)
WB_YEAR_START = 2010
WB_YEAR_END = 2018

# Chỉ số FRED cần lấy
FRED_SERIES = {
    "FEDFUNDS":  "fed_funds_rate",        # Lãi suất quỹ liên bang Mỹ (%)
    "M2SL":      "m2_money_supply_bn",    # Cung tiền M2 Mỹ (tỷ USD)
    "CPIAUCSL":  "cpi_us",               # CPI Mỹ
    "UNRATE":    "unemployment_us_pct",   # Tỷ lệ thất nghiệp Mỹ
}
FRED_START = "2010-01-01"
FRED_END = "2018-12-31"


# ============================================================
# World Bank API
# ============================================================

def fetch_worldbank(indicator_code: str, col_name: str) -> pd.DataFrame:
    """
    Gọi World Bank API v2, lấy chỉ số cho nhiều quốc gia và nhiều năm.
    API docs: https://datahelpdesk.worldbank.org/knowledgebase/articles/889392
    """
    countries_str = ";".join(WB_COUNTRIES)
    url = (
        f"https://api.worldbank.org/v2/country/{countries_str}"
        f"/indicator/{indicator_code}"
        f"?date={WB_YEAR_START}:{WB_YEAR_END}"
        f"&format=json&per_page=500"
    )

    try:
        resp = requests.get(url, timeout=60)
        resp.raise_for_status()
        data = resp.json()

        # World Bank trả về list[dict] ở phần tử [1]
        if len(data) < 2 or not data[1]:
            print(f"    ⚠️   {indicator_code}: không có dữ liệu")
            return pd.DataFrame()

        rows = []
        for item in data[1]:
            rows.append({
                "country_code": item["country"]["id"],
                "country_name": item["country"]["value"],
                "year":         int(item["date"]),
                col_name:       item["value"],
            })

        return pd.DataFrame(rows)

    except Exception as e:
        print(f"    ❌  Lỗi khi lấy {indicator_code}: {e}")
        return pd.DataFrame()


def extract_worldbank():
    """Lấy tất cả chỉ số World Bank và ghép thành 1 bảng."""
    print(f"\n{'='*55}")
    print("  CCIP — Extract: World Bank Macro Data")
    print(f"{'='*55}")

    dfs = []
    for code, col_name in WB_INDICATORS.items():
        print(f"  ⬇️   {col_name} ({code})...")
        df = fetch_worldbank(code, col_name)
        if not df.empty:
            dfs.append(df.set_index(["country_code", "country_name", "year"]))
            print(f"       → {len(df)} dòng")

    if not dfs:
        print("  ❌  Không lấy được dữ liệu nào từ World Bank")
        return

    # Ghép tất cả indicators theo country + year
    result = dfs[0]
    for df in dfs[1:]:
        result = result.join(df, how="outer")
    result = result.reset_index()
    result = result.sort_values(["country_code", "year"])

    # Lưu file
    MACRO_DIR.mkdir(parents=True, exist_ok=True)
    out_path = MACRO_DIR / "worldbank_macro.csv"
    result.to_csv(out_path, index=False, encoding="utf-8-sig")
    print(f"\n  ✅  World Bank: {len(result)} dòng → {out_path.name}")


# ============================================================
# FRED API
# ============================================================

def fetch_fred_series(series_id: str, col_name: str, api_key: str) -> pd.DataFrame:
    """
    Gọi FRED API, lấy một chuỗi thời gian.
    API docs: https://fred.stlouisfed.org/docs/api/fred/series_observations.html
    """
    url = (
        f"https://api.stlouisfed.org/fred/series/observations"
        f"?series_id={series_id}"
        f"&observation_start={FRED_START}"
        f"&observation_end={FRED_END}"
        f"&api_key={api_key}"
        f"&file_type=json"
        f"&frequency=m"   # monthly — lấy theo tháng
    )

    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        rows = []
        for obs in data.get("observations", []):
            try:
                value = float(obs["value"])
            except (ValueError, TypeError):
                value = None  # Kaggle dùng "." cho missing
            rows.append({
                "date":   obs["date"],
                col_name: value,
            })

        df = pd.DataFrame(rows)
        if not df.empty:
            df["date"] = pd.to_datetime(df["date"])
        return df

    except Exception as e:
        print(f"    ❌  Lỗi khi lấy {series_id}: {e}")
        return pd.DataFrame()


def extract_fred():
    """Lấy tất cả chuỗi FRED và ghép thành 1 bảng theo tháng."""
    print(f"\n{'='*55}")
    print("  CCIP — Extract: FRED Economic Data")
    print(f"{'='*55}")

    api_key = os.getenv("FRED_API_KEY")
    if not api_key:
        print("  ❌  Chưa có FRED_API_KEY trong .env")
        print("      → Đăng ký miễn phí tại: https://fred.stlouisfed.org/docs/api/api_key.html")
        return

    dfs = []
    for series_id, col_name in FRED_SERIES.items():
        print(f"  ⬇️   {col_name} ({series_id})...")
        df = fetch_fred_series(series_id, col_name, api_key)
        if not df.empty:
            dfs.append(df.set_index("date"))
            print(f"       → {len(df)} dòng")

    if not dfs:
        print("  ❌  Không lấy được dữ liệu nào từ FRED")
        return

    result = dfs[0]
    for df in dfs[1:]:
        result = result.join(df, how="outer")
    result = result.reset_index().sort_values("date")

    MACRO_DIR.mkdir(parents=True, exist_ok=True)
    out_path = MACRO_DIR / "fred_macro.csv"
    result.to_csv(out_path, index=False, encoding="utf-8-sig")
    print(f"\n  ✅  FRED: {len(result)} dòng → {out_path.name}")


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":
    extract_worldbank()
    extract_fred()
    print("\n✅  Extract Macro Data hoàn thành!\n")
