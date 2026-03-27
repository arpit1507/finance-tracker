import streamlit as st
import pandas as pd
import plotly.express as px
from financial_data_analyser.data import Data
from financial_data_analyser.model import SARIMAModel

def generate_key_insights(data: pd.DataFrame):
    df = data.copy()

    # keep only outgoing expenses
    expenses = df[df["Betrag"] < 0].copy()
    expenses["Betrag"] = expenses["Betrag"].abs()

    insights = {}

    # 1. Overall top spending category
    if not expenses.empty:
        top_category = expenses.groupby("Kategorie")["Betrag"].sum().sort_values(ascending=False)
        insights["top_category"] = top_category.index[0]
        insights["top_category_amount"] = top_category.iloc[0]
    else:
        insights["top_category"] = None
        insights["top_category_amount"] = 0

    # 2. Exclude Gasbill, Rent, Electricity bill, Sister
    excluded_categories = ["Gasbill", "Rent", "Electricity bill", "Sister"]

    filtered_expenses = expenses[~expenses["Kategorie"].isin(excluded_categories)].copy()

    if not filtered_expenses.empty:
        filtered_expenses["Month"] = filtered_expenses["Buchungstag"].dt.to_period("M").astype(str)

        monthly_spend = (
            filtered_expenses.groupby("Month")["Betrag"]
            .sum()
            .sort_values(ascending=False)
        )

        top_month = monthly_spend.index[0]
        top_month_amount = monthly_spend.iloc[0]

        category_spend_filtered = (
            filtered_expenses.groupby("Kategorie")["Betrag"]
            .sum()
            .sort_values(ascending=False)
        )

        top_filtered_category = category_spend_filtered.index[0]
        top_filtered_category_amount = category_spend_filtered.iloc[0]

        insights["top_month_excluding_fixed"] = top_month
        insights["top_month_excluding_fixed_amount"] = top_month_amount
        insights["top_category_excluding_fixed"] = top_filtered_category
        insights["top_category_excluding_fixed_amount"] = top_filtered_category_amount
    else:
        insights["top_month_excluding_fixed"] = None
        insights["top_month_excluding_fixed_amount"] = 0
        insights["top_category_excluding_fixed"] = None
        insights["top_category_excluding_fixed_amount"] = 0

    return insights

def plot_cumulative_cashflow(data: pd.DataFrame):
    graph = data.groupby("Buchungstag")["Betrag"].sum().sort_index().cumsum().reset_index()
    graph.columns = ["Date", "Amount"]

    fig = px.line(graph, x="Date", y="Amount", title="Cumulative Cashflow Over Time", markers=True)
    fig.update_traces(fill="tozeroy")
    fig.update_layout(hovermode="x unified")
    return fig


def plot_monthly_income_vs_expense(data: pd.DataFrame):
    df = data.copy()
    df["Month"] = df["Buchungstag"].dt.to_period("M").astype(str)

    income = df[df["Betrag"] > 0].groupby("Month")["Betrag"].sum()
    expense = df[df["Betrag"] < 0].groupby("Month")["Betrag"].sum().abs()

    monthly = pd.DataFrame({"Income": income, "Outgoing": expense}).fillna(0).reset_index()

    fig = px.bar(monthly, x="Month", y=["Income", "Outgoing"], barmode="group",
                 title="Monthly Income vs Outgoing")
    return fig


def monthly_category_spending_chart(data: pd.DataFrame):
    df = data.copy()
    df = df[df["Betrag"] < 0].copy()
    df["Betrag"] = df["Betrag"].abs()
    df["Month"] = df["Buchungstag"].dt.to_period("M").astype(str)

    monthly_category = df.groupby(["Month", "Kategorie"])["Betrag"].sum().reset_index()

    fig = px.bar(
        monthly_category,
        x="Month",
        y="Betrag",
        color="Kategorie",
        barmode="stack",
        title="Monthly Spending by Category"
    )
    return fig


def plot_top_categories(data: pd.DataFrame):
    df = data.copy()
    df = df[df["Betrag"] < 0].copy()
    df["Betrag"] = df["Betrag"].abs()

    category_sum = (
        df.groupby("Kategorie")["Betrag"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        category_sum,
        x="Betrag",
        y="Kategorie",
        orientation="h",
        title="Top Spending Categories"
    )
    return fig


def payment_method_pie_chart(method_counts: pd.Series):
    fig = px.pie(
        values=method_counts.values,
        names=method_counts.index,
        hole=0.5,
        title="Payment Method Distribution"
    )
    fig.update_traces(textinfo="percent+label")
    fig.update_layout(showlegend=False)
    return fig


def payment_method_amount_chart(each_method_sum: pd.Series):
    df = each_method_sum.abs().reset_index()
    df.columns = ["Method of Payement", "Amount"]

    fig = px.bar(df, x="Method of Payement", y="Amount", title="Amount by Payment Method")
    return fig


def forecast_chart(forecast: pd.Series):
    df = forecast.reset_index()
    df.columns = ["Date", "Forecast"]

    fig = px.line(df, x="Date", y="Forecast", title="Next 30 Days Forecast of Outgoing Expenses", markers=True)
    fig.update_traces(fill="tozeroy")
    return fig


def main():
    st.set_page_config(page_title="Financial Data Analyser", layout="wide")
    st.title("💰 Financial Data Analyser")

    uploaded_file = st.file_uploader("Upload your financial data (Excel)", type=["xlsx"])

    if uploaded_file is not None:
        raw_data = pd.read_excel(uploaded_file)
        financial_data = Data(None)
        financial_data.data = raw_data
        financial_data.preprocess_data()

        df = financial_data.data.copy()

        st.sidebar.header("Filters")
        what = st.sidebar.radio("Transaction Type", ["all", "outgoing", "incoming"])

        if what == "outgoing":
            newdata = df[df["Betrag"] < 0].copy()
        elif what == "incoming":
            newdata = df[df["Betrag"] > 0].copy()
        else:
            newdata = df.copy()

        total_expenses = abs(df[df["Betrag"] < 0]["Betrag"].sum())
        total_income = df[df["Betrag"] > 0]["Betrag"].sum()
        current_balance = df["Betrag"].sum()
        avg_transaction = df["Betrag"].mean()
        unique_categories = df["Kategorie"].nunique()

        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Transactions", len(df))
        c2.metric("Expenses", f"{total_expenses:.2f} €")
        c3.metric("Income", f"{total_income:.2f} €")
        c4.metric("Current Balance", f"{current_balance:.2f} €")
        c5.metric("Categories", unique_categories)

        st.divider()

        left, right = st.columns(2)
        with left:
            st.plotly_chart(plot_cumulative_cashflow(newdata), use_container_width=True)
        with right:
            st.plotly_chart(plot_monthly_income_vs_expense(df), use_container_width=True)

        st.divider()

        left, right = st.columns(2)
        with left:
            st.plotly_chart(monthly_category_spending_chart(df), use_container_width=True)
        with right:
            st.plotly_chart(plot_top_categories(df), use_container_width=True)

        st.divider()

        method_counts, each_method_sum = financial_data.Method_of_payements(newdata)

        left, right = st.columns(2)
        with left:
            st.plotly_chart(payment_method_pie_chart(method_counts), use_container_width=True)
        with right:
            st.plotly_chart(payment_method_amount_chart(each_method_sum), use_container_width=True)

        st.divider()

        st.subheader("🔮 Expense Forecast")
        try:
            model = SARIMAModel()
            model.fit(data=df[df["Betrag"] < 0].copy())
            forecast = model.predict(steps=30)

            if forecast is not None:
                st.plotly_chart(forecast_chart(forecast), use_container_width=True)

                f1, f2, f3 = st.columns(3)
                f1.metric("Predicted Total", f"{forecast.sum():.2f} €")
                f2.metric("Average Daily Forecast", f"{forecast.mean():.2f} €")
                f3.metric("Highest Predicted Day", f"{forecast.max():.2f} €")
        except Exception as e:
            st.error(f"Forecast error: {e}")

        st.divider()
        st.subheader("Filtered Data")
        st.dataframe(newdata, use_container_width=True)


if __name__ == "__main__":
    main()