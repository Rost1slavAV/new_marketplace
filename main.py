from fastapi import FastAPI

from api.handlers.article import article_router 
from api.handlers.user import user_router
from api.handlers.category import category_router
from core.middleware import auth_middleware
from api.handlers.images import images_router

app = FastAPI()

app.middleware("http")(auth_middleware)

app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(category_router, prefix="/categories", tags=["categories"])
app.include_router(article_router, prefix="/articles", tags=["articles"])
app.include_router(images_router)