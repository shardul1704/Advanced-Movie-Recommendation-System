import pickle
import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt



def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

# def recommend(movie):
#     index = movies[movies['title'] == movie].index[0]
#     distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
#     recommended_movie_names = []
#     recommended_movie_posters = []
#     for i in distances[1:6]:
#         # fetch the movie poster
#         movie_id = movies.iloc[i[0]].movie_id
#         recommended_movie_posters.append(fetch_poster(movie_id))
#         recommended_movie_names.append(movies.iloc[i[0]].title)
#
#     return recommended_movie_names, recommended_movie_posters
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    similarity_scores = similarity[index]
    indices = similarity_scores.argsort()[::-1][1:6]  # Get top 5 most similar movies
    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_ratings = []
    for i in indices:
        movie_id = movies.iloc[i]['movie_id']
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i]['title'])

        # Fetch the movie rating
        url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
            movie_id)
        data = requests.get(url)
        data = data.json()
        rating = data['vote_average']
        recommended_movie_ratings.append(rating)

    return indices, recommended_movie_names, recommended_movie_posters, recommended_movie_ratings


st.header('Movie Recommender System')
movies = pd.read_pickle('pickle/movie_list.pkl')
similarity = pd.read_pickle('pickle/similarity.pkl')
#movies = pickle.load(open('pickle/movie_list.pkl','rb'))
#similarity = pickle.load(open('pickle/similarity.pkl','rb'))

# movie_list = movies['title'].values
# selected_movie = st.selectbox(
#     "Type movie name below and click on Show Recommendation to get the Best Recommendations!! 😃",
#     movie_list
# )

## Generate the list of movie titles
movie_list = movies['title'].values

# Display the select box with larger text
st.markdown("<h3 style='font-size: 20px;'>Type movie name below and click on Show Recommendation to get the Best Recommendations!! 😃</h3>", unsafe_allow_html=True)
selected_movie = st.selectbox(
    "👇",
    movie_list
)


if st.button('Show Recommendation'):
    indices, recommended_movie_names, recommended_movie_posters, recommended_movie_ratings = recommend(selected_movie)

    # Display information for the selected movie
    st.header("Title: {}".format(selected_movie))
    selected_movie_index = movies[movies['title'] == selected_movie].index[0]
    selected_movie_poster = fetch_poster(movies.iloc[selected_movie_index]['movie_id'])
    selected_movie_overview = movies.iloc[selected_movie_index]['tags']
    #selected_movie_release_date = movies.iloc[selected_movie_index]['release_date']
    #st.text("Title: {}".format(selected_movie))

    col1, col2 = st.columns([1, 3])

    with col1:
        st.image(selected_movie_poster)

    with col2:
        #st.text("Release Date: {}".format(selected_movie_release_date))
        st.subheader("Overview:")
        st.write(selected_movie_overview)

    # Display recommendations
    st.header("Recommended Movies")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.image(recommended_movie_posters[0])
        st.text(recommended_movie_names[0])
    with col2:
        st.image(recommended_movie_posters[1])
        st.text(recommended_movie_names[1])
    with col3:
        st.image(recommended_movie_posters[2])
        st.text(recommended_movie_names[2])
    with col4:
        st.image(recommended_movie_posters[3])
        st.text(recommended_movie_names[3])
    with col5:
        st.image(recommended_movie_posters[4])
        st.text(recommended_movie_names[4])

    # Display additional visualizations
    #st.header("Additional Visualizations")

    # Bar chart of average ratings
    avg_ratings_chart_data = pd.DataFrame(
        {'Movie': recommended_movie_names, 'Average Rating': recommended_movie_ratings})
    st.subheader("Average Ratings of Recommended Movies")
    st.bar_chart(avg_ratings_chart_data.set_index('Movie'))









