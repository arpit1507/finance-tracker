import streamlit as st
from data import Data
from model import SARIMAModel
import pandas as pd
import plotly.express as px
import sys
import os

def main():
    st.title("Financial Data Analyser")
    
    # File uploader
    uploaded_file = st.file_uploader("Upload your financial data (Excel)", type=["xlsx"])
    
    if uploaded_file is not None:
        data=pd.read_excel(uploaded_file)
        financial_data = Data(None)  # Initialize with None since we will set data directly
        financial_data.data=data
        financial_data.preprocess_data()
        what = st.radio(
            "Please enter your choice",
            ["all","outgoing", "incoming"]
        )
        if what=="outgoing":
            newdata=financial_data.data[financial_data.data['Betrag']<0]
        elif what=="incoming":
            newdata=financial_data.data[financial_data.data['Betrag']>0]
        else:
            what=""
            newdata=financial_data.data
        
        graph=newdata.groupby('Buchungstag')['Betrag'].sum()
        graph = graph.sort_index()
        cumulative_graph = graph.cumsum()
        cumulative_graph.index = cumulative_graph.index.astype(str) 
        st.subheader(f"{what} Transactions Over Time")
        st.line_chart(cumulative_graph, x_label='Buchungstag', y_label='Amount')
        # Analyze data
        transactions_by_month, expenenses_by_month,_ = financial_data.monthly_expenses(newdata)
        transactions_by_month.index = transactions_by_month.index.astype(str)   
        method_counts, each_method_sum = financial_data.Method_of_payements(newdata)
        method_counts.index = method_counts.index.astype(str) 

        # Display results
        st.subheader(f"{what} Transactions by Month")
        st.bar_chart(transactions_by_month, x_label='Month', y_label='Number of Transactions')
        
        st.subheader("Expenses by Month")
        st.write(expenenses_by_month)
        
        
        fig = px.pie(
            values=method_counts.values,
            names=method_counts.index,
        )
        fig.update_traces(
            textinfo='percent+label',
            textposition='outside',
        )
        fig.update_layout(
            showlegend=False
        )
        st.subheader("Method of Payments Counts")
        st.plotly_chart(fig, use_container_width=True)
        

        st.subheader("Sum of Amount by Method of Payments")
        st.write(each_method_sum)

if __name__ == "__main__":
    main()
