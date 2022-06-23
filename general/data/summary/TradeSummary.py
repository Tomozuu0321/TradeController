import datetime
from dataclasses import dataclass
import pandas
from data.enum import CFlags
from data.biWconst import const
from general.utility.logger import log,MatrixSupportClassMethod
from general.utility.StopWatch import StopWatchEx
from data.environment.LivingFieldEnv.BrowserEnv import BrEmv

@dataclass
class CTradeSummary( pandas.DataFrame ):

    __oldAssets:float=const.InvalidValue

    from general.data.summary.tradeSummary.IoHandler import CIoHandler
    from general.data.summary.tradeSummary.DisplayHandler import _getHtml
    from general.data.summary.tradeSummary.CalceHandler import _SetRequestResult,_SetTradeResult,_isMarPossible,_SetExeCnts
    from general.data.summary.baseModules.DataClear import _DataClear

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

    def doDataClear( self,SummaryIndex,base,ExeCont):
        from data.biWconst import const
        #log.error(f" call {__name__}_SetRequestResult-000 {datetime.datetime.now()}")
        log.error(f" call {__name__}::doDataClear-000 {datetime.datetime.now()}")
        self._DataClear( SummaryIndex )
        if( base != const.InvalidValue ):
            if( SummaryIndex==BrEmv.SummaryIndex1 ):
                self.SetAssets( base,SummaryIndex )
            self.__SetBase( base,SummaryIndex )
        if( ExeCont != 100 ):
            self.__SetExeCont( ExeCont,SummaryIndex )

    #dbファイル読み込み
    @classmethod
    def doDbRead(cls,mode):
        return(CTradeSummary(cls.CIoHandler(mode).doDbRead()))

    #dbファイル書き込み
    def doDbWrite(self,mode):
        self.CIoHandler(mode).doDbWrite(self)

    #エクセルファイル書き込み
    def doEexcelWrite(self,mode):
        self.CIoHandler(mode).doEexcelWrite(self)

    def doUpdate(self,mode):
        self.CIoHandler(mode).doDbWrite(self)

    #
    # トレード結果関係
    #

    #
    # getter
    #

    #資産変動値
    @property
    def diff(self):
        return(self.loc[ BrEmv.SummaryIndex0,"Assets"]-self.__oldAssets)
    #連続数の更新
    @property
    def ExeCont(self):
        return(self.loc[ BrEmv.SummaryIndex0,"ExeCont"])

    """"
    @property
    def Assets(self):
        return(self.loc[ BrEmv.SummaryIndex0,"Assets"])

    #トレード稼働率
    @property
    def Assets
    TraNum(self):
        return(1)

    def TraScsPar(self):
        return(1)

    # 連続数
    
    #勝率
    def TraScsPar(self):
        return(1)
    """

    # setter
    #@StopWatchEx("SetTradeResult")
    #@MatrixSupportClassMethod
    def SetTradeResult(self,Params,Tran):
        self.__oldAssets=self.loc[ BrEmv.SummaryIndex0,"Assets"]
        return(self._SetTradeResult( Params,Tran ))

    #Set
    def SetAssets( self,Assets,mode=BrEmv.SummaryIndex0 ):
        self.loc[ mode,"Assets"]=Assets

    def __SetBase( self,base,mode=BrEmv.SummaryIndex0 ):
        self.loc[ mode,"Base"]=base
        """_summary_
        Args:
            base (_type_): _description_
            mode (_type_, optional): _description_. Defaults to BrEmv.SummaryIndex0.
        """

    def __SetExeCont(self,ExeConet,mode=BrEmv.SummaryIndex0 ):
        self.loc[ mode,"ExeCont"]=ExeConet

    # こっちはマーチン用リスト設定
    def SetExeCnts(self,inpNewlen):
        return(self._SetExeCnts(inpNewlen))

    #
    # トレードリクエスト関係
    #

    #購入成功率 Trade Success Percentage
    """
    @property
    def ReqScsPar(self):
        return(1)

    # 連続数
    def ReqCont(self):
        return(1)
        #'ReqCont':[3,30],       # 連続数
    """

    # setter
    def SetRequestResult(self,Params,Tran ):
        return(self._SetRequestResult(Params,Tran))

    def isMarPossible( self,Martingale ):
        return(self._isMarPossible(Martingale))

    def getHtml( self,Digits ):
        return(self._getHtml(Digits))

    