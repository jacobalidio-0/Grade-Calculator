import streamlit as st  # Import the Streamlit library for building the web app

# Define custom CSS to set a full-screen background image
page_bg_img = """
<style>
/* Target the main app container */
[data-testid="stAppViewContainer"] {
    background-image: url("https://images.unsplash.com/photo-1507525428034-b723cf961d3e");  /* Ocean sunset background from Unsplash */
    background-size: cover;              /* Scale image to fill the entire container */
    background-position: center;         /* Center the image within the container */
    background-repeat: no-repeat;        /* Prevent the image from repeating */
    background-attachment: fixed;        /* Keep the background fixed during scroll */
}
</style>
"""

# Inject the CSS into the Streamlit app
st.markdown(page_bg_img, unsafe_allow_html=True)  # Allow raw HTML/CSS for custom styling


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

