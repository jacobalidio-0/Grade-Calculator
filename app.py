import streamlit as st  # Import the Streamlit library for building the web app
import base64

# Function to convert image to base64
def get_base64(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Encode your local image
img_base64 = get_base64("jacob.jpg")

# Inject CSS with base64 image
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("data:image/png;base64,{img_base64}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)


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

st.subheader("🎯 Input Your Grades")
st.caption("💡 Tip: Use manual input for precise decimals like 89.75 or 92.33. Sliders are great for quick estimates.")



def synced_input(label, key, col_slider, col_input):
    # Initialize session state
    if key not in st.session_state:
        st.session_state[key] = 0.00

    # Create subcolumns for slider + buttons
    with col_slider:
        subcol = st.columns([6, 1, 1])  # Slider, ➖, ➕

        # ➖ Button
        if subcol[1].button("➖", key=f"{key}_minus"):
            st.session_state[key] = max(0.00, round(st.session_state[key] - 0.01, 2))

        # ➕ Button
        if subcol[2].button("➕", key=f"{key}_plus"):
            st.session_state[key] = min(100.00, round(st.session_state[key] + 0.01, 2))

        # Slider synced to session_state[key]
        slider_val = subcol[0].slider(
            label,
            min_value=0.00,
            max_value=100.00,
            value=float(st.session_state[key]),
            step=0.01,
            format="%.2f",
            key=f"{key}_slider"
        )

    # Manual input synced to session_state[key]
    number_val = col_input.number_input(
        f"{label} (Manual)",
        min_value=0.00,
        max_value=100.00,
        value=float(st.session_state[key]),
        step=0.01,
        format="%.2f",
        key=f"{key}_input"
    )

    # Final sync logic
    if abs(slider_val - st.session_state[key]) > 0.001:
        st.session_state[key] = slider_val
    elif abs(number_val - st.session_state[key]) > 0.001:
        st.session_state[key] = number_val

    return st.session_state[key]


col = st.columns(4)
prelim_exam   = synced_input("Prelim Grade",      "prelim",      col[0], col[0])
quizzes       = synced_input("Quizzes Grade",     "quizzes",     col[1], col[1])
requirements  = synced_input("Requirements Grade","requirements",col[2], col[2])
recitation    = synced_input("Recitation Grade",  "recitation",  col[3], col[3])

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
