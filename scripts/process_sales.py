"""Process daily sales CSVs into a single CSV with columns: Sales, Date, Region

Reads all files matching data/daily_sales_data_*.csv, filters for 'pink morsel',
parses price and quantity, computes sales = price * quantity, and writes output
as data/pink_morsel_sales.csv.
"""

import glob
import os
import pandas as pd


def process(input_dir="data", output_file="data/pink_morsel_sales.csv"):
    pattern = os.path.join(input_dir, "daily_sales_data_*.csv")
    files = sorted(glob.glob(pattern))
    if not files:
        print(f"No files found matching {pattern}")
        return

    out_frames = []
    for fp in files:
        print(f"Reading {fp}")
        df = pd.read_csv(fp)
        # Normalize column names
        df.columns = [c.strip().lower() for c in df.columns]
        # Ensure required cols exist
        if not {"product", "price", "quantity", "date", "region"}.issubset(set(df.columns)):
            print(f"Skipping {fp}: missing columns")
            continue
        # Filter product exactly "pink morsel" (case-insensitive)
        mask = df["product"].str.lower().str.strip() == "pink morsel"
        df = df.loc[mask].copy()
        if df.empty:
            continue
        # Clean price (remove $ and commas) and convert to float
        df["price"] = (
            df["price"].astype(str).str.replace("$", "", regex=False).str.replace(",", "", regex=False)
        )
        df["price"] = pd.to_numeric(df["price"], errors="coerce")
        df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
        # Drop rows with bad numeric parsing
        df = df.dropna(subset=["price", "quantity"])
        df["sales"] = df["price"] * df["quantity"]
        # Keep only Sales, Date, Region (capitalize headers as requested)
        out = df[["sales", "date", "region"]].copy()
        out.columns = ["Sales", "Date", "Region"]
        out_frames.append(out)

    if not out_frames:
        print("No pink morsel rows found in input files.")
        return

    result = pd.concat(out_frames, ignore_index=True)
    # Normalize Date to ISO YYYY-MM-DD
    result["Date"] = pd.to_datetime(result["Date"], errors="coerce").dt.date.astype(str)
    # Reorder columns
    result = result[["Sales", "Date", "Region"]]
    # Write output
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    result.to_csv(output_file, index=False)
    print(f"Wrote {len(result)} rows to {output_file}")


if __name__ == "__main__":
    process()
