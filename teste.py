# pip install streamlit fbprophet yfinance plotly
import streamlit as st
from datetime import date

import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go
import cx_Oracle
import sys

lib_dir = r"D:\oracle\instantclient_21_12"

START = "2015-01-01"
TODAY = date.today().strftime("%Y-%m-%d")    

st.title('Previsão de E-Commerce.')

stocks = ('AMZN', 'BABA', 'MELI', 'EBAY')
selected_stock = st.selectbox('Selecione o database para predição', stocks)

n_years = st.slider('Anos de predição:', 1, 4)
period = n_years * 365

@st.cache_data
def load_data(ticker):
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace=True)
    return data

data_load_state = st.text('Carregando data...')
data = load_data(selected_stock)
data_load_state.text('Carregando data... feito!')

st.subheader('Raw data')
st.write(data.tail())

# Plot raw data
def plot_raw_data():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="e-commerce_open"))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="e-commerce_close"))
    fig.layout.update(title_text='Time Series data with Rangeslider', xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)

plot_raw_data()

# Predict forecast with Prophet.
df_train = data[['Date','Close']]
df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

m = Prophet()
m.fit(df_train)
future = m.make_future_dataframe(periods=period)
forecast = m.predict(future)

# Show and plot forecast
st.subheader('Forecast data')
st.write(forecast.tail())

st.write(f'Forecast plot for {n_years} years')
fig1 = plot_plotly(m, forecast)
st.plotly_chart(fig1)

st.write("Forecast components")
fig2 = m.plot_components(forecast)
st.write(fig2)

# Option to insert forecast data into Oracle database
if st.button('Inserir previsões no banco de dados Oracle'):
    try:
        cx_Oracle.init_oracle_client(lib_dir=lib_dir)
        dsn = cx_Oracle.makedsn("oracle.fiap.com.br", 1521, service_name="orcl")
        connection = cx_Oracle.connect(user="rm551857", password="260804", dsn=dsn)
        cursor = connection.cursor()
        
        for index, row in forecast.iterrows():
            data_pred = (row['ds'], row['yhat'])
            cursor.callproc("proc_forecast", data_pred)
        
        connection.commit()
        st.write("Previsões inseridas com sucesso.")
    except cx_Oracle.DatabaseError as e:
        connection.rollback()
        error, = e.args
        st.write("Erro:", error.message)
    finally:
        cursor.close()
        connection.close()