from matplotlib.pyplot import show
import requests
import numpy as np
import pandas as pd
import FinanceDataReader as fdr
import pandas_datareader as pdr

pd.set_option('precision', 3)

# row 생략 없이 출력
pd.set_option('display.max_rows', None)
# col 생략 없이 출력
pd.set_option('display.max_columns', None)

df_kumho_petroleum = fdr.DataReader('011780','2003-06-01','2022-02-03')
#len(df_kumho_petroleum)

#데이터 전처리(각 월의 1일 추출 / 만약 1일이 없으면(일요일,토요일일 경우 주식 데이터 없음) 2일 또는 3일 데이터를 가져옴)
#문제1 공휴일이 끼어있는 경우 특정이 힘듬
#실제로 하나가 비는데 어쩌냐 이거
df_kumho_petroleum = df_kumho_petroleum.loc[(df_kumho_petroleum.index.is_month_start == True) | 
((df_kumho_petroleum.index.is_month_start == False) & (df_kumho_petroleum.index.day == 2)) |
((df_kumho_petroleum.index.is_month_start == False) & (df_kumho_petroleum.index.day == 3)) |
((df_kumho_petroleum.index.is_month_start == False) & (df_kumho_petroleum.index.day == 4)) |
((df_kumho_petroleum.index.is_month_start == False) & (df_kumho_petroleum.index.day == 5)) |
((df_kumho_petroleum.index.is_month_start == False) & (df_kumho_petroleum.index.day == 6))
]

i = 0
length_df = len(df_kumho_petroleum)
idx = 1
while i < length_df-1:
  if df_kumho_petroleum.index[idx].month == df_kumho_petroleum.index[idx-1].month:
    df_kumho_petroleum = df_kumho_petroleum.drop(index=df_kumho_petroleum.index[idx],axis=0)
    idx = idx-1
  idx = idx+1
  i = i+1

# 듀바이유(Dubai Crude), monthly
db_df = pdr.DataReader('POILDUBUSDM', 'fred', start='2003-06-01' , end='2022-02-03')

db_df = db_df.drop([db_df.index[173]])
df_compare_kumho = df_kumho_petroleum[0:221]
print(len(df_compare_kumho))

df_compare_kumho_open = np.array(df_compare_kumho['Open'])[:]
db_df_price = np.array(db_df['POILDUBUSDM'])[:]

compareater2_df = pd.DataFrame({'Open':df_compare_kumho_open[:],'POILDUBUSDM':db_df_price[:]},index=np.arange(len(df_compare_kumho_open)))
print(compareater2_df.corr())

df_butadiene = pd.read_csv('C:/Users/rurip/Desktop/finance/butadiene.csv')
# df의 처음 5행을 표시
#print(df_butadiene.head(5))

print(df_kumho_petroleum)

kumho_petroleum_op = np.array(df_kumho_petroleum['Open'])[:]
df_butadiene_price = np.array(df_butadiene['price'])[:]

#print(len(kumho_petroleum_op))
#print(len(df_butadiene_price))
compareater_df = pd.DataFrame({'Open':kumho_petroleum_op[:],'price':df_butadiene_price[:]},index=np.arange(len(df_kumho_petroleum)))
#print(compareater_df.corr())

#print(df_kumho_petroleum)
###################################################

df_lg_chem = fdr.DataReader('051910','2003-06-01','2022-02-03')
#len(df_kumho_petroleum)

#데이터 전처리(각 월의 1일 추출 / 만약 1일이 없으면(일요일,토요일일 경우 주식 데이터 없음) 2일 또는 3일 데이터를 가져옴)
#문제1 공휴일이 끼어있는 경우 특정이 힘듬
#실제로 하나가 비는데 어쩌냐 이거
#print(df_lg_chem)

# df_lg_chem = df_lg_chem.loc[(df_lg_chem.index.is_month_start == True) | 
# ((df_lg_chem.index.is_month_start == False) & (df_lg_chem.index.day == 2)) |
# ((df_lg_chem.index.is_month_start == False) & (df_lg_chem.index.day == 3)) |
# ((df_lg_chem.index.is_month_start == False) & (df_lg_chem.index.day == 4)) |
# ((df_lg_chem.index.is_month_start == False) & (df_lg_chem.index.day == 5)) |
# ((df_lg_chem.index.is_month_start == False) & (df_lg_chem.index.day == 6))
# ]

# i = 0
# length_df = len(df_lg_chem)
# idx = 1
# while i < length_df-1:
#   if df_lg_chem.index[idx].month == df_lg_chem.index[idx-1].month:
#     df_lg_chem = df_lg_chem.drop(index=df_lg_chem.index[idx],axis=0)
#     idx = idx-1
#   idx = idx+1
#   i = i+1
  

# df_butadiene = pd.read_csv('C:/Users/rurip/Desktop/finance/butadiene.csv')

# lg_chem_op = np.array(df_lg_chem['Open'])[:]
# df_butadiene_price = np.array(df_butadiene['price'])[:]

#print(len(lg_chem_op))
#print(len(df_butadiene_price))
compareater2_df = pd.DataFrame({'Open':lg_chem_op[:],'price':df_butadiene_price[:]},index=np.arange(len(df_lg_chem)))
#print(compareater2_df.corr())