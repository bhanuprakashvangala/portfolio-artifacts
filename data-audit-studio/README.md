# Data Audit Studio

A focused, transparent CSV data-quality auditing demo for technical teams and small businesses. Designed to validate a productized service offer, **not** yet a hosted SaaS.

## Capabilities
- CSV upload (10 MB UI limit), summary metrics and row preview
- Missing-value checks with adjustable threshold
- Required-column validation
- Duplicate row detection
- Numeric IQR outlier heuristics
- PASS / REVIEW / FAIL status and downloadable Markdown report
- Sample dataset and unit tests

## Quick start
```bash
cd data-audit-studio
pip install -r requirements.txt
streamlit run app.py
```
Upload `sample_data.csv`, then try requiring `order_id` and setting the missing threshold to 10%.

## Tests
```bash
python -m pytest -q
```

## Pilot offer (hypothesis, not a customer claim)
**$399 fixed-scope pilot:** audit one agreed CSV export, configure up to five validation rules, deliver an issue report and a 30-minute handoff. Confirm dataset size, access permissions, and acceptance criteria before agreeing to work.

## Limitations
This is an exploratory MVP. No login, payment system, customer data persistence, or production security review. Upload only synthetic or authorized nonsensitive data, especially on third-party deployments. IQR outliers are possible anomalies, not confirmed errors. PASS means no findings among enabled checks, not that data is universally correct.
