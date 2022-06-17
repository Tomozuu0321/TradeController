import pandas as pd
#import numpy as np
#import time
import matplotlib.pyplot as plt

import os
import io
import glob
from data.enum import CEvt
from data.environment.LivingFieldEnv.Folder import GrFolderDict as fenv
from data.environment.LivingFieldEnv.BrowserEnv import BrEmv
from general.utility.logger import log
import general.utility.pickler as pp
from general.utility.Requester import doCreate
from data.Estimate.EstiColumns import PEstimateColumns as _c


from matplotlib.backends.backend_agg import FigureCanvasAgg
#import cStringIO
from io import BytesIO

def GraphDraw( table,AannotateList ):
    _key=CEvt.ViSUAL.name
    f=os.path.join(fenv['Request'],pp.gwtUniqueFileNamee(".pickle"))
    _data=[table,AannotateList]
    dic=doCreate( _key,_data )
    pp.Serialize(f,dic)

def GraphDraw2( owner,table,AannotateList,mode=0 ):

    if( BrEmv.isGgraphNotShow ):
        return

    def _parseEsti(val):
        _id="Pass"
        if(val=='1'):
            _id="Buy"
        elif (val=='2'):
            _id="Sell"
        return(_id)

    def _inner_func( table,lists,st,max,interval,offset):
        plt.plot(table.index,table[_c.Target],label=_c.Target,marker="o")
        plt.plot(table.index,table[_c.item1],label=_c.item1)
        plt.plot(table.index,table[_c.item2],label=_c.item2)
        plt.plot(table.index,table[_c.item3],label=_c.item3)
        plt.plot(table.index,table[_c.item4],label=_c.item4)
        plt.plot(table.index,table[_c.item5],label=_c.item5)

        #アノテーション表示 ***注意*** yytext の値はxyからのオフセット
        for i in range(st,max):
            _idx =lists[i][0]
            _tidx=lists[i][1]
            #print(f" idx {_idx} t:{type(_idx)}")
            #print(f" ti  {_tidx} t:{type(_tidx)}")

            plt.annotate( _parseEsti(_tidx),
                            xy=[_idx,(table[_c.Target][_idx]+interval)],xytext=[-1,offset],fontsize=10,
                            color='red',textcoords='offset points',arrowprops=dict(width=1,color='black'))

    #グラフ全体の設定」
    plt.figure(figsize=(9,5))
    _max=len(AannotateList)-2
    plt.subplot(121)
    _inner_func(table,AannotateList,0,_max,-3,-30)
    plt.legend()    #注釈を表示　注*ラベルが必要
    plt.title('3 Bollinger Band ALL')
    plt.ylabel('BITCOIN')

    table1=table.drop(table.index[[0,1,2,7]])
    plt.subplot(122)
    plt.subplots_adjust(wspace=0.2)
    _inner_func(table1,AannotateList,_max-2,_max+2,-1,-30)
    plt.legend()    #注釈を表示　注*ラベルが必要
    plt.title('3 Bollinger Band Exp')
    #plt.ylabel('BITCOIN')

    _path=""
    if( mode == 0):
        #画像フォルダ一内のファイルを全て削除する
        try:
            for p in glob.glob( BrEmv.visualPAth+"*.*" ):
                if os.path.isfile(p):
                    os.remove(p)
            #os.remove(BrEmv.visualPAth+"*,*")
            #ユニークなファイル名を取得
            _path=BrEmv.visualPAth+pp.gwtUniqueFileNamee(".png")
            plt.savefig(_path)
        except Exception as e: # origin Exception
            log.error( f' GraphDraw2 savefig failed t:{type(e)} #e:{ e }')

    elif(mode == 1):
        plt.show()

    return(_path)

    #plt.savefig( os.path.join("templates",BrEmv.visualFile))
    #if( BrEmv.visualization == 1 ):
    #    plt.show()

