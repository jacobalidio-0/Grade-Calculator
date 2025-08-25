def get_valid_input(prompt, min_val=0, max_val=100, is_integer=False):
    while True:
        try:
            value = int(input(prompt)) if is_integer else float(input(prompt))
            if value < min_val or value > max_val:
                print(f"Please enter a value between {min_val} and {max_val}.")
            else:
                return value
        except ValueError:
            print("Invalid input. Please enter a number.")

# Inputs
absences = get_valid_input("Enter number of absences: ", min_val=0, is_integer=True)
if absences >= 4:
    print("Prelim Grade: FAILED due to excessive absences.")
    exit()

prelim_exam = get_valid_input("Enter Prelim Exam Grade (0-100): ")
quizzes = get_valid_input("Enter Quizzes Grade (0-100): ")
requirements = get_valid_input("Enter Requirements Grade (0-100): ")
recitation = get_valid_input("Enter Recitation Grade (0-100): ")

# Calculations
attendance = 100 - (absences * 10)
class_standing = (0.4 * quizzes) + (0.3 * requirements) + (0.3 * recitation)
prelim_grade = (0.6 * prelim_exam) + (0.1 * attendance) + (0.3 * class_standing)

# Required Midterm and Final Grades
def required_grades(target, prelim):
    # Solve: target = 0.2 * prelim + 0.3 * midterm + 0.5 * final
    # Assume midterm = final for simplicity
    remaining = target - (0.2 * prelim)
    midterm_final = remaining / 0.8
    return round(midterm_final, 2), round(midterm_final, 2)

pass_midterm, pass_final = required_grades(75, prelim_grade)
deans_midterm, deans_final = required_grades(90, prelim_grade)

# Output
print(f"\nPrelim Grade: {round(prelim_grade, 2)}")
print(f"To pass with 75%, you need a Midterm grade of {pass_midterm} and a Final grade of {pass_final}.")
print(f"To achieve 90%, you need a Midterm grade of {deans_midterm} and a Final grade of {deans_final}.")






import streamlit as st

st.title("📘 Grade Calculator")

# Input: Absences
absences = st.number_input("Number of Absences", min_value=0, step=1)

if absences >= 4:
    st.error("FAILED due to excessive absences.")
    st.stop()

# Input: Grades
prelim_exam = st.slider("Prelim Exam Grade", 0.0, 100.0)
quizzes = st.slider("Quizzes Grade", 0.0, 100.0)
requirements = st.slider("Requirements Grade", 0.0, 100.0)
recitation = st.slider("Recitation Grade", 0.0, 100.0)

# Calculations
attendance = 100 - (absences * 10)
class_standing = (0.4 * quizzes) + (0.3 * requirements) + (0.3 * recitation)
prelim_grade = (0.6 * prelim_exam) + (0.1 * attendance) + (0.3 * class_standing)

def required_grades(target, prelim):
    remaining = target - (0.2 * prelim)
    midterm_final = remaining / 0.8
    return round(midterm_final, 2), round(midterm_final, 2)

pass_midterm, pass_final = required_grades(75, prelim_grade)
deans_midterm, deans_final = required_grades(90, prelim_grade)

# Output
st.subheader("📊 Results")
st.write(f"Prelim Grade: **{round(prelim_grade, 2)}**")
st.write(f"To pass with 75%: Midterm = **{pass_midterm}**, Final = **{pass_final}**")
st.write(f"To achieve 90%: Midterm = **{deans_midterm}**, Final = **{deans_final}**")
