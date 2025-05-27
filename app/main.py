from fastapi import FastAPI
from app.routes import movies
from app.routes import health

app = FastAPI(
    title="🎬 Movie Recommender API",
    description="A production-grade movie recommendation engine powered by FastAPI and Neo4j.",
    version="1.0.0"
)

# Route registration
app.include_router(movies.router, prefix="/api/movies")
app.include_router(health.router)
