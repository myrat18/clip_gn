import os
import cv2
import shutil
import tempfile
import streamlit as st
from ultralytics import YOLO

model = YOLO('/Users/myrat/Desktop/test/goalpost_best.pt')

st.title("Highlighter test")

uploaded_file = st.file_uploader("Upload test video", type=["mp4", "avi", "mov"])

if uploaded_file is not None:
    temp_dir = tempfile.mkdtemp()
    video_path = os.path.join(temp_dir, uploaded_file.name)

    with open(video_path, 'wb') as f:
        f.write(uploaded_file.read())

    st.video(video_path)

    if st.button("Run YOLO inference"):
        results = model.predict(source=video_path, save=True)
        output_dir = results[-2].save_dir
        uploaded_file.name = uploaded_file.name.replace('mov', 'avi')
        uploaded_file.name = uploaded_file.name.replace('mp4', 'avi')
        output_video_path = os.path.join(output_dir, uploaded_file.name)

        st.success("Inference completed!")
        st.video(output_video_path)

        with open(output_video_path, "rb") as f:
            st.download_button(
                label="Download result video",
                data=f,
                file_name="processed_" + uploaded_file.name,
                mime="video/mp4"
            )

    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
