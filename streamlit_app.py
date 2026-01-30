import streamlit as st
import fal_client
import os

# --- 1. SETUP & KEYS ---
# This looks for your key in the Streamlit Cloud "Secrets" settings
if "FAL_KEY" in st.secrets:
    os.environ["FAL_KEY"] = st.secrets["FAL_KEY"]
else:
    st.error("Missing FAL_KEY! Please add it to your Streamlit Secrets.")

# --- 2. APP INTERFACE ---
st.set_page_config(page_title="AI Dressing Room", layout="centered")
st.title("👗 My AI Dressing Room")
st.write("Upload a photo of yourself and a dress to see the magic!")

# Step 1: User Photo
st.header("1. Upload Your Photo")
user_img = st.file_uploader("Take a photo of yourself", type=['jpg', 'jpeg', 'png'], key="user")

# Step 2: Dress Photo
st.header("2. Upload the Dress")
dress_img = st.file_uploader("Upload the dress to try on", type=['jpg', 'jpeg', 'png'], key="dress")

# --- 3. PROCESSING ---
if st.button("✨ Fit the Dress!"):
    if user_img and dress_img:
        with st.spinner("AI is sewing the dress to fit you..."):
            try:
                # We get the raw bytes from the Streamlit upload
                user_data = user_img.getvalue()
                dress_data = dress_img.getvalue()

                # We upload the bytes directly to fal.ai to get a URL
                # This 'fal_client.upload_file' is smart enough to handle raw bytes
                user_url = fal_client.upload_file(user_data)
                dress_url = fal_client.upload_file(dress_data)

                # Now we send those URLs to the Try-On AI model
                handler = fal_client.submit(
                    "fal-ai/fashn/tryon/v1.5",
                    arguments={
                        "model_image": user_url,
                        "garment_image": dress_url,
                        "category": "one-pieces"
                    },
                )
                
                result = handler.get()
                
                # --- 4. DISPLAY RESULT ---
                st.success("Success!")
                st.image(result['images'][0]['url'], caption="Your New Look!")
                
                # Add a download button for the user
                st.download_button(
                    label="📥 Download Image",
                    data=result['images'][0]['url'],
                    file_name="my_new_look.png",
                    mime="image/png"
                )

            except Exception as e:
                # This helps us see exactly what goes wrong if there is a mistake
                st.error(f"AI Error: {str(e)}")
    else:
        st.warning("Please upload both photos first.")
