import pandas as pd

def CalcPercent( inpValue1,inpValue2 ):
    wrkinpValue= (((inpValue1)/(inpValue2)))
    return((wrkinpValue)*100)

# 平均を求める
# a+((b-a)/cnt)
#
def CalcAverage( inpValue1,inpValue2,inpCount ):
    if( 1 > inpCount  ):
        return(inpValue2)
    return(inpValue1 +((inpValue2-inpValue1)/inpCount))

def GetFutur( inpValue1,inpValue2,inpCount):
    _diff=inpValue2-inpValue1
    return(inpValue2+_diff*inpCount)

#偏差値を計算する
def CalcDivision( inpValue1,inpValue2,inpStd ):
    return(((inpValue1-inpValue2)/inpStd))

def CalcBollingerBands( df,_c ):
    # ボリンジャーバンドの計算
    table = pd.DataFrame()
    table[_c.Target]= df[_c.Target]
    table[_c.item1] = df[_c.Target].rolling(window=_c.Period).mean()
    table[_c.item0] = df[_c.Target].rolling(window=_c.Period).std()
    table[_c.item6] = CalcDivision(table[_c.Target],table[_c.item1],table[_c.item0])
    table[_c.item2] = table[_c.item1] + (table[_c.item0] * _c.Division0)
    table[_c.item3] = table[_c.item1] - (table[_c.item0] * _c.Division0)
    table[_c.item4] = table[_c.item1] + (table[_c.item0] * _c.Division1)
    table[_c.item5] = table[_c.item1] - (table[_c.item0] * _c.Division1)
    
    return(table)

