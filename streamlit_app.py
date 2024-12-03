import os
import shutil
import tempfile
import streamlit as st
from ultralytics import YOLO

# Initialize YOLO model
model = YOLO('yolov8n.pt')

st.title("YOLOv8 Video Processor")

# Upload a video file
uploaded_video = st.file_uploader("Upload a video", type=["mp4", "avi", "mov"])

if uploaded_video:
    # Save the video to a temporary directory
    temp_dir = tempfile.mkdtemp()
    video_path = os.path.join(temp_dir, uploaded_video.name)
    with open(video_path, 'wb') as f:
        f.write(uploaded_video.read())
    st.video(video_path)

    # Process video with YOLO
    if st.button("Run YOLO Inference"):
        output_dir = os.path.join(temp_dir, "yolo_results")
        os.makedirs(output_dir, exist_ok=True)

        results = model.predict(source=video_path, save=True, save_dir=output_dir)
        output_files = [f for f in os.listdir(output_dir) if f.endswith(('.mp4', '.avi'))]

        if output_files:
            output_video = os.path.join(output_dir, output_files[0])
            st.success("Inference Completed!")
            st.video(output_video)

            with open(output_video, "rb") as f:
                st.download_button(
                    "Download Processed Video",
                    data=f,
                    file_name=f"processed_{uploaded_video.name}",
                    mime="video/mp4"
                )
        else:
            st.error("No output video found.")

    # Cleanup
    shutil.rmtree(temp_dir)
