import pandas as pd

def missing_value_report(df: pd.DataFrame, only_missing: bool = True) -> pd.DataFrame:
    """
    Returns a DataFrame with missing value counts and ratios (%).
    If only_missing=True, returns only columns where nan_count > 0.
    """
    summary = pd.DataFrame({
        "nan_count": df.isna().sum(),
        "nan_ratio_pct": df.isna().mean() * 100
    })

    if only_missing:
        summary = summary[summary["nan_count"] > 0].sort_values("nan_ratio_pct", ascending=False)

    return summary


def overall_stats(df: pd.DataFrame) -> dict:
    rows, cols = df.shape
    total_cells = df.size
    total_missing = int(df.isna().sum().sum())
    overall_missing_ratio = (total_missing / total_cells) * 100 if total_cells else 0.0

    return {
        "rows": rows,
        "columns": cols,
        "total_cells": total_cells,
        "total_missing": total_missing,
        "overall_missing_ratio_pct": overall_missing_ratio
    }


def main(input_csv: str, only_missing: bool = True) -> None:
    # 1) Read dataset
    df = pd.read_csv(input_csv)

    # 2) Per-column missing summary
    summary = missing_value_report(df, only_missing=only_missing)

    # 3) Print results
    print("\n=== Missing Value Summary (per column) ===")
    if summary.empty:
        print("No missing values found.")
    else:
        print(summary.to_string())

    # 4) Overall statistics
    stats = overall_stats(df)
    print("\n=== Overall Dataset Stats ===")
    print(f"Number of rows: {stats['rows']}")
    print(f"Number of columns: {stats['columns']}")
    print(f"Total cells: {stats['total_cells']}")
    print(f"Total missing cells: {stats['total_missing']}")
    print(f"Overall missing value ratio: {stats['overall_missing_ratio_pct']:.2f}%")


if __name__ == "__main__":
    # Change this path to your file location if needed:
    INPUT_CSV = "Gold_Import_TradeData_clean_final.csv"

    # True -> only columns that have missing values
    # False -> all columns (including 0% missing)
    ONLY_MISSING_COLUMNS = True

    main(INPUT_CSV, only_missing=ONLY_MISSING_COLUMNS)
