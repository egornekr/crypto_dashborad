import streamlit as st
import pandas as pd
import numpy as np
import requests
import json
import plotly.express as px
import datetime
from datetime import timedelta

# ---- Настройки страницы ----

st.set_page_config(page_title='Crypto graph',
                   page_icon=':chart_with_upwards_trend:',
                   layout='wide')


# ---- SIDEBAR ----

# выбор криптовалюты
option = st.sidebar.selectbox(
    'Choose your hero',
    ('bitcoin', 'ethereum', 'monero','litecoin'))


# выбор даты
today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)

start_date, right_column = st.sidebar.columns(2)
start_date = st.sidebar.date_input('Date from', today - timedelta(days=30))
end_date = st.sidebar.date_input('Date to', today)

# проверка на корректность
if start_date < end_date:
    pass
else:
    st.error('Error: End date must fall after start date.')


# преобразуем в миллисекунды
start_millisec = pd.to_datetime(start_date).timestamp() * 1000
end_millisec = pd.to_datetime(end_date).timestamp() * 1000


# ----- Создаём запрос к API ------
payload = {}
headers = {}


url = f"http://api.coincap.io/v2/assets/{option}/history?interval=d1&start={start_millisec}&end={end_millisec}"

payload = {}
headers= {}

response = requests.request("GET", url, headers=headers, data = payload)

json_data = json.loads(response.text.encode('utf8'))

# ----- Формируем датафрейм и рисуем график ----
df = pd.DataFrame(json_data['data'])


fig = px.line(df,
              x = 'date',
              y = 'priceUsd',
              title = option+' graph',
              labels={'date': 'Date', 'priceUsd' : 'Price $(K)'}
              )
fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightPink')
fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightPink')

st.plotly_chart(fig)