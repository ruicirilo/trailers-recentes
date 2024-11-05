from flask import Flask, render_template
import requests

app = Flask(__name__)
API_KEY = '516adf1e1567058f8ecbf30bf2eb9378'

def get_latest_movies():
    url = f'https://api.themoviedb.org/3/movie/now_playing?api_key={API_KEY}&language=en-US&page=1'
    response = requests.get(url)
    data = response.json()
    return data.get('results', [])

def get_movie_trailer(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={API_KEY}&language=en-US'
    response = requests.get(url)
    videos = response.json().get('results', [])
    for video in videos:
        if video['type'] == 'Trailer' and video['site'] == 'YouTube':
            return f"https://www.youtube.com/watch?v={video['key']}"
    return None

def get_cast(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={API_KEY}'
    response = requests.get(url)
    cast_data = response.json().get('cast', [])
    return ", ".join([actor['name'] for actor in cast_data[:5]])

def get_trailers():
    movies = get_latest_movies()
    trailers = []
    for movie in movies:
        trailer_url = get_movie_trailer(movie['id'])
        if trailer_url:
            trailers.append({
                'title': movie['title'],
                'poster_url': f"https://image.tmdb.org/t/p/w500{movie['poster_path']}",
                'synopsis': movie['overview'],
                'cast': get_cast(movie['id']),
                'trailer_url': trailer_url
            })
    return trailers

@app.route('/')
def index():
    trailers = get_trailers()
    return render_template('index.html', trailers=trailers)

if __name__ == '__main__':
    app.run(debug=True)
