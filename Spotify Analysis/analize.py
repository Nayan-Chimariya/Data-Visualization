from matplotlib import pyplot as plt
import pandas as pd
from collections import Counter


# Process Data
def processdata(counterObj, range):
    counterObj_tuple = counterObj.most_common(range)
    counterObj_dict = dict(counterObj_tuple)
    listX = list(counterObj_dict.keys())
    listY = list(counterObj_dict.values())
    listX.reverse()
    listY.reverse()
    return (listX, listY)


# Reading the CSV file
data = pd.read_csv("songs.csv")

# Accessing Required data
artists = data["artist"]
genres = data["genre"]
popularity_score = data["popularity"]
danceability = data["danceability"]

axd = plt.figure(layout="constrained", figsize=(12, 10)).subplot_mosaic(
    """
    CCCC
    AABB
    """
)

# Top 20 artist
artist_counter = Counter()

for artist in artists:
    artist_counter.update(artist.split(";"))

ax1 = axd["A"]
ax1.set_title("Top 20 artist")
ax1.set_xlabel("Frequency of being the top")
ax1.set_ylabel("Artist")
artist_list, artist_frequency = processdata(artist_counter, 20)

ax1.barh(artist_list, artist_frequency, 0.8, color="#FFA500")

# Top 5 Genres
genre_counter = Counter()

for genre in genres:
    genre_counter.update(genre.split(";"))

ax2 = axd["B"]
ax2.set_title("Top 5 Genres")
genre_list, genere_frequency = processdata(genre_counter, 5)
color_palette = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]

ax2.pie(
    genere_frequency,
    labels=genre_list,
    colors=color_palette,
    startangle=160,
    autopct="%1.1f%%",
)

# Corelation of Popularity Score with Danceability

ax3 = axd["C"]
ax3.set_title("Corelation of popularity score with danceability score")
ax3.set_xlabel("Popularity Score")
ax3.set_ylabel("Dancability")
ax3.scatter(popularity_score, danceability, s=25, color="g")

plt.show()
