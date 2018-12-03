import numpy as np
import pickle
import joblib
from sklearn.preprocessing import StandardScaler, MultiLabelBinarizer, OneHotEncoder


model = joblib.load(open('./models/rf_full_month_rec', 'rb'))

example = {
  'airport_code': 'SEA',  # str
  'airline': 'Emirates',    # str
  'claim_type': 'PropertyLoss',    # str
  'claim_site': 'Checkpoint',  # str
  'item_category': 'Clothing',  # str
  'num_items_or_incidents_claimed': 1,  # int
  'days_waited_to_file_claim': 7, # int
  'Month_received': 1, # int (1-12)
}


def make_prediction(features):
    '''
    :param features: dictionary like 'example' above
    :return: 2 pair dict of binary outcome (compensate and not compensate) and the probablity
    '''
    X = pd.DataFrame(data=features, index=[0])

    categorical = ['airport_code', 'airline', 'claim_type', 'claim_site', 'Month_received']
    continuous = ['days_waited_to_file_claim', 'num_items_or_incidents_claimed']

    trans_dir = './models/transformers'
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
