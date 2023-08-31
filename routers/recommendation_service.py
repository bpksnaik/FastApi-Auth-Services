import json
import time

from fastapi import APIRouter, HTTPException, status, Query
from starlette.responses import JSONResponse
from common.mongo import get_movie_recommendation_data
from common.redis_cache import RedisOperation, cache
from common.logger import logger
from common.utils import time_check
from models.service_response_schema import RecommendationResponse

rec = APIRouter()


@rec.get(
    "/movie/recommendation/v1",
    response_model=RecommendationResponse,
    tags=["Recommendation Service"],
    description="Provides recommendations for movies",
    summary="Provides a bunch of recommendation for movies based on specified keyword.",
)
def recommendation(
    title: str = Query(..., description="Enter the movie title name")
) -> JSONResponse:
    """
    Give's a bunch of movie recommendations to user based on title name.
    :param title: Movie title name.
    :return: list[dict] which contains movie recommendations.
    """
    start_time = time.perf_counter()
    try:
        # cache_data = RedisOperation.get_cache_data(title)
        cache_data = cache.get(title)
        if not cache_data:
            logger.info(
                f"Data is not present in Cache for given keyword - {str(title)}"
            )
            result = get_movie_recommendation_data(title)
            return JSONResponse({"result": result, "source": "db"})
        return JSONResponse({"result": json.loads(cache_data), "source": "cache"})

    except Exception as err:
        logger.error(f"Error in Movie recommendation api and Error - {str(err)}")
        HTTPException(
            detail=f"Error in Movie recommendation api and Error - {str(err)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    finally:
        logger.info(
            f"Total time taken for Recommendation service is {time_check(start_time, time.perf_counter())}"
        )


# if __name__ == "__main__":
#     a = recommendation("1997")
#     print(a)
