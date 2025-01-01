# GUI CODE

# IMPORT LIBRARIES
import csv
from scholarly import scholarly
import feedparser
import urllib.parse
from openai import OpenAI
import requests
import time
import os
os.system("apt-get update && apt-get install -y imagemagick")
import re
import random
from lumaai import LumaAI
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips, TextClip, CompositeVideoClip, CompositeAudioClip
from resemble import Resemble
from pydub import AudioSegment
from moviepy import editor
import subprocess
import textwrap
import streamlit as st
from moviepy.config import change_settings

# INITIALIZE API KEYS
# Main program
def main():
    
    ## Dfine music and video
    music = "bollywoodkollywood-sad-love-bgm-13349.mp3"
    video = "final_video.mp4"

    # Display video
    video_file = open(video, "rb")
    video_bytes = video_file.read()
    st.video(video_bytes)  # Display the video in the app

    # Allow users to download the music
    if os.path.exists(music):
        with open(music, "rb") as file:
            st.download_button(
                label="Download Final Song",
                data=file,
                file_name="music.mp3",
                mime="video/mp4"
            )
    # Allow users to download the video
    if os.path.exists(video):
        with open(video, "rb") as file:
            st.download_button(
                label="Download Final Video",
                data=file,
                file_name="video.mp4",
                mime="video/mp4"
            )


if __name__ == "__main__":
    main()
