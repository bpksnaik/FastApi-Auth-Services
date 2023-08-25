from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from routers.auth_service import auth

tags_metadata = [
    {
        "name": "Auth Service",
        "description": "Providing services for user registration and login.",
    }
]

app = FastAPI(
    title="My Services",
    description="List of My Api services",
    openapi_tags=tags_metadata,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth)
