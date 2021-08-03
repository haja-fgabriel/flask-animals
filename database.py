from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///app.db", echo=True)
Session = sessionmaker(engine)


def create_tables(base):
    base.metadata.create_all(bind=engine)
