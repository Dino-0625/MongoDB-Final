import logging
import datetime

import pymongo
import database


MAX_MSG_SHOW_COUNT = 10000

collection = database.db.message


def message_get_all() -> list:
    """retur all message"""
    # from new to old
    msg_list = collection.find().sort("_id", pymongo.DESCENDING).limit(MAX_MSG_SHOW_COUNT)
    return msg_list


def message_get_date_between(date_begin: datetime.datetime, date_end: datetime.datetime) -> list:
    """return all message between two dates"""
    msg_list = collection.find({"date": {"$gt": date_begin.isoformat()}, "date": {"$lt": date_end.isoformat()}}) \
        .sort("_id", pymongo.DESCENDING).limit(MAX_MSG_SHOW_COUNT)
    return msg_list


def message_insert(user_id: str, msg: str) -> bool:
    """add new message into database"""
    # check if there's user or not
    user_name = database.user_id_to_nickname(user_id)
    if user_name == None:
        logging.warning("failed to insert message because there is no user with id \"{}\"".format(user_id))
        return False

    logging.info("inserting message \"{}\" from user \"{}\"".format(msg, user_name))

    post = {
        "_id": _find_next_id(), 
        "user_id": user_id,
        "user_name": user_name,
        "msg": msg, "date": datetime.datetime.utcnow(),
        }

    try:
        post_id = collection.insert_one(post).inserted_id
        logging.info("message \"{}\" inserted successfully with id {}".format(msg, post_id))
        return True
    except Exception as err:
        logging.warning("cannot insert chat message due to the following error:\n{}".format(err))
        return False


def _find_next_id() -> str:
    """find the currently max id, and +1"""
    # exception happens when database was not initialized, return id 0
    try:
        cursor = collection.find().sort("_id", pymongo.DESCENDING).limit(1)
        max_id = cursor[0]["_id"]
    except Exception as err:
        logging.warning(err)
        return 0
    return max_id + 1


def message_delete_one(user_id: str, msg_id: int):
    """delete one message"""
    try:
        logging.info("deleting message \"{}\" from user \"{}\"".format(msg_id, user_id))
        collection.delete_one({"user_id": user_id, "_id": msg_id})
    except Exception as err:
        logging.warning("cannot delete message from user \"{}\" due to the following error:{}\n".format(user_id, err))


def message_delete_all(user_id: str):
    """delete all messages from one user"""
    try:
        logging.info("deleting all message from user \"{}\"".format(user_id))
        collection.delete_many({"user_id": user_id})
    except Exception as err:
        logging.warning("cannot delete all messages from user \"{}\" due to the following error:{}\n".format(user_id, err))


def message_edit(user_id: str, msg_id: int, new_msg: str):
    """edit one message from one user"""
    try:
        logging.info("editing message from user \"{}\"".format(user_id))
        collection.update_one({"user_id": user_id, "_id": msg_id}, {"$set": {"msg": new_msg}})
    except Exception as err:
        logging.warning("cannot delete all messages from user \"{}\" due to the following error:{}\n".format(user_id, err))
