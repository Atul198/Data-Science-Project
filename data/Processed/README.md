# Processed Data

This folder contains cleaned, standardized, and analysis-ready datasets produced as part of the data engineering pipeline.  
All raw data located under `data/Raw/` remains unchanged.

## Folder Structure


- `GOLD/`  
  Cleaned and standardized gold trade and price-related datasets.

- `SWIFT/`  
  Cleaned SWIFT RMB Tracker data, providing monthly indicators of RMB usage in global and international payments.

## Data Engineering Notes

- All datasets are standardized to a **monthly time index** using a **month-start date format (YYYY-MM-01)**.
- Column names are normalized (lowercase, snake_case).
- Numeric fields are explicitly cast to appropriate data types.
- Missing or inconsistent values in raw data were handled during the cleaning process.
- Each dataset is exported as a standalone CSV file and is **merge-ready** for downstream analysis.

## Intended Use

These processed datasets are designed to support:
- Time-series analysis
- Cross-dataset integration
- Econometric and statistical modeling
- Data visualization and reporting

This structure ensures reproducibility, transparency, and separation of concerns between raw and processed data.

