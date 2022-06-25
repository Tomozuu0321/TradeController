from dataclasses import dataclass
from typing import List
from data.enum import CFlags,CEsti
import copy
from data.biWconst import const
from data.environment.LivingFieldEnv.BrowserEnv import BrEmv
from data.Sounds.SoundHandler import CSoundHandler

@dataclass
class CTrade():
    SummaryFlags:CFlags
    Amount:float=0
    Impossible:bool=True
    Assets:float=0.0
    Esti:CEsti=CEsti.PASS
    #lost:float=0.0
    IsLimitOver:bool=False
    Result:int=0
    mode:str=BrEmv.DefAction
    MaxValune:float=const.MaxValune
    table:object=None
    AannotateList:object=None
    diffC3533:float=0 
    diffM3533:float=0
    std35:float=0
    #diffstd:float=0
    Dev35:float=0           #偏差値
    poOp:bool=True          # PositiveOperation 積極的運用
    Issimulate=bool=False
    #MarMin:int=0
    #MarMax:int=1

    def copy(self):
        return(copy.copy(self))

    # setter
    def setTradeParams( self,Params ):
        args=Params.Receive

        if( type(args) is not list ):
            return
        _len=len(args)
        if( _len > 1 ):  #0 "loss" 1:ロス額
            Params.Loss(float(args[1]))
            Params.BfLoss(0.0)
        if( _len > 2 ): #2 積極的運用フラグ
            if( args[2] == '1' ):
                self.poOp=True
            else:
                self.poOp=False
        if( _len > 3 ): #4 損失許容額
            self.MaxValune=float(args[3])

        self.IsLimitOver=bool(False)

    #def setIsLimitOver(self,inpIsLimitOver):
    #    self.IsLimitOver=bool(inpIsLimitOver)

    def __getLoss(self,Params,mar):
        _baseAmount=Params.Amount()
        _lost=0.0
        _AllLoss=Params.Loss()

        if( _AllLoss > (_baseAmount*-1) ):
            #現在は500円以下の場合
            _lost=_AllLoss
            Params.Loss(0.0)
        else:
            #__lost=(_AllLoss*mar*-1.13) #88% payoutだから
            _lost=(_AllLoss*-1.15) + _baseAmount #86% payoutだから
            # ロスカット処理
            if( _lost > self.MaxValune ):
                #ロス額の退避
                _BfLoss=Params.BfLoss()
                Params.BfLoss(round(_BfLoss + Params.Loss() - _baseAmount,0 ))
                _lost=_baseAmount*-1
                Params.Loss(_lost)
                """
                #投資額が5000円超えたら2/3逃がして,投資資金を減らす
                _33loss=_lost/3
                _33loss=round(_33loss,0)
                # 2/3はロスカット
                Params.Loss(_33loss)
                _lost=_33loss
                """
                CSoundHandler().PlaySound( const.NoticeModeSound )

        return(_lost)

    def __lossUpdate(self,df,Params ):
    #def __lossCut(self,df,Params ):
        if( df.diff == const.InvalidValue ):
            return

        _diff=df.diff
        _AllLoss=Params.Loss()
        _AllLoss+=_diff
        _diff=0
        if( _AllLoss > 0.0 ):
            _diff=_AllLoss
            _AllLoss=0.0

        Params.Loss(_AllLoss)

        if( _diff > 0.0 ):
            _BfLoss=Params.BfLoss()
            _BfLoss+=_diff
            if( _BfLoss > 0.0 ):
                _BfLoss=0.0
            Params.BfLoss(_BfLoss)

        #self.lost+=df.diff

        #現在は資産が10%目減りしたらアラートを鳴らすだけ
        if((df.loc[ BrEmv.SummaryIndex0,"Base"] /const.lossCutBase*-1) >= _AllLoss ):
            #self.lost=0.0
            self.IsLimitOver=True

    def __NoticeMode(self,newMode):
        if( self.mode != newMode ):
            self.mode = newMode
            print(f"====取引モードが変更されました ==> {newMode} ================")
            CSoundHandler().PlaySound( const.NoticeModeSound )

    def getAmount( self,df,Martingale,Params ):

        #df.loc[ BrEmv.SummaryIndex0,'ExeCont'] =-3
        _mode=BrEmv.DefAction
        if( Params.Amount() < const.Amount ):
            Params.Amount(const.Amount)

        _baseAmount=Params.Amount()
        _Amount=_baseAmount
    
        self.__lossUpdate( df,Params )
        if df.loc[ BrEmv.SummaryIndex0,"ExeCont"] < 0 :
            simulateValue:int=1
            if(self.poOp ):
                _val = divmod(Martingale,100)
                _mar=_val[1]+1
            else:
                _mar= df.isMarPossible(Martingale)
            if(_mar==0):
                _mode=BrEmv.WaitAction
            _cnt=(df.loc[ BrEmv.SummaryIndex0,"ExeCont"])*-1
            if( _cnt < _mar ):
                _loss=self.__getLoss(Params,_cnt)
                _Amount=_loss+(_baseAmount)
                #_Amount=((_baseAmount*_cnt)*1.13) + _baseAmount
            else:
                _Amount=self.__BasicAmount(_baseAmount,_cnt+1)

            #シュミレーｔモード判定
            _mar = divmod(Martingale,100)
            if( _cnt < _mar[0]  or _mar[1] < _cnt  ):
                self.Issimulate=True
            else:
                self.Issimulate=False
        else:
            self.Issimulate=False
            #２連勝したら前回のロス額を戻す
            _cnt= df.loc[ BrEmv.SummaryIndex0,"ExeCont"]
            if(self.poOp ):
                _ExeMin=0
            else:
                _ExeMin=1
            if _cnt > _ExeMin :
                _lost=Params.BfLoss()
                if( _lost < 0.0 ):
                    _Amount=self.__BasicAmount(_baseAmount,_cnt)*-2
                    if( _lost < _Amount ):
                       _lost-=_Amount
                    else:
                       _Amount=_lost
                       _lost=0.0

                    Params.Loss(_Amount)
                    Params.BfLoss(_lost)

            _Amount=self.PositiveOperation(_baseAmount,Params.Loss(),_cnt )
            #if df.loc[ BrEmv.SummaryIndex0,"ExeCont"] > 0 :
            #self.__getLoss(Params)
            #if( self.lost > 0.0 ):
            #self.lost = 0.0

        self.__NoticeMode(_mode)

        if( self.IsLimitOver ):
            CSoundHandler().PlaySound( const.lossCutSound )

        if( _Amount < 500 ):
            _Amount=_baseAmount
            print(f"getAmount bug a{_Amount} b {_Amount }")

        self.Amount=_Amount

        _text=f"{ '積極運用' if self.poOp==True else '通常運用' } { '検証中' if self.Issimulate==True else '実行中' } 上限値 { round(self.MaxValune,2)} bF {Params.BfLoss()}"

        print(f"+++ {_text} +++++")

        print(f" getAmount { _Amount } loss {Params.Loss()} cnt { df.loc[ BrEmv.SummaryIndex0,'ExeCont'] } S:{ self.Issimulate } M: { self.mode }  -------------")

        Params.TradeMsg=_text

        return(_Amount,Params.Loss(),_mode)

    def PositiveOperation( self,baseAmount,Loss,cnt):
        if( self.poOp and Loss < 0.0 ):
            #積極的運用 かつ　損失額ありの場合
            _Amount=baseAmount+(baseAmount*1.5)     #1.5倍は適当
            pass
        else:
          _Amount=self.__BasicAmount(baseAmount,cnt)

        return(_Amount )
    
    def __BasicAmount(self,baseAmount,cnt ):
        if( cnt > 1 ):
            _Amount=(baseAmount*1.15)   #86% payoutだから
        else:
            _Amount=baseAmount
        return(_Amount )
        