import sys
import pymongo
import logging

USER_NAME = "user0"
USER_PASSWORD = "nvBnZYTYtU6HSSJj"

db = None

LOG_FORMAT = "[%(levelname)s] %(asctime)s - %(message)s"
logging.basicConfig(stream = sys.stdout, 
                    filemode = "w",
                    format = LOG_FORMAT,
                    level=logging.NOTSET)

# connect to database (mongoDB)
try:
    logging.info("Connecting to mongodb atlas...")
    client = pymongo.MongoClient("mongodb+srv://{}:{}@cluster0.ybzp5.mongodb.net/?retryWrites=true&w=majority".format(USER_NAME, USER_PASSWORD))
    # the name of this database is "mongoch"
    db = client.mongoch
    logging.info("Mongodb connected successfully")
except Exception as e:
    logging.fatal("Connection failed: {}".format(e))
    sys.exit(0)

from database import message
from database import user
