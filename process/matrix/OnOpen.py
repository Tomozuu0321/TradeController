
from data.environment.LivingFieldEnv.Folder import GrFolderDict as fenv
from data.environment.LivingFieldEnv.BrowserEnv import BrEmv
from data.biWconst import const
from general.utility.logger import MatrixFunction,log
from general.utility.StopWatch import MatrixFunctionEx

@MatrixFunctionEx
def OnOpen(Params,sts,evt):

    from data.enum import CPmd,CFlags
    #import LivingFieldEnv.BrowserEnv as e

    def __doRaad(Params,sts,evt):

        from general.data.environment.LivingFieldEnvUrl import CLivingFieldEnvUrl
        Params.conf= CLivingFieldEnvUrl().doRead()

        from general.data.informationSystem import CinformationSystem
        info=CinformationSystem()

        if( BrEmv.ShortStart ):
            Params.dfs=info.doRead()
        else:
            try:
                Params.dfs=info.read_sql(Params.Mode())
            except:
                Params.dfs=info.doRead()

        if( Params.Amount() < const.Amount ):
            Params.Amount(const.Amount)

        from general.data.summary.TradeSummary import CTradeSummary
        Params.TradeSummary=CTradeSummary().doDbRead(Params.Mode())
        from general.data.summary.TranSummary import CTranSummary
        Params.TranSummary=CTranSummary().doDbRead(Params.Mode())
        #Params.dfs=info.doRead()   # メンテナンス用

        from data.TradeInfo import CTrade
        Params.trade=CTrade(CFlags.FAILED)
        Params.trade.Assets=const.InvalidValue
        Params.tran=CTrade(CFlags.FAILED)
        Params.trade.Impossible=True

    #設定読み込み処理
    __doRaad(Params,sts,evt)
    _PlatformMode= BrEmv.PlatformMode

    if( _PlatformMode !=CPmd.NOCHG ):
        if( _PlatformMode ==CPmd.TO_A ):
            Params.PlatformName(BrEmv.PlatformAndroid)

        if( _PlatformMode ==CPmd.TO_W ):
            Params.PlatformName(BrEmv.PlatformWindows)

    #if( _PlatformMode != CPmd.NOSTART ):
    #    import process.matrix.modules.BrowserControl.BrowserControls as _ctl
    #    _ctl.BrOpen(Params,sts,evt)
    #    #　以下ログイン処理
    #    #_ctl.BrLogin(Params,sts,evt)”
