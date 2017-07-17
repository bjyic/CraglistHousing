import os
from flask import Flask, render_template, request, redirect
import get_data as gd
import plot_stock_prices as psp

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
        df_data = gd.get_data_df(ticker=ticker_input)

        if len(df_data) > 0:
            script, div = psp.get_plot_ticker_components(
                ticker=ticker_input,
                df_data=df_data
            )

            return render_template('plot_template.html', script=script, div=div)

        else:
            return redirect('/error_page')


@app.route('/error_page', methods=['GET', 'POST'])
def error_page():
    return render_template('error_page.html')


# if __name__ == '__main__':
#     app.run(port=33507)
'''
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
'''
if __name__ == '__main__':
     app.run(host='0.0.0.0')