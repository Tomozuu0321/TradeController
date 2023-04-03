# %%
import pickle
import urllib
import pandas as pd
from sqlalchemy import create_engine, text
from data.environment.LivingFieldEnv.Folder import GrFolderDict as fenv
from data.environment.LivingFieldEnv.BrowserEnv import BrEmv
from general.utility.logger import log

# %%
class CDbConInformationSystem():

    __FOLDER__=path=fenv['database']+'/database/'
    __DATA_BASE_PATH__=""
    __TABLENAME__="InfoSys"
    __engine=None

    # コンストラクタの定義
    def __init__(self, mode ):
        if( mode == BrEmv.ModeDemo ):
            self.__DATA_BASE_PATH__= self.__FOLDER__+'LivingFieldD.db'
        else:
            self.__DATA_BASE_PATH__= self.__FOLDER__+'LivingFieldR.db'

    def open(self):
        _echoOn=False   #True
        self.__engine = create_engine(self.__DATA_BASE_PATH__, echo=_echoOn)

    def close(self):
        self.__engine.dispose()
        #self.__db.session.close_all()

    #dbファイル読み込み
    def doRead(self):
        query = "SELECT Name,value FROM {0};".format(self.__TABLENAME__ )
        _df = pd.read_sql(sql=text(query), con=self.__engine.connect())
        self.__Deserialize(_df)
        return(_df)

    #dbファイル書き込み
    def doWrite(self,df):
        try:
            _df=df.copy()
            self.__Serialize(_df)
            #print(_df)
            _df.to_sql( self.__TABLENAME__, con=self.__engine,if_exists='replace',index_label='id')
            pass    # commit if successful
        except Exception as e:
            log.error(e)
            pass    # rollback if failed

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
