import logging
import datetime

import pymongo
import database


MAX_MSG_SHOW_COUNT = 10000

collection = database.db.message


def get_all() -> list:
    """retur all message"""
    # from new to old
    msg_list = collection.find().sort(
        "_id", pymongo.DESCENDING).limit(MAX_MSG_SHOW_COUNT)
    return list(msg_list)


def get_between_dates(date_begin: datetime.datetime, date_end: datetime.datetime) -> list:
    """return all message between two dates"""
    msg_list = collection.find({"date": {"$gt": date_begin.isoformat()}, "date": {"$lt": date_end.isoformat()}}) \
        .sort("_id", pymongo.DESCENDING).limit(MAX_MSG_SHOW_COUNT)
    return list(msg_list)


def get_all_statistics() -> list:
    query = [
        {
            "$group": {
                "_id": "$user_id",
                "name": {
                    "$first": "$user_name",
                },
                "msg_count": {
                    "$sum": 1,
                },
                "char_count": {
                    "$sum": {
                        "$strLenCP": "$msg",
                    },
                },
                "avg_len": {
                    "$avg": {
                        "$strLenCP": "$msg",
                    },
                },
            }
        }
    ]
    try:
        result = list(collection.aggregate(query))
        return result
    except Exception as err:
        logging.warning(
            "Getting message statistic of everyone: {}".format(err))
        return list()


def get_statistic_of_user(user_id: str) -> dict:
    logging.info("Getting statistic of user \"{}\"".format(user_id))

    name = database.user.id_to_nickname(user_id)
    if name == "":
        logging.warning("No such user")
        return dict()

    query = [
        {
            "$match": {
                "user_id": user_id,
            }
        },
        {
            "$group": {
                "_id": "null",
                "name": {
                    "$first": "$user_name",
                },
                "msg_count": {
                    "$sum": 1,
                },
                "char_count": {
                    "$sum": {
                        "$strLenCP": "$msg",
                    },
                },
                "avg_len": {
                    "$avg": {
                        "$strLenCP": "$msg",
                    },
                },
            }
        }
    ]
    try:
        result = list(collection.aggregate(query))
        # no message yet
        if len(result) == 0:
            return {"msg_count": 0, "char_count": 0, "avg_len": 0}
        return result[0]
    except Exception as err:
        logging.warning(
            "Getting message statistic of user \"{}\": {}".format(user_id, err))
        return dict()


def insert(user_id: str, msg: str) -> bool:
    """add new message into database"""
    # check if there's user or not
    user_name = database.user.id_to_nickname(user_id)
    if user_name == "":
        logging.warning(
            "Failed to insert message because there is no user with id \"{}\"".format(user_id))
        return False

    logging.info(
        "Inserting message \"{}\" from user \"{}\"".format(msg, user_name))

    # cannot send empty string
    if len(msg) == 0:
        logging.info("Empty message is rejected")
        return False

    post = {
        "_id": _find_next_id(),
        "user_id": user_id,
        "user_name": user_name,
        "msg": msg,
        "date": datetime.datetime.now().isoformat(),
    }

    try:
        post_id = collection.insert_one(post).inserted_id
        logging.info(
            "Message \"{}\" inserted successfully with id {}".format(msg, post_id))
        return True
    except Exception as err:
        logging.warning(
            "Cannot insert chat message due to the following error:\n{}".format(err))
        return False


def _find_next_id() -> int:
    """find the currently max id, and +1"""
    # exception happens when database was not initialized, return id 0
    try:
        cursor = collection.find().sort("_id", pymongo.DESCENDING).limit(1)
        max_id = int(cursor[0]["_id"])
    except Exception as err:
        logging.warning(err)
        return 0
    return max_id + 1


def delete_one(user_id: str, msg_id: int) -> bool:
    """delete one message"""
    try:
        logging.info(
            "Deleting message \"{}\" from user \"{}\"".format(msg_id, user_id))
        collection.delete_one({"user_id": user_id, "_id": msg_id})
        return True
    except Exception as err:
        logging.warning(
            "Cannot delete message from user \"{}\" due to the following error:{}\n".format(user_id, err))
        return False


def delete_all(user_id: str) -> bool:
    """delete all messages from one user"""
    try:
        logging.info("Deleting all message from user \"{}\"".format(user_id))
        collection.delete_many({"user_id": user_id})
        return True
    except Exception as err:
        logging.warning(
            "Cannot delete all messages from user \"{}\" due to the following error:{}\n".format(user_id, err))
        return False


def edit_one(user_id: str, msg_id: int, new_msg: str) -> bool:
    """edit one message from one user"""
    try:
        logging.info("Editing message from user \"{}\"".format(user_id))
        collection.update_one(
            {"user_id": user_id, "_id": msg_id},
            {"$set": {"msg": new_msg}},
        )
        return True
    except Exception as err:
        logging.warning(
            "Cannot edit messages from user \"{}\" due to the following error:{}\n".format(user_id, err))
        return False
