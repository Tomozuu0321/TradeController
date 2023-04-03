import os
import pandas as pd
#from flask import Flask
#from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
from general.utility.logger import log
from data.environment.LivingFieldEnv.Folder import GrFolderDict as fenv
from data.environment.LivingFieldEnv.BrowserEnv import BrEmv

class CIoHandler():

    __FOLDER__=path=fenv['database']+'/database/'
    __TABLENAME__="tranSummary"
    __DATA_BASE_PATH__=""
    __EXCEL_PATH__=""
    __engine=None
    #__db=None

    # コンストラクタの定義
    def __init__(self, mode ):
        if( mode == BrEmv.ModeDemo ):
            self.__DATA_BASE_PATH__= self.__FOLDER__+'LivingFieldTD.db'
            self.__EXCEL_PATH__=os.path.join( os.path.join(fenv['data'],'summary'),'TranSummaryTD.xlsx')
            self.__CSV_PATH__=os.path.join( os.path.join(fenv['data'],'summary'),'TranSummaryTD.csv')
        else:
            self.__DATA_BASE_PATH__= self.__FOLDER__+'LivingFieldTR.db'
            self.__EXCEL_PATH__=os.path.join( os.path.join(fenv['data'],'summary'),'TranSummaryTR.xlsx')
            self.__CSV_PATH__=os.path.join( os.path.join(fenv['data'],'summary'),'TranSummaryTR.csv')

    def open(self):
        _echoOn=False   #True
        self.__engine = create_engine(self.__DATA_BASE_PATH__, echo=_echoOn)
        """
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = self.__DATA_BASE_PATH__
        app.config["SQLALCHEMY_ECHO"] =False #True  # default True
        #警告メッセージを抑制すろ為,「SQLALCHEMY_TRACK_MODIFICATIONSS」を設定する 追跡機能らしい
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
        self.__db = SQLAlchemy(app)
        """

    def close(self):
        self.__engine.dispose()
        #self.__db.session.close_all()

    #dbファイル読み込み
    def doDbRead(self):
        _df=None
        #_clsObj=None
        self.open()
        try:
            _df=self.__doRead()
        except Exception : # origin Exception
            pass
        finally:
            self.close()

        if(issubclass(type(_df),pd.DataFrame)):
            #print("dbよみこみ成功")
            pass
        else:
            #print("dbよみこみ失敗")
            df=pd.DataFrame(dict({'id':[0]}))
            pass
        return(_df)

    def __doRead(self):
        #query = "SELECT Name,value FROM {0};".format(self.__TABLENAME__ ) 
        #query = "SELECT * FROM {0};".format(self.__TABLENAME__ ) #要素が固まってないのでしょうがない
        #query = "SELECT id FROM {0} ORDER BY id DESC LIMIT 10 ;".format(self.__TABLENAME__ ) 
        #query = "SELECT * FROM {0};".format(self.__TABLENAME__ ) #要素が固まってないのでしょう
        #query = "SELECT  COUNT(*) FROM {0} ;".format(self.__TABLENAME__ ) 
        query = "SELECT * FROM {0} ORDER BY id DESC LIMIT 10 ;".format(self.__TABLENAME__ ) 
        #query = "SELECT * FROM {0} ".format(self.__TABLENAME__ ) 
        _df=None
        try:
            #_df = pd.read_sql(query, self.__db.engine)
            _df = pd.read_sql(sql=text(query), con=self.__engine.connect())
            #_df.drop( columns='id', inplace=True)                # Trnは追記の為 Idが必要
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
            #_df.to_sql( self.__TABLENAME__,self.__db.engine,if_exists='replace',index_label='id')
            #_df.to_sql( self.__TABLENAME__,self.__db.engine,if_exists='fail',index_label='id')
             #_df.to_sql( self.__TABLENAME__,self.__db.engine,if_exists='append',index_label='id')
            _df.to_sql( self.__TABLENAME__, con=self.__engine,if_exists='append',index_label='id')
            pass    # commit if successful
        except Exception as e:
            log.error(e)
            pass    # rollback if failed
        """
            self.__db.session.commit()
            #log.error("sussss")
        except:
            self.__db.session.rollback()
            pass
        """
    #エクセルファイル読み込み
    def __doEexcelRead(self):
        _df=pd.read_excel(self. __EXCEL_PATH__,index_col=0 )
        return(_df)

    #エクセルファイル書き込み
    def doEexcelWrite(self,_df ):
        _df.to_excel(self.__EXCEL_PATH__)

    #CSVファイル書き込み
    # 特定カラムだけ　df.to_csv('data/dst/to_csv_out_columns.csv', columns=['age'])
    # 書き込みモード（新規作成、上書き、追記）: def mode='w' mode='x' mode='a'
    # ヘッダー、インデックスありなし: 引数header, index
    # df.to_csv('data/dst/to_csv_out_header_index.csv', header=False, index=False)
    def doCsvWrite( self,df,inpColumns="",Inpheader=False ):
        if( inpColumns =="" ):
            df.to_csv( self.__CSV_PATH__,header=Inpheader,mode='a',index=False )
        else:
            df.to_csv( self.__CSV_PATH__,header=Inpheader,mode='a',index=False,columns=inpColumns )
