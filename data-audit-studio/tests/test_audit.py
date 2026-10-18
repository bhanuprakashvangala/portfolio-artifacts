import pandas as pd
from audit import audit_dataframe, report_markdown

def test_summary():
    result = audit_dataframe(pd.DataFrame({"x":[1,1,None], "y":["a","a","b"]}))
    assert result["rows"] == 3
    assert result["duplicate_rows"] == 1
    assert result["columns_detail"][0]["missing_count"] == 1
    assert "Data Quality Report" in report_markdown(result)
