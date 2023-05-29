import yfinance as yf
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import datetime 
import os


#prices of the stocks for today (or most recent busness day)
priceToday = {}
#moving averages starting from today (or most recent business day) and ending 100 days prior
movingAveragesMap = {}



#helper function to calculate tor date 100 BUSINESS days prior to today
def startDate():
	daysBetween = 100
	tod = datetime.datetime.now()
	print(f"Today: {tod}")
	d = datetime.timedelta(days = daysBetween)
	a = tod - d
	print(np.busday_count(a.strftime('%Y-%m-%d'),tod.strftime('%Y-%m-%d')))
	while np.busday_count(a.strftime('%Y-%m-%d'),tod.strftime('%Y-%m-%d')) != 100:
		daysBetween = daysBetween + 1
		d = datetime.timedelta(days = daysBetween)
		a = tod - d
	print()

	return a


def retrieveFaangData():
	#Retrieve price data of FAANG Companies and converts it into a CSV file
	# facebook = yf.download("META", start = startDate(), end = datetime.datetime.now())
	# apple = yf.download("AAPL", start = startDate(), end = datetime.datetime.now())
	# amazon = yf.download("AMZN", start = startDate(), end = datetime.datetime.now())
	# netflix = yf.download("NFLX", start = startDate(), end = datetime.datetime.now())
	# google = yf.download("GOOGL", start = startDate(), end = datetime.datetime.now())
	ticker = ["META","AAPL","AMZN","NFLX","GOOGL"]
	faangStocks = yf.download(ticker, start = startDate(), end = datetime.datetime.now())
	#convert into a CSV file 
	faangStocks.to_csv("faangStocks.csv")
	faangStocks = pd.read_csv("faangStocks.csv")
	faangStocks = pd.read_csv("faangStocks.csv",header = [0,1])
	faangStocks = pd.read_csv("faangStocks.csv",header = [0,1], index_col=[0])
	return faangStocks


#returns a dictionary containing each comapny (key) and its corresponding 100 day moving average (value)
def calculateMovingAverages():
	data = retrieveFaangData()
	#locate todays stock price for the stocks and add to dictionary 
	currentTradePrice = data.loc[:,"Close"].tail(1)
	name = currentTradePrice.columns
	price =currentTradePrice.to_numpy().tolist()
	#Maps current day prices to a dictionary
	for i in range(len(name)):
		priceToday[name[i]] = price[0][i]
	print(f"Todays stock Prices {priceToday}")
	#locate the closing prices of all stocks and calculate averages
	describeData = data.loc[:,"Close"].describe()
	movingAverages = describeData.iloc[1]
	# print(movingAverages)
	for rows in range(len(movingAverages.index)):
		movingAveragesMap[movingAverages.index[rows]] = movingAverages[rows]
	print(f"100 Day Moving Average: {movingAveragesMap}")
	print("\n")

	return movingAveragesMap



movingAverages = calculateMovingAverages()



#returns an array of stocks that are 5% below the moving average
def PercentDropCheck():
	print("Percentage Change between moving average and current price:")
	stocksToBuy = []
	for i in priceToday:
		#calculate the percent increase/decrease
		increase = priceToday[i] - movingAveragesMap[i]
		percentChange = increase/movingAveragesMap[i]
		percentChange = percentChange * 100
		#if the percent increase is less than 5% we buy
		print(f"{i}: {percentChange}")
		if percentChange <= 5:
			stocksToBuy.append(i)
	if len(stocksToBuy) == 0:
		print("none below 5% ")
	print("stocks to buy array: ")
	return stocksToBuy




	
print(PercentDropCheck())





os.remove('faangStocks.csv')
