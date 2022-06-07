import logging
import datetime
import string
import secrets

import database

# 52 letters with length 6 have 19,770,609,664 combinations
ID_LEN = 6

collection = database.db.user


def _random_id() -> str:
    id = [secrets.choice(string.ascii_letters) for _ in range(ID_LEN)]
    return "".join(id)


def user_add(nickname: str) -> str:
    """add new user when someone first come into chatroom"""
    logging.info("inserting user \"{}\"".format(nickname))
    
    user_id = _random_id()
    # deal with id duplication, which is rarely happen
    row = collection.find_one({"_id": user_id})
    # row == None if there is no user yet
    while (row != None) and (len(row) != 0):
        user_id = _random_id()

    post = {"_id": user_id, "nickname": nickname, "reg_date": datetime.datetime.utcnow()}
    try:
        post_id = collection.insert_one(post).inserted_id
        logging.info("user \"{}\" inserted successfully with id \"{}\"".format(nickname, post_id))
        return user_id
    except Exception as err:
        logging.warning("cannot insert user due to the following error:\n{}".format(err))
        return ""


def user_change_name(user_id: str, new_name: str) -> bool:
    """change user nickname"""
    logging.info("user \"{}\" is changing nickname to \"{}\"".format(user_id, new_name))
    try:
        collection.update_one({"_id": user_id}, {"$set": {"nickname": new_name}})
        logging.info("user \"{}\" nickname changed successfully".format(user_id))
        return True
    except Exception as err:
        logging.log("user \"{}\" nickname change failed with following error:\n{}".format(user_id, err))
        return False


def user_delete(user_id: str) -> bool:
    """delete user with corresponding messages"""
    logging.info("user \"{}\" is deleting".format(user_id))
    try:
        collection.delete_one({"_id": user_id})
        # delete corresponding messages
        database.message_delete_all(user_id)
        logging.info("user \"{}\" deleted successfully".format(user_id))
        return True
    except Exception as err:
        logging.log("user \"{}\" failed to delete with following error:\n{}".format(user_id, err))
        return False
        

def user_id_to_nickname(user_id: str) -> str:
    """return user nickname from id"""
    try:
        res = collection.find_one({"_id": user_id}, {"_id": 0, "nickname": 1})
        return res["nickname"]
    except Exception as err:
        logging.warning("converting user id to nickname:\n{}".format(err))
        return None
