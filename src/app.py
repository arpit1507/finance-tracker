import streamlit as st
from data import Data
import pandas as pd

def main():
    st.title("Financial Data Analyser")
    
    # File uploader
    uploaded_file = st.file_uploader("Upload your financial data (Excel)", type=["xlsx"])
    
    if uploaded_file is not None:
        data=pd.read_excel(uploaded_file)
        print(data)
        financial_data = Data(None)  # Initialize with None since we will set data directly
        financial_data.data=data
        financial_data.preprocess_data()
        what = st.radio(
            "Please enter your choice",
            ["outgoing", "incoming", "all"]
        )
        if what=="outgoing":
            newdata=financial_data.data[financial_data.data['Betrag']<0]
        elif what=="incoming":
            newdata=financial_data.data[financial_data.data['Betrag']>0]
        else:
            newdata=financial_data.data
        # Analyze data
        transactions_by_month, expenenses_by_month, average_expenses_by_month = financial_data.monthly_expenses(newdata)
        method_counts, each_method_sum = financial_data.Method_of_payements()
        
        # Display results
        st.subheader("Transactions by Month")
        st.bar_chart(transactions_by_month)
        
        st.subheader("Expenses by Month")
        st.write(expenenses_by_month)
        
        st.subheader("Average Expenses by Month")
        st.write(average_expenses_by_month)
        
        st.subheader("Method of Payments Counts")
        st.write(method_counts)
        
        st.subheader("Sum of Amount by Method of Payments")
        st.write(each_method_sum)

if __name__ == "__main__":
    main()

