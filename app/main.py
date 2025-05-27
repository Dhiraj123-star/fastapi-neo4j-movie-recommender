from fastapi import FastAPI
from app.routes import movies

app = FastAPI(title="Movie Recommender System")

app.include_router(movies.router, prefix="/api")