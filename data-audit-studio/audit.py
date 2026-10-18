import pandas as pd

def audit_dataframe(df):
    details = []
    for col in df.columns:
        s = df[col]
        flags = None
        if pd.api.types.is_numeric_dtype(s) and not pd.api.types.is_bool_dtype(s):
            n = pd.to_numeric(s, errors="coerce").dropna()
            if len(n) >= 4:
                q1, q3 = n.quantile([0.25, 0.75])
                iqr = q3 - q1
                flags = int(((n < q1 - 1.5*iqr) | (n > q3 + 1.5*iqr)).sum()) if iqr > 0 else 0
        details.append({"column": str(col), "dtype": str(s.dtype), "missing_count": int(s.isna().sum()), "missing_pct": round(100*s.isna().mean(), 2) if len(s) else 0, "unique_values": int(s.nunique(dropna=True)), "iqr_outlier_flags": flags})
    return {"rows": len(df), "columns": len(df.columns), "duplicate_rows": int(df.duplicated().sum()), "columns_detail": details}

def report_markdown(result):
    lines = ["# Data Quality Report", "", f"Rows: {result['rows']}", f"Columns: {result['columns']}", f"Duplicate rows: {result['duplicate_rows']}", "", "| Column | Type | Missing | Missing % | Unique | IQR flags |", "|---|---|---:|---:|---:|---:|"]
    for c in result["columns_detail"]:
        name = c["column"].replace("|", "\\|").replace("\n", " ")
        lines.append(f"| {name} | {c['dtype']} | {c['missing_count']} | {c['missing_pct']} | {c['unique_values']} | {c['iqr_outlier_flags'] if c['iqr_outlier_flags'] is not None else 'N/A'} |")
    return "\n".join(lines + ["", "IQR flags are heuristics, not confirmed errors.", ""])
