import pandas as pd
import numpy as np
import os 
import sys

class Data:
    def __init__(self, path):
        self.path = path
        self.data = None

    def load_data(self):
        if self.path.endswith('.xlsx'):
            try:
                self.data = pd.read_excel(self.path)
                print("Data loaded successfully.")
            except Exception as e:
                print(f"Error loading data: {e}")
                sys.exit(1)
        else:
            try:
                self.data = pd.read_excel(self.path,engine='latin-1')
                print("Data loaded successfully.")
            except Exception as e:
                print(f"Error loading data: {e}")
                sys.exit(1)

    def preprocess_data(self):
        if self.data is not None:
            # Example preprocessing steps
            self.data.dropna(inplace=True)  # Remove missing values
            self.data['Buchungstag'] = pd.to_datetime(self.data['Buchungstag'], format="%d.%m.%y")  # Convert date column to datetime
            self.data['Betrag'] = self.data['Betrag'].astype(str).str.replace(',', '.').astype(float)
            print("Data preprocessed successfully.")
        else:
            print("Data not loaded. Please load data before preprocessing.")
    
    def Method_of_payements(self,newdata=None):
        if newdata is None:
            newdata=self.data
        try:
            # Example method of payments analysis
            method_counts = newdata['Method of Payement'].value_counts()
            each_method_sum=newdata.groupby('Method of Payement')['Betrag'].sum()
            # Method of payement for each category
            MPFEK=newdata.groupby(['Method of Payement','Kategorie'])['Betrag'].sum().unstack(fill_value=0)
            return method_counts,each_method_sum
        except Exception as e:
            print(f"Error analyzing method of payments: {e}")
            return None, None
    
    def monthly_expenses(self, newdata=None):
        if newdata is None:
            newdata = self.data
        try:
            transactions_by_month = newdata.groupby(newdata['Buchungstag'].dt.to_period('M')).size()
            expenenses_by_month = newdata.groupby(newdata['Buchungstag'].dt.to_period('M'))['Betrag'].sum()
            average_expenses_by_month = newdata.groupby(newdata['Buchungstag'].dt.to_period('M'))['Betrag'].mean()
            return transactions_by_month, expenenses_by_month, average_expenses_by_month
        except Exception as e:
            print(f"Error analyzing monthly expenses: {e}")
            return None, None, None
        
    def category_analysis(self, newdata=None):
        if newdata is None:
            newdata = self.data
        try:
            category_counts = newdata['Kategorie'].value_counts()
            each_category_sum = newdata.groupby('Kategorie')['Betrag'].sum()
            ECEMP = newdata.groupby(['Kategorie', 'Method of Payement'])['Betrag'].sum().unstack(fill_value=0)
            ECEM = newdata.groupby(['Kategorie', newdata['Buchungstag'].dt.to_period('M')])['Betrag'].sum().unstack(fill_value=0)
            return category_counts, each_category_sum.sort_values(ascending=False), ECEMP, ECEM
        except Exception as e:
            print(f"Error analyzing categories: {e}")
            return None, None, None, None
    

if __name__ == "__main__":
    data_path = '/Users/arpitagrawal/Desktop/Resume Projects/Financial_Data_Analyser/sample.xlsx'  # Update this path to your actual data file
    financial_data = Data(data_path)
    financial_data.load_data()
    financial_data.preprocess_data()

    transactions_by_month, expenenses_by_month, average_expenses_by_month=financial_data.monthly_expenses()
    method_counts,each_method_sum=financial_data.Method_of_payements()
    print("Transactions by Month:")
    print(transactions_by_month)
    print("\nExpenses by Month:")
    print(expenenses_by_month)
    print("\nAverage Expenses by Month:")
    print(average_expenses_by_month)
    print("\nMethod of Payments Counts:")
    print(method_counts)
    print("\nSum of Amount by Method of Payments:")
    print(each_method_sum)

    