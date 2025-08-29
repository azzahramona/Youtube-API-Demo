import streamlit as st
import pandas as pd
import json

# --- Dummy CSV data for channels (Option B) ---


corey_schafer_videos_csv = """
video_id,title,views,published,likes,comments,thumbnail_url
oAkLSJNr5zY,Python Tutorial: AsyncIO - Complete Guide to Asynchronous Programming with Animations,1100000,2020-01-01,15000,500,https://i.ytimg.com/vi/uDPdrdyQSF8/hqdefault.jpg
Rf9Ujpq5Ob0,Pandas Data Analysis Tutorial,850000,2021-05-20,12000,320,https://i.ytimg.com/vi/Rf9Ujpq5Ob0/hqdefault.jpg
O-I-9r5Q2pY,Flask Web Development,650000,2019-09-15,10000,280,https://i.ytimg.com/vi/O-I-9r5Q2pY/hqdefault.jpg
"""

kevin_stratvert_videos_csv = """
video_id,title,views,published,likes,comments,thumbnail_url
avQMU1yJkyY,Zapier AI Agents Tutorial for Beginners — Automate Your Workflows,6777654,2018-05-10,145000,1300,https://i.ytimg.com/vi/6TspvRRIQ0I/hqdefault.jpg
v=p7Wb4akva80,How to Watch Movies for Free (Kevin Stratvert),6426814,2019-03-15,98000,890,https://i.ytimg.com/vi/p7Wb4akva80/hqdefault.jpg
v=IfjGwmAYZPc,BEST CapCut Video Editing Tips (Kevin Stratvert),5627728,2021-07-22,86000,710,https://i.ytimg.com/vi/IfjGwmAYZPc/hqdefault.jpg
v=lyBDu_rE9cY,How to Convert PDF to Word (Kevin Stratvert),4708557,2018-11-05,75000,560,https://i.ytimg.com/vi/lyBDu_rE9cY/hqdefault.jpg
v=uqTRVJjzNs0,Pivot Table Excel Tutorial (Kevin Stratvert),4254920,2019-08-12,82000,630,https://i.ytimg.com/vi/uqTRVJjzNs0/hqdefault.jpg
"""



# Helper function to load CSV string into DataFrame
def load_channel_data(csv_string):
    from io import StringIO
    return pd.read_csv(StringIO(csv_string))


# --- Option A: Load dummy search results from embedded JSON ---
# For simplicity, embedding dummy data directly here.
# You can also load from external 'search_results.json' if you want.
import json
import pandas as pd

# Load the nested JSON
with open('search_results.json', encoding='utf-8') as f:
    raw_data = json.load(f)


# Flatten the nested structure
flattened_data = []
for topic, videos in raw_data.items():
    for video in videos:
        video["topic"] = topic
        flattened_data.append(video)

# Convert to DataFrame
dummy_search_data = pd.DataFrame(flattened_data)
# --- Streamlit UI ---
st.title("YouTube API Demo App")

option = st.sidebar.selectbox(
    "What would you like to do?",
    ["Extract Videos from YouTube Search", "View Channel Video List"]
)

if option == "Extract Videos from YouTube Search":
    st.header("Extract Videos from YouTube Search")
    
    search_terms = list(dummy_search_data.topic.unique())
    selected_search = st.selectbox("Select a search query:", search_terms)

    # ✅ Get only rows that match the selected topic
    videos = dummy_search_data[dummy_search_data["topic"] == selected_search].to_dict(orient='records')


    st.write(f"Showing results for **{selected_search}**:")

    for video in videos:
        st.markdown("---")
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image(video["thumbnail_url"], width=120)
        with col2:
            st.markdown(f"### [{video['title']}](https://youtube.com/watch?v={video['video_id']})")
            st.write(f"Channel: {video['channel']}")
            st.write(f"Views: {video['views']:,}")
            st.write(f"Published: {video['published']}")

elif option == "View Channel Video List":
    st.header("View Channel Video List")

    channel = st.sidebar.selectbox(
        "Select a YouTube channel:",
        ["Corey Schafer", "Kevin Stratvert"]
    )

    # Load appropriate CSV data based on selection
    if channel == "Corey Schafer":
        df = load_channel_data(corey_schafer_videos_csv)
    elif channel == "Kevin Stratvert":
        df = load_channel_data(kevin_stratvert_videos_csv)
    st.write(f"Showing videos for channel: **{channel}**")
    
    for idx, row in df.iterrows():
        st.markdown(f"### [{row['title']}](https://youtube.com/watch?v={row['video_id']})")
        cols = st.columns([1,3])
        with cols[0]:
            st.image(row["thumbnail_url"], width=150)
        with cols[1]:
            st.write(f"**Views:** {row['views']:,}")
            st.write(f"**Published Date:** {row['published']}")
            st.write(f"**Likes:** {row['likes']:,}")
            st.write(f"**Comments:** {row['comments']:,}")
        st.markdown("---")
