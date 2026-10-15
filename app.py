import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Student Performance Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom visual theme
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #f4f7fb 0%, #edf2ff 100%);
    }
    [data-testid="stHeader"] {
        background: rgba(244, 247, 251, 0.85);
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #14213d 0%, #1f3a5f 100%);
    }
    [data-testid="stSidebar"] * {
        color: #f8fafc !important;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] label {
        background: rgba(255, 255, 255, 0.07);
        padding: 9px 12px;
        border-radius: 10px;
        margin-bottom: 5px;
    }
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2.5rem;
        max-width: 1400px;
    }
    h1 {
        color: #14213d;
        font-weight: 800 !important;
        letter-spacing: -0.7px;
    }
    h2, h3 {
        color: #1f3a5f;
        font-weight: 700 !important;
    }
    [data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e1e8f5;
        padding: 18px 20px;
        border-radius: 16px;
        box-shadow: 0 5px 18px rgba(31, 58, 95, 0.07);
    }
    [data-testid="stMetricLabel"] {
        color: #52627a;
    }
    [data-testid="stMetricValue"] {
        color: #2457c5;
        font-weight: 750;
    }
    div[data-testid="stDataFrame"] {
        border: 1px solid #e1e8f5;
        border-radius: 12px;
        overflow: hidden;
    }
    .stButton button, .stDownloadButton button {
        border-radius: 10px;
        font-weight: 600;
        border: 0;
    }
    .stDownloadButton button {
        background: #2457c5;
        color: white;
    }
    .stDownloadButton button:hover {
        background: #183f99;
        color: white;
    }
    [data-testid="stAlert"] {
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

st.title("📊 Student Performance Dashboard")
st.caption("A clear overview of marks, attendance, and academic progress.")
st.markdown("---")

# Load student data
df = pd.read_csv("students.csv")
subjects = ["Math", "Python", "Computer_Networks"]
df["Average_Marks"] = df[subjects].mean(axis=1)

# Sidebar navigation
st.sidebar.title("📘 Dashboard Menu")
st.sidebar.caption("Student analytics workspace")
section = st.sidebar.radio(
    "Choose a section",
    [
        "Student Information",
        "Performance Analysis",
        "Attendance Analysis",
        "Pass/Fail Analysis"
    ]
)

# 1. Student Information
if section == "Student Information":
    st.subheader("Class Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Students", len(df))
    col2.metric("Overall Average", f"{df[subjects].mean().mean():.1f}")
    col3.metric("Avg. Attendance", f"{df['Attendance'].mean():.1f}%")

    st.subheader("Individual Student Information")
    selected_student = st.selectbox(
        "Choose a student",
        df["Name"],
        key="info_student"
    )
    student_data = df[df["Name"] == selected_student]
    st.dataframe(student_data, hide_index=True, use_container_width=True)

    st.subheader("All Students")
    st.dataframe(df, hide_index=True, use_container_width=True)

    search_name = st.text_input("Search by student name")
    if search_name:
        search_result = df[
            df["Name"].str.contains(search_name, case=False, na=False)
        ]
        if not search_result.empty:
            st.dataframe(search_result, hide_index=True, use_container_width=True)
        else:
            st.warning("No student found with that name.")

    csv_data = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Student Data as CSV",
        data=csv_data,
        file_name="student_performance.csv",
        mime="text/csv"
    )

# 2. Performance Analysis
elif section == "Performance Analysis":
    st.subheader("Average Marks by Subject")
    selected_subject = st.selectbox(
        "Choose a subject",
        subjects,
        key="performance_subject"
    )
    subject_average = df[selected_subject].mean()
    st.metric(f"Average Marks in {selected_subject}", f"{subject_average:.1f}")

    averages = df[subjects].mean()
    st.subheader("Average Marks Chart")
    st.bar_chart(averages)

    st.subheader("Subject-wise Marks Comparison")
    comparison = pd.DataFrame({
        "Highest Marks": df[subjects].max(),
        "Lowest Marks": df[subjects].min()
    })
    st.bar_chart(comparison)

    st.subheader("Average Marks by Student")
    student_averages = df.set_index("Name")["Average_Marks"]
    st.bar_chart(student_averages)

    topper = df.loc[df["Average_Marks"].idxmax()]
    st.subheader("Class Topper")
    col1, col2 = st.columns(2)
    col1.metric("Topper", topper["Name"])
    col2.metric("Average Marks", f"{topper['Average_Marks']:.1f}/100")

    st.subheader("Individual Student Marks")
    chart_student = st.selectbox(
        "Choose a student for the marks chart",
        df["Name"],
        key="chart_student"
    )
    chart_data = df.loc[df["Name"] == chart_student, subjects].iloc[0]
    st.bar_chart(chart_data)

    st.subheader("Students Needing Improvement")
    improvement_threshold = st.slider(
        "Show students with an average below",
        min_value=0,
        max_value=100,
        value=60,
        key="improvement_threshold"
    )
    needs_improvement = df[df["Average_Marks"] < improvement_threshold]
    if not needs_improvement.empty:
        st.dataframe(
            needs_improvement[["Name", "Average_Marks"]],
            hide_index=True,
            use_container_width=True
        )
    else:
        st.success(f"No students have an average below {improvement_threshold}.")

    improvement_csv = needs_improvement.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Students Needing Improvement",
        data=improvement_csv,
        file_name="students_needing_improvement.csv",
        mime="text/csv"
    )

# 3. Attendance Analysis
elif section == "Attendance Analysis":
    st.subheader("Attendance Analysis")
    attendance_data = df[["Name", "Attendance"]]
    st.bar_chart(attendance_data, x="Name", y="Attendance")

    st.subheader("Low Attendance Students")
    threshold = st.slider(
        "Select attendance threshold (%)",
        min_value=50,
        max_value=100,
        value=85
    )
    low_attendance = df[df["Attendance"] < threshold]
    st.write(f"Students with attendance below {threshold}%:")
    st.dataframe(
        low_attendance[["Name", "Attendance"]],
        hide_index=True,
        use_container_width=True
    )

    attendance_csv = low_attendance[["Name", "Attendance"]].to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Low Attendance List",
        data=attendance_csv,
        file_name="low_attendance_students.csv",
        mime="text/csv"
    )

# 4. Pass/Fail Analysis
elif section == "Pass/Fail Analysis":
    st.subheader("Pass/Fail Analysis")
    passed_condition = (df[subjects] >= 40).all(axis=1)
    passed_students = df[passed_condition]
    failed_students = df[~passed_condition]
    total_students = len(df)
    pass_percentage = (len(passed_students) / total_students * 100) if total_students else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Students Passed", len(passed_students))
    col2.metric("Students Failed", len(failed_students))
    col3.metric("Pass Percentage", f"{pass_percentage:.1f}%")

    result_filter = st.selectbox(
        "Choose result",
        ["All Students", "Passed", "Failed"]
    )
    if result_filter == "Passed":
        result_students = passed_students
    elif result_filter == "Failed":
        result_students = failed_students
    else:
        result_students = df

    st.subheader(result_filter)
    st.dataframe(
        result_students[["Name"] + subjects],
        hide_index=True,
        use_container_width=True
    )

    st.write("Students who passed")
    st.dataframe(passed_students[["Name"]], hide_index=True, use_container_width=True)

    st.write("Students who failed")
    st.dataframe(failed_students[["Name"]], hide_index=True, use_container_width=True)
