import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier,RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn import preprocessing
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc,recall_score,precision_score

##### Classification

## numeric 
df_raw = df_raw[keep_list]
df_raw[num_list] = df_raw[num_list].astype(float)
df_raw[num_list] = df_raw[num_list].fillna(df_raw.median())

## Categroy 
Cate_list = list(set(list(df_raw.columns)) - set(num_list))
df_raw[Cate_list] = df_raw[Cate_list].fillna('Others')
le = preprocessing.LabelEncoder()
df_raw[Cate_list] = df_raw[Cate_list].apply(le.fit_transform)

## Balance the data
df_model_balanced = pd.concat([df_model[df_model['y'] == 0]\
                   .sample(201772,random_state=2),df_model[df_model['y'] == 1]],axis=0)
df_model_balanced = df_model_balanced.sample(frac=1)

#Train test split
x = df_model_balanced.drop(columns=['y'])
y = df_model_balanced.y
x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=1000, shuffle=True, test_size=0.3)

#Fit the model
clf = GradientBoostingClassifier(n_iter_no_change=4, validation_fraction=0.3, verbose=1, min_samples_leaf=10)
clf.fit(x_train,y_train)

Y_predicted_prob = clf.predict_proba(x_test)
Y_predicted = clf.predict(x_test)

## Evaluation
accuracy = metrics.accuracy_score(y_test, Y_predicted)
accuracy_percentage = 100 * accuracy

recall_pen = metrics.recall_score(y_test, Y_predicted,pos_label=1) * 100
precision_pen = metrics.precision_score(y_test, Y_predicted,pos_label=1) * 100
print('accuracy: ' + str(accuracy_percentage))
print('recall: ' + str(recall_pen))
print('precision: ' + str(precision_pen))

pd.DataFrame(sorted(zip(x.columns,clf.feature_importances_),key=lambda _: -_[1]))
