import time
from datetime import datetime
import json

import pymongo.collection
from pymongo import MongoClient
from fastapi import HTTPException, status

from common.utils import generate_unique_id, hashing_pw, time_check
from common.redis_cache import RedisOperation
from common.logger import logger
from config import user_collection_name, db_name, movie_collection_name, mongo_url

from .authorizer import generate_token


class MongoConnection:
    @staticmethod
    def make_connection(collection_name):
        """Makes a mongo connection
        :return: collection
        """
        # making a mongo connection for a specific db and collection
        logger.info(f"Establishing a Mongo connection.")
        client = MongoClient(mongo_url)
        db = client[db_name]
        return db[collection_name]


def user_exist(user_details) -> (bool, pymongo.collection.Collection):
    """Checks whether the user exists in our system or not.
    :param user_details: user information provided by the user
    :return: tuple(bool, pymongo.collection.Collection)
    """
    try:
        # making a mongo connection
        collection = MongoConnection.make_connection(user_collection_name)
        # query to find the respective document from mongo collection
        query = {"email_id": user_details.email_id}
        collection_data = [data for data in collection.find(query)]
        if collection_data:
            return True, collection
        return False, collection

    except Exception as err:
        logger.error(f"Error while validating the User and Error {err}")


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


def get_movie_recommendation_data(title: str) -> list[dict]:
    """
    Get's movie recommendation from mongo and stores in redis.
    :param title: movie title name
    :return: list[dict]
    """
    start_time = time.perf_counter()
    try:
        logger.info(f"Fetching Recommendation data from Mongo.")
        collection = MongoConnection.make_connection(
            collection_name=movie_collection_name
        )
        query = {"$text": {"$search": title}}
        data = [
            data
            for data in collection.find(
                query,
                {
                    "_id": 0,
                    "title": 1,
                    "genres": 1,
                    "overview": 1,
                    "runtime": 1,
                    "spoken_languages": 1,
                    "original_title": 1,
                },
            )
        ]

        # cache the data in redis
        RedisOperation.set_cache_data(title, json.dumps(data))
        return data

    except Exception as err:
        logger.error(
            f"Error in getting movie recommendation from db and Error  - {str(err)}"
        )
        raise HTTPException(
            detail=f"Error in getting movie recommendation from db and Error  - {str(err)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    finally:
        logger.info(
            f"Time taken to fetch the data from mongo is {time_check(start_time, time.perf_counter())}"
        )
