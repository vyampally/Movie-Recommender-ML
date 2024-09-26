#import for frontend
import streamlit as st
#imports for movie data and posters
import pickle
import requests

#getting the poster for ach movie recommendation
def get_poster(movie_id):
     #using TMBD api url for movie details
     url = "https://api.themoviedb.org/3/movie/{}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US".format(movie_id)
     
     data = requests.get(url)
     data = data.json()
     
     poster_path = data['poster_path']
     full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
     return full_path

#load presaved data of over 10,000 movies 
movies = pickle.load(open("movies_list.pkl", 'rb'))

#how similar and recommendable these movies are
similarity = pickle.load(open("similarity.pkl", 'rb'))

#gets the titles of movie instead of index
movies_list = movies['title'].values

st.header("Movie Recommender System")

#dropdown for movie selection
#for future make search feature#
select_Movie = st.selectbox("Select a movie", movies_list)

#recommend movies based on chosen movie
def recommend(movie):
    #getting index of movie in presaved data
    index = movies[movies['title'] == movie].index[0]
    close_Movies = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector:vector[1])
    #store movies in list
    recommend_movie = []
    #store posters for movies
    recommend_poster = []

    #get first 5 movies that are most similar
    for i in close_Movies[1:6]:
        #get id and append movies and posters to list
        movies_id = movies.iloc[i[0]].id
        recommend_movie.append(movies.iloc[i[0]].title)
        recommend_poster.append(get_poster(movies_id))
    return recommend_movie, recommend_poster


#recommend button
if st.button("What we recommend"):
    movie_name, movie_poster = recommend(select_Movie)
    
    col1,col2,col3,col4,col5=st.columns(5)
    
    #display movie and poster for 5 movies
    with col1:
        st.text(movie_name[0])
        st.image(movie_poster[0])
    with col2:
        st.text(movie_name[1])
        st.image(movie_poster[1])
    with col3:
        st.text(movie_name[2])
        st.image(movie_poster[2])
    with col4:
        st.text(movie_name[3])
        st.image(movie_poster[3])
    with col5:
        st.text(movie_name[4])
        st.image(movie_poster[4])