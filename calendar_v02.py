import pandas as pd
import requests
import streamlit as st 
import datetime as dt

st.header("Financial Report Calendar")

try:
    uploaded_file = st.file_uploader("Please Upload Excel File Here", type=["csv"])

    if uploaded_file is not None:
        barry_list = pd.read_csv(uploaded_file, header=None)
    else:
        barry_list = pd.read_csv("List_barry_Feb.csv", header=None)       

    barry_list.columns = ["symbol"]

    # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    CSV_URL = 'https://www.alphavantage.co/query?function=EARNINGS_CALENDAR&horizon=3month&apikey=QE8EMF2BQZL1ZM2L'
    df = pd.read_csv(CSV_URL)

    calendar_list = pd.merge(barry_list, df, on='symbol', how='left')
    calendar_list.drop_duplicates(subset='symbol',keep='first',inplace=True)

    calendar_list.sort_values(by='reportDate', ascending=True, inplace=True)
    calendar_list.rename(columns={'estimate': 'EPS (estimate)'}, inplace=True)
    calendar_list['reportDate'] = pd.to_datetime(calendar_list['reportDate'])

    # Date range filter
    min_date = calendar_list['reportDate'].min().date()
    max_date = calendar_list['reportDate'].max().date()
    date_range = st.slider('Select a date range', min_date, max_date, (min_date, max_date))
    
    # Filter data within the selected date range
    filtered_calendar_list = calendar_list[(calendar_list['reportDate'].dt.date >= date_range[0]) & (calendar_list['reportDate'].dt.date <= date_range[1])]
    st.dataframe(filtered_calendar_list)

except Exception as e:
    st.error(f"An error occurred: {e}")
