from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import authentication, posts, users, likes

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["https://www.google.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST ...
    allow_headers=["*"],
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(authentication.router)
app.include_router(likes.router)


@app.get("/")
async def root():
    return {"success": True, "message": "Hello FastAPI!"}
