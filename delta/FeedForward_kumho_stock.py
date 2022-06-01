from datetime import datetime
from msilib import sequence
from sklearn.model_selection import train_test_split
import torch
import pandas as pd
import re
import torch.nn.functional as F
import torch.nn as nn
#from sklearn.preprocessing import QuantileTransformer
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import Ridge
import FinanceDataReader as fdr
import requests
from bs4 import BeautifulSoup
import os
import sys
import urllib.request
import torch.optim as optim
import numpy as np
import matplotlib.pyplot as plt
import json
import warnings

warnings.filterwarnings(action='ignore')

# Random seed to make results deterministic and reproducible
torch.manual_seed(0)

# 1. Hyper Parameter
input_dim = 3
hidden_dim = 10
sequence_size = 5
layer_size = 1
output_dim = 1
learning_rate = 0.01


#환율 데이터 전처리(csv 파일 읽고 date 칼럼을 datetime64로 형변환)
df_exchange = fdr.DataReader('USD/KRW', '2010')
df_exchange = df_exchange.reset_index(drop=False)
df_exchange.rename(columns={'Date':'date'},inplace=True)
df_exchange['exchange_price'] = (df_exchange['High'] + df_exchange['Low']) / 2
df_exchange = df_exchange.drop(['Open','High','Low','Change','Close'],axis=1)

#두바이 오일 전처리 (csv 파일 읽고 date 칼럼을 datetime64로 형변환 / oil값이 0이면 제거)
df_dubai_oil = pd.read_csv('C:/Users/rurip/Desktop/stock_analysis/coding/alpha/dubai_oil.csv')

for i in range(0,len(df_dubai_oil)):
    df_dubai_oil.iat[i,1] = pd.to_datetime(datetime.strptime(df_dubai_oil.loc[i]['date'],"%Y-%m-%d"))

df_dubai_oil = df_dubai_oil.drop(df_dubai_oil.columns[0],axis=1)
df_dubai_oil.rename(columns={'price':'oil_price'},inplace=True)
df_dubai_oil['date'] = df_dubai_oil['date'].astype('datetime64')
df_dubai_oil = df_dubai_oil.drop(df_dubai_oil[df_dubai_oil['oil_price'] == 0].index)
#print(df_dubai_oil.dtypes)

#금호 석유 주가 (High,Low 가격의 평균치를 price로 설정/ date와 price를 제외한 나머지 열 제거 )
df_kumho_petroleum = fdr.DataReader('011780','2010-01-01','2022-04-23')
df_kumho_petroleum['price_kumho_prtroleum'] = (df_kumho_petroleum['High'] + df_kumho_petroleum['Low']) / 2
df_kumho_petroleum = df_kumho_petroleum.drop(['Open','High','Low','Volume','Change','Close'],axis=1)
df_kumho_petroleum['date'] = df_kumho_petroleum.index
df_kumho_petroleum = df_kumho_petroleum.reset_index(drop=True)


#inner join / key = date / 날짜가 겹치는 날의 데이터를 병합
merge_val = pd.merge(df_dubai_oil,df_kumho_petroleum,on='date')
merge_val = pd.merge(merge_val,df_exchange,on='date')
merge_val.sort_values('date')

#oil price를 달러/배럴 -> 원/리터 로 변환
merge_val['oil_price_won'] = merge_val['oil_price'] * merge_val['exchange_price'] / 158.987
merge_val = merge_val.drop(['exchange_price','oil_price'],axis=1)
#print(merge_val)

#네이버 API 키워드 검색 데이터 불러오기
client_id = "GfGQDa_FOTVxq9Zd0Pm5"
client_secret = "umNZPmOMGo"
url = "https://openapi.naver.com/v1/datalab/search";
today = datetime.today().date()
#print(today)
body = "{\"startDate\":\"2016-01-01\",\"endDate\":"+"\"{}\"".format(today)+",\"timeUnit\":\"date\",\"keywordGroups\":[{\"groupName\":\"금호석유\",\"keywords\":[\"금호석유\",\"kumho_petroleum\",\"금호석유화학\"]}]}"
#{\"groupName\":\"합성고무\"\",\"keywords\":[\"합성고무\",\"합성고무 가격인상\",\"부타디엔 가격 인상\"]}

request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id",client_id)
request.add_header("X-Naver-Client-Secret",client_secret)
request.add_header("Content-Type","application/json")
response = urllib.request.urlopen(request, data=body.encode("utf-8"))
rescode = response.getcode()
if(rescode==200):
    response_body = response.read()
    #print(response_body.decode('utf-8'))
    search_count = response_body.decode('utf-8')
else:
    print("Error Code:" + rescode)

search_count_json = json.loads(search_count)

df_json = pd.DataFrame(search_count_json["results"][0]["data"])
df_json.columns = ['date', 'kumho_search_count']
df_json['date'] = pd.to_datetime(df_json['date'])

body = "{\"startDate\":\"2016-01-01\",\"endDate\":"+"\"{}\"".format(today)+",\"timeUnit\":\"date\",\"keywordGroups\":[{\"groupName\":\"합성고무\",\"keywords\":[\"합성고무\",\"합성고무 가격인상\",\"부타디엔 가격 인상\"]}]}"

request2 = urllib.request.Request(url)
request2.add_header("X-Naver-Client-Id",client_id)
request2.add_header("X-Naver-Client-Secret",client_secret)
request2.add_header("Content-Type","application/json")
response = urllib.request.urlopen(request2, data=body.encode("utf-8"))
rescode = response.getcode()
if(rescode==200):
    response_body = response.read()
    #print(response_body.decode('utf-8'))
    search_count = response_body.decode('utf-8')
else:
    print("Error Code:" + rescode)

search_count_json = json.loads(search_count)

df2_json = pd.DataFrame(search_count_json["results"][0]["data"])
df2_json.columns = ['date', 'rubber_search_count']
df2_json['date'] = pd.to_datetime(df2_json['date'])

merge_df = pd.merge(df_json,df2_json,on='date')
merge_df.sort_values('date')

merge_val = pd.merge(merge_val,merge_df,on='date')
merge_val.sort_values('date')

#데이터 정규화 MinMaxScaler
scalerx = MinMaxScaler()
scalery = MinMaxScaler()

merge_val[['oil_price_won','kumho_search_count','rubber_search_count']] = scalerx.fit_transform(merge_val[['oil_price_won','kumho_search_count','rubber_search_count']])
merge_val[['price_kumho_prtroleum']] = scalery.fit_transform(merge_val[['price_kumho_prtroleum']])

seq_x = []
seq_y = []
num_days = 4
feature_list = ['oil_price_won','kumho_search_count','rubber_search_count']

s_idx=0
e_idx=len(merge_val)
date_interval = 1 
for idx in range(s_idx,e_idx,date_interval):
    x = merge_val.loc[idx:idx+num_days][feature_list].to_numpy().tolist()
    y = merge_val.loc[idx:idx+num_days]['price_kumho_prtroleum'].to_numpy().tolist()

    seq_x.append(x) if len(x) == 5 else None
    seq_y.append(y) if len(x) == 5 else None
    

train_x,test_x,train_y,test_y = train_test_split(seq_x,seq_y,test_size=0.2)

class RNNModel(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim,num_layer = 1 ):
        super(RNNModel, self).__init__()
        self.rnn = torch.nn.RNN(input_dim, hidden_dim,num_layers = num_layer,batch_first =True)
        self.linear_classifier = torch.nn.Linear(hidden_dim,output_dim,bias=True)
    def forward(self, x):
        x, _ = self.rnn(x.unsqueeze(0))
        print("rnn_out_;ast_layer", x[:,-1])
        x = self.linear_classifier(x)
        print("classfierX : ",x,x.size())
        return x
      
model = RNNModel(input_dim,hidden_dim,output_dim)
loss_function = torch.nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(),lr=learning_rate)

def train(train_x,train_y, loss_function, optimizer,model):
    total_loss = []

    for idx in range(len(train_x)):
        model.train()
        optimizer.zero_grad()
        train_x_tensor = torch.tensor(train_x[idx]).float()
        train_y_tensor = torch.tensor(train_y[idx]).float()
        logit = model(train_x_tensor)
        loss = loss_function(logit,train_y_tensor)

        loss.backward()
        optimizer.step()

    return total_loss

best_model = None
nb_epochs = 10
loss_epoch = []
for epoch in range(nb_epochs):
    loss_list = train(train_x,train_y,loss_function,optimizer,model)
    loss_epoch.append(sum(loss_list)/len(train_x))


#원유 가격 크롤링 #https://www.opinet.co.kr/gloptotSelect.do #opinet
url = 'https://www.opinet.co.kr/gloptotSelect.do'

response = requests.get(url)

if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.select_one('#tbody1 > tr > td:nth-of-type(1) > p')
    title2 = title.get_text().split()

state = title2[1]
price = float(title2[3])
date_oil = title2[5]

#제공받은 원유 가격 / 날짜 출력
print(date_oil,'원유 가격 : ',price)
price = torch.FloatTensor([price])
price = price.view([-1,1])

new_var =  torch.FloatTensor(scalerx.transform([[price,merge_df.iloc[-1][1],merge_df.iloc[-1][2]]]))
# 입력한 값 price에 대해서 예측값 y를 리턴받아서 pred_y에 저장
pred_y = model(new_var) # forward 연산

#네이버 금융에서 현재가 크롤링
url = 'https://finance.naver.com/item/main.naver?code=011780'

response = requests.get(url)

if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.select_one('#chart_area > div.rate_info > div > p.no_today')
    now_kumho_price = title.get_text().split()

#예측값 출력
print("예측값 : ", scalery.inverse_transform(pred_y.detach())[0][0])
print("현재가 : ", now_kumho_price[0])

input("Press enter to exit ;)")