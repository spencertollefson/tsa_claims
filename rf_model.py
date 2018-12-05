import numpy as np
import pandas as pd
import datetime as dt
import joblib
import sklearn
from sklearn.preprocessing import StandardScaler, MultiLabelBinarizer, OneHotEncoder
from sklearn.model_selection import GridSearchCV
from sklearn import metrics
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split, cross_validate, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_curve, auc
from imblearn.over_sampling import SMOTE

df = pd.read_pickle('./data/clean/clean_for_classifier_df.pkl')
col_names = ['claim_number', 'date_received', 'incident_date', 'airport_code', 'airport_name',
           'airline', 'claim_type', 'claim_site', 'item_category', 'close_amount', 'disposition']
# Create Dataset limited to top 40 airports and top 14 airlines
passengers = pd.read_pickle('./data/clean/usa2016-17-enplanements.pkl')

top_airports = list(passengers.airport.iloc[:40].unique())
top_airlines = df.airline.value_counts()[:14].index.tolist()


df = df[df.airport_code.isin(top_airports)]
df = df[df.airline.isin(top_airlines)]
df = df[(df.claim_site == 'Checked Baggage') | (df.claim_site == 'Checkpoint')]
df = df[(df.claim_type == 'PropertyLoss') | (df.claim_type == 'PropertyDamage')]

passengers = None
top_airports = None
top_airlines = None

df.dropna(inplace=True)

df['binary_disposition'] = df['disposition']
df['binary_disposition'] = df['binary_disposition'].where(df['binary_disposition'] == 'Deny', other='Compensate')

# Change some text to make it more human readable
df.claim_site[df.claim_site == '-'] = 'Unknown'
df.claim_type[df.claim_type == '-'] = 'Unknown'

# Feature Engineering

### Count of items claimed

# TODO: Consider only using this for where claim_type is related to property.
df['num_items_or_incidents_claimed'] = df['item_category'].str.split(pat=';').apply(lambda x: len(x))
df['num_items_or_incidents_claimed'] = df['num_items_or_incidents_claimed'].where(df['claim_type'].str.contains('property', case=False) == True, other= 0)

### Time calculation
wait_period = df.date_received - df.incident_date
df['days_waited_to_file_claim'] = wait_period.dt.days

# Drop days where the 'date_received" was reported before 'incident_date'
df = df[df.days_waited_to_file_claim >= 0]

df.reset_index(inplace=True,drop=True)
df['bin_dispos_onehot'] = df['binary_disposition'].apply(lambda x: 1 if x == 'Compensate' else 0)

df['Month_received'] = df['date_received'].apply(lambda x: "%d" % (x.month))

X_small_df = df[['airport_code', 'airline', 'claim_type', 'claim_site', 'item_category', 'days_waited_to_file_claim', 'Month_received']]
y_small = df['binary_disposition'].apply(lambda x: 1 if x == 'Compensate' else 0)

categorical = ['airport_code', 'airline', 'claim_type', 'claim_site', 'Month_received', 'item_category']
continuous =  ['days_waited_to_file_claim']

enc = OneHotEncoder(sparse=False)
onehotarray = enc.fit_transform(X_small_df[categorical])

ss = StandardScaler()
continuousarray = ss.fit_transform(X_small_df[continuous])

mlb = MultiLabelBinarizer(sparse_output=False)
onehot_itemcategories = mlb.fit_transform(X_small_df['item_category'].str.replace(' ','').str.split(pat=';'))

X_small = np.concatenate((onehotarray, continuousarray, onehot_itemcategories), axis=1)

X_train, X_test, y_train, y_test = train_test_split(X_small, y_small, test_size=0.3, random_state=42, stratify=y_small)

df = None

rf = RandomForestClassifier(random_state=42)

criterions = ['gini']#, 'entropy']
n_ests = [300]
m_depths = [30, 35, 40]
param_grid = dict(criterion=criterions, n_estimators=n_ests, max_depth=m_depths)

grid_rf = GridSearchCV(rf, param_grid, scoring='roc_auc', cv=6, n_jobs=5)

grid_rf.fit(X_train, y_train)

print(grid_rf.best_score_)
print(grid_rf.best_params_)
print(grid_rf.best_estimator_)

y_pred = grid_rf.predict(X_test)
print(roc_auc_score(y_test, y_pred))