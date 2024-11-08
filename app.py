import matplotlib
matplotlib.use('Agg') 

from flask import Flask, render_template, request
import requests
import os
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

app = Flask(__name__)

stock_symbols = ['AAPL', 'GOOG', 'MSFT', 'AMZN', 'TSLA']

api_key = "A5XGJKIF1F4259FR"

def fetch_stock_data(symbol, time_series_function):
    url = f"https://www.alphavantage.co/query"
    params = {
        "function": time_series_function,
        "symbol": symbol,
        "apikey": api_key
    }

    if time_series_function == "TIME_SERIES_INTRADAY":
        params["interval"] = "5min"  
    elif time_series_function in ["TIME_SERIES_DAILY", "TIME_SERIES_WEEKLY", "TIME_SERIES_MONTHLY"]:
        pass

    response = requests.get(url, params=params)
    data = response.json()

    if "Time Series (5min)" in data: 
        return data["Time Series (5min)"]
    elif "Time Series (Daily)" in data:  
        return data["Time Series (Daily)"]
    elif "Weekly Time Series" in data:  
        return data["Weekly Time Series"]
    elif "Monthly Time Series" in data:  
        return data["Monthly Time Series"]
    else:
        return None

def parse_time_series(stock_data, time_series_function, start_date, end_date):
    dates = []
    opens = []
    highs = []
    lows = []
    closes = []

    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()

    for date_str, data in stock_data.items():
        if time_series_function == "TIME_SERIES_INTRADAY":
            date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").date()
        else:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        
        if start_date_obj <= date_obj <= end_date_obj:
            dates.append(date_obj)
            opens.append(float(data["1. open"]))
            highs.append(float(data["2. high"]))
            lows.append(float(data["3. low"]))
            closes.append(float(data["4. close"]))
    
    return dates, opens, highs, lows, closes

def generate_chart(dates, opens, highs, lows, closes, symbol, chart_type, time_series_function, start_date, end_date):
    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(dates, closes, label="Close Price", color="b")

    if chart_type == "line":
        ax.plot(dates, opens, label="Open Price", color="g")
        ax.plot(dates, highs, label="High Price", color="r")
        ax.plot(dates, lows, label="Low Price", color="orange")
    elif chart_type == "bar":
        ax.bar(dates, closes, label="Close Price", color="b", alpha=0.6)

    ax.set_xlabel("Date")
    ax.set_ylabel("Price (USD)")
    ax.set_title(f"{symbol} Stock Prices: {start_date} to {end_date}")
    
    if time_series_function == "TIME_SERIES_INTRADAY":
        ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
    elif time_series_function == "TIME_SERIES_DAILY":
        ax.xaxis.set_major_locator(mdates.DayLocator())
    elif time_series_function == "TIME_SERIES_WEEKLY":
        ax.xaxis.set_major_locator(mdates.WeekdayLocator())
    elif time_series_function == "TIME_SERIES_MONTHLY":
        ax.xaxis.set_major_locator(mdates.MonthLocator())

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.xticks(rotation=45)
    ax.legend()

    chart_filename = f"chart_{symbol}_{start_date}_{end_date}.png"
    fig.tight_layout()
    chart_path = os.path.join("static", chart_filename)
    plt.savefig(chart_path)
    plt.close()
    return chart_filename

def validate_dates(start_date, end_date):
    try:
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
        return start_date_obj <= end_date_obj
    except ValueError:
        return False

@app.route("/", methods=["GET", "POST"])
def index():
    chart_url = None
    chart_symbol = None
    chart_start_date = None
    chart_end_date = None
    
    if request.method == "POST":
        symbol = request.form["symbol"]
        chart_type = request.form["chart_type"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        time_series_function = request.form["time_series_function"]
        
        if not validate_dates(start_date, end_date):
            return render_template("index.html", stock_symbols=stock_symbols)

        stock_data = fetch_stock_data(symbol, time_series_function)
        if stock_data:
            dates, opens, highs, lows, closes = parse_time_series(stock_data, time_series_function, start_date, end_date)
            
            chart_filename = generate_chart(dates, opens, highs, lows, closes, symbol, chart_type, time_series_function, start_date, end_date)
            
            chart_url = f"/static/{chart_filename}"
            chart_symbol = symbol
            chart_start_date = start_date
            chart_end_date = end_date
    
    return render_template("index.html", stock_symbols=stock_symbols, chart_url=chart_url,
                           chart_symbol=chart_symbol, chart_start_date=chart_start_date, chart_end_date=chart_end_date)

if __name__ == "__main__":
    if not os.path.exists('static'):
        os.makedirs('static')
    
    app.run(debug=True, host="0.0.0.0", port=5000)  # Port set to 5000 for Docker compatibility
