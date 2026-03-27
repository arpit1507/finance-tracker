```markdown
# 💰 Financial Data Analyser

A **Streamlit-based financial analytics dashboard** that helps users analyze transaction data, understand spending behavior, and forecast future outgoing expenses using a **SARIMA time series model**.

---

## 🚀 Features

### 📊 Data Analysis
- Upload Excel financial data
- Automatic preprocessing of dates and amounts
- Income vs outgoing transaction separation
- Monthly transaction analysis

### 📈 Visualizations
- Cumulative cashflow over time
- Monthly income vs outgoing comparison
- Category-wise spending analysis
- Payment method distribution
- Top spending categories

### 🤖 Forecasting
- SARIMA model for future outgoing expense prediction
- 30-day forecast visualization
- Summary forecast metrics:
  - predicted total outgoing
  - average daily outgoing
  - highest predicted day

---

## 📁 Project Structure

```
Financial_Data_Analyser/
├── pyproject.toml
├── README.md
├── .gitignore
├── sample.xlsx
├── src/
│   └── financial_data_analyser/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py
│       ├── app.py
│       ├── data.py
│       └── model.py
```

---

## 🔹 File Description

| File | Description |
|------|-------------|
| `app.py` | Streamlit dashboard user interface |
| `data.py` | Data loading, preprocessing, and analysis logic |
| `model.py` | SARIMA forecasting model |
| `cli.py` | Command-line entry point |
| `__main__.py` | Module entry point for `python -m` execution |
| `pyproject.toml` | Python package configuration |

---

## ⚙️ Installation

Make sure you have **Python 3.10 or higher** installed.

```bash
uv venv
source .venv/bin/activate
uv pip install -e .
```

---

## ▶️ Running the Project

### Run as a Python module

```bash
uv run -m financial_data_analyser
```

### Run the Streamlit dashboard

```bash
uv run -m financial_data_analyser --streamlit
```

---

## 📊 Input Data Format

| Column Name | Description |
|-------------|-------------|
| `Buchungstag` | Transaction date in `DD.MM.YY` format |
| `Betrag` | Transaction amount (comma decimal supported) |
| `Kategorie` | Transaction category |
| `Method of Payement` | Payment method |

---

## 🧠 Methodology

### Data Processing
- Convert dates to datetime
- Convert amounts to float
- Remove missing values
- Separate income and outgoing transactions

### Time Series Modeling
- Aggregate outgoing expenses by day
- Fill missing dates
- Fit SARIMA model
- Forecast next 30 days

---

## ⚠️ Limitations

- SARIMA captures trend and seasonality but:
  - cannot predict sudden large expenses
  - struggles with irregular patterns
- Forecast represents baseline expected spending

---

## 📸 Dashboard Sections

- Overview metrics
- Spending trends
- Category analysis
- Payment insights
- Forecast section

---

## 💡 Future Improvements

- LSTM-based forecasting
- Anomaly detection
- Budget tracking
- ML-based categorization
- Export reports

---

## 🧑‍💻 Author

**Arpit Agrawal**
```
