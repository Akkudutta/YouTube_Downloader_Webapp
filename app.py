import streamlit as st
from pytube import YouTube
import io
from moviepy.editor import AudioFileClip
import os
import re
import tempfile
import base64

# Define the function to generate the download link
def get_binary_file_downloader_html(bin_file, file_label='File', button_label='Download'):
    bin_str = base64.b64encode(bin_file.read()).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{file_label}">{button_label}</a>'
    return href

st.set_page_config(page_title="YouTube Video/Audio Downloader", page_icon='📼', layout= 'wide')

l1, l2 = st.columns((0.4,2))
with l2:
    # Set Streamlit app title
    st.title("YouTube Audio & Video Downloader App")

st.write("---")
l1, l2 = st.columns((0.3,2))
with l2:
    st.write("<span style='color:red'>**Streamline your YouTube experience with our free online converter – easily download and convert videos and audios to your chosen formats.**</span>",unsafe_allow_html=True)

l1, l2, l3 = st.columns(3)
with l2:
    # Create a form to group the input elements
    with st.form("youtube_downloader_form"):
        # Get YouTube video URL from user input
        video_url = st.text_input("Enter the YouTube video URL:")

        # Choose the output format
        output_format = st.selectbox("Select Output Format:", [".mp3", ".wav", ".mp4"])

        # Submit button
        submit_button = st.form_submit_button("Generate Download Link")

        # Check if the URL and format are selected
        if video_url and output_format:
            try:
                # Create a YouTube object
                my_video = YouTube(video_url)

                # Get the video title and clean it for use as a filename
                video_title = re.sub(r'\W+', '_', my_video.title)

                if output_format != ".mp4":
                    # Get the audio stream in .mp4 format
                    audio_stream = my_video.streams.filter(only_audio=True, file_extension="mp4").first()

                    # Download the audio stream as .mp4 using pytube
                    mp4_path = audio_stream.download(output_path=tempfile.gettempdir())

                    # Convert the downloaded .mp4 audio to the selected output format
                    audio_clip = AudioFileClip(mp4_path)
                    converted_file_path = os.path.join(tempfile.gettempdir(), f"{video_title}{output_format}")
                    if output_format == ".wav":
                        audio_clip.write_audiofile(converted_file_path, codec="pcm_s16le")
                    else:
                        audio_clip.write_audiofile(converted_file_path, codec=output_format[1:])
                    audio_clip.close()
                else:
                    # Download the video stream as .mp4 using pytube
                    video_stream = my_video.streams.get_highest_resolution()
                    converted_file_path = video_stream.download(output_path=tempfile.gettempdir())

                # Download the selected stream
                if submit_button:
                    with st.spinner("Processing..."):
                        with open(converted_file_path, "rb") as f:
                            st.markdown(get_binary_file_downloader_html(f, f"{video_title}{output_format}", f"Click here to download your {output_format} file"), unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Error: {str(e)}")

l1, l2 = st.columns((0.3,2))
with l2:
    st.write("""
             *Experience the convenience of our free online YouTube converter. With our user-friendly app, you can effortlessly download and convert YouTube videos and audios to your preferred formats. Choose from a variety of options such as MP3, WAV, and even video formats like MP4. Say goodbye to complicated downloads – our straightforward tool makes it simple to transform your favorite content into the format you desire.*
             """)
st.write("---")
st.markdown(
                '<div style="text-align: center;">'
                '<p>Created by <a href="https://github.com/Akkudutta">Aakarshan Dutta</a></p>'
                '</div>',
                unsafe_allow_html=True
            )
