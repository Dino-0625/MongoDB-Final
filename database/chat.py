import logging
import datetime

import pymongo
import database


def message_insert(user_id: str, msg: str) -> bool:
    logging.info("inserting message \"{}\" from user \"{}\"".format(msg, user_id))
    # the message collection
    collection = database.db.message
    post = {"_id": find_next_id(), "user": user_id, "msg": msg, "timestamp": datetime.datetime.now().isoformat()}
    try:
        post_id = collection.insert_one(post).inserted_id
        logging.info("message \"{}\" inserted successfully with id {}".format(msg, post_id))
        return True
    except Exception as err:
        logging.warning("cannot insert chat message due to the following error:\n{}".format(err))
        return False


def find_next_id() -> str:
    """find the currently max id, and +1"""
    collection = database.db.message
    max_id = collection.find().sort("_id", pymongo.DESCENDING).limit(1)
    max_id_int = int(max_id[0]["_id"])
    return str(max_id_int + 1)


def message_edit():
    pass