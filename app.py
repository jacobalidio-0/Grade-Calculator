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


# --- Absence Inputs ---
absences = st.number_input("Prelim Absences", min_value=0, step=1, key="prelim_absences")
midterm_absences = st.number_input("Midterm Absences", min_value=0, step=1, key="midterm_absences")
final_absences = st.number_input("Final Absences", min_value=0, step=1, key="final_absences")


# Total absences across the semester
total_absences = absences + midterm_absences + final_absences

# If total absences are 4 or more, student automatically fails
if total_absences >= 4:
    st.error(f"FAILED due to excessive absences. Total absences: {total_absences}")
    st.stop()

attendance = 100 - (absences * 10)

st.subheader("🎯 Input Your Grades")


col = st.columns(4)

prelim_exam   = col[0].number_input("Prelim Exam", min_value=0.00, max_value=100.00, step=0.01)
quizzes       = col[1].number_input("Quizzes Grade", min_value=0.00, max_value=100.00, step=0.01)
requirements  = col[2].number_input("Requirements Grade", min_value=0.00, max_value=100.00, step=0.01)
recitation    = col[3].number_input("Recitation Grade", min_value=0.00, max_value=100.00, step=0.01)

st.subheader("🧪 Input Your Midterm Grades")


midterm_attendance = 100 - (midterm_absences * 10)

col_mid = st.columns(4)
midterm_exam       = col_mid[0].number_input("Midterm Exam", min_value=0.00, max_value=100.00, step=0.01)
midterm_quizzes    = col_mid[1].number_input("Midterm Quizzes", min_value=0.00, max_value=100.00, step=0.01)
midterm_projects   = col_mid[2].number_input("Midterm Projects", min_value=0.00, max_value=100.00, step=0.01)
midterm_recitation = col_mid[3].number_input("Midterm Recitation", min_value=0.00, max_value=100.00, step=0.01)



st.subheader("🎓 Input Your Final Grades")


final_attendance = 100 - (final_absences * 10)


col_final = st.columns(4)
final_exam       = col_final[0].number_input("Final Exam", min_value=0.00, max_value=100.00, step=0.01)
final_quizzes    = col_final[1].number_input("Final Quizzes", min_value=0.00, max_value=100.00, step=0.01)
final_projects   = col_final[2].number_input("Final Projects", min_value=0.00, max_value=100.00, step=0.01)
final_recitation = col_final[3].number_input("Final Recitation", min_value=0.00, max_value=100.00, step=0.01)




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

# --- Midterm Grade Calculation ---
midterm_grade = (
    0.4 * midterm_exam +
    0.2 * midterm_quizzes +
    0.15 * midterm_projects +
    0.15 * midterm_recitation +  
    0.1 * midterm_attendance 
)



# --- Final Grade Calculation ---
final_grade = (
    0.4 * final_exam +
    0.2 * final_quizzes +
    0.15 * final_projects +
    0.15 * final_recitation +
    0.1 * final_attendance
)




# --- Output Section ---

# Display results
st.subheader("📊 Results")
st.write(f"Prelim Grade: **{round(prelim_grade, 2)}**")  # Show calculated prelim grade
st.write(f"To pass with 75%: Midterm = **{pass_midterm}**, Final = **{pass_final}**")  # Required grades to pass
st.write(f"To achieve 90%: Midterm = **{deans_midterm}**, Final = **{deans_final}**")  # Required grades for dean's list

# --- Overall Grade Calculation ---
overall_grade = (
    0.2 * prelim_grade +
    0.3 * midterm_grade +
    0.5 * final_grade
)

st.subheader("📊 Final Grade Summary")
st.write(f"Prelim Grade: **{round(prelim_grade, 2)}**")
st.write(f"Midterm Grade: **{round(midterm_grade, 2)}**")
st.write(f"Final Grade: **{round(final_grade, 2)}**")
st.write(f"Overall Grade: **{round(overall_grade, 2)}**")

# Status
if overall_grade >= 90:
    st.success("🎉 Dean's List! Outstanding performance.")
elif overall_grade >= 75:
    st.info("✅ You passed the course.")
else:
    st.error("❌ You did not meet the passing grade.")
