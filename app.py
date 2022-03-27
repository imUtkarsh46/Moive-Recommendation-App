import re
from urllib import response
import streamlit as st
import pickle
import pandas as pd
import requests
from urllib3 import Retry

movies_rowlist = pickle.load(open('movie_list.pkl', 'rb'))
movies_list = sorted(movies_rowlist['title'].values)

similarity = pickle.load(open('similarity.pkl', 'rb'))

def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=b0c535db1be77e14e7c1326b967caf21&language=en-US')
    data = response.json()
    return 'https://image.tmdb.org/t/p/w500/'+ data['poster_path']



def recommend(movie):
    movie_index = movies_rowlist[movies_rowlist['title'] == movie].index[0] #Fetch Index
    dist = similarity[movie_index] #Fetch Distance or Similarity
    result_list = sorted(list(enumerate(dist)), reverse=True, key=lambda x : x[1])[1:6] #Sort similarty into des
    
    result = []
    recommend_movie_poster = []
    for i in result_list:
        movie_id = movies_rowlist.iloc[i[0]].movie_id

        result.append(movies_rowlist.iloc[i[0]]['title'])
        #fetch poster of movie from API
        recommend_movie_poster.append(fetch_poster(movie_id))

    return result, recommend_movie_poster

st.title('Movie Recommendation System')
seleted_movie = st.selectbox('How would you like to be contacted', (movies_list))

if st.button('Recommend'):
    names, posters = recommend(seleted_movie)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])
    
    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])