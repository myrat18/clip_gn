import streamlit as st
import tempfile
import gdown
import os

def convert_to_drive_direct_url(google_drive_link):
    """Convert Google Drive share link to direct download link."""
    file_id = google_drive_link.split('id=')[1].split('&')[0]
    return f"https://drive.google.com/uc?export=download&id={file_id}"

st.title("Google Drive Video Viewer")

# Input for Google Drive link
drive_link = st.text_input("Enter the Google Drive video link:")

if drive_link:
    try:
        # Convert Google Drive link to direct download link
        download_link = convert_to_drive_direct_url(drive_link)

        # Download the video from Google Drive
        temp_dir = tempfile.mkdtemp()
        video_path = os.path.join(temp_dir, "downloaded_video.mp4")

        st.write("Downloading video...")
        gdown.download(url=download_link, output=video_path, quiet=False)
        st.success("Video downloaded successfully!")

        # Display the video
        st.video(video_path)

        # Button for next steps
        if st.button("Do Something"):
            st.write("Further actions can be implemented here.")

    except Exception as e:
        st.error(f"Error downloading video: {e}")
