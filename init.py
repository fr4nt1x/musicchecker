from models import Base

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os.path

basedir = os.path.split(os.path.dirname(os.path.realpath(__file__)))[1]
SQLALCHEMY_DATABASE_URI = 'sqlite:///db\musicfr4.db'

# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine(SQLALCHEMY_DATABASE_URI)
 

 
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine


DBSession = sessionmaker(bind=engine)

# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()
