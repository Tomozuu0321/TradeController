# %%
from os import path
from datetime import date,time
import pandas as pd
from data.environment.LivingFieldEnv.Folder import GrFolderDict as fenv
from data.environment.LivingFieldEnv.BrowserEnv import BrEmv
from  process.MatrixTable import CSts,CEvt

# %%
class CinformationSystem:

    __FOLDER__=path.join( fenv['data'],'information')
    __JSON_PATH__=path.join( __FOLDER__,'System.json')
    __EXCEL_PATH__=path.join( __FOLDER__,'System.xlsx')

    #josnファイル読み込み
    def doRead(self):
        _df=pd.read_json(self.__JSON_PATH__)
        self.__Deserialize(_df)
        return(_df)

    #josnファイル書き込み
    def doWrite(self,df):
        _df=df.copy()
        self.__Serialize(_df)
        _df.to_json(self.__JSON_PATH__,date_format='iso')

    #エクセルファイル読み込み
    def read_excel(self):
        _df=pd.read_excel(self. __EXCEL_PATH__,index_col=0 )
        self.__Deserialize(_df)
        return(_df)

    #エクセルファイル書き込み
    def to_excel(self,df):
        _df=df.copy()
        self.__Serialize(_df)
        _df.to_excel(self.__EXCEL_PATH__)

    #dbファイル読み込み
    def read_sql(self,mode):
        #if __name__ == '__main__':
        #   from database.DbConInformationSystem import CDbConInformationSystem
        #else:
        from general.data.database.DbConInformationSystem import CDbConInformationSystem

        _db=CDbConInformationSystem(mode)
        _db.open()
        try:
            _df=_db.doRead()
        finally:
            _db.close()
        return(_df)

    #dbファイル書き込み
    def to_sql(self,mode,df):
        from general.data.database.DbConInformationSystem import CDbConInformationSystem

        _db=CDbConInformationSystem(mode)
        #df.to_pickle();
        
        _db.open()
        try:
            _db.doWrite(df)
        finally:
            _db.close()

    def __Serialize(self,df):
        _sts=df['value'][0]
        _evt=df['value'][1]
        df['value'][0]=CSts[_sts.name].name
        df['value'][1]=CEvt[_evt.name].name
        df['value'][9]=str(pd.to_datetime(df['value'][9]))

        """
        _d=df['value'][7]
        list=[_d.year,_d.month,_d.day]
        df['value'][7]=list
        _t=df['value'][8]
        list=[_t.hour,_t.minute,_t.second]
        df['value'][8]=list

        #if __name__ == '__main__':
        """
    def __Deserialize(self,df):
        _sts=df['value'][0]
        _evt=df['value'][1]
        df['value'][0]=CSts[_sts]
        df['value'][1]=CEvt[_evt]
        df['value'][9]=pd.Timestamp(df['value'][9])
        #df['value'][7]=pd.to_datetime(df['value'][7])

        """
        list=df['value'][7]
        if( type(list) is str ):
            list = [int(s) for s in list.lstrip("[").rstrip("]").split(',',3)]
        _date=date(list[0],list[1],list[2])
        df['value'][7]=_date

        list=df['value'][8]
        if( type(list) is str ):
            list = [int(s) for s in list.lstrip("[").rstrip("]").split(',',3)]
        _time=time(list[0],list[1],list[2])
        df['value'][8]=_time
        """

    def getHtml( self,df,Digits):
        _df=df.copy()
        _val=_df.loc[9,"value"]
        _datetime= pd.to_datetime(_val)
        _df.loc[9,"value"]=_datetime.strftime('%Y/%m/%d')
        _df.loc[10,"value"]=_datetime.strftime('%H:%M:%d')
        _df.loc[10,"Name"]="Time"
        #_df=_df.reindex(index=[0,1,2,3,4,5,6,7,8,9])
        _df=_df.round(Digits+2)
        return(_df.to_html())


