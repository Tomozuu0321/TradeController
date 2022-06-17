import os
import pandas as pd
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from general.utility.logger import log
from data.environment.LivingFieldEnv.Folder import GrFolderDict as fenv
from data.environment.LivingFieldEnv.BrowserEnv import BrEmv

class CIoHandler():

    __FOLDER__=path=fenv['database']+'/database/'
    __TABLENAME__="TradeSummary"
    __DATA_BASE_PATH__=""
    __EXCEL_PATH__=""
    __db=None

    # コンストラクタの定義
    def __init__(self, mode ):
        if( mode == BrEmv.ModeDemo ):
            self.__DATA_BASE_PATH__= self.__FOLDER__+'LivingFieldD.db'
            self.__EXCEL_PATH__=os.path.join( os.path.join(fenv['data'],'summary'),'TradeSummaryD.xlsx')
        else:
            self.__DATA_BASE_PATH__= self.__FOLDER__+'LivingFieldR.db'
            self.__EXCEL_PATH__=os.path.join( os.path.join(fenv['data'],'summary'),'TradeSummaryR.xlsx')

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
    def doDbRead(self):
        _df=None
        #_clsObj=None
        self.open()
        try:
            _df=self.__doRead()
        except Exception : # origin Exception
            _df=self.__doEexcelRead()
            pass
        finally:
            self.close()

        if(issubclass(type(_df),pd.DataFrame)):
            #print("dbよみこみ成功")
            pass
        else:
            #print("dbよみこみ失敗")
            _df=pd.DataFrame()
        return(_df)

    def __doRead(self):
        #query = "SELECT Name,value FROM {0};".format(self.__TABLENAME__ ) 
        query = "SELECT * FROM {0};".format(self.__TABLENAME__ ) #要素が固まってないのでしょうがない
        _df=None
        try:
            _df = pd.read_sql(query, self.__db.engine)
            _df.drop( columns='id', inplace=True)                # idはいらないので削る

            for i in range(0,len(_df.loc[:,"lastUpR" ])) :
                #pass
                #log.error(f' D EXEC st {type(_df.loc[ 1,"lastUp" ])} {_df.loc[ 1,"lastUp" ]}')
                _df.loc[ i,"lastUpR" ]=pd.to_datetime(_df.loc[ i,"lastUpR" ])
                #log.error(f' D EXEC ed {type(_df.loc[ 1,"lastUp" ])} {_df.loc[ 1,"lastUp" ]}')

            for i in range(0,len(_df.loc[:,"lastUpE" ])) :
                #pass
                #log.error(f' D EXEC st {type(_df.loc[ 1,"lastUp" ])} {_df.loc[ 1,"lastUp" ]}')
                _df.loc[ i,"lastUpE" ]=pd.to_datetime(_df.loc[ i,"lastUpE" ])
                #log.error(f' D EXEC ed {type(_df.loc[ 1,"lastUp" ])} {_df.loc[ 1,"lastUp" ]}')

            for i in range(0,len(_df.loc[:,"first" ])) :
                _df.loc[ i,"first" ]=pd.to_datetime(_df.loc[ i,"first" ])

            _df.index=['Daily', 'Accum']

        except Exception as e:
            log.error(f"::doRead failed {e}")
            _df =self.__doEexcelRead()

        return(_df)

    #dbファイル書き込み
    def doDbWrite(self,df):
        #print("かきこみます")
        self.open()
        try:
            self.__doWrite(df)
        finally:
            self.close()
        pass;

    def __doWrite(self,_df):
        try:
            #_df=df.copy()
            #self.__Serialize(_df)
            _df.to_sql( self.__TABLENAME__,self.__db.engine,if_exists='replace',index_label='id')
            self.__db.session.commit()
            #log.error("sussss")
        except:
            self.__db.session.rollback()
            pass

    #エクセルファイル読み込み
    def __doEexcelRead(self):
        _df=pd.read_excel(self.__EXCEL_PATH__,index_col=0 )
        return(_df)

    #エクセルファイル書き込み
    def doEexcelWrite(self,_df ):
        _df.to_excel(self.__EXCEL_PATH__)

# %%
"""
if __name__ == '__main__':
    import datetime
    from general.data.summary.TradeSummary import CTradeSummary
    #雛形作成 #1列目 当日 累計　デモとリアルで別々に持つ
    def _doCreate():
        #_df=pd.DataFrame(
        _df = CTradeSummary(
        {
            'ReqNumA':[1,10],
            'ReqNumS':[2,20],
            'ReqCont':[3,30],       # 連続数

            'ExeNumA':[4,40],
            'ExeNumS':[5,50],
            'ExeCont':[30,300],     # 連続数

            'Assets':[6.00,60.00],  # 資産
            'Profit':[7.00,70.00],  # 利益
            'loss'  :[8.00,80.00],  # 損益
            'PayMe' :[9.00,90.00],  # 収支Payments
            'Progr' :[10.00,100.00],# 勝率 Progress

            'lastUp':[datetime.datetime.now(),datetime.datetime.now()],
            'Term'  :["Term1","Term2"]
        }
        )
        return(_df)
"""
