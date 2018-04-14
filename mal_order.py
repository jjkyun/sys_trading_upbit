'''
Utilizing Moving Average Line in Bitcoin:: 정배열
@ Jae Kyun Kim
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pprint import pprint

def ChangeDateFormat(unixtime):
    return pd.to_datetime(unixtime, unit='s')

## Loading Bitcion Data and set date as index
def LoadBitcoinData():
    df = pd.read_csv('bitcoin.csv').drop_duplicates()
    df['last_updated'] = df['last_updated'].apply(ChangeDateFormat)
    df = df.set_index('last_updated')
    df = df.reindex(df.index.rename('date'))

    return df

def MakeMovingAverageLine(df):
    price_usd_series = df['price_usd']
    moving_average_df = pd.DataFrame(price_usd_series)
    moving_average_df.columns = [1]
    ## Made 5, 15, 30, 60, 120 MAL with 5 min data
    for size in [3, 6, 12, 24, 48, 144, 288, 432, 576]:
        moving_average_df[size] = price_usd_series.rolling(window=size).mean()

    return moving_average_df


'''
1. Catch the Order of Moving Averge lines
2. Invest 80000000 won at the time
'''
def MalInOrderAlgorithm(df):
    ## Removing all rows including NaN
    df = df.dropna()

    ## Sell, Buy signal
    old_status = 'sell'
    new_status = 'sell'

    seed_money = 100000000 # 1억원 in KRW
    invest_money = 80000000 # 8천만원 in KRW 
    saving_account = 20000000 
    last_money = invest_money
    bitcoin_amount = 0

    success = 0
    fail = 0
    
    for index, row in df.iterrows():
        ## if MAL is in order: BUY
        if row[6] < row[12] and row[12] < row[24] and row[24] < row[48] and row[48] < row[144] and row[144] < row[288] and row[288] < row[432]:
            new_status = 'buy'            
        else:
            new_status = 'sell'

        ## can't SELL at first time AND can't do transaction in same status
        if old_status != new_status:
            if new_status == 'buy':
                bitcoin_amount = last_money // row[1]
                last_money = 0
                print(index, " 매수 가격: ", row[1])
                buy_price = row[1]

            elif new_status == 'sell':
                profit = bitcoin_amount * row[1]
                last_money = profit
                bitcoin_amount = 0
                seed_money += (last_money - invest_money)
                seed_money -= seed_money*0.00085
                sell_price = row[1]
                
                if buy_price < sell_price:
                    success += 1
                else:
                    fail += 1

                print(index, "매도 가격: ", row[1])
                print("수익률: ", last_money/invest_money, "시드머니: ", seed_money, "\n")

                ## Check if last_money is lower than 80000000 
                if last_money <= invest_money:
                    saving_account = saving_account - (invest_money - last_money)
                    last_money = invest_money
                    if saving_account < 0:
                        print("\n 신용 등급이 위험해질 수도 있다.. ")
                        exit()
                else:
                    saving_account = saving_account + (last_money - invest_money)
                    last_money = invest_money
            
            

        old_status = new_status
       
    print("익절: ", success, "\n손절 :", fail)    
        



if __name__ == '__main__':
    df = LoadBitcoinData()
    
    ## raw data is 5 min
    minute_data = dict({
        '5-min': df.copy(),
        '15-min': df[::3],
        '30-min': df[::6],
        '60-min': df[::12],
        '120-min': df[::24]
    })

    ## Using the smallest data:: 5min
    mal = MakeMovingAverageLine(minute_data['5-min'])
    MalInOrderAlgorithm(mal)