import logging
import datetime
from bson import objectid

import database

collection = database.db.user

def user_add(nickname) -> bool:
    logging.info("inserting user \"{}\"".format(nickname))
    # not giving _id, let mongoDB create one
    post = {"nickname": nickname, "reg_time": datetime.datetime.utcnow()}
    try:
        post_id = collection.insert_one(post).inserted_id
        logging.info("user \"{}\" inserted successfully with id \"{}\"".format(nickname, post_id))
        return True
    except Exception as err:
        logging.warning("cannot insert user due to the following error:\n{}".format(err))
        return False


def user_change_name(user_id: str, new_name: str):
    logging.info("user \"{}\" is changing nickname to \"{}\"".format(user_id, new_name))
    try:
        collection.update_one({"_id": objectid.ObjectId(user_id)}, {"$set": {"nickname": new_name}})
        logging.info("user \"{}\" nickname changed successfully".format(user_id))
    except Exception as err:
        logging.log("user \"{}\" nickname change failed with following error:\n{}".format(user_id, err))


def user_delete(user_id: str):
    """delete user with corresponding messages"""
    logging.info("user \"{}\" is deleting".format(user_id))
    try:
        collection.delete_one({"_id": objectid.ObjectId(user_id)})
        # delete corresponding messages
        database.message_delete_all(user_id)
        logging.info("user \"{}\" deleted successfully".format(user_id))
    except Exception as err:
        logging.log("user \"{}\" failed to delete with following error:\n{}".format(user_id, err))


def user_id_to_nickname(user_id: str) -> str | None:
    """return user nickname from id"""
    try:
        return collection.find_one({"_id": objectid.ObjectId(user_id)})["nickname"]
    except Exception as err:
        return None
