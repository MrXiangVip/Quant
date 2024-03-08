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
        logger.debug("getOptional")
        df = pd.DataFrame( )
        items =self.collection.find()
        for item in items:
            print( item )
            row = pd.DataFrame.from_dict([item])
            df=df.append(row, ignore_index=True)
        return  df

    def addOptional(self, new_optional):
        logger.debug( "addOptional", new_optional)
        result = self.collection.insert_one(new_optional)
        logger.info("add Optional", result)

    def updateOptional(self, new_optional):
        logger.debug("update optional")
        # try:
        #     new_optional.to_sql( 'optional', self.engine, index=False, if_exists='replace')
        # except Exception as e:
        #     logger.debug(("error ", e))
        return