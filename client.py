import streamlit as st
from PIL import Image
import ollama
import os
import logging
from prompts import ADMIN_ROLE_PROMPT, USER_ROLE_PROMPT
 
 
UPLOAD_DIR = "input_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)
 
# Page configuration
st.set_page_config(page_title="Radiology report generation", layout="wide")
 
# Sidebar for image upload
st.sidebar.header("Upload Image")
uploaded_files = st.sidebar.file_uploader("upload image", type=["png", "jpg", "jpeg", "bmp"],accept_multiple_files=False)
 
# Main layout
st.title("Report from Xray")
 
col1, col2 = st.columns([1, 2])
 
# Display the uploaded image in the first column
with col1:
    if len(uploaded_files) > 0 :
        if len(uploaded_files) > 1:
            st.error(f"{len(uploaded_files)} files uploaded. Only 1 file upload supported")
        # print(f"Num uploaded files: {len(uploaded_files)}")
        for uploaded_file in uploaded_files:
            try:
                image = Image.open(uploaded_file)
                st.image(image, caption="Uploaded Image", use_container_width=True)
            except Exception as e:
                st.error(f"Error: Could not process the image. {e}")
    else:
        st.info("Upload an image in the sidebar to display it here.")
 
# Chat interface in the second column
with col2:
    st.subheader("Chat Interface")
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
 
    # Input box for chat
    user_message = st.text_input("Enter your prompt:", key="chat_input")
 
    if st.button("Send"):
        if len(user_message) > 0 and  len(uploaded_files) > 0 :
            file_paths_list = []
            for uploaded_file in uploaded_files:
                # Save the uploaded file
                file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
                logging.info(file_path)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                file_paths_list.append(file_path)
            # logging.info(file_paths_list)
            response = ollama.chat(
                model="llama3.2-vision",
                messages=[
                    {
                        "role": "system",
                        "content": ADMIN_ROLE_PROMPT,
                        "images": [file_paths_list[0]]
                    },
                    # {
                    #     "role": "user",
                    #     "content": USER_ROLE_PROMPT,
                    #     "images": [file_paths_list[1]]
                    # },
                ]
            )
            # Extract cleaned text
            cleaned_text = response['message']['content'].strip()
            st.write(cleaned_text)