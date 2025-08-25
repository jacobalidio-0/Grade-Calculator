import streamlit as st  # Import the Streamlit library for building the web app
import base64
import os

# Function to set a custom background image using base64 encoding
def set_background(image_path):
    # Open the image file in binary mode
    with open(image_path, "rb") as image_file:
        # Encode the image to base64 so it can be embedded directly in HTML
        encoded = base64.b64encode(image_file.read()).decode()

   # Inject custom CSS into the Streamlit app to style the background and text
    st.markdown(
    f"""
    <style>
    /*  Style the main app container */
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/jpeg;base64,{encoded}");  /* Embed base64 image as background */
        background-size: cover;              /* Scale image to cover entire container */
        background-position: center;         /* Center the image */
        background-repeat: no-repeat;        /* Prevent tiling */
        background-attachment: fixed;        /* Keep background fixed during scroll */
        color: #111111;                      /* Set default text color to dark gray */
    }}

    /* 🖋️ Style key text elements for readability */
    .stMarkdown, .stText, .stTitle, .stSubheader {{
        color: #111111 !important;           /* Force dark text color */
        font-weight: 600 !important;         /* Make text semi-bold */
        text-shadow: 0px 0px 2px #ffffff;    /* Add subtle white glow for contrast */
    }}
    </style>
    """,
    unsafe_allow_html=True  # Allow raw HTML/CSS injection into the app
)


# Specify the full path to your local image file
# Use raw string (r"...") to avoid escape character issues on Windows
image_path = r"C:\Users\Jacob\Downloads\blue-office-stationery-with-copy-space.jpg"

# Apply the background to your Streamlit app
set_background(image_path)


# Title of the app
st.title("📚 Grade Calculator")

# --- Input Section ---

# Input field for number of absences (must be a non-negative integer)
absences = st.number_input("Number of Absences", min_value=0, step=1)

# If absences are 4 or more, student automatically fails
if absences >= 4:
    st.error("FAILED due to excessive absences.")  # Display error message
    st.stop()  # Stop further execution of the app

# Slider inputs for different grade components (range: 0 to 100)
prelim_exam = st.slider("Prelim Exam Grade", 0.0, 100.0)
quizzes = st.slider("Quizzes Grade", 0.0, 100.0)
requirements = st.slider("Requirements Grade", 0.0, 100.0)
recitation = st.slider("Recitation Grade", 0.0, 100.0)

# --- Grade Calculations ---

# Attendance grade is reduced by 10 points per absence
attendance = 100 - (absences * 10)

# Class standing is a weighted average of quizzes, requirements, and recitation
class_standing = (0.4 * quizzes) + (0.3 * requirements) + (0.3 * recitation)

# Prelim grade is calculated using weights: 60% exam, 10% attendance, 30% class standing
prelim_grade = (0.6 * prelim_exam) + (0.1 * attendance) + (0.3 * class_standing)

# --- Function to Calculate Required Midterm and Final Grades ---

# Calculates the required midterm and final grades to reach a target final grade
def required_grades(target, prelim):
    remaining = target - (0.2 * prelim)  # Subtract prelim's contribution (20%) from target
    midterm_final = remaining / 0.8      # Remaining 80% split equally between midterm and final
    return round(midterm_final, 2), round(midterm_final, 2)  # Return both as rounded values

# Calculate required grades to pass (75%) and to reach dean's list (90%)
pass_midterm, pass_final = required_grades(75, prelim_grade)
deans_midterm, deans_final = required_grades(90, prelim_grade)

# --- Output Section ---

# Display results
st.subheader("📊 Results")
st.write(f"Prelim Grade: **{round(prelim_grade, 2)}**")  # Show calculated prelim grade
st.write(f"To pass with 75%: Midterm = **{pass_midterm}**, Final = **{pass_final}**")  # Required grades to pass
st.write(f"To achieve 90%: Midterm = **{deans_midterm}**, Final = **{deans_final}**")  # Required grades for dean's list




