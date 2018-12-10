import numpy as np
import pandas as pd
import joblib

import pickle
from sklearn.preprocessing import StandardScaler, MultiLabelBinarizer, OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
model = joblib.load(open('./stat_models/catboost_month_incident_12.06.2018.joblib', 'rb'))

import joblib
import altair as alt

example = {
  'airport_code': 'SEA',  # str
  'airline': 'Delta Air Lines',    # str
  'claim_type': 'PropertyLoss',    # str
  'claim_site': 'Checkpoint',  # str
  'item_category': 'Clothing',  # str
  'days_waited_to_file_claim': 7,  # int
  'Month_inc_date': '1'  # int (1-12)
}


def make_prediction(features):
    '''
    :param features: dictionary like 'example' above
    :return: 2 pair dict of binary outcome (compensate and not compensate) and the probablity
    '''
    X = pd.DataFrame(data=features, index=[0])

    categorical = ['airport_code', 'airline', 'claim_type', 'claim_site', 'Month_inc_date']
    continuous = ['days_waited_to_file_claim']

    trans_dir = './stat_models/transformers'
    enc = joblib.load(f'{trans_dir}/onehotencode.joblib')
    onehotarray = enc.transform(X[categorical])

    ss = joblib.load(f'{trans_dir}/standardscaler.joblib')
    continuousarray = ss.transform(X[continuous])

    mlb = joblib.load(f'{trans_dir}/item_category.joblib')
    onehot_itemcategories = mlb.transform(X['item_category'].str.replace(' ', '').str.split(pat=';'))

    X = np.concatenate((onehotarray, continuousarray, onehot_itemcategories), axis=1)

    prob_receive_compensation = model.predict_proba(X)[0, 1]

    result = prob_receive_compensation

    # result = {
    #     'compensation': int(prob_receive_compensation > 0.5),
    #     'prob_receive_compensation': prob_receive_compensation
    # }

    return result



def make_plot(features):

    WIDTH = 600
    HEIGHT = 300
    period = list(range(1, 63))
    scores = []
    smoothscores = []
    features['days_waited_to_file_claim'] = 0

    for i in period:
        features['days_waited_to_file_claim'] = i
        scores.append(make_prediction(features))

    for i in period[1:-2]:
        smoothscores.append((scores[i] + scores[i + 1] + scores[i + 2]) / 3)

    df = pd.DataFrame({'days': period[1:-2], 'prob': smoothscores})

    chart = alt.Chart(data=df, height=HEIGHT, width=WIDTH).mark_line().encode(
        x='days:Q',
        y='prob'
          ':Q'
    )
    return chart.to_json()



def make_prediction2(features):
    '''
    :param features: dictionary like 'example' above
    :return: 2 pair dict of binary outcome (compensate and not compensate) and the probablity
    '''
    X = pd.DataFrame(data=features, index=[0])

    categorical = ['airport_code', 'airline', 'claim_type', 'claim_site', 'Month_inc_date']
    continuous = ['days_waited_to_file_claim']

    trans_dir = './stat_models/transformers'
    enc = joblib.load(f'{trans_dir}/onehotencode.joblib')
    onehotarray = enc.transform(X[categorical])

    ss = joblib.load(f'{trans_dir}/standardscaler.joblib')
    continuousarray = ss.transform(X[continuous])

    mlb = joblib.load(f'{trans_dir}/item_category.joblib')
    onehot_itemcategories = mlb.transform(X['item_category'].str.replace(' ', '').str.split(pat=';'))

    X = np.concatenate((onehotarray, continuousarray, onehot_itemcategories), axis=1)

    prob_receive_compensation = model.predict_proba(X)[0, 1]

    result = {
        'compensation': int(prob_receive_compensation > 0.5),
        'prob_receive_compensation': prob_receive_compensation
    }

    return result

if __name__ == '__main__':
    print(make_prediction(example))
