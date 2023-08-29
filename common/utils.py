import uuid
from logging import getLogger

import bcrypt
from fastapi import HTTPException, status

from common.logger import logger


def hashing_pw(password: bytes) -> bytes:
    """Hashing the user password.
    :param password: user password in bytes
    :return: hashed password in bytes
    """
    try:
        # hashing the user password
        logger.info(f"Hashing the User Password.")
        hashed_pw = bcrypt.hashpw(password, bcrypt.gensalt())
        return hashed_pw

    except Exception as err:
        logger.error(f"Error while hashing the password and Error - {str(err)}")
        raise HTTPException(
            detail=f"Error while hashing the password and Error - {str(err)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


def generate_unique_id() -> str:
    """Generating a unique id for the user
    :return: str
    """
    try:
        # Generating unique id for the user's
        logger.info(f"Generating a Unique id for the user.")
        uid = str(uuid.uuid4())
        return uid

    except Exception as err:
        logger.error(f"Error while generating the user id and Error - {str(err)}")
        raise HTTPException(
            detail=f"Error while generating the user id and Error - {str(err)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


def user_validation(user_details, collection) -> bool:
    """Validating the user credential when he's logging in.
    :param user_details: user details
    :param collection : mongo collection
    :return: bool
    """
    try:
        query = {"email_id": user_details.email_id}
        user_hashed_pw = [
            data for data in collection.find(query, {"password": 1, "_id": 0})
        ][0].get("password", "")

        # checks user provided password matches with user's login password stored in mongo
        logger.info(f"Validating the user password.")
        if bcrypt.checkpw(user_details.password.encode("utf-8"), user_hashed_pw):
            return True
        return False

    except Exception as err:
        logger.error(f"Error while validating the user and Error - {str(err)}")
        raise HTTPException(
            detail=f"Error while validating the user and Error - {str(err)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


def time_check(start_time: float, end_time: float) -> float:
    """Gives the time difference between two epoch time.
    :param start_time: start epoch time
    :param end_time: end epoch time
    :return: float
    """
    return end_time - start_time
