import streamlit as st
import gdown
import os

def download_video_from_gdrive(gdrive_url):
    """Download video from a Google Drive link using gdown."""
    try:
        output = "temp_video.mp4"
        gdown.download(gdrive_url, output, quiet=False)
        return output
    except Exception as e:
        return None

def app():
    st.title("Google Drive Video Player and Clip Generator")

    # Input for the Google Drive link
    gdrive_url = st.text_input("Enter a Google Drive video URL (direct link):")

    if gdrive_url:
        st.info("Ensure the Google Drive link is in a shareable or direct download format.")
        
        if st.button("Download and Play Video"):
            with st.spinner("Downloading video..."):
                video_path = download_video_from_gdrive(gdrive_url)
                
                if video_path:
                    st.success("Video downloaded successfully!")
                    st.video(video_path)
                else:
                    st.error("Failed to download video. Please check the link format.")

    # Generate Clip button
    if st.button("Generate Clip"):
        st.success("Generate Clip button clicked! Add your processing logic here.")

    # Clean up downloaded video on app stop
    if os.path.exists("temp_video.mp4"):
        os.remove("temp_video.mp4")

if __name__ == "__main__":
    app()
