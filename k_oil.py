import torch
import torch.optim as optim
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import urllib.request
import json
import re
import torch.nn.functional as F
import torch.nn as nn
#from sklearn.preprocessing import QuantileTransformer
from sklearn.preprocessing import MinMaxScaler
# Random seed to make results deterministic and reproducible
torch.manual_seed(0)
import pandas_datareader as pdr

import string
import requests
from bs4 import BeautifulSoup


#금호 석유 가격 가져오기
import FinanceDataReader as fdr
df_krx = fdr.StockListing('KRX')
df_krx.head()

df_kumho_petroleum = fdr.DataReader('011780','2003-06-01','2022-02-03')

#매 월 1일 데이터 가져옴 / 주말이나 공휴일이라 가져오지 못하면 다음 날 데이터로 가져옴
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

df_exchange = pd.read_csv('C:/Users/rurip/Desktop/finance/exchange.csv')

print(len(df_exchange))

# 두바이유(Dubai Crude), monthly
# 1배럴당 usd
# 1배럴 = 158.987 리터

# 1배럴당 달러니깐 이걸 리터로 바꾸고 원으로 다시 바꿔야함;;;
# 환율 데이터 가져와서 곱하고 다시 리터로 나누면 될 듯
db_df = pdr.DataReader('POILDUBUSDM', 'fred', start='2003-06-01' , end='2022-02-03')

db_df = db_df.drop([db_df.index[173]])
df_kumho_petroleum = df_kumho_petroleum[0:221]

db_df_poildbubusdm = np.array(db_df['POILDUBUSDM'])[:]
df_exchange_exchange = np.array(df_exchange['exchange'])[:]

db_price_liter_won = db_df_poildbubusdm * df_exchange_exchange / 158.987

scalerx = MinMaxScaler()
scalery = MinMaxScaler()
# 데이터

x_train = torch.tensor(db_price_liter_won)
x_train = x_train.view([-1,1])
x_train = x_train.float()
scalerx.fit(x_train)
x_train = scalerx.transform(x_train)
x_train = torch.FloatTensor(x_train)

y_train = torch.tensor(df_kumho_petroleum["Open"].values)
y_train = y_train.view([-1,1])
y_train = y_train.float()
scalery.fit(y_train)
y_train = scalery.transform(y_train)
y_train = torch.FloatTensor(y_train)

class LinearRegressionModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = nn.Linear(1, 1)

    def forward(self, x):
        return self.linear(x)
model = LinearRegressionModel()
# optimizer 설정. 경사 하강법 SGD를 사용하고 learning rate를 의미하는 lr은 0.01
optimizer = torch.optim.SGD(model.parameters(), lr=0.01) 
# 전체 훈련 데이터에 대해 경사 하강법을 2,000회 반복
nb_epochs = 15000
for epoch in range(nb_epochs+1):

    # H(x) 계산
    prediction = model(x_train)

    # cost 계산
    cost = F.mse_loss(prediction, y_train) # <== 파이토치에서 제공하는 평균 제곱 오차 함수

    # cost로 H(x) 개선하는 부분
    # gradient를 0으로 초기화
    optimizer.zero_grad()
    # 비용 함수를 미분하여 gradient 계산
    cost.backward() # backward 연산
    # W와 b를 업데이트
    optimizer.step()

    if epoch % 100 == 0:
    # 100번마다 로그 출력
      print('Epoch {:4d}/{} Cost: {:.6f}'.format(
          epoch, nb_epochs, cost.item()
      ))

print(list(model.parameters()))


url = 'https://www.opinet.co.kr/gloptotSelect.do'

response = requests.get(url)

if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.select_one('#tbody1 > tr > td:nth-child(1) > p')
    title2 = title.get_text().split()

#원유 가격 크롤링 #https://www.opinet.co.kr/gloptotSelect.do #opinet

state = title2[1]
price = float(title2[3])
date_oil = title2[5]
price = torch.FloatTensor([price])
price = price.view([-1,1])
print(price)

# 사이트에서 가져온 원유 가격 출력
new_var =  torch.FloatTensor(scalerx.transform(price))
# 입력한 값 price에 대해서 예측값 y를 리턴받아서 pred_y에 저장
pred_y = model(new_var) # forward 연산

#예측값  출력
print(date_oil)
print("예측값 :", scalery.inverse_transform(pred_y.detach()))
