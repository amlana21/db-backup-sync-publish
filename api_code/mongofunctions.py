import os
from flask_pymongo import PyMongo

class mongoFuncs:
    def __init__(self,flaskapp,mongourl):
        self.flaskapp=flaskapp
        self.flaskapp.config["MONGO_URI"] = mongourl
        self.mongo = PyMongo(self.flaskapp)
        self.collectionNames=self.mongo.db.list_collection_names()

    def getAll(self):
        queryRslts=self.mongo.db.users.find()
        # print(self.mongo.db.list_collection_names())
        return queryRslts


    def getAllTable(self,tablename):
        listdata=[]
        queryRslts = self.mongo.db[tablename].find()
        for v in queryRslts:
            listdata.append(v)
        # print(listdata)
        if len(listdata)==0:
            raise Exception('empty')
        return listdata

    def emptyTable(self,tablename):
        deleted_count=0
        delresponse=self.mongo.db[tablename].delete_many({"_id":{"$ne":None}})
        deleted_count=delresponse.deleted_count
        # if delresponse.deleted_count==0:
        #     raise Exception('empty')
        return deleted_count

    def insertData(self,tablename,data):
        for rw in data:
            self.mongo.db[tablename].insert_one(rw)
        return True


