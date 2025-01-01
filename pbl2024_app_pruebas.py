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

# Function to add subtitles using OpenCV
def annotate_frame(frame, text, position=(50, 50), font_scale=1, color=(255, 255, 255), thickness=2):
    font = cv2.FONT_HERSHEY_SIMPLEX
    wrapped_text = text.split('\n')  # Split text into lines for wrapping
    y_offset = position[1]
    for line in wrapped_text:
        cv2.putText(frame, line, (position[0], y_offset), font, font_scale, color, thickness, lineType=cv2.LINE_AA)
        y_offset += 30  # Line spacing
    return frame

# Function to create temporary directories for video processing
def create_temp_dir():
    return tempfile.mkdtemp(suffix=None, prefix="SMW_", dir=None)

# Function to process videos with subtitles and output to temporary files
def process_videos_with_subtitles(video_files, subtitles, temp_dir):
    processed_videos = []
    for i, (video, subtitle) in enumerate(zip(video_files, subtitles)):
        subtitle_file = os.path.join(temp_dir, f"processed_video_{i}.mp4")
        process_video_with_subtitles(video, [subtitle], subtitle_file)
        if os.path.exists(subtitle_file):
            processed_videos.append(subtitle_file)
        else:
            st.write(f"Subtitle video creation failed for {subtitle_file}")
    return processed_videos

# Function to combine video and audio files
def combine_videos_and_audio(processed_videos, voice_files, temp_dir):
    combined_videos = []
    for i, (video, audio) in enumerate(zip(processed_videos, voice_files)):
        combined_file = os.path.join(temp_dir, f"combined_video_{i}.mp4")
        combine_video_and_audio(video, audio, combined_file)
        if os.path.exists(combined_file):
            combined_videos.append(combined_file)
        else:
            st.write(f"Failed to create combined video for {combined_file}")
    return combined_videos

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


    # Create a temporary directory
    temp_dir = create_temp_dir()

    try:
        # Process videos with subtitles
        processed_videos = process_videos_with_subtitles(video_files, narrators, temp_dir)
        if not processed_videos:
            st.write("No processed videos available.")
            return

        # Combine videos and audio
        combined_videos = combine_videos_and_audio(processed_videos, voice_files, temp_dir)
        if not combined_videos:
            st.write("Failed to create combined videos.")
            return

        # Add background music to the first combined video
        final_video_with_bgm = os.path.join(temp_dir, "final_video_with_bgm.mp4")
        add_BGM(music, combined_videos[0], output_file=final_video_with_bgm)

        if os.path.exists(final_video_with_bgm):
            st.write(f"Final video created: {final_video_with_bgm}")
            # Display the final video in the app
            with open(final_video_with_bgm, "rb") as video_file:
                st.video(video_file)

            # Allow users to download the final video
            with open(final_video_with_bgm, "rb") as file:
                st.download_button(
                    label="Download Combined Video",
                    data=file,
                    file_name="final_video_with_bgm.mp4",
                    mime="video/mp4"
                )
        else:
            st.write("Failed to create the final video with background music.")

    except Exception as e:
        st.write(f"Error combining video and voice segments: {e}")

    finally:
        # Cleanup temporary files after the video is displayed
        if st.button("Cleanup Temporary Files"):
            shutil.rmtree(temp_dir, ignore_errors=True)
            st.info("Temporary files cleaned up.")


if __name__ == "__main__":
    main()

