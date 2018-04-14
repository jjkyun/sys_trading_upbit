import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pprint import pprint

def ChangeDateFormat(unixtime):
    return pd.to_datetime(unixtime, unit='s')

def LoadBitcoinData():
    df = pd.read_csv('../2018-03-18/bitcoin.csv').drop_duplicates()
    df['last_updated'] = df['last_updated'].apply(ChangeDateFormat)
    df = df.set_index('last_updated')
    df = df.reindex(df.index.rename('date'))
    return df

def MakeMovingAverageDF(df):
    price_usd_series = df['price_usd']
    moving_average_df = pd.DataFrame(price_usd_series)
    moving_average_df.columns = [1]
    for size in range(2, 61):
        moving_average_df[size] = price_usd_series.rolling(window=size).mean()

    return moving_average_df

def GoldenDeadCrossAlgorithm(aver_start, aver_end, df):
    old_status = 'sell'
    new_status = 'sell'

    money = 100000000 # 종잣돈
    first_money = money
    bitcoin = 0 # 비트코인 갯수
    last_money = 0

    for index, row in df.iterrows():
        if row[aver_start] > row[aver_end]:
            new_status = 'buy'
        elif row[aver_end] > row[aver_start]:
            new_status = 'sell'

        if old_status != new_status:
            # dead cross
            if new_status == 'sell':
                gain = bitcoin * row[1]
                money += gain
                bitcoin = 0

            # golden cross
            else:
                last_money = money
                bitcoin = money // row[1]
                money -= bitcoin * row[1]

        old_status = new_status


    profit = money - first_money + bitcoin * int(df.tail(1)[1])
    profit_ratio = profit / first_money * 100


    print('이평 [' + str(aver_start) + ',' + str(aver_end) + ']: ' + str(profit) + ' ' + str(profit_ratio) + '%')

if __name__ == '__main__':
    df = LoadBitcoinData()
    minute_data = dict({
        '5-min': df.copy(),
        '15-min': df[::3],
        '30-min': df[::6],
        '60-min': df[::12],
        })

    start = 1
    end = 59
    for key, value in minute_data.items():
        print(key, '-------------------------------------------')
        madf = MakeMovingAverageDF(value)
        for inner_start in range(start, end + 1):
            for inner_end in range(inner_start + 1, end + 2):
                GoldenDeadCrossAlgorithm(inner_start, inner_end, madf)
