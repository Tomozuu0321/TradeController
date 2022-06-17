# %%
import pickle
import urllib
import pandas as pd
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from data.environment.LivingFieldEnv.Folder import GrFolderDict as fenv
from data.environment.LivingFieldEnv.BrowserEnv import BrEmv

# %%
class CDbConInformationSystem():

    __FOLDER__=path=fenv['database']+'/database/'
    __DATA_BASE_PATH__=""
    __TABLENAME__="InfoSys"
    __db=None

    # コンストラクタの定義
    def __init__(self, mode ):
        if( mode == BrEmv.ModeDemo ):
            self.__DATA_BASE_PATH__= self.__FOLDER__+'LivingFieldD.db'
        else:
            self.__DATA_BASE_PATH__= self.__FOLDER__+'LivingFieldR.db'

    def open(self):
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = self.__DATA_BASE_PATH__
        app.config["SQLALCHEMY_ECHO"] = False #True   # default True
        #警告メッセージを抑制すろ為,「SQLALCHEMY_TRACK_MODIFICATIONSS」を設定する 追跡機能らしい
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
        self.__db = SQLAlchemy(app)

    def close(self):
        self.__db.session.close_all()

    #dbファイル読み込み
    def doRead(self):
        #query = "SELECT * FROM {0};".format(self._tableName)
        query = "SELECT Name,value FROM {0};".format(self.__TABLENAME__ )
        _df = pd.read_sql(query, self.__db.engine)
        #for i in range(0,len(_df.loc[:,"first" ])) :
        #_df.loc[ i,"first" ]=pd.to_datetime(_df.loc[ i,"first" ])
        self.__Deserialize(_df)
        return(_df)

    #dbファイル書き込み
    def doWrite(self,df):
        try:
            _df=df.copy()
            self.__Serialize(_df)
            _df.to_sql( self.__TABLENAME__,self.__db.engine,if_exists='replace',index_label='id')
            self.__db.session.commit()
        except:
            self.__db.session.rollback()

    def __Serialize(self,df):
        for i in range(len(df)):
            try:
                if( type(df['value'][i]) is str ):
                    #print("pass")
                    pass
                else:
                    df['value'][i]=urllib.parse.quote(pickle.dumps(df['value'][i]))
                    #df['value'][i]=urllib.parse.quote(pickle.dumps(df['value'][i]))
            except:
                #print(f"err {i}")
                pass

    def __Deserialize(self,df):
        for i in range(len(df)):
            #print(i)
            try:
                #print(f"s {i}={type(df['value'][i])}")
                _text=urllib.parse.unquote_to_bytes(df['value'][i])
                #print(f"s1 {i}={type(_text)}")
                df['value'][i]=pickle.loads(_text)
                #print(f"e {i}={type(df['value'][i])}")
            except:
                #print(f"err {i}")
                pass
