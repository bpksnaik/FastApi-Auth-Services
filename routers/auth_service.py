import logging
import time

from fastapi import APIRouter, HTTPException, status
from starlette.responses import JSONResponse

from common.mongo import create_user, user_exist
from common.utils import time_check, user_validation
from models.payload_schema import UserCredentials, Userdetails
from models.service_response_schema import UserResponse

logger = logging.getLogger(__name__)

auth = APIRouter(prefix="/user")


@auth.post(
    "/register/v1",
    tags=["Auth Service"],
    response_model=UserResponse,
    description="This Api helps the user to register into our system.",
    summary="Creation of new user in our system.",
)
def user_registration(user: Userdetails) -> JSONResponse:
    start_time = time.perf_counter()
    try:
        user_present, collection = user_exist(user)
        if not user_present:
            create_user(user, collection)
            return JSONResponse({"body": "success"}, status.HTTP_201_CREATED)

        return JSONResponse(
            {"body": "User already exist! Please login..!"}, status.HTTP_200_OK
        )
    except Exception as err:
        logger.error(f"Error in registration api and Error - {str(err)}")
        raise HTTPException(
            detail=f"Error in registration api and Error - {str(err)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    finally:
        logger.info(
            f"Total time taken for registering a user is {time_check(start_time, time.perf_counter())}ms"
        )


@auth.post(
    "/login/v1",
    tags=["Auth Service"],
    response_model=UserResponse,
    summary="Login service to Authenticate the user.",
    description="Authenticates the user to provide the access to our system after successful login.",
)
def user_login(user: UserCredentials) -> JSONResponse:
    start_time = time.perf_counter()
    try:
        user_present, collection = user_exist(user)
        if not user_present:
            return JSONResponse(
                {"body": "User doesn't exist , Please register"}, status.HTTP_200_OK
            )
        if user_validation(user, collection):
            return JSONResponse({"body": "successfully logged in"}, status.HTTP_200_OK)

        return JSONResponse(
            {"body": "Wrong credentials..!"}, status.HTTP_401_UNAUTHORIZED
        )
    except Exception as err:
        logger.error(f"Error in registration api and Error - {str(err)}")
        raise HTTPException(
            detail=f"Error in registration api and Error - {str(err)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    finally:
        logger.info(
            f"Total time taken for registering a user is {time_check(start_time, time.perf_counter())}ms"
        )
