import streamlit as st, pandas as pd, numpy as np, yfinance as yf
import plotly.express as px

st.title('Stock Screener')
ticker = st.sidebar.text_input('Ticker')
start_date = st.sidebar.date_input('Start Date')
end_date = st.sidebar.date_input('End Date')

data = yf.download(ticker, start=start_date, end=end_date)
fig = px.line(data, x = data.index, y = data['Adj Close'], title = ticker)
st.plotly_chart(fig)

pricing_data, fundamental_data, news, openAi= st.tabs(["Pricing Data", "Fundamental Data", "Top News"])

with pricing_data:
    st.header('Pricing Movement')
    data2 =data
    data2['%Change'] = data['Adj Close']/data['Adj Close'].shift(1)-1
    data2.dropna(inplace=True)
    st.write(data2)
    annual_return = data['%Change'].mean()*252*100
    if(annual_return>0):
        st.write(f'Annual Return is <span style = "color: green;">{annual_return}%</span>',unsafe_allow_html=True)
    else:
        st.write(f'Annual Return is <span style="color:red;">{annual_return}%</span>', unsafe_allow_html=True)

from stocknews import StockNews 
with news:
    st.header(f'News of {ticker}')
    test_ticker = 'AAPL'#only getting the first letter
    sn = StockNews(test_ticker, save_news=False)
    df_news = sn.read_rss()
    for i in range(10):
        st.header(f'News {i+1}')
        st.write(df_news['published'][i])
        st.write(df_news['title'][i])
        st.write(df_news['summary'][i])
        title_sentiment =df_news['sentiment_title'][i]
        st.write(f'Title Sentiment {title_sentiment}')
        news_sentiment =df_news['sentiment_summary'][i]
        st.write(f'News Sentiment {news_sentiment}')

from alpha_vantage.fundamentaldata import FundamentalData    #only 25 requests a day
with fundamental_data:
    key = 'EC29DMVVH2ZMV59E'
    st.write('Fundamental')
    fd = FundamentalData(key, output_format = 'pandas')
    st.subheader('Balance Sheet')
    balance_sheet = fd.get_balance_sheet_annual(ticker)[0]
    bs = balance_sheet.T[2:]
    bs.columns = list(balance_sheet.T.iloc[0])
    st.write(bs)
    st.subheader('Income Statement')
    income_statement = fd.get_income_statement_annual(ticker)[0]
    is1 = income_statement.T[2:]
    is1.columns = list(income_statement.T.iloc[0])
    st.write(is1)
    st.subheader('Cash Flow')
    cash_flow = fd.get_cash_flow_annual(ticker)[0]
    cf = cash_flow.T[2:]
    cf.columns = list(cash_flow.T.iloc[0])
    st.write(cf)


