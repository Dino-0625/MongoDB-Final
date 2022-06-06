import logging
import datetime
import string
import secrets

import database

# 52 letters with length 6 have 19,770,609,664 combinations
ID_LEN = 6

collection = database.db.user


def random_id() -> str:
    id = [secrets.choice(string.ascii_letters) for _ in range(ID_LEN)]
    return "".join(id)


def user_add(nickname: str) -> bool:
    """add new user when someone first come into chatroom"""
    logging.info("inserting user \"{}\"".format(nickname))
    
    user_id = random_id()
    # deal with id duplicated, which is rarely happen
    row = collection.find_one({"_id": user_id})
    while (row != None) and (len(row) != 0):
        user_id = random_id()

    post = {"_id": user_id, "nickname": nickname, "reg_date": datetime.datetime.utcnow()}
    try:
        post_id = collection.insert_one(post).inserted_id
        logging.info("user \"{}\" inserted successfully with id \"{}\"".format(nickname, post_id))
        return True
    except Exception as err:
        logging.warning("cannot insert user due to the following error:\n{}".format(err))
        return False


def user_change_name(user_id: str, new_name: str):
    """change user nickname"""
    logging.info("user \"{}\" is changing nickname to \"{}\"".format(user_id, new_name))
    try:
        collection.update_one({"_id": user_id}, {"$set": {"nickname": new_name}})
        logging.info("user \"{}\" nickname changed successfully".format(user_id))
    except Exception as err:
        logging.log("user \"{}\" nickname change failed with following error:\n{}".format(user_id, err))


def user_delete(user_id: str):
    """delete user with corresponding messages"""
    logging.info("user \"{}\" is deleting".format(user_id))
    try:
        collection.delete_one({"_id": user_id})
        # delete corresponding messages
        database.message_delete_all(user_id)
        logging.info("user \"{}\" deleted successfully".format(user_id))
    except Exception as err:
        logging.log("user \"{}\" failed to delete with following error:\n{}".format(user_id, err))


def user_id_to_nickname(user_id: str) -> str | None:
    """return user nickname from id"""
    try:
        res = collection.find_one({"_id": user_id}, {"_id": 0, "nickname": 1})
        return res["nickname"]
    except Exception as err:
        logging.warning("converting user id to nickname:\n{}".format(err))
        return None
