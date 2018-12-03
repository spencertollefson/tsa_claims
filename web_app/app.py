from flask import Flask, abort, render_template, jsonify, request
from api import make_prediction
import joblib

app = Flask('TSA-app')

@app.route('/predict', methods=['POST'])
def do_prediction():
    if not request.json:
        abort(400)
    data = request.json

    response = make_prediction(data)

    return jsonify(response)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['GET'])
def dropdown():
    featuredir = './featurelists'
    airportlist = joblib.load(f'{featuredir}/airports.joblib')
    airlinelist = joblib.load(f'{featuredir}/airlines.joblib')
    claim_typelist = joblib.load(f'{featuredir}/claim_types.joblib')
    claim_sitelist = joblib.load(f'{featuredir}/claim_sites.joblib')
    item_catlist = joblib.load(f'{featuredir}/item_category.joblib')
    monthlist = list(range(1, 13))
    return render_template('index.html', airportlist=airportlist, airlinelist=airlinelist,
                           claim_typelist=claim_typelist, claim_sitelist=claim_sitelist,
                           item_catlist=item_catlist, monthlist=monthlist)


    
app.run(debug=True)
