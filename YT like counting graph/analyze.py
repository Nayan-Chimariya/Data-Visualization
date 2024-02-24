from googleapiclient.discovery import build
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd
import numpy as np
import os
import re
import time

API_KEY = os.environ.get("YT_API_KEY")


# Getting video ID from URL
def extractVideoID(url):
    pattern = r"(?<=v=)[a-zA-Z0-9_-]+(?=&|\?)"
    match = re.search(pattern, url)
    if match:
        return match.group()
    else:
        return None


# ask the url
url = input("Enter the video URL: ")

# get video id
ID = extractVideoID(url)

# create empty csv file
column_labels = ["like_counter", "time,"]
with open("data.csv", "w") as f:
    f.write(",".join(column_labels))


# create figure and axis
fig, ax = plt.subplots()


# The animation function
def animate(i):
    # Setting up API connection
    youtube = build("youtube", "v3", developerKey=API_KEY)
    request = youtube.videos().list(part="statistics", id=ID)
    response = request.execute()

    # getting the like count
    like_count = []
    like_counter = response["items"][0]["statistics"]["likeCount"]
    like_count.append(like_counter)

    # checking the time of the count
    check_time_list = []
    check_time = time.time()
    check_time_list.append(check_time)

    # adding the likes and time of counting to a csv
    new_data = {"like_counter": like_count, "time": check_time_list}
    new_data_df = pd.DataFrame(new_data)
    new_data_df.to_csv("data.csv", mode="a", header=False, index=False)

    # Reading the CSV
    data = pd.read_csv("data.csv")
    read_like_counter = data["like_counter"]
    read_time_counter = data["time"]

    ax.cla()

    ax.plot(read_like_counter, read_time_counter, marker="o", color="g")
    plt.tight_layout()
    time.sleep(2)


ani = FuncAnimation(plt.gcf(), animate, cache_frame_data=False, interval=1000)

plt.tight_layout()

plt.show()
