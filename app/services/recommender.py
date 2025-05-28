from app.db import neo4j_conn, opensearch_conn

def add_movie(movie_id: str, title: str):
    query = "MERGE (m:Movie {id: $movie_id, title: $title})"
    neo4j_conn.query(query, {"movie_id": movie_id, "title": title})
    opensearch_conn.index_movie(movie_id, title)

def add_user(user_id: str):
    query = "MERGE (u:User {id: $user_id})"
    neo4j_conn.query(query, {"user_id": user_id})

def user_likes_movie(user_id: str, movie_id: str):
    query = """
    MATCH (u:User {id: $user_id}), (m:Movie {id: $movie_id})
    MERGE (u)-[:LIKES]->(m)
    """
    neo4j_conn.query(query, {"user_id": user_id, "movie_id": movie_id})

def user_rates_movie(user_id: str, movie_id: str, score: float):
    query = """
    MATCH (u:User {id: $user_id}), (m:Movie {id: $movie_id})
    MERGE (u)-[r:RATED]->(m)
    SET r.score = $score
    """
    neo4j_conn.query(query, {"user_id": user_id, "movie_id": movie_id, "score": score})

def recommend_movies(user_id: str):
    query = """
    MATCH (u:User {id: $user_id})-[r1:RATED]->(m:Movie)<-[r2:RATED]-(other:User)-[r3:RATED]->(rec:Movie)
    WHERE r1.score >= 3 AND r2.score >= 3 AND r3.score >= 4
    AND NOT (u)-[:RATED]->(rec)
    RETURN DISTINCT rec.title AS recommendation
    LIMIT 5
    """
    return neo4j_conn.query(query, {"user_id": user_id})