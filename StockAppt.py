import streamlit as st, pandas as pd, numpy as np, yfinance as yf
import plotly.express as px

st.title('Stock Screener')
ticker = st.sidebar.text_input('Ticker')
start_date = st.sidebar.date_input('Start Date')
end_date = st.sidebar.date_input('End Date')

data = yf.download(ticker, start=start_date, end=end_date)
fig = px.line(data, x = data.index, y = data['Adj Close'], title = ticker)
st.plotly_chart(fig)

pricing_data, fundamental_data, news, openAi= st.tabs(["Pricing Data", "Fundamental Data", "Top News", "ChatGPT Responses"])

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

'''
from pyChatGPT import ChatGPT
session_token = 'eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..97V6_2RmpbrxGWsO.B2pTR597ghdemAwxi8_LNpD_utRM58Uh4uUUKtFLpQYt3eMtc6V1ozAd3981ttKIvv_nnfNLirED1EYjdpb5n4WYmuYC6_Kgwnc-kamiF9E3h3hwj0oHMGSA5i46z3UPZmnCiof005wXfh3yrWKx5SjjAdcgTPdyUZrbTjAkNOtcczy7qAQ6yiYMYIrRadj7SfG3nhf-4NS3-vzbXxXw-4ImtNvYRLFz3o3g2nKfGA7ziDhH35thehkmJjta6w_hNUYTsB4TKD9CihEGTFPKE7fI4Sr-UEjHp1WF1phVLEuIORWOLNbFCQosvGl3lzS2A_-NoB_9Qr5U4gWkYhwniXJ9pnh92d5nh9IYrqug_k_hsRiyC1RfyzMixTqXwQpH0hFm8ffcoHDlroq6fMZPnmDpSIqMzK0prekAh7R9t0QCckY1s3_rsYyBjQb7I_llNQ7EF0V9OVDib--foY3e4Rb6FHVkADTuiGqSbU9hWfiaKC22FWwxXbwcLD8thNOf27N2dzAQP0-o_O88GTQ3VljhTchQ5XRRyg7RwhvlR0UFc8oXQ7GjB1DGB21aAxjFQMB-zULeY3KNVN3N66Hz2zMfeG2uwaKDNRirOOD3D8jsFq1pAiamz02YHR_OpCrkCryc_4xZ3IsP_VKapnRiA8YbObK6Kg_Th6UMWgXgQ2CXEzKVuzEmj5RzEyvcOVT0Cbm7t0m0dDkEK-jx2rV_nWA0oRXHRpqRHv6UKpTL5uEt7_QqA6Zo60wEEDFQ5KhbXa2zkGcWO6wkSAegzgTJRCHB2CnIM54rM04X5MzmDq2RnWnSimA2Sbtns59Ndlg9eOVcsvtqKdS-VykhvW20VH-cLyPTLqf8sAv6BaVlJg8BdpIkvor_puhvDrIHW8ExcaYtkAzF5z7xceEcRFpo7QeZQ2Uz62iVm0O53YkIiRBrZe5u4KJfT6_TLV_ZaUQ8bchlfUaqCxxhkCWEHRyQHjWYXNRP0msFcpfLtxqyrU86VFU_kuJ7yN-TryOEOBJ_GbUxi8is2hipzNNDvX89vM1hr6TBjgC2tcBks4mc0wA2Rm_JbwnYmS3bg4OTZAaqRsP2z9S3s0cWxJyUqiTPpXJY4JY-CHLggN5xXx5XC9n7NL6h80X5RhxmRqz_K56z2clkbh4BpsxeaHT5YAAZ0IzrmZNcgACyO4NzBlXbWsm3JRgkyuN2qLJaeUyKZB6eBpEsv8mauCYN2RNcJ4Hn95TVLabKAAAbVHUWxGMgLeChw__DGbvQwAt7EtzzWMoE7Ts6rLkJcKSnF5FxjoDHonMk2YflqE8OMNt1WAf2-oIjtpFiX8heykxX4smet1XsjnDhU1Ub-gleQuT5IFXjc2dQg5Jst-EHaTP8M8jeJcNxqC0nN2Py0v-FcXFl7BdrlyMmHOYv_dPXpBSYvuPtQq7SSulfqKWsq2nzBIP5fCRuZWgvToKUyFzvr2RYvzxTCYr-9jssX9mTxo5-88VPpafaBWwTrjFQkcCtPCxr4f00kq5gu988dnxkiROdhryDx97YrAWHBNXcoLLLrdo7cVyN1CEpJFbfQnvnLJdwqPy38lGdJb8o_hLjkjpVg7QQXXFJEPWa1ZidoTst1mn0W9bbbeFe_ag8Ys5KmtO_TxBH6ujZ4gkwtG-a87T3plIlvjvglENhQvz9Le2a07X9-xOnVMa6FWQgF14_NVOZVhlcv_BUdZuT9zhkqV25cDQ96biHdvBzRZJu9svumjXxQEnpdkw0XZiHszuMDMAxe952mDvcQ5lRtKpbAMcfYeQfTWgZ16R3A9sjn4ZFktyYxagO0hO1pt6jxuVXz8ee5vlu9P7YNfjTEJ3KayfaOl2RJ7vgCIz76CCEtrbJuDKQ3gXxnOkAr7_ZjNZWXg0Y4sV1vY9M1EPGorXqjhMQTPNfXy154aBwLfvZgmnd8uaCC916BxojlHMbDxZEWcE2TxObAMDHX86-7QgyLZj3XmD-taPLaO2OxZXu5deEssUd1C5z8UX1y_lPGMF41AsJLa6EpY-e-tLoSWBX7BwmdVGTOAoGLTCigxT1pBI0Xhz0TbLEPcw9Nn4dJxKJlwKPV3bdzXKEKSDoxCNAR-SkAWPbPo7fvwD27szkG3cHck-GQybiYHX0G5W5idnFEQXjgKOW9xGufesCvsK3w_4RxyBmDQq_4Dy2BCsjJyG0FspApbe0_lbSU7EGjdNeJIXUctVpdYDlkEakJHu829IZHDYrDrTql23KGFWJmJBw3Qad6J-RbGRIMyAO5d5EFnodofZl7aE5nhfyUareLpCSsWwTq6nr9FFTGI6A4AbAOKK_nG7wtGB02QouStI-P7rixpRpQwgeqQ2lv4o1bf8sDOZt7zoaRtVoH0GsSFLSOefieUhvjWwY9u-afFHJBCa39rPGpgcLSRmUhCHIWUMDw9lc2cMboCxdunM9nVkZV8dDuq6Xi2K_vrwIDvUN87BFQQg_rnxs77Xgq1RgvQZSp2JAcKq0279z2hrHmKioh3-rc_8LCs6wl6ViQPWA0voIgnXOKOPrpEZWFi3grM1jCQTbMOKAPK-0kZZrq-jmbvLl-Xc1SFVXQYucU_Jx_J8DWCPOT2qaNJu0cKpcKwfcd8TMm8pDdRQR-vx9ssXcIiw1rmMBxzSHOWv_RGAX_va99Zy5rkbchCi7-45RV6CG5LYlceYrZozrZgQG_OSTqFK91YhhiBf5CZEGqNgIZx0rq19-1Qwy8m9BIslZodEmpEAwuzy5TGA0K1QK78clhXHc9gaHZeMPLBRw0iEaf3kCeSqvgohGnYyG20vr1Y1gtG-vCYZgTPLELsixXA.fuE_91QOgo1b8B_NzncWOg'
api2 = ChatGPT(session_token)
buy = api2.send_message(f'3 reasons to buy {ticker} stock')
sell = api2.send_message(f'3 reasons to sell {ticker} stock')
swot = api2.send_message(f'Give me a SWOT analysis of {ticker} stock')
with openAi:
    buy_reason, sell_reason, swot_analysis = st.tabs(['3 Reasons to Buy', '3 Reasons to Sell', 'SWOT Analysis'])

    with buy_reason:
        st.subheader(f'3 Reasons to Buy {ticker}')
        st.write(buy['message'])
    with sell_reason:
        st.subheader(f'3 Reasons to Sell {ticker}')
        st.write(sell['message'])
    with swot_analysis:
        st.subheader(f'SWOT Analysis for {ticker}')
        st.write(swot['message'])
'''
