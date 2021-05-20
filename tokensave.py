import pandas as pd
import time
import sqlite3

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String,  create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///token.db', echo=True)

Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()
Base.metadata.create_all(engine)


'''class Token(Base):
    __tablename__ = 'token'

    id = Column(Integer, primary_key=True)
    token = Column(String(7), unique=True)'''


with open('tokens.csv', 'r') as file:
    # use chucksize to read faster then normal read csv
    tp = pd.read_csv(file, chunksize=100000, iterator=True)
    df = pd.concat(tp, ignore_index=True)
    duplicate = df[df.duplicated()]
    # print duplicated tokens with frequencies
    print(duplicate.value_counts())
    noduplicate = df.drop_duplicates(keep='first')

# save non-duplicate token to database token.db
noduplicate.to_sql('token', con=engine, index=True,
                   index_label='id', if_exists='replace')
