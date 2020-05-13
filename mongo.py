import pymongo
import random
from secrets import Mongo
from datetime import datetime

print("Mongo")

class MongoDB:

    def __init__(self):
        print("Connecting to MongoDB...")
        self.client = pymongo.MongoClient(Mongo.connectionString)
        print("Available databases: ")
        print(self.client.list_database_names())
        print("\n\nConnecting to database: redditScrapper")
        self.database = self.client["redditScrapper"]
        print("Available collections: ")
        print(self.database.list_collection_names())
        self.logs = self.database["logs"]
        self.data = self.database["data"]

    def writeLog(self, logMessage):
        print("Logging...")
        self.logs.insert_one(logMessage)

    def writeData(self, data):
        timestamp = datetime.now()
        try:
            item = {
                **data,
                "timestamp": timestamp
            }
            self.data.insert_one(item)
            self.writeLog({
                "status": "success",
                "message": "Data inserted",
                "timestamp": timestamp
            })
        except Exception as e:
            print(e)
            self.writeLog({
                "status": "fail",
                "message": "Data not inserted",
                "exception": e,
                "timestamp": timestamp
            })

    def findMeme(self, query):
        return self.data.find_one(query)

    def getAllMeme(self, **kwargs):
        arg_limit = 0
        if "limit" in kwargs:
            arg_limit = kwargs["limit"]
        return self.data.find({}, limit=arg_limit)

    def findMemeAndUpdate(self, query, newThing):
        return self.data.find_one_and_update(query, newThing)


if __name__ == '__main__':
    mongodb = MongoDB()