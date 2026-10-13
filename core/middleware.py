from fastapi import Request

from core.security import get_user_from_token
from db.session import async_session


async def auth_middleware(request: Request, call_next):
    token = request.cookies.get("access_token")
    if token is None:
        request.state.user = None
        return await call_next(request)

    try:
        async with async_session() as session:
            request.state.user = await get_user_from_token(token, session)
    except Exception:
        request.state.user = None

    return await call_next(request)