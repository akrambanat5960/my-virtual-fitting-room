import streamlit as st
import fal_client
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI Dressing Room", layout="centered")
st.title("👗 My AI Dressing Room")

# --- STEP 1: LOGIN ---
# You will get this key from fal.ai for free
fal_key = st.text_input("Enter your FAL_KEY", type="password")
os.environ["FAL_KEY"] = fal_key

# --- STEP 2: UPLOAD PHOTOS ---
st.header("1. Upload Your Photo")
user_img = st.file_uploader("Take a photo or upload one", type=['jpg', 'png'], key="user")

st.header("2. Upload the Dress")
dress_img = st.file_uploader("Upload the dress image", type=['jpg', 'png'], key="dress")

# --- STEP 3: RUN THE AI ---
if st.button("✨ Fit the Dress!"):
    if not fal_key:
        st.error("Please enter your API key first!")
    elif user_img and dress_img:
        with st.spinner("AI is sewing the dress to fit you..."):
            # This sends your photos to the AI server
            handler = fal_client.submit(
                "fal-ai/fashn/tryon/v1.5",
                arguments={
                    "model_image": user_img,
                    "garment_image": dress_img,
                    "category": "one-pieces"
                },
            )
            result = handler.get()
            
            # Show the result!
            st.image(result['images'][0]['url'], caption="Your New Look!")
    else:
        st.warning("Please upload both photos.")
