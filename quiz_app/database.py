from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


URL_BASE = "postgresql://postgres:juniorfoda123@localhost:5432/quizapp"


engine = create_engine(URL_BASE)
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()