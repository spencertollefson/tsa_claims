from flask import Flask, abort, render_template, jsonify, request
import joblib
from sklearn.ensemble import RandomForestClassifier
from api import make_prediction

app = Flask('TSA-app')

@app.route('/predict', methods=['POST'])
def do_prediction():
    if not request.json:
        abort(400)
    data = request.json

    response = make_prediction(data)

    return jsonify(response)

# @app.route('/')
# def index():
#     return render_template('index.html')

@app.route('/', methods=['GET'])
def dropdown():
    featuredir = './featurelists'
    airports = joblib.load(f'{featuredir}/airports.joblib')
    airlines = joblib.load(f'{featuredir}/airlines.joblib')
    claim_types = joblib.load(f'{featuredir}/claim_types.joblib')
    claim_sites = joblib.load(f'{featuredir}/claim_sites.joblib')
    item_cats = joblib.load(f'{featuredir}/item_category.joblib')
    months = list(range(1, 13))
    return render_template('index.html', airports=airports, airlines=airlines,
                           claim_types=claim_types, claim_sites=claim_sites,
                           item_cats=item_cats, months=months)


    
app.run(debug=True)
