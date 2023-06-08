from datetime import date,time
from dataclasses import field,dataclass
from data.enum import CBSize,CFlags,CSts,CEvt
from data.biWconst import const
from data.environment.LivingFieldEnv.BrowserEnv import BrEmv

@dataclass
class CParam:
    #sts=CSts.NONE
    #evt: str="aa"
    dfs: dict=field(default_factory=dict)   # information.System dict
    conf:dict=field(default_factory=dict )  
    driver:object=None
    bsize:CBSize=CBSize.SMALL   # browser size small or large
    Receive:object=None
    #BrowserEnv:object=None
    TradeSummary:object=None
    TranSummary:object=None
    Msg:str=""          # Message general string
    EstiMsg:str=""      # Message Estimate string
    EstiMsg2:str=""     # Message Estimate string
    TradeMsg:str=""     # Message Trade string
    Flags:CFlags=CFlags.CLEAN
    Flags:CFlags=CFlags.CLEAN
    e:object=Exception("test Err")
    trade:object=None
    tran:object=None
    #Estimate:object=None

    #SummaryFlags:CFlags=CFlags.CLEAN
    #owner:object=None   #オーナオブジェクト

    #def SetConf(selse,iconf):

    def GetUrlEx(self,UrlIdx,HostIdx,PortIdx):
        url=self.conf['Url'][UrlIdx] % (self.conf['Host'][HostIdx],self.conf['Port'][PortIdx])
        return(url)

    def GetUrl(self,UrlIdx):
        url=self.conf['Url'][UrlIdx]
        return(url)

    def __accessor__(self,idx,DefaultValue,*args):
        try:
            if len(args) == 1 :
                self.dfs["value"][idx]=args[0]
            _val=self.dfs["value"][idx]
            return(_val)
        except:
            return(DefaultValue)

    def sts(self,*args) :
        return( self.__accessor__(0,CSts.NONE,*args))

    def evt(self,*args) :
        return( self.__accessor__(1,CEvt.NONE,*args))

    def PlatformName(self,*args) :
        return( self.__accessor__(2,BrEmv.PlatformWindows,*args))

    def Mode(self,*args) :
        return( self.__accessor__(3,BrEmv.DefMode,*args))

    def action(self,*args) :
        return( self.__accessor__(4,BrEmv.DefAction,*args))

    def Martingale(self,*args) :
    #def Payments(self,*args) :
        return( self.__accessor__(5,305,*args))

    def Amount(self,*args) :
        return( self.__accessor__(6,const.Amount,*args))

    def Loss(self,*args) :                          #2022 5/28ロス額に変更

        if len(args) >= 1 :
            if(args[0] > 20000.000 or args[0] < -20000.00 ):
                from data.Sounds.SoundHandler import CSoundHandler
                from data.biWconst import const
                #print(f"CParam::Los over (20000) { args[0] }")
                #CSoundHandler().PlaySound( const.NoticeModeSound )

        return( self.__accessor__(7,0.0,*args))

    def BfLoss(self,*args) :
        return( self.__accessor__(8,0.0,*args))

    def Date(self,*args) :
        return( self.__accessor__(9,date(1999,11,12),*args))

    def __setattr__(self, key, value):
        _s=str(value);
        #log.debug(_s)
        if( len( _s ) > 0 ) : 
            if( _s.startswith("<function")):
                #print.error("CParam Method cannot be changed")
                raise Exception("CParam Method cannot be changed")
        super().__setattr__(key, value)

