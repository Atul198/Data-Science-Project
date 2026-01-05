import pandas as pd
import numpy as np
import csv
from pathlib import Path

# CONFIG
files = [
    "TradeData2019.csv",
    "TradeData2020.csv",
    "TradeData2021.csv",
    "TradeData2022.csv",
    "TradeData2023.csv",
    "TradeData2024.csv",
]

OUT_FILE = "Gold_Import_TradeData_clean_final.csv"

# Helpers

def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = (
        df.columns.str.strip().str.lower()
          .str.replace(" ", "_")
          .str.replace("-", "_")
          .str.replace(".", "_")
    )
    return df

def robust_read(path: str) -> pd.DataFrame:
    # Aynı derste yaşadığımız encoding issue + olası quoting garipliklerine dayanıklı okuma
    return pd.read_csv(
        path,
        encoding="latin1",
        sep=",",
        engine="python",
        quoting=csv.QUOTE_MINIMAL,
        index_col=False
    )

def build_month_start_date(df: pd.DataFrame) -> pd.DataFrame:
    # Öncelik: refperiodid (YYYYMMDD) varsa ondan üret
    if "refperiodid" in df.columns:
        df["refperiodid"] = pd.to_numeric(df["refperiodid"], errors="coerce")
        dt = pd.to_datetime(df["refperiodid"].astype("Int64").astype(str), format="%Y%m%d", errors="coerce")
        df["date"] = dt.dt.to_period("M").dt.to_timestamp()  # month-start
    # Alternatif: period (YYYYMM) varsa ondan üret
    elif "period" in df.columns:
        df["period"] = pd.to_numeric(df["period"], errors="coerce")
        dt = pd.to_datetime(df["period"].astype("Int64").astype(str) + "01", format="%Y%m%d", errors="coerce")
        df["date"] = dt.dt.to_period("M").dt.to_timestamp()
    else:
        raise ValueError("Ne refPeriodId ne de period kolonu var. Tarih üretilemiyor.")

    df["refyear_clean"] = df["date"].dt.year
    df["refmonth_clean"] = df["date"].dt.month
    return df

def force_desc_to_text(df: pd.DataFrame) -> pd.DataFrame:
    for c in [c for c in df.columns if c.endswith("desc")]:
        df[c] = df[c].astype("string").str.strip()
    return df

def coerce_numeric(df: pd.DataFrame) -> pd.DataFrame:
    # Comtrade/Trade exportlarında bu 3 kolon genelde temel
    for c in ["cifvalue", "fobvalue", "primaryvalue", "qty", "altqty", "netwgt", "grosswgt"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df

def rename_quantity_columns(df: pd.DataFrame) -> pd.DataFrame:
    # Eğer önceki dosyada "has_*" gibi isimlerle geldiyse normalize et
    ren = {}
    if "has_qty" in df.columns: ren["has_qty"] = "qty"
    if "has_alt_qty" in df.columns: ren["has_alt_qty"] = "alt_qty"
    if "has_net_wgt" in df.columns: ren["has_net_wgt"] = "net_wgt"
    if "has_gross_wgt" in df.columns: ren["has_gross_wgt"] = "gross_wgt"
    df = df.rename(columns=ren)

    # altqty/netwgt gibi camel varyasyonları varsa da normalize edelim
    df = df.rename(columns={
        "altqty": "alt_qty",
        "netwgt": "net_wgt",
        "grosswgt": "gross_wgt",
    })
    return df

def keep_useful_schema(df: pd.DataFrame) -> pd.DataFrame:
    # Analizde işimize yarayan, merge-friendly şema
    keep = [
        "date","refyear_clean","refmonth_clean",
        "refperiodid","period","freqcode","refyear","refmonth",
        "flowcode","flowdesc",
        "reportercode","reporteriso","reporterdesc",
        "partnercode","partneriso","partnerdesc",
        "cmdcode","cmddesc",
        "cifvalue","fobvalue","primaryvalue",
        "qty","alt_qty","net_wgt","gross_wgt",
        "qtyunitcode","qtyunitabbr","altqtyunitcode","altqtyunitabbr",
        "isreported","isaggregate","isleaf","aggrlevel"
    ]
    keep = [c for c in keep if c in df.columns]
    return df[keep].copy()

def normalize_flow(df: pd.DataFrame) -> pd.DataFrame:
    if "flowdesc" in df.columns:
        df["flowdesc_norm"] = df["flowdesc"].astype("string").str.strip().str.lower()
    return df


all_clean = []
report = []

for f in files:
    df = robust_read(f)
    df = standardize_columns(df)
    df = force_desc_to_text(df)
    df = rename_quantity_columns(df)
    df = coerce_numeric(df)
    df = build_month_start_date(df)
    df = normalize_flow(df)

    # IMPORT filtresi: hem flowdesc hem flowcode üzerinden deniyoruz (dataset’e göre değişebilir)
    if "flowdesc_norm" in df.columns:
        df_imp = df[df["flowdesc_norm"].eq("import")].copy()
    else:
        df_imp = df.copy()  # flow yoksa filtrelemiyoruz, ama bu nadir

    df_imp = keep_useful_schema(df_imp)

    # Kalite mini rapor
    report.append({
        "file": f,
        "rows_raw": len(df),
        "rows_import": len(df_imp),
        "date_nat": int(df_imp["date"].isna().sum()) if "date" in df_imp.columns else None,
        "date_min": str(df_imp["date"].min()) if "date" in df_imp.columns else None,
        "date_max": str(df_imp["date"].max()) if "date" in df_imp.columns else None,
    })

    all_clean.append(df_imp)

imports_master = pd.concat(all_clean, ignore_index=True)

# Duplicate check (özellikle aynı ay/ülke/ürün tekrar etmiş mi)
dup_key = [c for c in ["date","reportercode","partnercode","cmdcode","flowcode"] if c in imports_master.columns]
dups = imports_master.duplicated(subset=dup_key).sum() if dup_key else None

# Save
imports_master.to_csv(OUT_FILE, index=False)

print("✅ Saved:", OUT_FILE)
print("Master shape:", imports_master.shape)
print("Duplicate rows (key-based):", dups)
print("\nPer-file report:")
print(pd.DataFrame(report))

