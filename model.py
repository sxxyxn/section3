# 데이터 불러오기
import pandas as pd

col = ['주문날짜','주문시간','주문요일','시도','시군구','품목']

data = pd.read_csv('/content/drive/MyDrive/KGU_3rd_ORIGIN_KGUAREADOITEM_20200701000000.csv')

data.columns = col
data = data.drop('주문날짜',axis=1)
data['지역'] = data['시도']+' '+data['시군구']
data = data.drop(['시도','시군구'],axis=1)

data = data[data['지역'].str.contains('서울')]
data = data.reset_index(drop=True)

# 데이터 전처리
from category_encoders import OrdinalEncoder

oe = OrdinalEncoder()
encoded = oe.fit_transform(data)

# 카테고리 맵핑 확인
print(oe.category_mapping[0].values())
print(oe.category_mapping[1].values())

# 훈련, 테스트 셋 분리
target = '품목'
feature = ['주문시간','주문요일']

from sklearn.model_selection import train_test_split

train, test = train_test_split(encoded, test_size=0.2, random_state=2)
print(train.shape, test.shape)

X_train = train[feature]
y_train = train[target]
X_test = test[feature]
y_test = test[target]

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

model = RandomForestRegressor()
model.fit(X_train, y_train)

y_pred1 = model.predict(X_train)
mae1 = round(mean_absolute_error(y_train, y_pred1))
print(f'훈련 에러: {mae1}')

y_pred2 = model.predict(X_test)
mae2 = round(mean_absolute_error(y_test, y_pred2))
print(f'테스트 에러: {mae2}')

# 모델 부호화
import pickle

with open('model.pkl','wb') as pickle_file:
    pickle.dump(model, pickle_file)
