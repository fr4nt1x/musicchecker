from sqlalchemy import Column, ForeignKey, Integer, String, Float, Date, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Title(Base):
    __tablename__ = 'title'
    id = Column(Integer, primary_key=True)
    name = Column(String(300),index=True)
    id3tag = relationship("ID3", uselist=False, backref="title")
    directoryFromRoot = Column(String(300),index=True)
    fileSize = Column(BigInteger)
    dateLastChanged = Column(Date)
    #root is specified by the user
    
class ID3(Base):
    __tablename__ = 'id3'
    # Here we define columns for the table meal
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    artist = Column(String(300))
    trackNumber = Column(Integer)
    title_id = Column(Integer, ForeignKey('title.id'))


