from flask import Flask, abort, render_template, jsonify, request
import joblib
import altair as alt
from flask import render_template
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models.sources import AjaxDataSource

from api import make_prediction, make_plot

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
    days = list(range(1, 61))
    months = list(range(1, 13))
    return render_template('index.html', airports=airports, airlines=airlines,
                           claim_types=claim_types, claim_sites=claim_sites,
                           item_cats=item_cats, days=days, months=months)

# @app.route('/dashboard/')
# def show_dashboard():
#     plots = []
#     plots.append(make_plot())
#
#     return render_template('dashboard.html', plots=plots)
#
#
# def make_ajax_plot():
#     source = AjaxDataSource(data_url="http://localhost:5000/predict/',
#                             polling_interval=2000, mode='append')
#
#     source.data = dict(x=[], y=[])
#
#     plot = figure(plot_height=300, sizing_mode='scale_width')
#     plot.line('x', 'y', source=source, line_width=4)
#
#     script, div = components(plot)
#     return script, div
#
# x = 0
# @app.route('/data/', methods=['POST'])
# def data():
#     global x
#     x += 1
#     y = 2**x
#     return jsonify(x=x, y=y)







#
# WIDTH = 600
# HEIGHT = 300
#
# @app.route("/data/line")
# def data_line():
#     period = list(range(1,63))
#     scores = []
#     smoothscores = []
#     example = {}
#     example['days_waited_to_file_claim'] = 0
#
#     for i in period:
#         example['days_waited_to_file_claim'] = i
#         scores.append(make_prediction(example))
#
#     for i in period[:-3]:
#         smoothscores.append((scores[i] + scores[i + 1] + scores[i+2]) / 3)
#
#     df = pd.DataFrame(data=)
#
#
#     chart = alt.Chart(data=df, height=HEIGHT, width=WIDTH).mark_line().encode(
#         color='symbol:N',
#         x='days:T',
#         y='make_prediction'
#           ':Q'
#     )
#     return chart.to_json()


    
app.run(debug=True)
