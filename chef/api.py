from ninja import NinjaAPI
from posts.api import router as posts_router
from users.api import router as users_router

api = NinjaAPI()

api.add_router("/posts/", posts_router)
api.add_router("/users/", users_router)
