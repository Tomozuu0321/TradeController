from general.utility.logger import MatrixFunction,log

#@MatrixFunction
def OnVisual(Params,sts,evt):

    _data=Params.Receive
    _key=_data['MT'][0]["Evt"]

    Params.trade.table=_data['MT'][0][_key][0]
    Params.trade.AannotateList=_data['MT'][0][_key][1]

