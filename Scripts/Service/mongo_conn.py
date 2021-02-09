import pandas as pd
import pymongo



myclient = pymongo.MongoClient("mongodb+srv://xfactor-test:1g5riG7DgDAqEGW4@cluster0.13dtx.mongodb.net/ex-factor-test?retryWrites=true&w=majority")
mydb = myclient["ex-factor-test"]['users']
df = pd.DataFrame(list(mydb.find({})))
