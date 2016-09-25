
from sqlalchemy import create_engine
import models
from models import Title,ID3


engine = create_engine('sqlite:///db\musicfr4.db')
models.Base.metadata.create_all(engine)
