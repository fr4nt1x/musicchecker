
from sqlalchemy import create_engine
import models
from models import File,Folder


engine = create_engine('sqlite:///db\musicfr4.db')
models.Base.metadata.create_all(engine)
