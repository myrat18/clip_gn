import os
import shutil
import tempfile
import streamlit as st
from ultralytics import YOLO

# Initialize YOLO model (auto-downloads 'yolov8n.pt' if not already available)
model = YOLO('yolov8n.pt')

st.title("Highlighter Test")

uploaded_file = st.file_uploader("Upload test video", type=["mp4", "avi", "mov"])

if uploaded_file is not None:
    # Save the uploaded video to a temporary directory
    temp_dir = tempfile.mkdtemp()
    video_path = os.path.join(temp_dir, uploaded_file.name)

    with open(video_path, 'wb') as f:
        f.write(uploaded_file.read())

    st.video(video_path)

    if st.button("Run YOLO Inference"):
        try:
            # Define a temporary directory for YOLO outputs
            yolo_output_dir = os.path.join(temp_dir, "yolo_results")
            os.makedirs(yolo_output_dir, exist_ok=True)

            # Perform YOLO inference and save results in the specified directory
            results = model.predict(source=video_path, save=True, save_dir=yolo_output_dir)

            # Locate the output video file
            output_files = [f for f in os.listdir(yolo_output_dir) if f.endswith(('.mp4', '.avi'))]
            if output_files:
                output_video_path = os.path.join(yolo_output_dir, output_files[0])

                # Display the output video
                st.success("Inference completed!")
                st.video(output_video_path)

                # Provide a download button for the processed video
                with open(output_video_path, "rb") as f:
                    st.download_button(
                        label="Download Result Video",
                        data=f,
                        file_name="processed_" + uploaded_file.name,
                        mime="video/mp4"
                    )
            else:
                st.error("No output video found after inference.")

        except Exception as e:
            st.error(f"Inference failed: {e}")

        finally:
            # Clean up the temporary directory
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
