import os; os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import time
import datetime
from http import HTTPStatus
from flask import Flask, jsonify, request
from yahoo_fin import stock_info as yf

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'Message': 'Hello World!'
    }), HTTPStatus.OK

@app.route('/saham/<string:STOCK>', methods=['GET'])
def getSaham(STOCK):
    try:
        date_now = time.strftime('%Y-%m-%d')
        date_3_years_back = (datetime.date.today() - datetime.timedelta(days=1104)).strftime('%Y-%m-%d')
        init_df = yf.get_data(STOCK, start_date=date_3_years_back, end_date=date_now, interval='1d')
        if init_df.empty:
            return jsonify({'error': True, 'message': 'STOCK Tidak Ada'}), 404
        init_numpy = init_df.to_numpy()
        init_json = init_numpy.tolist()
        init_dict = list(map(lambda data: {'open': data[0], 'high': data[1], 'low': data[2], 'close': data[3], 'adjclose': data[4], 'volume': data[5], 'ticker': data[6]}, init_json))
        return jsonify({
            'message': 'GET Saham Success!',
            'header': ['open', 'height', 'low', 'close', 'adjclose', 'volume', 'ticker'],
            'data_array': init_json,
            'data_object': init_dict
        }), HTTPStatus.OK
    except Exception:
        return jsonify({'error': True, 'message': 'STOCK Tidak Ada'}), 404
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))