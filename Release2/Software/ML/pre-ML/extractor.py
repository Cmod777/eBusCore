#!/usr/bin/env python3

# ### extractor.py ###
# Extracts columns with "include: YES" from legenda.yaml (skipping rows 2-4 of db.csv),
# handles -999 values by converting them to NaN, and applies the interpolation
# specified in legenda.yaml for each column.
# Writes the result with numerical headers to db_clean.csv.

import csv
import yaml
from pathlib import Path
import numpy as np
import pandas as pd

# === Paths ===
CSV_INPUT_PATH = Path("db.csv")
YAML_PATH = Path("datacheck/legenda.yaml")
CSV_OUTPUT_PATH = Path("db_clean.csv")

# === Value to replace with NaN ===
VALUE_TO_REPLACE = "-999"

# === Number of rows to skip AFTER the header ===
ROWS_TO_SKIP = 3

# === Load YAML legend ===
try:
    with open(YAML_PATH, "r", encoding="utf-8") as f:
        legend_data = yaml.safe_load(f)
except FileNotFoundError:
    print(f"Error: The file '{YAML_PATH}' was not found.")
    exit(1)
except yaml.YAMLError as e:
    print(f"Error reading YAML file '{YAML_PATH}': {e}")
    exit(1)

column_legend = legend_data.get("column_codes", {})

# === Build code → column info map ===
code_to_info_map = {str(k): v for k, v in column_legend.items()}

# === Read headers from the first row of the CSV ===
try:
    with open(CSV_INPUT_PATH, "r", encoding="utf-8") as infile:
        reader = csv.reader(infile)
        csv_headers = next(reader)
        print("CSV Headers read:", csv_headers) # <--- ADDED FOR DEBUGGING
except FileNotFoundError:
    print(f"Error: The file '{CSV_INPUT_PATH}' was not found.")
    exit(1)

# === Load data using pandas, skipping rows after the header ===
try:
    df = pd.read_csv(CSV_INPUT_PATH, skiprows=ROWS_TO_SKIP + 1, header=None) # +1 because we already read the header
except FileNotFoundError:
    print(f"Error: The file '{CSV_INPUT_PATH}' was not found.")
    exit(1)
except pd.errors.EmptyDataError:
    print(f"Error: The file '{CSV_INPUT_PATH}' is empty after skipping rows.")
    exit(1)
except pd.errors.ParserError:
    print(f"Error: Could not parse the CSV file '{CSV_INPUT_PATH}'. Check the formatting.")
    exit(1)

# === Build CSV column name → index map ===
csv_name_to_index_map = {name: i for i, name in enumerate(csv_headers)}

# === Identify columns to include and their interpolation logic ===
columns_to_include_indices = {}
legend_name_to_code_map = {v["Name"]: str(k) for k, v in column_legend.items()}
legend_name_to_code_include_map = {v["Name"]: str(k) for k, v in column_legend.items() if str(v.get("include", "")).strip().upper() == "YES" or str(k) == "100"}

indices_to_select = []
output_column_codes = []

for legend_column_name, code in legend_name_to_code_include_map.items():
    if legend_column_name in csv_name_to_index_map:
        csv_index = csv_name_to_index_map[legend_column_name]
        indices_to_select.append(csv_index)
        output_column_codes.append(code)
    elif code == "100" and legend_column_name in csv_name_to_index_map:
        csv_index = csv_name_to_index_map[legend_column_name]
        indices_to_select.append(csv_index)
        output_column_codes.append(code)
    elif legend_column_name in csv_name_to_index_map:
        pass # If it's in the CSV but not "include: YES" and not "100", don't include it
    else:
        print(f"Warning: Column '{legend_column_name}' defined in legend not found in CSV.")

# Select only the desired columns
df_filtered = df.iloc[:, indices_to_select].copy()
df_filtered.columns = output_column_codes

# === Replace the specific value with NaN ===
df_filtered.replace(VALUE_TO_REPLACE, np.nan, inplace=True)

# === Apply specific interpolation for each column ===
df_interpolated = df_filtered.copy()
for column_code in df_interpolated.columns:
    column_info = code_to_info_map.get(column_code)
    if column_info and "interpolation" in column_info:
        interpolation_method = column_info["interpolation"]
        if interpolation_method.lower() == "linear":
            df_interpolated[column_code] = df_interpolated[column_code].interpolate(method='linear')
        elif interpolation_method.lower() == "mean":
            df_interpolated[column_code] = df_interpolated[column_code].fillna(df_interpolated[column_code].mean())
        elif interpolation_method.lower() == "ffill":
            df_interpolated[column_code] = df_interpolated[column_code].ffill()
        elif interpolation_method.lower() == "bfill":
            df_interpolated[column_code] = df_interpolated[column_code].bfill()
        elif interpolation_method.lower().startswith("value:"):
            try:
                value = float(interpolation_method.split(":")[1].strip())
                df_interpolated[column_code] = df_interpolated[column_code].fillna(value=value)
            except ValueError:
                print(f"Warning: Invalid interpolation value for column '{column_code}'.")
        else:
            print(f"Warning: Interpolation method '{interpolation_method}' not recognized for column '{column_code}'.")
        # Force interpolation to fill any remaining NaNs
        df_interpolated[column_code] = df_interpolated[column_code].interpolate(method='linear').bfill()
    elif column_code != "100" and str(code_to_info_map.get(column_code, {}).get("include", "")).strip().upper() == "YES":
        print(f"Warning: No interpolation method specified for column with code '{column_code}'.")

# === Write the output to db_clean.csv ===
try:
    with open(CSV_OUTPUT_PATH, "w", newline="", encoding="utf-8") as outfile:
        writer = csv.writer(outfile)
        # Write the header row (codes)
        writer.writerow(df_interpolated.columns.tolist())
        # Write all data rows from the interpolated DataFrame
        for index, row in df_interpolated.iterrows():
            writer.writerow(row.tolist())
        if df_interpolated.empty:
            print("Warning: The interpolated DataFrame is empty, no data written.")
        else:
            print(f"File '{CSV_OUTPUT_PATH}' generated successfully with {len(df_interpolated)} data rows and {len(df_interpolated.columns)} columns (values -999 replaced and specific interpolation applied).")

except Exception as e:
    print(f"Error during writing to file '{CSV_OUTPUT_PATH}': {e}")
