import streamlit as st
import fal_client
import os

# 1. Access the hidden key (We will set this up in Step 2)
if "FAL_KEY" in st.secrets:
    os.environ["FAL_KEY"] = st.secrets["FAL_KEY"]
else:
    st.error("Missing FAL_KEY in Secrets! Please add it in Settings.")

# --- APP INTERFACE ---
st.set_page_config(page_title="AI Dressing Room", layout="centered")
st.title("👗 My AI Dressing Room")

st.header("1. Upload Your Photo")
user_img = st.file_uploader("Take a photo or upload one", type=['jpg', 'png'], key="user")

st.header("2. Upload the Dress")
dress_img = st.file_uploader("Upload the dress image", type=['jpg', 'png'], key="dress")

if st.button("✨ Fit the Dress!"):
    if user_img and dress_img:
        with st.spinner("AI is sewing the dress to fit you..."):
            handler = fal_client.submit(
                "fal-ai/fashn/tryon/v1.5",
                arguments={
                    "model_image": user_img,
                    "garment_image": dress_img,
                    "category": "one-pieces"
                },
            )
            result = handler.get()
            st.image(result['images'][0]['url'], caption="Your New Look!")
    else:
        st.warning("Please upload both photos first.")
Step 2: Hide your Key in Streamlit Settings
Now you need to "feed" the key to the server so it stays there forever.

Go to your Streamlit Cloud Dashboard (where you see your app listed).

Click the three dots (...) next to your app and select Settings.

On the left sidebar, click Secrets.

In the dark text box that appears, paste exactly this (replacing the letters with your actual key):

Ini, TOML

FAL_KEY = "your-actual-long-key-here"
