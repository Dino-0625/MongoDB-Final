import sys
import pymongo
import logging

from database.chat import *
from database.user import *

USER_NAME = "user0"
USER_PASSWORD = ""

db = None

LOG_FORMAT = "[%(levelname)s] %(asctime)s - %(message)s"
logging.basicConfig(stream = sys.stdout, 
                    filemode = "w",
                    format = LOG_FORMAT,
                    level=logging.NOTSET)

# connect to database (mongoDB)
try:
    logging.info("connecting to mongodb atlas...")
    client = pymongo.MongoClient("mongodb+srv://{}:{}@cluster0.ybzp5.mongodb.net/?retryWrites=true&w=majority".format(USER_NAME, USER_PASSWORD))
    # the name of this collection is "mongochat"
    db = client.mongochat
    print(client.list_database_names())
    logging.info("connected successfully!")
except Exception as e:
    logging.fatal(e)
    sys.exit(0)

user_add("nickeeeeee")
message_insert("629dba9a9911925d8ab5dd72", "helloooo")