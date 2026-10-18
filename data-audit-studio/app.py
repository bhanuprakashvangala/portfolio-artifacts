import io
import pandas as pd
import streamlit as st
from audit import audit_dataframe, report_markdown

st.set_page_config(page_title="Data Audit Studio", page_icon="📊", layout="wide")
st.title("Data Audit Studio")
st.caption("CSV quality reporting without external AI APIs")
file = st.file_uploader("Upload CSV (up to 10 MB)", type=["csv"])
if file:
    if file.size > 10*1024*1024:
        st.error("File exceeds 10 MB limit.")
        st.stop()
    try:
        df = pd.read_csv(io.BytesIO(file.getvalue()))
        if df.empty or len(df.columns) > 200:
            st.error("CSV must be nonempty and have at most 200 columns.")
            st.stop()
        result = audit_dataframe(df)
        a,b,c = st.columns(3)
        a.metric("Rows", result["rows"])
        b.metric("Columns", result["columns"])
        c.metric("Duplicate rows", result["duplicate_rows"])
        st.dataframe(pd.DataFrame(result["columns_detail"]), use_container_width=True)
        st.subheader("Data preview")
        st.dataframe(df.head(20), use_container_width=True)
        st.download_button("Download report", report_markdown(result), "data_quality_report.md", "text/markdown")
    except (ValueError, UnicodeError, pd.errors.ParserError) as exc:
        st.error(f"Invalid CSV: {exc}")
else:
    st.info("Files are processed wherever this application is hosted. Avoid sensitive data on untrusted deployments.")
