# %%
#from data.Param import CParam
#from general.data.database.DbConInformationSystem import CDbConInformationSystem
#from data.Param import CParam
#Params=CParam()
#_df=None

# %%
import pickle
import urllib
import pandas as pd
import numpy as np
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from general.utility.logger import log

# %%
from dataclasses import dataclass
import datetime
import pandas
#from data.Param import CParam
#from data.TradeInfo import CTrade

@dataclass
class CTranSummary( pandas.DataFrame ):

    from general.data.summary.tranSummary.IoHandler import CIoHandler
    #from general.data.summary.tranSummary.DisplayHandler import _getHtml
    from general.data.summary.tranSummary.CalceHandler import _SetTransaction

    #self._ioHandler=self.CIoHandler()
    #_ioHandler=None

    # コンストラクタの定義 (DataFrameを継承するモデルの場合このコンストラクタが必要 )
    def __init__( self,*args,**kargs ):
        self = super().__init__(*args,**kargs)
        return(self)

    def __str__(self):
        return(super().__str__())
        #ret=super().__str__()
        #return ret
    def __repr__(self):
        return(super().__repr__())
        #ret=super().__repr__()
        #return ret

    def doDataClear( self,SummaryIndex):
        #log.error(f" call {__name__}_SetRequestResult-000 {datetime.datetime.now()}")
        log.error(f" call {__name__}::doDataClear-000 {datetime.datetime.now()}")

    #dbファイル読み込み
    @classmethod
    def doDbRead(cls,mode):
        return(CTranSummary(cls.CIoHandler(mode).doDbRead()))

    #dbファイル書き込み
    def doDbWrite(self,mode,df):
        self.CIoHandler(mode).doDbWrite(df)

    #エクセルファイル書き込み
    def doEexcelWrite(self,mode):
       self.CIoHandler(mode).doEexcelWrite(self)

    #CSV書き出し
    def doCsvWrite(self,mode,df,inpColumns,header=False):
        self.CIoHandler(mode).doCsvWrite(df,inpColumns,header)

    #
    # #トランザクションを結果関係
    #

    # setter
    def SetTransaction(self,Params,Tran):
        #return(self.aaa(Params,Tran))
        return(self._SetTransaction(Params,Tran))

    #画面表示データ作成
    #def getHtml( self,Digits ):
        #return(self._getHtml( self,Digits ))

# %%
