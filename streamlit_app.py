import streamlit as st
import fal_client
import os

# This checks for your secret key automatically
if "FAL_KEY" in st.secrets:
    os.environ["FAL_KEY"] = st.secrets["FAL_KEY"]
else:
    st.error("Missing FAL_KEY! Go to Settings > Secrets in Streamlit to add it.")

# --- APP INTERFACE ---
st.set_page_config(page_title="AI Dressing Room", layout="centered")
st.title("👗 My AI Dressing Room")

st.header("1. Upload Your Photo")
user_img = st.file_uploader("Take a photo of yourself", type=['jpg', 'png'], key="user")

st.header("2. Upload the Dress")
dress_img = st.file_uploader("Upload the dress to try on", type=['jpg', 'png'], key="dress")

if st.button("✨ Fit the Dress!"):
    if user_img and dress_img:
        with st.spinner("AI is sewing the dress to fit you..."):
            try:
                # 1. Upload images to fal.ai to get valid URLs
                user_url = fal_client.upload_file(user_img)
                dress_url = fal_client.upload_file(dress_img)

                # 2. Use those URLs to run the try-on
                handler = fal_client.submit(
                    "fal-ai/fashn/tryon/v1.5",
                    arguments={
                        "model_image": user_url,
                        "garment_image": dress_url,
                        "category": "one-pieces"
                    },
                )
                result = handler.get()
                
                # 3. Show the result!
                st.image(result['images'][0]['url'], caption="Your New Look!")
                
            except Exception as e:
                st.error(f"AI Error: {e}")
    else:
        st.warning("Please upload both photos first.")
