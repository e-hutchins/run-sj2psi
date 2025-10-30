#!/usr/bin/env python3
import argparse
import pandas as pd
from pathlib import Path

# Expects:
# SJ.withPSIs.txt (TSV): chrom, first_bp_intron, last_bp_intron, ... (keep all extra columns)
# CE_junctions.csv (CSV): first column is the ID (often unnamed), then chr,start,end,gene,...

def main():
    ap = argparse.ArgumentParser(description="Subset STAR SJ table using CE_junctions coordinates (fixed column names), keeping CE ID column.")
    ap.add_argument("--sj", required=True, help="SJ.withPSIs.txt (TSV with header).")
    ap.add_argument("--ce", required=True, help="CE_junctions.csv (CSV with leading ID column).")
    ap.add_argument("--out", required=True, help="Output TSV with matched SJ rows + CE columns (including ID).")
    ap.add_argument("--ce-not-found", default=None, help="Optional CSV path for CE rows with no SJ match.")
    ap.add_argument("--shift-start", type=int, default=1, help="Shift to apply to CE start (default: +1).")
    ap.add_argument("--shift-end", type=int, default=-1, help="Shift to apply to CE end (default: -1).")
    args = ap.parse_args()

    # Load SJ (keep all columns)
    sj = pd.read_csv(args.sj, sep="\t")
    sj = sj.copy()
    sj["chr"] = sj["chrom"].astype(str).str.strip()
    sj["chr"] = sj["chr"].apply(lambda c: c if c.startswith("chr") else f"chr{c}")
    sj["start"] = pd.to_numeric(sj["first_bp_intron"], errors="coerce").astype("Int64")
    sj["end"]   = pd.to_numeric(sj["last_bp_intron"],  errors="coerce").astype("Int64")
    sj = sj.dropna(subset=["start","end"])

    # Load CE WITHOUT using index_col so we retain the first ID column
    ce = pd.read_csv(args.ce)
    # Ensure the first column is treated as an ID column, even if unnamed (",chr,start,...")
    id_col = ce.columns[0]
    if id_col.startswith("Unnamed"):
        ce = ce.rename(columns={id_col: "junction_id"})
        id_col = "junction_id"

    # Coordinate normalization + shifts
    ce["chr"] = ce["chr"].astype(str).str.strip()
    ce["chr"] = ce["chr"].apply(lambda c: c if c.startswith("chr") else f"chr{c}")
    ce["start"] = (pd.to_numeric(ce["start"], errors="coerce") + args.shift_start).astype("Int64")
    ce["end"]   = (pd.to_numeric(ce["end"],   errors="coerce") + args.shift_end).astype("Int64")
    ce = ce.dropna(subset=["start","end"])

    keys = ["chr","start","end"]

    # Subset SJ to matched coordinates
    sj_matched = sj.merge(ce[keys].drop_duplicates(), on=keys, how="inner")

    # Attach full CE columns (prefix non-key columns to avoid collisions), including the ID column
    ce_pref = ce.copy()
    for c in list(ce_pref.columns):
        if c not in keys:
            ce_pref.rename(columns={c: f"ce_{c}"}, inplace=True)
    out_df = sj_matched.merge(ce_pref, on=keys, how="left")

    # Write outputs
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    out_df.to_csv(args.out, sep="\t", index=False)

    # Optionally, report CE rows without SJ matches
    if args.ce_not_found:
        found = out_df[keys].drop_duplicates()
        ce_not = ce.merge(found, on=keys, how="left", indicator=True)
        ce_not = ce_not[ce_not["_merge"]=="left_only"].drop(columns=["_merge"])
        Path(args.ce_not_found).parent.mkdir(parents=True, exist_ok=True)
        ce_not.to_csv(args.ce_not_found, index=False)

    # Summary
    print(f"Matched SJ rows: {len(out_df)}")
    print(f"Unique coordinate keys matched: {out_df[keys].drop_duplicates().shape[0]}")
    if args.ce_not_found:
        print(f"Wrote CE rows with no SJ match to: {args.ce_not_found}")
    print(f"Wrote subset SJ table (with CE annotations, including CE ID as 'ce_{id_col}') to: {args.out}")

if __name__ == "__main__":
    pd.set_option('display.max_columns', None)
    main()
