from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.config import API_TOKEN


security = HTTPBearer()


def verify_api_token(
    credentials: HTTPAuthorizationCredentials
):
    """
    Verify the API bearer token.
    """

    if credentials.credentials != API_TOKEN:

        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API token",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    return True