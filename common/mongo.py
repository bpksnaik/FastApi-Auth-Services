import logging
from datetime import datetime

import pymongo.collection
from pymongo import MongoClient

from common.utils import generate_unique_id, hashing_pw
from settings import config

from .authorizer import generate_token

logger = logging.getLogger(__name__)


class MongoConnection:
    mongo_uri = config.get("MONGO_URL")
    db_name = config.get("DB_NAME")
    collection_name = config.get("COLLECTION_NAME")

    @staticmethod
    def make_connection():
        """Makes a mongo connection
        :return: collection
        """
        # making a mongo connection for a specific db and collection
        client = MongoClient(MongoConnection.mongo_uri)
        db = client[MongoConnection.db_name]
        return db[MongoConnection.collection_name]


# def user_exist(user_details):
def user_exist(user_details) -> (bool, pymongo.collection.Collection):
    """Checks whether the user exists in our system or not.
    :param user_details: user information provided by the user
    :return: tuple(bool, pymongo.collection.Collection)
    """
    try:
        # making a mongo connection
        collection = MongoConnection.make_connection()
        # query to find the respective document from mongo collection
        query = {"email_id": user_details.email_id}
        collection_data = [data for data in collection.find(query)]
        if collection_data:
            return True, collection
        return False, collection

    except Exception as err:
        logger.error(f"Error while validating the User and Error {err}")


# def create_user(user_details, collection) -> None:
def create_user(user_details, collection: pymongo.collection.Collection) -> None:
    """Creates user in our system when user is registering for the 1st time.
    :param user_details: user information provided by the user.
    :param collection: Mongo collection.
    :return: None
    """
    try:
        # Hashing the password using bcrypt lib
        hashed_pw = hashing_pw(str(user_details.password).encode("utf-8"))
        # generating Unique for the user using UUID
        uid = generate_unique_id()
        token = generate_token(
            {
                "name": user_details.name,
                "uid": uid,
                "timestamp": datetime.timestamp(datetime.now()),
            }
        )
        user_data = {
            "name": user_details.name,
            "email_id": user_details.email_id,
            "password": hashed_pw,
            "token": token,
        }

        # loading the user document in mongo collection
        collection.insert_one(user_data)
    except Exception as err:
        logger.error(f"Error while creating the user and Error - {str(err)}")
