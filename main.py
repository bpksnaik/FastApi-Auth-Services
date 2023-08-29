from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from routers.auth_service import auth
from routers.recommendation_service import rec

tags_metadata = [
    {
        "name": "Auth Service",
        "description": "Providing services for user registration and login.",
    },
    {
        "name": "Recommendation Service",
        "description": "Providing services for different recommendations.",
    },
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
app.include_router(rec)
