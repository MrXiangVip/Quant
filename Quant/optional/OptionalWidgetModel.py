#  data  interface
#add 20231120
import  pandas as pd
import settings
from db.DataManager import DataManager
from settings import logger


class OptionalWidgetModel( DataManager ):

    # 获取自选表数据
    def getOptional(self):
        logger.debug("getOptional")
        try:
            sql = '''select * from optional'''
            self.optional = pd.read_sql(sql, self.engine)
        except Exception as e:
            # 如果表不存在, 则创建空表 并写回数据库
            logger.debug("error ", e)
            self.optional = pd.DataFrame( data=None, columns=settings.optional_columns)
            self.optional.to_sql( 'optional', self.engine, index=False)

        return  self.optional

    def addOptional(self, new_optional):
        logger.debug( "addOptional")
        try:
            new_optional.to_sql( 'optional', self.engine, index=False, if_exists='append')
        except Exception as e:
            logger.debug("error ", e)
        return

    def updateOptional(self, new_optional):
        logger.debug("update optional")
        try:
            new_optional.to_sql( 'optional', self.engine, index=False, if_exists='replace')
        except Exception as e:
            logger.debug("error ", e)
        return