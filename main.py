import pandas as pd 
import numpy as np
from datetime import datetime as dt
from get_data import *
from utils import *
VERSION = "1.0.0"


#connect to portfolio data
connect()
sqlalchemy_engine()
db = get_portfolio_data()

#create classes
class Stock:

    def __init__(self, ticker: str,  period_in_months = 3):

        #get stock data
        print("Retriewing stock data ...")
        end = dt.now()
        start = period_finder(end, period_in_months)
        self.ticker = ticker
        prices = yf.download(ticker, start=start, end=end)
        
        #calculating metrics
        print("Calculating risk metrics ...")
        self.returns = pd.DataFrame(prices['Close'])
        self.cum_returns = (self.returns+1).cumprod() - 1
        self.er = expected_return(self.returns)
        self.volatility = volatility(self.returns)
        self.sharpe = sharpe(self.returns)
        self.skew = skew(self.returns)
        self.kurtosis = kurtosis(self.returns)
        #self.sortino_ratio = sortino_ratio(self.returns)
        self.var = var(self.returns)
        self.cvar = cvar(self.returns)
        #self.win_rate = win_rate(self.returns)
        self.tail_ratio = tail_ratio(self.returns)
        #self.kelly_criterion = kelly_criterion(self.returns)

        #create metrics data frame

        self.basic_risk_metrics = pd.Series({
            "Expected Returns" : self.er,
            "Total Cummulative Returns" : self.cum_returns.loc[max(self.cum_returns.index)].values[0],
            "Volatiliy" : self.volatility,
            "Sharpe Ratio" : self.sharpe,
            "Skewness" : self.skew,
            "Kurtosis" : self.kurtosis,
            #"Sortino Ratio" : self.sortino_ratio,
            #"Win Rate" : self.win_rate,
            "Tail Ratio" : self.tail_ratio
            #"Kelly Criterion" : self.kelly_criterion
        },
        name = self.ticker)
        


        print("Initialization sucessful!")

    def return_destribution_chart():
        pass

    def historical_returns_bm():
        pass

    def portfolio_influence_bm():
        pass


if __name__ == "__main__":

    running = True
    print(f"\nWelcome to the PMC stock screening tool. (Version: {VERSION})\n")

    ticker = input("Provide a stock ticker to be analysed: ")
    stock = Stock(ticker)


    while running == True:

        #main menu
        print("\nPlease select you desired action:\n")
        print("1 - Basic Risk and Return Metrics")
        print("2 - Value at Risk Table")
        print("3 - Exit")

        valid_options = [1,2]
        option = int(input("\nSelection: "))

        if option == 1:
            print("\nThe basic risk metrics are the following:\n")
            print(stock.basic_risk_metrics)

        elif option == 2:
            pass

        elif option == 3:
            print("\nGood Bye. Until next time!")
            running = False

        else:
            print("Please select a valid option. Option must be passed in as an interger.")








