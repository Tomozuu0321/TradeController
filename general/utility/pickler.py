# %%
import pickle
import uuid

# %%
def gwtUniqueFileNamee(extension):
    f=str(uuid.uuid4())+extension
    return(f)


# %%
def Serialize( inpFileNamee,inpobj ):
    with open(inpFileNamee, 'wb') as f:
        pickle.dump(inpobj, f)


# %%
def Deserialize(inpFileNamee):
    with open(inpFileNamee, 'rb') as f:
        _tmpobj = pickle.load(f)
    return( _tmpobj)
    
