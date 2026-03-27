import sys
import pandas as pd
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.statespace.sarimax import SARIMAX

from financial_data_analyser.data import Data


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
            df["Buchungstag"] = pd.to_datetime(df["Buchungstag"])
            df = df.sort_values("Buchungstag")

            ts = df.groupby("Buchungstag")["Betrag"].sum()
            ts = ts.asfreq("D").fillna(0)

            self.ts = ts

            result = adfuller(ts)
            print("ADF p-value:", result[1])

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
            return self.results.forecast(steps=steps)
        except Exception as e:
            print(f"Error making predictions: {e}")
            return None


def main():
    if len(sys.argv) < 2:
        print("Please provide the path to the financial data file.")
        sys.exit(1)

    data_obj = Data(sys.argv[1])
    data_obj.load_data()
    data_obj.preprocess_data()

    sarima_model = SARIMAModel()
    sarima_model.fit(data_obj.data)

    forecast = sarima_model.predict(steps=30)
    print("Next 30 days forecast:")
    print(forecast)


if __name__ == "__main__":
    main()