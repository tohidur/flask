**database.py**
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = 'sqlite:///.test.db'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})
SessoinLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
```

Import the Base class above into the models.py

**models.py**
```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.types import Date
from .database import Base


class Record(Base):
    __tablename__ = 'Records'
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    country = Column(String, index=True)
    cases = Column(Interger)
    deaths = Column(Integer)
    recoveries = Column(Integer)

```


**Example script**
```python
import csv
import datetime

from app import models
from app.database import SessionLocal, engine


db = SessionLocal()

model.Base.metadata.create_all(bind=engine)

with open('filename.csv', 'r+') as f:
    csv_reader = csv.DictReader(f)

    for row in csv_reader:
        db_record = models.Record(
            date=datetime.datetime.strptime(row['date'], '%Y-%m-%d'),
            # ....
        )
        db.add(db_record)

    db.commit()
```

Above, this separate load.py file allows us to insert data into the database
without ever running the app


**Declarative Base and MetaData**
The `declarative_base()` base class contains a MetaData object where newly
defined `Table` objects are collected. This is accessed when
`models.Base.metadata.create_all()` is called.


**Handling Threading issue: Scopped session and Session local**
With `scoped_session` function SQLAlchemy can handle worker threading issues.

The sessionmaker is a factory for initializing new Session objects by
requesting a connection from the engine's connection pool and attaching a
connection to the new Session object.

Initializing a new session object is also referred to as "checking out" a
connection. So when you begin a new session, you are starting a new process
within the database too.

```python
from flask import Flask, _app_ctx_stack, jsonify, url_for
from flask_cors import CORS
from sqlalchemy.orm import scoped_session

from . import models
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = Flask(__name__)
CORS(app)
app.session = scoped_session(
    SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)
```


Additionally, scoped sessions give us access to a query_property. So if you
style used by flask_sqlalchemy you can use this with SQLAlchemy

```python
Base = declarative_base()
Base.query = db_session.query_property()
```

Check this project for reference
https://github.com/edkrueger/sars-flask/blob/master/app/models.py

