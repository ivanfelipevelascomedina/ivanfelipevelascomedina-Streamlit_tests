import subprocess
import streamlit as st
from moviepy.config import change_settings
import os

# Check if ImageMagick is installed
def check_imagemagick():
    try:
        result = subprocess.run(["magick", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            st.success("ImageMagick is properly configured.")
            st.write(result.stdout.decode())
            return True
    except FileNotFoundError:
        st.error("ImageMagick is not installed or not configured correctly.")
        return False

# Check if FFmpeg is installed
def check_ffmpeg():
    try:
        result = subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            st.success("FFmpeg is properly configured.")
            st.write(result.stdout.decode())
            return True
    except FileNotFoundError:
        st.error("FFmpeg is not installed or not configured correctly.")
        return False

# Main Streamlit app
def main():
    os.environ["IMAGEMAGICK_BINARY"] = "/usr/bin/magick"
    st.title("Streamlit Troubleshooting")

    # Check ImageMagick
    st.header("ImageMagick Check")
    if not check_imagemagick():
        st.stop()

    # Check FFmpeg
    st.header("FFmpeg Check")
    if not check_ffmpeg():
        st.stop()

    # Test MoviePy
    st.header("MoviePy Test")
    try:
        from moviepy.editor import TextClip
        clip = TextClip("Hello, Streamlit!", fontsize=70, color='white', size=(600, 400))
        clip.write_videofile("test_video.mp4", fps=24)
        st.video("test_video.mp4")
        st.success("MoviePy works correctly.")
    except Exception as e:
        st.error(f"Error with MoviePy: {e}")

if __name__ == "__main__":
    main()
