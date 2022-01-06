import streamlit as st
from bokeh.plotting import figure
import pandas as pd
import requests
import os


ticker = ''
year = 'Select'
month = 'Select'

st.sidebar.title('Select plot parameters:')

ticker = st.sidebar.text_input('Ticker (e.g. AAPL):',help='')

year = st.sidebar.selectbox(
    'Year:',
    ('Select',2021)
)

month = st.sidebar.selectbox(
    'Month:',
    ('Select',8,9,10,11,12)
)

st.title("TDI Milestone")

if (ticker != '') and (year != 'Select') and (month !='Select'):
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+ ticker + '&apikey='+ os.environ['API_KEY']
    r = requests.get(url)
    data = r.json()

    if 'Time Series (Daily)' in data:
        df = pd.DataFrame.from_dict(data['Time Series (Daily)'], orient ="index")
        df.reset_index( inplace=True)
        df.rename(columns={'index':'date','1. open':'open','2. high':'high','3. low':'low','4. close':'close','5. volume':'volume'},inplace=True)
        df['date'] = pd.to_datetime(df['date'])
        df = df[(df['date'].dt.year==year) & (df['date'].dt.month==month)]


        p = figure(
            title=ticker + ': ' + str(month) + '/' + str(year),
            x_axis_label='Date',
            y_axis_label='Close',
            x_axis_type='datetime')

        p.line(df['date'], df['close'], legend_label='Trend', line_width=2)

        st.bokeh_chart(p, use_container_width=True)
    else:
        st.warning('No data. Change input')

# Test
# streamlit run app.py

