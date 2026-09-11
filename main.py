from fastapi import FastAPI, HTTPException

app = FastAPI()

movies = [
    {
        "id": 1,
        "title": "The Matrix",
        "genre": "sci-fi",
        "year": 1999,
        "rating": 8.7
    },

    {
        "id": 2,
        "title": "Inception",
        "genre": "sci-fi",
        "year": 2010,
        "rating": 8.8
    },

    {
        "id": 3,
        "title": "The Dark Knight",
        "genre": "action",
        "year": 2008,
        "rating": 9.0
    },

    {
        "id": 4,
        "title": "Forrest Gump",
        "genre": "drama",
        "year": 1994,
        "rating": 8.8
    },

    {
        "id": 5,
        "title": "The Hangover",
        "genre": "comedy",
        "year": 2009,
        "rating": 7.7
    },

    {
        "id": 6,
        "title": "Interstellar",
        "genre": "sci-fi",
        "year": 2014,
        "rating": 8.7
    },

    {
        "id": 7,
        "title": "Parasite",
        "genre": "drama",
        "year": 2019,
        "rating": 8.5
    },

    {
        "id": 8,
        "title": "Barbie",
        "genre": "comedy",
        "year": 2023,
        "rating": 6.8
    }
]


@app.get("/movies/{movie_id}")
def get_movie(movie_id: int):

    for movie in movies:
        if movie["id"] == movie_id:
            return movie

    raise HTTPException(
        status_code=404,
        detail="Movie not found"
    )


@app.get("/movies")
def get_movies(genre: str | None = None, year: int | None = None, min_raiting: float | None = None, search: str | None = None):
    result = movies

    if genre is not None:
        result = [movie for movie in result
                  if movie["genre"].lower() == genre.lower()]


    if year is not None:
        result = [movie for movie in result
                  if movie["year"] == year]


    if min_raiting is not None:
        result =[ movie for movie in result
                 if movie["raiting"] >= min_raiting]

    if search is not None:
        result =[ movie for movie in result
                 if search.lower() in movie["title"].lower()]

    return result
        


