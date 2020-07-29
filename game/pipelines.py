# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import pymysql
from pymysql import cursors
from twisted.enterprise import adbapi

class GamePipeline:
    def __init__(self):
        self.headers = ['game_name','box_txt','game_tag','detail_url','game_intro']
        # with open('game.csv','a+',encoding='utf-8',newline='') as fp:
        #     self.writer = csv.DictWriter(fp, self.headers)
        #     self.writer.writeheader()

    def process_item(self, item, spider):
        with open('game.csv','a+',encoding='utf-8',newline='') as fp:
            writer = csv.DictWriter(fp, self.headers)
            writer.writeheader()
            writer.writerows([dict(item)])

        # self.writer.writerows([dict(item)])
        return item

class GameSqlPipeline:
    def __init__(self):
        dbparams = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': '34808',
            'db': 'game',
            'charset': 'utf8'
        }
        self.conn = pymysql.connect(**dbparams)
        self.cursor = self.conn.cursor()
        self._sql = None

    def process_item(self, item, spider):
        self.cursor.execute(self.sql, (item['game_name'],item['game_tag'],
                                       item['box_txt'],item['game_fever'],
                                       item['game_fav'],item['game_neg'],
                                       item['game_avg'],item['feedback_rate'],
                                       item['detail_url'],item['game_intro']))
        self.conn.commit()
        return item

    @property
    def sql(self):
        if not self._sql:
            self._sql = """
                    insert into info
                    values
                    (null, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
            return self._sql
        return self._sql


class GameTwistedPipeline(object):
    def __init__(self):
        dbparams = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': '34808',
            'db': 'game',
            'charset': 'utf8',
            'cursorclass': cursors.DictCursor
        }
        self.dbpool = adbapi.ConnectionPool('pymysql', **dbparams)
        self._sql = None

    def process_item(self,item,spider):
        defer = self.dbpool.runInteraction(self.insert_item,item)
        defer.addErrback(self.handle_error,item,spider)

    def insert_item(self,cursor,item):
        cursor.execute(self.sql, (item['game_name'],item['game_tag'],
                                   item['box_txt'],item['game_fever'],
                                   item['game_fav'],item['game_neg'],
                                   item['game_avg'],item['feedback_rate'],
                                   item['detail_url'],item['game_intro']))

    def handle_error(self,error,item,spider):
        print("=" * 10 + 'error' + "=" * 10)
        print(error)
        print("=" * 10 + 'error' + "=" * 10)

    @property
    def sql(self):
        if not self._sql:
            self._sql = """
                insert into info
                values
                (null, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            return self._sql
        return self._sql