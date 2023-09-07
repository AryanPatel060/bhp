
from flask import Flask, render_template,request,jsonify
import util
from flask_cors import CORS
import json

import json,pickle
import numpy as np
__location = None
__data_columns= None
__model=None 
app = Flask (__name__)
CORS(app, resources={r"/predict_home_price": {"origins": "http://127.0.0.1:5500"}})


@app.route('/')
def index():
    return render_template('app.html')

@app.route('/get_location_name', methods=['GET'])
def get_location_name():
    response = jsonify({
        'locations':util.get_location_name()
    })
    response.headers.add('Access-Control-Allow-Origin','*')

    return response


@app.route('/predict_home_price',  methods=['GET', 'POST'] )
def predict_home_price():
    try:
        # print(data['bhk'])
        data = request.get_json()
        total_sqft = data['total_sqft']
        # print(total_sqft)
        location = data['location']
        bhk = data['bhk']
        bath = data['bath']
        price=get_estimatet_price(total_sqft , location  , bath, bhk)
        print(price)
        response = {
            'message': 'Data received successfully',
            'price':price
        }
        # response.headers.add('Access-Control-Allow-Origin','*')
        # response_data = {'message': 'Data received successfully', 'data': data}
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500





def get_estimatet_price(sqft,location,bath,bhk):
    try:
        loc_index = __data_columns.index(location.lower())
    except:
        loc_index = -1

    x = np.zeros(len(__data_columns))

    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index>=0:
        x[loc_index] = 1
    return round(__model.predict([x])[0],2)



def get_location_name():
    load_saved_artifacts()
    return __location



def load_saved_artifacts():

    print("loading saved artifacts ....  start")
    global __data_columns
    global __location
    global __model

    with open("server/artifacts/columns.json",'r') as f:
        __data_columns = json.load(f)["data_columns"]
        __location = __data_columns[3:]

    with open ("server/artifacts/banglore_home_prices_model.pickle",'rb') as f:
        __model = pickle.load(f)

    print("loading saved artifacts .... done")






# @app.route('/predict_home_price',  methods=['GET', 'POST'] )
# def predict_home_price():
    
#     total_sqft = float(request.form['total_sqft'])
#     location = request.form['location']
#     bhk = int(request.form['bhk'])
#     bath = int(request.form['bath'])
#     print(total_sqft)
#     response = jsonify({
#         'estimated price of the house is ':util.get_estimatet_price (total_sqft , location , bhk , bath)
#     })

#     response.headers.add('Access-Control-Allow-Origin','*')
#     return response

if __name__ == "__main__":
    print('starting server')
    get_location_name()
    print(get_estimatet_price(1000,'tygfgr',3,3))
    app.run()
