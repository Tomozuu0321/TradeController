import os
# %%
GrFolderDict = dict(
{
    "data":"./data",
    "database":"sqlite:////MyPython/MyDesire/WebService/TradeController/data",
    #"home":"D:\\MyPython\\MyDesire\\WebService\\TradeController",
    "home":f"{ ((os.getcwd())[0:2]) }\\MyPython\\MyDesire\\WebService\\TradeController",
    "Request":"./data/Request"
})