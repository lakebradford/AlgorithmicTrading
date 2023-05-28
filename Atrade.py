import yfinance as yf
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import datetime 


#helper function to calculate tor date 100 days prior to today
def startDate():
	tod = datetime.datetime.now()
	d = datetime.timedelta(days = 100)
	a = tod - d
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



print(retrieveFaangData())

