"""VERY UGLE CODE - Testing Cursor and having AI generate it"""

import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

@st.cache_data  # Cache the data to avoid repeated API calls
def load_data(ticker):
    # Example: Fetch data from FastAPI endpoint
    response = requests.post(
        url="http://fastapi:8080/v1/api/playground", json={"ticker": ticker}
    )
    return response.json()

def create_candlestick_chart(df):
    fig = go.Figure(data=[go.Candlestick(x=df['timestamp'],
                    open=df['open'],
                    high=df['high'],
                    low=df['low'],
                    close=df['close'])])
    fig.update_layout(title='Stock Price',
                      xaxis_title='Date',
                      yaxis_title='Price',
                      xaxis_rangeslider_visible=False)
    return fig

def main():
    st.set_page_config(layout="wide")
    
    # Navigation bar
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Select a page:", ["Dashboard", "Statistics", "Full Dataset"])
    
    # Input box for stock ticker
    ticker = st.text_input("Enter stock ticker:", "")
    
    if ticker:
        data = load_data(ticker)  # Pass the ticker to load_data
        if not data:  # Check if the data is empty
            st.error(f"No data found for the provided stock ticker '{ticker}'. Please try a different one.")
            return  # Exit the function early if no data
        
        df = pd.DataFrame(data)
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        
        if page == "Dashboard":
            st.title("Stock Data Dashboard")
            st.subheader(f"Analyzing: {ticker}")
            st.markdown("---")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.plotly_chart(create_candlestick_chart(df), use_container_width=True)
            
            with col2:
                st.subheader("Latest Stock Data")
                st.dataframe(df.tail(), use_container_width=True)
        
        elif page == "Statistics":
            st.title("Key Statistics")
            st.subheader(f"Analyzing: {ticker}")
            st.markdown("---")
            
            # Get the latest date from the DataFrame
            latest_date = df['timestamp'].iloc[-1].date()
            st.subheader(f"Latest Statistics as of {latest_date}")
            
            metric1, metric2, metric3, metric4 = st.columns(4)
            metric1.metric("Open", f"${df['open'].iloc[-1]:.2f}")
            metric2.metric("Close", f"${df['close'].iloc[-1]:.2f}")
            metric3.metric("High", f"${df['high'].iloc[-1]:.2f}")
            metric4.metric("Low", f"${df['low'].iloc[-1]:.2f}")
        
        elif page == "Full Dataset":
            st.title("Full Dataset")
            st.subheader(f"Analyzing: {ticker}")
            st.markdown("---")
            st.dataframe(df, use_container_width=True)
    
    else:
        st.title("Please enter a stock ticker to analyze.")

if __name__ == "__main__":
    main()
