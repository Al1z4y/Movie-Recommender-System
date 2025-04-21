import pickle
import streamlit as st
import pandas as pd
import requests
import os

def download_file(url, filename):
    if not os.path.exists(filename):
        st.write("Downloading similarity file... (This may take a while)")
        response = requests.get(url)
        with open(filename, 'wb') as f:
            f.write(response.content)
    return filename

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movie_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movie_posters

# Load movies_dict (small file)
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Load similarity.pkl from Google Drive
similarity_url = "https://drive.google.com/uc?export=download&id=16xj_B1vpr19jxYXQvqjARR8nLsLPFNS7"  # Your actual file ID
similarity_file = download_file(similarity_url, "similarity.pkl")
similarity = pickle.load(open(similarity_file, 'rb'))

# Streamlit UI
st.title('Movie Recommender System')
movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

if st.button('Show Recommendation'):
    names, posters = recommend(selected_movie)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])