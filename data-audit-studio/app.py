import io
import pandas as pd
import streamlit as st
from audit import audit_dataframe, report_markdown

st.set_page_config(page_title="Data Audit Studio",page_icon="📊",layout="wide")
st.title("Data Audit Studio")
st.caption("Transparent, deterministic data-quality checks — no AI API or external processing service")
with st.sidebar:
    st.header("Validation rules")
    threshold = st.slider("Maximum missing values (%)",0,100,10)
    required_text = st.text_input("Required columns (comma-separated)",placeholder="order_id, customer_id")
    st.info("Outliers are flagged for review, not automatically removed.")
file = st.file_uploader("Upload a CSV file (maximum 10 MB)",type=["csv"])
if file is None:
    st.info("Start with the included sample_data.csv to see the quality report.")
    st.stop()
if file.size > 10*1024*1024:
    st.error("File exceeds the 10 MB upload limit.")
    st.stop()
try:
    df = pd.read_csv(io.BytesIO(file.getvalue()))
    if df.empty or len(df.columns)>200:
        st.error("CSV must contain rows and no more than 200 columns.")
        st.stop()
    required = [x.strip() for x in required_text.split(",") if x.strip()]
    result = audit_dataframe(df,required=required,max_missing_pct=threshold)
    st.subheader(f"Audit status: {result['status']}")
    a,b,c,d=st.columns(4)
    a.metric("Rows",result["rows"])
    b.metric("Columns",result["columns"])
    c.metric("Duplicates",result["duplicate_rows"])
    d.metric("Findings",len(result["issues"]))
    st.subheader("Findings")
    if result["issues"]:
        st.dataframe(pd.DataFrame(result["issues"]),use_container_width=True,hide_index=True)
    else:
        st.success("No findings for the configured checks.")
    st.subheader("Column profile")
    st.dataframe(pd.DataFrame(result["columns_detail"]),use_container_width=True,hide_index=True)
    with st.expander("Preview first 20 rows"):
        st.dataframe(df.head(20),use_container_width=True)
    st.download_button("Download Markdown report",report_markdown(result),"data_quality_report.md","text/markdown")
except (ValueError,UnicodeError,pd.errors.ParserError) as exc:
    st.error(f"Unable to read CSV: {exc}")
