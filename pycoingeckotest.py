# the pycoingecko library 
from pycoingecko import CoinGeckoAPI


# Import the CoinGecko API wrapper
from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()

# Fetch Bitcoin market data for the past 30 days in USD
# This returns prices, market_caps, and total_volumes
bitcoin_data = cg.get_coin_market_chart_by_id(id='bitcoin', vs_currency='usd', days=30)

import pandas as pd

# Create a DataFrame from the "prices" field, which contains [timestamp, price]
data = pd.DataFrame(bitcoin_data['prices'], columns=['TimeStamp', 'Price'])

# Convert the timestamp (in milliseconds) into a readable datetime
data['Date'] = pd.to_datetime(data['TimeStamp'], unit='ms')

# Group the data by calendar day and aggregate to get OHLC values:
# min = daily low, max = daily high, first = opening price, last = closing price
candlestick_data = data.groupby(data.Date.dt.date).agg({'Price': ['min', 'max', 'first', 'last']})

import plotly.graph_objects as go

fig = go.Figure(data=[go.Candlestick(
    x=candlestick_data.index,
    open=candlestick_data['Price']['first'],
    high=candlestick_data['Price']['max'],
    low=candlestick_data['Price']['min'],
    close=candlestick_data['Price']['last'],
    increasing_line_color='pink',
    increasing_fillcolor='pink',
    decreasing_line_color='red',
    decreasing_fillcolor='red',
    showlegend=False  # prevent candlesticks from appearing in legend
)])

# Add dummy traces for legend
fig.add_trace(go.Scatter(
    x=[None], y=[None],
    mode='markers',
    marker=dict(color='pink'),
    name='Up (Close > Open)'
))

fig.add_trace(go.Scatter(
    x=[None], y=[None],
    mode='markers',
    marker=dict(color='red'),
    name='Down (Close < Open)'
))

# Update the chart layout for a cleaner look
fig.update_layout(
    xaxis_rangeslider_visible=False,
    xaxis_title='Date',
    yaxis_title='Price (USD $)',
    title={
        'text': '📊 Bitcoin Price Candlestick Chart – Last 30 Days',
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': dict(size=22, color='black')
    },
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(showgrid=True, gridcolor='lightgray'),
    yaxis=dict(showgrid=True, gridcolor='lightgray'),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="center",
        x=0.5
    )
)

fig.show()

