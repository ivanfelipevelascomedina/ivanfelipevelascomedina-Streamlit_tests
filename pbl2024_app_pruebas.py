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

# Function to add subtitles using OpenCV
def annotate_frame(frame, text, position=(50, 50), font_scale=1, color=(255, 255, 255), thickness=2):
    font = cv2.FONT_HERSHEY_SIMPLEX
    wrapped_text = text.split('\n')  # Split text into lines for wrapping
    y_offset = position[1]
    for line in wrapped_text:
        cv2.putText(frame, line, (position[0], y_offset), font, font_scale, color, thickness, lineType=cv2.LINE_AA)
        y_offset += 30  # Line spacing
    return frame

# Function to process video with subtitles
def process_video_with_subtitles(video_file, subtitles, output_file):
    cap = cv2.VideoCapture(video_file)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        # Annotate the frame with subtitles
        text = subtitles[min(frame_count // fps, len(subtitles) - 1)]  # Choose subtitle based on time
        frame = annotate_frame(frame, text, position=(50, height - 50))
        out.write(frame)
        frame_count += 1

    cap.release()
    out.release()

# Function to combine video and audio
def combine_video_and_audio(video_file, audio_file, output_file):
    ffmpeg_merge_video_audio(video_file, audio_file, output_file, vcodec="libx264", acodec="aac")

# Main program
def main():
   
    # Define music, video and subtitles
    music = "bollywoodkollywood-sad-love-bgm-13349.mp3"
    video = "final_video.mp4"
    video_files = [
        "video_1.mp4", "video_2.mp4", "video_3.mp4",
        "video_4.mp4", "video_5.mp4", "video_6.mp4"
    ]
    voice_files = [
        "voice_1.mp3", "voice_2.mp3", "voice_3.mp3",
        "voice_4.mp3", "voice_5.mp3", "voice_6.mp3"
    ]
    narrators = ["Welcome to the story.", "Once upon a time, in a distant land...", "This is how it begins.", "4", "5", "6"]

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

    # Combine the text, music and video segments
    try:
        processed_videos = []
        for i, (video, audio, subtitle) in enumerate(zip(video_files, voice_files, narrators)):
            subtitle_file = f"processed_video_{i}.mp4"
            process_video_with_subtitles(video, [subtitle], subtitle_file)
            processed_videos.append(subtitle_file)
        
        final_video = "final_video_with_audio.mp4"
        combine_video_and_audio(processed_videos[0], voice_files[0], combined_video)
        ## Need to save the music somewhere
        combined_video = add_BGM("bollywoodkollywood-sad-love-bgm-13349.mp3", "final_video.mp4")
        st.write(f"Final video created: {combined_video}")
        combined_video_file = open(combined_video, "rb")
        combined_video_bytes = combined_video_file.read()
        st.video(combined_video_bytes)  # Display the video in the app

    except Exception as e:
        st.write(f"Error combining video and voice segments: {e}")

    # Allow users to download the combined video
    if os.path.exists(combined_video):
        with open(combined_video, "rb") as file:
            st.download_button(
                label="Download Combined Video",
                data=file,
                file_name="combined_video.mp4",
                mime="video/mp4"
            )


if __name__ == "__main__":
    main()
