import sys
import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.statespace.sarimax import SARIMAX
from data import Data
import matplotlib.pyplot as plt



class SARIMAModel:
    def __init__(self, order=(1, 1, 1), seasonal_order=(1, 1, 1, 7)):
        self.order = order
        self.seasonal_order = seasonal_order
        self.model = None
        self.results = None
        self.ts = None

    def fit(self, data: pd.DataFrame):
        try:
            df = data.copy()

            # Keep only outgoing expenses
            df = df[df["Betrag"] < 0].copy()

            # Convert to positive values for easier interpretation

            # Ensure date column is datetime
            df["Buchungstag"] = pd.to_datetime(df["Buchungstag"])

            # Sort by date
            df = df.sort_values("Buchungstag")

            # Aggregate daily outgoing expenses
            ts = df.groupby("Buchungstag")["Betrag"].sum()

            # Make regular daily time series
            ts = ts.asfreq("D")
            ts = ts.fillna(0)

            self.ts = ts

            # Stationarity test
            result = adfuller(ts)
            print("ADF p-value:", result[1])

            # Fit SARIMA
            self.model = SARIMAX(
                ts,
                order=self.order,
                seasonal_order=self.seasonal_order,
                enforce_stationarity=False,
                enforce_invertibility=False,
            )

            self.results = self.model.fit(disp=False)
            print("SARIMA model fitted successfully.")

        except Exception as e:
            print(f"Error fitting SARIMA model: {e}")

    def predict(self, steps=30):
        if self.results is None:
            print("Model not fitted. Please fit the model before making predictions.")
            return None

        try:
            forecast = self.results.forecast(steps=steps)
            return forecast
        except Exception as e:
            print(f"Error making predictions: {e}")
            return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the path to the financial data file.")
        sys.exit(1)

    data_obj = Data(sys.argv[1])
    data_obj.load_data()
    data_obj.preprocess_data()
    print(data_obj.data[data_obj.data["Betrag"] < 0])
    sarima_model = SARIMAModel(order=(1, 1, 1), seasonal_order=(1, 1, 1, 7))
    sarima_model.fit(data_obj.data)  # Fit model on outgoing expenses

    forecast = sarima_model.predict(steps=30)
    print("Next 30 days forecast:")
    print(forecast)
    plt.figure(figsize=(10,5))
    plt.figure(figsize=(10,5))
    plt.plot(sarima_model.ts, label="Actual")
    plt.plot(forecast, label="Forecast", color='red')
    plt.legend()
    plt.title("Outgoing Expense Forecast")
    plt.show()