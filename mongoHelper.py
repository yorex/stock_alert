# coding=utf-8

# sudo pip install pymongo
from pymongo import MongoClient
import logger
import pymongo
import types

class MongoHelper:
    def __init__(self, dbName):
        self.dbName = dbName
        try:
            self.conn = MongoClient("127.0.0.1", 27017)
            self.db = self.conn[dbName]
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

    def insert(self, collectionName, data):
        ## 例如insert({"name":"zhangsan","age":18})
        collection = self.db[collectionName]
        if collection:
            return collection.insert(data)
        else:
            logger.error("mongo is not inited, insert fail")
    
    def update(self, collectionName, query, data, isUpsert=True):
        collection = self.db[collectionName]
        if collection:
            return collection.update(query, {"$set":data}, upsert=isUpsert)
        else:
            logger.error("mongo is not inited, update fail")
    
    def remove(self, collectionName, query):
        collection = self.db[collectionName]
        if collection:
            return collection.remove(query)
        else:
            logger.error("mongo is not inited, remove fail")

    # sort ascending by key:date
    def find(self, collectionName, query, limit=300):
        collection = self.db[collectionName]
        if collection:
            cursor = collection.find(query).sort("date", pymongo.ASCENDING)
            count = cursor.count()
            limit = limit if limit < count else count;
            datas = [d for d in cursor.skip(count-limit).limit(limit)]
            cursor.close()
            return datas 
        else:
            logger.error("mongo is not inited, remove fail")

    def drop(self, collectionName):
        if collectionName:
            self.db.drop_collection(collectionName)
            logger.warn("drop collection: " + collectionName)
    

if __name__ == '__main__':
    mongo=MongoHelper('stock')
    date="20190810"
    collection='test2'
    print(mongo.insert(collection, {"date":date, "index":234}))
    
    result=mongo.find(collection, {"date":date})
    for r in result:
        print("r:%s" % r)

    mongo.remove(collection, {"date":date})
    
    result=mongo.find(collection, {})
    print("size: %d" % len(result))
    for r in result:
        print("r:%s" % r)
