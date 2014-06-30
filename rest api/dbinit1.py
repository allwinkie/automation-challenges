#!/usr/bin/python
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging

# db connection information
#sqlPass = 'test'
#sqlUser = 'test'
#db ='test'
#dbHost='127.0.0.1'
#dbPort=3306

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# base howto
#http://docs.sqlalchemy.org/en/rel_0_8/orm/extensions/declarative.html

Base = declarative_base()
engine = sqlalchemy.create_engine( 'mysql://test:test@127.0.0.1/test')
GetDbSession = sessionmaker(bind=engine)

def initSchema():
    #Initialize the data model in memory by creating all the needed tables
    Base.metadata.create_all(engine)

class Words(Base):
    __tablename__ = 'words'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.TEXT)
    count = sqlalchemy.Column(sqlalchemy.Integer)

#http://docs.sqlalchemy.org/en/rel_0_9/orm/extensions/declarative.html
    @classmethod
    def putWord(cls, wordName):
        dbSession = GetDbSession()
        wordOrmObj = dbSession.query(cls).filter_by(name=wordName).first()
        if wordOrmObj == None:
            cls.new(wordName)
            dbSession.close()
            ret = 1
        else:
            wordOrmObj.count += 1
            dbSession.commit()
            ret = wordOrmObj.count
            dbSession.close()
        return ret

#http://docs.sqlalchemy.org/en/rel_0_9/orm/extensions/declarative.html
    @classmethod
    def new(cls, name):
        dbSession = GetDbSession()
        dbSession.add( cls(name=name, count=1) )
        dbSession.commit()
        dbSession.close()

    @classmethod
    def getWordCount(cls, name):
        dbSession = GetDbSession()
        wordOrmObj = dbSession.query(cls).filter_by(name=name).first()
        if wordOrmObj == None:
            ret = None
        else:
            ret = wordOrmObj.count
        dbSession.close()
        return ret

    @classmethod
    def getAll(cls):
        ret = {}
        dbSession = GetDbSession()
        for wordOrmObj in dbSession.query(cls).all():
            ret[wordOrmObj.name] = wordOrmObj.count
        dbSession.close()
        return ret

if __name__ == '__main__':
    pass
