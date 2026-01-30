import streamlit as st
import fal_client
import os
import base64

# --- 1. SETUP ---
# Ensure your key is in Streamlit Secrets
if "FAL_KEY" in st.secrets:
    os.environ["FAL_KEY"] = st.secrets["FAL_KEY"]
else:
    st.error("⚠️ FAL_KEY missing! Please add it in Streamlit Settings > Secrets.")

st.set_page_config(page_title="AI Try-On", layout="centered")
st.title("👗 AI Virtual Dressing Room")

# --- 2. UPLOADERS ---
user_file = st.file_uploader("Step 1: Upload your photo", type=['jpg', 'jpeg', 'png'])
dress_file = st.file_uploader("Step 2: Upload the dress photo", type=['jpg', 'jpeg', 'png'])

# --- 3. PROCESSING ---
if st.button("✨ Generate My Look"):
    if user_file and dress_file:
        with st.spinner("AI is sewing the dress to fit you... (takes ~20 seconds)"):
            try:
                # Convert images to Base64 strings (the most stable way for AI)
                user_base64 = base64.b64encode(user_file.getvalue()).decode("utf-8")
                dress_base64 = base64.b64encode(dress_file.getvalue()).decode("utf-8")
                
                user_data_url = f"data:{user_file.type};base64,{user_base64}"
                dress_data_url = f"data:{dress_file.type};base64,{dress_base64}"

                # Run the AI model
                result = fal_client.subscribe(
                    "fal-ai/fashn/tryon/v1.5",
                    arguments={
                        "model_image": user_data_url,
                        "garment_image": dress_data_url,
                        "category": "one-pieces"
                    },
                )
                
                # --- 4. DISPLAY ---
                if "images" in result:
                    st.success("Your look is ready!")
                    st.image(result['images'][0]['url'], use_container_width=True)
                    st.balloons()
                else:
                    st.error("AI finished but no image was found.")

            except Exception as e:
                st.error(f"AI Error: {str(e)}")
    else:
        st.warning("Please upload both photos first!")
