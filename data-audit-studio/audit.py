"""Deterministic CSV profiling and configurable quality checks."""
import pandas as pd

def audit_dataframe(df, required=None, max_missing_pct=10):
    required = required or []
    missing_required = [c for c in required if c not in df.columns]
    details = []
    issues = []
    if missing_required:
        issues.append({"severity":"error","check":"required_columns","column":", ".join(missing_required),"message":"Required columns are missing"})
    duplicates = int(df.duplicated().sum())
    if duplicates:
        issues.append({"severity":"warning","check":"duplicate_rows","column":"—","message":f"{duplicates} duplicate rows"})
    for col in df.columns:
        s = df[col]
        missing = int(s.isna().sum())
        pct = round(100 * missing / len(df), 2) if len(df) else 0
        outliers = None
        if pd.api.types.is_numeric_dtype(s) and not pd.api.types.is_bool_dtype(s):
            n = pd.to_numeric(s, errors="coerce").dropna()
            if len(n) >= 4:
                q1, q3 = n.quantile([.25, .75])
                iqr = q3-q1
                outliers = int(((n < q1-1.5*iqr) | (n > q3+1.5*iqr)).sum()) if iqr > 0 else 0
        if pct > max_missing_pct:
            issues.append({"severity":"warning","check":"missing_values","column":str(col),"message":f"{pct}% missing (threshold {max_missing_pct}%)"})
        if outliers:
            issues.append({"severity":"info","check":"iqr_outliers","column":str(col),"message":f"{outliers} potential outliers; review before removal"})
        details.append({"column":str(col),"dtype":str(s.dtype),"missing_count":missing,"missing_pct":pct,"unique_values":int(s.nunique(dropna=True)),"iqr_outlier_flags":outliers})
    return {"rows":len(df),"columns":len(df.columns),"duplicate_rows":duplicates,"columns_detail":details,"issues":issues,"status":"FAIL" if missing_required else "REVIEW" if issues else "PASS"}

def report_markdown(result):
    lines = ["# Data Quality Report","",f"Status: **{result['status']}**",f"Rows: {result['rows']}",f"Columns: {result['columns']}",f"Duplicate rows: {result['duplicate_rows']}","","## Findings"]
    if not result["issues"]:
        lines.append("No findings under the selected checks.")
    for item in result["issues"]:
        lines.append(f"- **{item['severity'].upper()}** — {item['check']} ({item['column']}): {item['message']}")
    lines += ["","## Column profile","| Column | Type | Missing | Missing % | Unique | IQR flags |","|---|---|---:|---:|---:|---:|"]
    for c in result["columns_detail"]:
        name = c["column"].replace("|","\\|").replace("\n"," ")
        lines.append(f"| {name} | {c['dtype']} | {c['missing_count']} | {c['missing_pct']} | {c['unique_values']} | {c['iqr_outlier_flags'] if c['iqr_outlier_flags'] is not None else 'N/A'} |")
    return "\n".join(lines + ["","Outlier flags are heuristics, not confirmed errors.",""])
