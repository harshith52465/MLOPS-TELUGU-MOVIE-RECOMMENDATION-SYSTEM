from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import joblib
import os

app = FastAPI()

# CORS (allow frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model
movies = joblib.load("movies.pkl")
similarity = joblib.load("similarity.pkl")

movies["Movie_clean"] = movies["Movie"].str.strip().str.lower()


#  API endpoint
@app.post("/predict")
def recommend(req: dict):
    movie_name = req.get("movie", "").strip().lower()

    match = movies[movies["Movie_clean"] == movie_name]

    if match.empty:
        return {"error": "Movie not found"}

    idx = match.index[0]

    distances = similarity[idx]

    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommendations = [movies.iloc[i[0]].Movie for i in movie_list]

    return {
        "input_movie": movies.iloc[idx].Movie,
        "recommendations": recommendations
    }
