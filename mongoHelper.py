# coding=utf-8

# sudo pip install pymongo
from pymongo import MongoClient

class MongoHelper:
    def __init__(self, host, dbName, collectionName):
        self.dbName = dbName
        self.collectionName = collectionName 
        self.client = MongoClient(host, 27021)
        self.db = self.client.get_database(dbName)
        self.collection = self.db.get_collection(collectionName)

    def cmp_date(self, x, y):
        return x < y ? 1 : -1

    # 首先默认对date字段进行降序排序, 然后检查是否插入
    # 假如keys对应条件的记录不存在，则插入
    def checkAndInsert(self, data, existsKeys):
        data.sort(self.cmp_date)
        print data
