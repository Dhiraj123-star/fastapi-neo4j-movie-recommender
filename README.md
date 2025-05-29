---

# 🎬 Movie Recommender System

A lightweight, scalable Movie Recommendation System built using **FastAPI**, **Neo4j**, and **OpenSearch** 🚀

---

## 💡 Features

* 📁 Upload movie metadata CSV files (e.g., from Kaggle)
* 👤 Create users in the graph database
* ❤️ Like movies
* ⭐ Rate movies from 0 to 5
* 🎯 Get personalized movie recommendations based on collaborative filtering logic
* 🔍 Fuzzy search for movies by title
* 🩺 Health check endpoint `/healthz` for service status monitoring
* 🚀 Continuous Integration & Deployment (CI/CD) with GitHub Actions and DockerHub

---

## 🧠 Tech Stack

* ⚡ FastAPI (Python)
* 🧠 Neo4j Graph Database
* 🔎 OpenSearch for fuzzy text search
* 🐍 Pandas for CSV parsing
* 🐳 Docker + Docker Compose for containerized deployment
* 🔐 Environment variables managed via `.env` and `python-dotenv`
* 🔄 GitHub Actions for CI/CD
* 🐙 DockerHub (Image Repository: `dhiraj918106/fastapi-neo4j-movie-recommender`)

---

## 📦 Core Functionality

* **Movie Upload and Indexing**: Upload movie metadata via CSV, create movie nodes in Neo4j, and index them in OpenSearch for efficient search.
* **User Management**: Add new users to Neo4j to track preferences and interactions.
* **Movie Interactions**: Allow users to like and rate movies (0–5), creating relationships in Neo4j for personalized recommendations.
* **Fuzzy Movie Search**: Search movies by title using OpenSearch’s fuzzy matching, enabling flexible queries with partial matches or typos.
* **Personalized Recommendations**: Generate movie recommendations using Neo4j graph queries based on collaborative filtering, leveraging user ratings.
* **Health Monitoring**: Expose a `/healthz` endpoint to monitor API, Neo4j, and OpenSearch connectivity.
* **CI/CD Deployment**: Automatically build and push Docker images to DockerHub on every push to the `main` branch.

---

## 🌐 API Access

Interactive API documentation available via Swagger UI at:
`http://localhost:8000/docs`

---

## 🚀 CI/CD Pipeline

This project uses GitHub Actions to:

* ✅ Lint and validate code
* 🐳 Build Docker images
* ☁️ Push images to DockerHub: `dhiraj918106/fastapi-neo4j-movie-recommender`

### Triggering CI/CD

CI/CD is triggered automatically on every push to the `main` branch.

---
