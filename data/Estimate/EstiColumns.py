import os
from datetime import datetime
from dataclasses import dataclass
import pandas as pd
import numpy as np
from data.environment.LivingFieldEnv.Folder import GrFolderDict as fenv

@dataclass(frozen=True)
class CEstimateColumns:
    Target:str='close'      #計算対象のカラム
    item0:str='std'
    item1:str='mean'
    item2:str='upper0'
    item3:str='lower0'
    item4:str='upper1'
    item5:str='lower1'
    item6:str='division'

    #Ool:int=0   # Not used
    Buy:int=0   # df idx0
    Sell:int=1   # df idx1

    AannotateTextindex:int=4
    Aannotateindex:float=3.5
    Division0:float=1.5
    Division1:float=0.5
    Period:int=3
    #OutOfRange:float=1.0
    #dMin:float=-0.5
    #dMax:float=1.5
    __EXCEL_PATH__:str=os.path.join( os.path.join(fenv['data'],'Estimate'),'Estimate.xlsx')
    __CSV_PATH__:str=os.path.join( os.path.join(fenv['data'],'Estimate'),'Estimate.csv')

    #__EXCEL_PATH__:str='Estimate.xlsx'
    #__CSV_PATH__:str='Estimate.csv'

    #_Values:object=None
    _Values:object=pd.read_csv( __CSV_PATH__,dtype=np.float64,sep=",")
    #_Values.columns=[ i for i in range(24)]

    #@property  # 2022/06/12  propertyは引数を渡せない事が判明　あたりまえか
    #def OutOfRange(self):
    #return(0.3)

    def __ChkValue( self,val ):
        if( val > 1.2 ):
            _val=1.2
        elif( val < -1.2 ):
            _val=1.2
        elif( -0.05 < val ) and ( val <= -0.0 ):
            #print(f"hit2 { round(val,1) }")
            _val=0.0
        else:
            _val=round(val,1)

        return(f"{_val:0.1f}")

    def dBuy(self,std30):
        _std=self.__ChkValue( std30 )
        #print(f"Call dBuy {type(_std)} { _std }")
        return(self._Values[_std][self.Buy])

    def dSell(self,std30):
        _std=self.__ChkValue( std30 )
        #print(f"all dSell {type(_std)} { _std }")
        return(self._Values[_std][self.Sell])

    #エクセルファイル読み込み
    def read_excel(self):
        _Values=pd.read_excel(self.__EXCEL_PATH__,index_col=0 )
        #_Values=pd.read_excel(self.__EXCEL_PATH__,index_col=0 )
        return(_Values)

    #エクセルファイル書き込み
    def to_excel(self):
        self._Values.to_excel(self.__EXCEL_PATH__)

    #CSVファイル書き込み
    def doCsvWrite( self ):
        self._Values.to_csv( self.__CSV_PATH__,float_format="%0.3f",sep=",",mode='w' )

    #CSVファイル読み込み
    """
    def doCsvRaad( self ):
        self._Values=pd.read_csv( self.__CSV_PATH__,dtype=np.float64,sep=",")
        print("OK")
    #"""
    """
    def CreateValues(self):
        _Values=pd.DataFrame( np.array([
                            [0.3 for n in range(24)],
                            [-0.5 for n in range(24)],
                            [1.5 for n in range(24)]
                            ])
                            #,index=[0.0,1.0,1.2,1.3,4.0,5.0,6.0]
                            #,columns=[_c.Target]
                            )
        _Values.to_csv( self.__CSV_PATH__,float_format="%0.3f",sep=",",mode='w' )
        _Values.to_excel(self.__EXCEL_PATH__)
    """

PEstimateColumns=CEstimateColumns()

"""
if __name__ == '__main__':

    #_e=CEstimateColumns()
    #_e.doCsvRaad()
    #print(f"{type(_e._Values) } {_e._Values}" )

    _df=_e.read_excel()

    _dic={}
    for _column in _df.columns:
        print(type(_column))
        _newCol=f'{ str(_column ) }'
        _dic[_column]=_newCol
        _df2=_df.rename(columns=_dic)

    print( _df2 )

    print("sesss")
    
    #_e.doCsvWrite()
    _df2.to_csv( 'Estimate.csv',float_format="%0.3f",sep=",",mode='w' )
    
    print("end")
"""