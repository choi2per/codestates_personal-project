import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline, Pipeline 
from category_encoders import OrdinalEncoder
from sklearn.ensemble import RandomForestClassifier
import pickle

df = pd.read_csv('noshow.csv')

## 잘못된 컬럼명 수정

df.rename(columns ={'Handcap' : 'Handicap'}, inplace = True)
df.rename(columns ={'Hipertension' : 'Hypertension'}, inplace = True)

## 데이터 전처리

df['Gender'].replace(['M','F'], [1,0], inplace = True)
df['No-show'].replace(['No','Yes'], [0,1], inplace = True)

## 데이터셋 분할
# training set, test set을 8:2로 분할했습니다.
train, test = train_test_split(df, test_size=0.20, random_state=7)

# training set, validation set을 8:2로 분할했습니다.
train, val = train_test_split(train, test_size=0.25, random_state=7) # 0.25 x 0.8 = 0.2


# 독립변수와 종속변수세트 분리

features = df.drop(columns=['PatientId', 'AppointmentID', 'ScheduledDay',	'AppointmentDay','No-show','Neighbourhood','No-show']).columns
target = 'No-show'

X_train = train[features]
y_train = train[target]
X_val = val[features]
y_val = val[target]
X_test = test[features]
y_test = test[target]


## 모델 학습

# class weights 계산 : n_samples / (n_classes * np.bincount(y))
custom = len(y_train)/(2*np.bincount(y_train))

# 파이프라인을 만들기

pipe = make_pipeline(
    OrdinalEncoder(), 
    RandomForestClassifier(n_estimators=100, random_state=2, class_weight={0:custom[0], 1:custom[1]}, n_jobs=-1)
)

# 모델 Fitting
pipe.fit(X_train, y_train)

# 기존것
# # Saving model to disk
# pickle.dump(pipe, open('rfmodel.pkl','wb'))

# 3.28 저녁 시도
from joblib import dump,load
dump(pipe,'randomforestmodel.joblib')