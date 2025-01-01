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
import cv2
import numpy as np
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_merge_video_audio
import tempfile

# Function to add music to a video
def add_BGM(music, video, music_volume=0.3, output_file="final_video_BGM.mp4"):
    # Load the video clip and extract the original audio
    video_clip = VideoFileClip(video)
    original_audio = video_clip.audio

    # Load the background music and adjust its volume
    bgm = AudioFileClip(music).volumex(music_volume)

    # Ensure both audios have the same duration (either trim the BGM or loop it)
    if bgm.duration > video_clip.duration:
        bgm = bgm.subclip(0, video_clip.duration)  # Trim BGM if it's longer than the video
    elif bgm.duration < video_clip.duration:
        bgm = bgm.loop(duration=video_clip.duration)  # Loop BGM if it's shorter than the video

    # Mix the original audio with the background music (using CompositeAudioClip)
    final_audio = CompositeAudioClip([original_audio, bgm])

    # Set the final audio to the video
    video_clip = video_clip.set_audio(final_audio)

    # Write the final video with background music
    video_clip.write_videofile(output_file, codec="libx264", audio_codec="aac")

    return output_file

# Function to combine videos
def combine_videos(video_paths):
    """
    Combines a list of videos into one video and saves it as a temporary file.
    """
    clips = [VideoFileClip(video) for video in video_paths]
    combined_clip = concatenate_videoclips(clips, method="compose")

    # Save to a temporary file
    temp_file = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False)
    combined_clip.write_videofile(temp_file.name, codec="libx264", audio_codec="aac")
    return temp_file.name

# Main program
def main():
   
    # Define music, video and subtitles
    music = "bollywoodkollywood-sad-love-bgm-13349.mp3"
    video = "final_video.mp4"
    #video_files = [
    #    "video_1.mp4", "video_2.mp4", "video_3.mp4",
    #    "video_4.mp4", "video_5.mp4", "video_6.mp4"
    #]
    #voice_files = [
    #    "voice_1.mp3", "voice_2.mp3", "voice_3.mp3",
    #    "voice_4.mp3", "voice_5.mp3", "voice_6.mp3"
    #]
    #narrators = ["Welcome to the story.", "Once upon a time, in a distant land...", "This is how it begins.", "4", "5", "6"]

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

    # Combine the music and video segments
    try:
        ## Need to save the music somewhere
        music_video = add_BGM("bollywoodkollywood-sad-love-bgm-13349.mp3", "final_video.mp4")
        st.write(f"Final video created: {music_video}")
        music_video_file = open(music_video, "rb")
        music_video_bytes = music_video_file.read()
        st.video(music_video_bytes)  # Display the video in the app

    except Exception as e:
        st.write(f"Error combining video and voice segments: {e}")

    # Allow users to download the music video
    if os.path.exists(music_video):
        with open(music_video, "rb") as file:
            st.download_button(
                label="Download Music Video",
                data=file,
                file_name="music_video.mp4",
                mime="video/mp4"
            )

    # Simulate videos as input
    video_1 = "video_1.mp4"
    video_2 = "video_2.mp4"
    video_3 = "video_3.mp4"

    # Combine video_1 and video_2 into video_12
    st.write("Combining video_1 and video_2 into video_12...")
    video_12 = combine_videos([video_1, video_2])
    st.write("video_12 created.")
    with open(video_12, "rb") as file:
        st.video(file.read())

    # Combine video_12 and video_3 into video_123
    st.write("Combining video_12 and video_3 into video_123...")
    video_123 = combine_videos([video_12, video_3])
    st.write("video_123 created.")
    with open(video_123, "rb") as file:
        st.video(file.read())


if __name__ == "__main__":
    main()

