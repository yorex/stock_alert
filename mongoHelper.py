# coding=utf-8

# sudo pip install pymongo
from pymongo import MongoClient
import logger
import pymongo

class MongoHelper:
    def __init__(self, host, dbName, collectionName):
        self.dbName = dbName
        self.collectionName = collectionName 
        try:
            self.conn = MongoClient(host, 27017)
            self.db = self.conn[dbName]
            self.collection = self.db[collectionName]
        except Exception as e:
            logger.error("mongo exception: %s" % str(e))

    def __del__(self):
        pass

    '''
        LINE FORMAT:
        {
            "date":"20190801", 
            ... , 
            "alert_emergs":{"rule1":["a11","a12"], "rule2":["a21", "a22"]}, 
            "alert_warns":{"rule1":["b11","b12"], "rule2":["b21", "b22"]} 
        }
    '''
    @staticmethod
    def get_alert_emergs(iterator):
        emergs_days=[]
        for rec in iterator:
            emergs_per_day = []
            for value in rec["alert_emergs"].values():
                emergs_per_day += value
            emergs_days.append(emergs_per_day)
        return emergs_days

    @staticmethod
    def get_alert_warns(iterator):
        warns_days=[]
        for rec in iterator:
            warns_per_day = []
            for value in rec["alert_warns"].values():
                warns_per_day += value
            warns_days.append(warns_per_day)
        return warns_days

    def cmp_date(self, x, y):
        return 1 if x < y else 0

    # 首先默认对date字段进行降序排序, 然后检查是否插入
    # 假如keys对应条件的记录不存在，则插入
    def checkAndInsert(self, data, existsKeys):
        data.sort(self.cmp_date)
        print data

    def insert(self, data):
        ## 例如insert({"name":"zhangsan","age":18})
        if self.collection:
            return self.collection.insert(data)
        else:
            logger.error("mongo is not inited, insert fail")
    
    def update(self, query, update, isUpsert=True):
        if self.collection:
            return self.collection.update(query, {"$set":update}, upsert=isUpsert)
        else:
            logger.error("mongo is not inited, update fail")
    
    def remove(self, query):
        if self.collection:
            return self.collection.remove(query)
        else:
            logger.error("mongo is not inited, remove fail")

    # sort ascending by key:date
    def find(self, query):
        if self.collection:
            cursor = self.collection.find(query).sort("date", pymongo.ASCENDING)
            datas = [d for d in cursor]
            cursor.close()
            return datas 
        else:
            logger.error("mongo is not inited, remove fail")


if __name__ == '__main__':
    mongo=MongoHelper('127.0.0.1', 'stock', 'test2')
    print(mongo.insert({"date":"20190804", "index":234}))
    
    result=mongo.find({"date":"20190804"})
    for r in result:
        print("r:%s" % r)

    mongo.remove({"date":"20190804"})
    
    result=mongo.find({})
    print("size: %d" % result.count())
    for r in result:
        print("r:%s" % r)
