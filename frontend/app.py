from bokeh.charts import TimeSeries
from bokeh.embed import components

import datetime
import requests
import pandas as pd

import os
#os.chdir(r'C:\Users\cnyi\Box Sync\Github\local_test_others\Stock_plot')
from flask import Flask, render_template, request, redirect
#import get_data as gd
#import plot_stock_prices as psp

base_url = 'https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json'
base_params = {
    'api_key': 'fVoNngaAV1uiM-etf31B',
    'qopts.columns': 'date,close'
}


def convert_month_string(month):
    if len(str(month)) == 1:
        return '0' + str(month)
    else:
        return str(month)


def get_date_range():

    current_month = datetime.datetime.now().month
    current_year = datetime.datetime.now().year

    if current_month != 1:
        last_month = current_month - 1
        start_year = current_year
    else:
        last_month = 12
        start_year = current_year - 1

    start_range = str(start_year) + \
        convert_month_string(last_month) + '01'
    end_range = str(current_year) + \
        convert_month_string(current_month) + '01'

    date_range = {
        'start_range': start_range,
        'end_range': end_range
    }
    return date_range


def get_data(
    ticker,
    base_url=base_url,
    base_params=base_params
):
    # get date range
    date_range = get_date_range()
    base_params['ticker'] = ticker
    base_params['date.gte'] = date_range['start_range']
    base_params['date.lt'] = date_range['end_range']

    response = requests.get(base_url, base_params)

    if response.status_code != 200:
        response.raise_for_status()

    return response.json()


def get_data_df(
    ticker,
    base_url=base_url,
    base_params=base_params
):
    data = get_data(
        ticker=ticker.lower(),
        base_url=base_url,
        base_params=base_params
    )
    data_list = data['datatable']['data']
    column_headers = [
        'date',
        'closing_price'
    ]

    data_df = pd.DataFrame(
        data=data_list,
        columns=column_headers
    )
    data_df['date'] = pd.to_datetime(data_df['date'])
    return data_df.set_index('date')



def get_plot_ticker_components(ticker, df_data):
    plot_title = 'Last Month ' + ticker.upper() + ' Closing Price'

    p = TimeSeries(df_data.closing_price, legend=True, title=plot_title, xlabel='Date', ylabel='Stock Prices')
    p.title.text_font_size = '14pt'

    script, div = components(p)

    return script, div
    
app = Flask(__name__)


@app.route('/')
def main():
    return redirect('/index')


@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')

    else:
        ticker_input = request.form['ticker_symbol']
        df_data = get_data_df(ticker=ticker_input)

        if len(df_data) > 0:
            script, div = get_plot_ticker_components(
                ticker=ticker_input,
                df_data=df_data
            )

            return render_template('plot_template.html', script=script, div=div)

        else:
            return redirect('/error_page')


@app.route('/error_page', methods=['GET', 'POST'])
def error_page():
    return render_template('error_page.html')

'''
if __name__ == '__main__':
    app.run(port=33507)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
'''
if __name__ == '__main__':
     app.run(host='0.0.0.0')