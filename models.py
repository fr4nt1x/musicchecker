from sqlalchemy import Column, ForeignKey, Integer, String, Float, Date, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship,backref

Base = declarative_base()


class Folder(Base):
    __tablename__ = 'folder'
    id = Column(Integer, primary_key=True)
    name = Column(String(300),index=True)
    folders = relationship("Folder" ,backref=backref('parent',remote_side=[id]))
    parent_id = Column(Integer, ForeignKey('folder.id'))
    files = relationship("File" ,backref='parent')
    pathToFolder = Column(String(300),index=True)
    #root is specified by the user
    
class File(Base):
    __tablename__ = 'file'
    # Here we define columns for the table meal
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    title = Column(String(250))
    artist = Column(String(300))
    trackNumber = Column(Integer)
    dateLastChanged = Column(Date)
    bitrate = Column(Integer)
    
    parent_id = Column(Integer, ForeignKey('folder.id'))


