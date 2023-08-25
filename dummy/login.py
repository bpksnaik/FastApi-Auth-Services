import logging
import time

from fastapi import FastAPI, status
from pydantic import BaseModel, EmailStr, Field
from starlette.responses import JSONResponse

from common.mongo import create_user, user_exist
from common.response import response_structure
from common.utils import time_check, user_validation

app = FastAPI(
    title="Auth Service",
    description="Providing services for user registration and login",
    tags=["Auth Service"],
)
logger = logging.getLogger(__name__)


class Userdetails(BaseModel):
    name: str = Field(description="name of the user")
    email_id: EmailStr = Field(description="User's Email_id")
    password: str = Field(description="user's password")


class UserCredentials(BaseModel):
    email_id: EmailStr = Field(description="User's Email_id")
    password: str = Field(description="User's password")


class response(BaseModel):
    body: str = Field(description="response details")
    status_code: int = Field(description="status code")


@app.post("/register/v1")
def user_registration(user: Userdetails, q: str | None = None) -> JSONResponse:
    start_time = time.perf_counter()
    try:
        user_present, collection = user_exist(user)
        if not user_present:
            create_user(user, collection)
            # return {"result": "success"}
            return response_structure({"body": "success"}, status.HTTP_201_CREATED)

        return response_structure(
            {"body": "User already exist! Please login..!"}, status.HTTP_200_OK
        )
    except Exception as err:
        logger.error(f"Error in registration api and Error - {str(err)}")
    finally:
        logger.info(
            f"Total time taken for registering a user is {time_check(start_time, time.perf_counter())}ms"
        )


@app.post("/login/v1")
def user_login(user: UserCredentials) -> JSONResponse:
    start_time = time.perf_counter()
    try:
        user_present, collection = user_exist(user)
        if not user_present:
            return response_structure(
                {"body": "User doesn't exist , Please register"}, status.HTTP_200_OK
            )
        if user_validation(user, collection):
            return response_structure(
                {"body": "successfully logged in"}, status.HTTP_200_OK
            )

        return response_structure(
            {"body": "Wrong credentials..!"}, status.HTTP_401_UNAUTHORIZED
        )
    except Exception as err:
        logger.error(f"Error in registration api and Error - {str(err)}")
    finally:
        logger.info(
            f"Total time taken for registering a user is {time_check(start_time, time.perf_counter())}ms"
        )
