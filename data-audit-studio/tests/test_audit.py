import pandas as pd
from audit import audit_dataframe, report_markdown

def test_missing_and_duplicates():
    r=audit_dataframe(pd.DataFrame({"x":[1,1,None],"y":["a","a","b"]}))
    assert r["duplicate_rows"]==1
    assert r["columns_detail"][0]["missing_count"]==1
    assert r["status"]=="REVIEW"

def test_required_columns_fail():
    r=audit_dataframe(pd.DataFrame({"x":[1,2]}),required=["id"])
    assert r["status"]=="FAIL"
    assert any(i["check"]=="required_columns" for i in r["issues"])

def test_clean_pass():
    r=audit_dataframe(pd.DataFrame({"x":[1,2,3],"y":["a","b","c"]}))
    assert r["status"]=="PASS"
    assert "Data Quality Report" in report_markdown(r)

def test_outlier_flag():
    r=audit_dataframe(pd.DataFrame({"x":[1,1,2,2,3,100]}))
    assert r["columns_detail"][0]["iqr_outlier_flags"]==1
