import logging

from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


def response_structure(result: dict, status_code: int) -> JSONResponse:
    """Common response structure for Api result
    :param result: Api returning result data
    :param status_code: status code
    :return: JSONResponse
    """

    try:
        return JSONResponse(content=result, status_code=status_code)

    except Exception as err:
        logger.error(
            f"Error while structuring the final response and Error - {str(err)}"
        )
