#
# 20231120
#
from db.DataManager import DataManager

import datetime
import pandas as pd
from settings import logger

class NewsWidgetModel(DataManager):

    # 获取新闻数据
    def getNews(self, start_date, end_date=0):
        logger.debug(("get news","start date ->", start_date, "end date ->", end_date ))

        today = datetime.datetime.today().date()
        # 先从数据库中查询 这天的新闻,如果数据库中不存在表，则去tushare 获取并插入表中
        self.news_df = pd.DataFrame()
        try:
            if start_date.date() ==  today:
                if end_date==0:
                    self.news_df = self.pro.news( start_date = str(start_date.date()) )
                    self.news_df['focus'] = self.news_df['content'].apply( self.getFocus )

                else:
                    self.news_df = self.pro.news( start_date=str(start_date), end_date= str(end_date) )
                    self.news_df['focus'] = self.news_df['content'].apply( self.getFocus )

            else:
                logger.debug( "start ", start_date, " end ",end_date)
        except Exception as e:
            logger.debug("error", e)
        return  self.news_df
    #

