import logging
import database

def user_add(nickname) -> bool:
    logging.info("inserting user \"{}\"".format(nickname))
    # the user collection
    collection = database.db.user
    # not giving _id, let mongoDB create one
    post = {"nickname": nickname}
    try:
        post_id = collection.insert_one(post).inserted_id
        logging.info("user \"{}\" inserted successfully with id {}".format(nickname, post_id))
        return True
    except Exception as err:
        logging.warning("cannot insert user due to the following error:\n{}".format(err))
        return False
