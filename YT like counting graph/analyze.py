from googleapiclient.discovery import build
import httplib2
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from urllib.parse import urlparse, parse_qs
import pandas as pd
import os
import time

API_KEY = os.environ.get("YT_API_KEY")

startup = True


# Getting video ID from URL
def extractVideoID(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    video_id = query_params.get("v")
    if video_id:
        return video_id[0]
    else:
        return None


# Ask the url and refresh time
url = input("Enter the video URL: ")
ID = extractVideoID(url)
while ID is None:
    print("\nInvalid URL\n")
    url = input("Enter the video URL: ")
    ID = extractVideoID(url)

while True:
    try:
        refresh_time = int(input("Enter refresh time: "))
        break
    except (ValueError, TypeError):
        print("\nEnter an interger value\n")

# create empty csv file
column_labels = ["like_counter", "time,"]
with open("data.csv", "w") as f:
    f.write(",".join(column_labels))


# create figure and axis
fig, ax = plt.subplots()

# Setting up API connection
try:
    youtube = build("youtube", "v3", developerKey=API_KEY)
except httplib2.ServerNotFoundError:
    print("No internet connection or Server not Found")


# The animation function
def animate(i):
    global startup
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
    print(f"Likes on the video : {like_counter}")
    if startup is True:
        time.sleep(0)
        startup = False
    else:
        time.sleep(refresh_time)


ani = FuncAnimation(plt.gcf(), animate, cache_frame_data=False, interval=1000)

plt.tight_layout()

plt.show()
