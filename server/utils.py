""" Utility File for Helper functions """

def clean_movie_title(movie_title: str) -> str:
    split_title = movie_title.split()
    return " ".join(title.capitalize() for title in split_title).strip()