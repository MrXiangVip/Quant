#  data  interface
#add 20231120
import  pandas as pd
import settings
from db import DataManager
from settings import logger


class OptionalWidgetModel( ):
    settings={
        "collection_name":"optional"
    }
    def __init__(self):
        self.dm =DataManager()
        self.collection = self.dm.db[ OptionalWidgetModel.settings['collection_name']]
        print("OptionalModel")


    def getOptional(self):
        logger.info("getOptional")
        df = pd.DataFrame( )
        items =self.collection.find()
        for item in items:
            print( item )
            row = pd.DataFrame.from_dict([item])
            df=df.append(row, ignore_index=True)
        logger.info( df.columns )
        if not df.empty:
            df.drop('_id', axis=1, inplace=True)
        return  df

    def addOptional(self, new_optional):
        logger.info(( "addOptional", new_optional))
        result = self.collection.insert_one(new_optional)
        logger.info(("add Optional", result))

    def updateOptional(self, newOptional):
        logger.info("update optional")
        # 先删除全部数据集
        result=self.collection.delete_many({})
        # 再写入
        for index, row in newOptional.iterrows():
            logger(index, row, row.to_dict())
            result = self.collection.insert_one( row.to_dict() )
        return