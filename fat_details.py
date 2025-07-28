import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

st.title("Body Fat Percentage Estimator")
st.markdown("Enter your details and upload front + side full-body images to estimate body fat % and get categorized insights.")

# User input form
with st.form("input_form"):
    gender = st.selectbox("Gender", ["Male", "Female"])
    age = st.number_input("Age", 10, 100, 25)
    height = st.number_input("Height (cm)", 100, 250, 170)
    weight = st.number_input("Weight (kg)", 30, 200, 70)
    front_image = st.file_uploader("Upload Front View Image", type=["jpg", "jpeg", "png"])
    side_image = st.file_uploader("Upload Side View Image", type=["jpg", "jpeg", "png"])
    submit = st.form_submit_button("Estimate")

if submit:
    if not front_image or not side_image:
        st.warning("Please upload both front and side images.")
    else:
        front_img = Image.open(front_image)
        side_img = Image.open(side_image)
        st.image(front_img, caption="Front View", use_container_width=True)
        st.image(side_img, caption="Side View", use_container_width=True)

        with st.spinner("Analyzing..."):
            # Prompt
            prompt = f"""You are a certified body composition expert.
            Given the user's age, gender, height, weight, and two full-body images (front and side views), do the following:
            1. Estimate the user's body fat percentage.
            2.Identify the dominant type of fat distribution (e.g., abdominal/visceral fat, subcutaneous fat, or evenly distributed fat) based on visual signs in the images
            2. Classify the result into one of the health categories: essential fat, athletic, fit, average, or obese — based on their gender.
            3. Recommend a healthy goal fat percentage range based on standard fitness guidelines for their gender and age.
            User Information:
            - Gender: {gender}
            - Age: {age}
            - Height: {height} cm
            - Weight: {weight} kg
            Please respond in plain English in natural sentences. Do not use lists or JSON."""

            try:
                response = model.generate_content(
                    [prompt, front_img, side_img],
                    generation_config={"temperature": 0.4}
                )
                st.subheader("Estimation & Health Insight")
                st.success(response.text.strip())

            except Exception as e:
                st.error(f"Error during analysis: {e}")
