import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

st.title("Body Composition Estimator")
st.markdown("Upload front and side full-body images to estimate height, weight, and body fat percentage.")

# File upload
front_file = st.file_uploader("Upload Front View Image", type=["jpg", "jpeg", "png"])
side_file = st.file_uploader("Upload Side View Image", type=["jpg", "jpeg", "png"])

# When both files are uploaded
if front_file and side_file:
    front_image = Image.open(front_file)
    side_image = Image.open(side_file)

    st.image(front_image, caption="Front View", use_container_width=True)
    st.image(side_image, caption="Side View", use_container_width=True)

    if st.button("Estimate"):
        with st.spinner("Analyzing images..."):
            prompt = """You are a health and fitness expert.
            Given the following **front-view** and **side-view** full-body images of a person, estimate their physical metrics based on visual analysis. Assume the person is standing upright, with typical body proportions and neutral posture.
            Your task is to estimate the following:
            1. **Height** (in centimeters)
            2. **Weight** (in kilograms)
            3. **Body Fat Percentage** (in %)
            Use visual cues such as:
            - Abdominal protrusion
            - Muscle tone
            - Waist-to-hip ratio
            - Neck size
            - Overall body composition and build
            Return the result in as shown below:
            "height_cm": ...,
            "weight_kg": ...,
            "body_fat_percentage": ..."""

            try:
                response = model.generate_content(
                    [prompt, front_image, side_image],
                    generation_config={"temperature": 0.4}
                )
                st.subheader("Estimated Body Composition:")
                st.code(response.text.strip(), language="json")
            except Exception as e:
                st.error(f"Error: {e}")
