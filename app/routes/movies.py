from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
import pandas as pd
from io import StringIO
from app.services.recommender import (
    add_movie, add_user, user_likes_movie, user_rates_movie, recommend_movies
)
from app.db import opensearch_conn

router = APIRouter()

class RateRequest(BaseModel):
    score: float

@router.post("/upload-movies")
async def upload_movies_csv(file: UploadFile = File(...)):
    contents = await file.read()
    decoded = contents.decode('utf-8')

    try:
        df = pd.read_csv(StringIO(decoded))
    except Exception as e:
        return {"error": f"Failed to read CSV: {str(e)}"}

    if 'id' in df.columns:
        df.rename(columns={'id': 'movieId'}, inplace=True)
    if not {'movieId', 'title'}.issubset(df.columns):
        return {"error": "CSV must contain 'movieId' and 'title' columns."}

    df = df[['movieId', 'title']].dropna()
    df['movieId'] = df['movieId'].astype(str)
    df['title'] = df['title'].astype(str)
    df.drop_duplicates(subset=['movieId'], inplace=True)

    count = 0
    for _, row in df.iterrows():
        try:
            add_movie(row['movieId'], row['title'])  # Indexes in Neo4j and OpenSearch
            count += 1
        except Exception as e:
            print(f"Skipping row {row['movieId']} due to error: {e}")
            continue

    return {"msg": f"{count} movies added and indexed successfully."}

@router.post("/users/{user_id}")
def create_user(user_id: str):
    add_user(user_id)
    return {"msg": f"User {user_id} added."}

@router.post("/users/{user_id}/like/{movie_id}")
def like_movie(user_id: str, movie_id: str):
    user_likes_movie(user_id, movie_id)
    return {"msg": f"User {user_id} liked movie {movie_id}."}

@router.post("/users/{user_id}/rate/{movie_id}")
def rate_movie(user_id: str, movie_id: str, rating: RateRequest):
    if rating.score < 0 or rating.score > 5:
        raise HTTPException(status_code=400, detail="Rating must be between 0 and 5")
    user_rates_movie(user_id, movie_id, rating.score)
    return {"msg": f"User {user_id} rated movie {movie_id} with score {rating.score}"}

@router.get("/users/{user_id}/recommendations")
def get_recommendations(user_id: str):
    recs = recommend_movies(user_id)
    return {"recommendations": [r["recommendation"] for r in recs]}

@router.get("/search")
def search_movies(query: str):
    if not query:
        raise HTTPException(status_code=400, detail="Query parameter is required")
    results = opensearch_conn.search_movies(query)
    return {"results": results}