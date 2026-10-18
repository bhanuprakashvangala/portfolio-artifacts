# Data Audit Studio

A small Streamlit CSV-quality demo for customer discovery. Flags missing data, duplicate rows and numeric IQR outliers, and exports a Markdown report.

## Run
```bash
pip install -r requirements.txt
streamlit run app.py
python -m pytest -q
```

This is an MVP, not a production SaaS. No authentication, billing or persistent storage. Never upload confidential data to an untrusted deployment. Outlier flags are heuristics, not verified errors.
