import psycopg2
from sqlalchemy import create_engine
import pandas as pd

# 서버정보입력
conn = psycopg2.connect(host='localhost',dbname='project',user='postgres',password='aki1711',port='5432')

cur = conn.cursor()

# 데이터불러오기
col = ['주문날짜','주문시간','주문요일','시도','시군구','품목']

data = pd.read_csv('KGU_3rd_ORIGIN_KGUAREADOITEM_20200701000000.csv')

data.columns = col
data = data.drop('주문날짜',axis=1)
data['지역'] = data['시도']+' '+data['시군구']
data = data.drop(['시도','시군구'],axis=1)

data = data[data['지역'].str.contains('서울')]
data = data.reset_index(drop=True)

# 데이터 저장
engine = create_engine('postgresql://postgres:aki1711@localhost:5432/project')

engine.execute("DROP TABLE IF EXISTS public.delivery;")

data.to_sql(name='delivery',con=engine,schema='public',if_exists='replace',index=True)

conn.commit()