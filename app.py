import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(
    page_title="Space Debris Risk Analysis System",
    page_icon="🛰",
    layout="wide"
)

st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    padding-left: 3rem;
    padding-right: 3rem;
}

h1, h2, h3 {
    color: white;
}

[data-testid="metric-container"] {
    background-color: #161B22;
    border: 1px solid #30363D;
    padding: 18px;
    border-radius: 14px;
}

section[data-testid="stSidebar"] {
    background-color: #111827;
}

</style>
""", unsafe_allow_html=True)


st.title("🛰 Space Debris Risk Analysis Dashboard")

st.markdown("""
This dashboard analyzes potential collision risks between active satellites and space debris
using orbital analysis and rule-based risk evaluation.
""")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

data_folder = os.path.join(BASE_DIR, "2_Files")

risk_path = os.path.join(data_folder, "risk_output.csv")
active_path = os.path.join(data_folder, "active_final.csv")
debris_path = os.path.join(data_folder, "debris_final.csv")

try:
    risk_df = pd.read_csv(risk_path)
    active_df = pd.read_csv(active_path)
    debris_df = pd.read_csv(debris_path)

except Exception as e:
    st.error(f"Error loading CSV files: {e}")
    st.stop()

st.sidebar.title("Dashboard Navigation")

section = st.sidebar.radio(
    "Select Section",
    [
        "Overview",
        "Risk Analysis",
        "Visualization",
        "Search & Reports"
    ]
)
if section == "Overview":

    st.header("📊 Project Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Active Satellites",
        len(active_df)
    )

    col2.metric(
        "Debris Objects",
        len(debris_df)
    )

    col3.metric(
        "Risk Cases",
        len(risk_df)
    )

    st.markdown("---")

    st.subheader("System Description")

    st.write("""
    The system processes satellite and debris datasets to identify 
    potential collision risks in orbital regions.

    Core functionalities include:
    - Altitude Calculation
    - Orbit Classification
    - Velocity Estimation
    - Risk Evaluation
    - Data Visualization
    - Report Generation
    """)

    st.subheader("Technology Stack")

    t1, t2, t3, t4 = st.columns(4)

    t1.info("Python")
    t2.info("Pandas")
    t3.info("Plotly")
    t4.info("Streamlit")

elif section == "Risk Analysis":

    st.header("⚠ Collision Risk Analysis")

    risk_filter = st.selectbox(
        "Filter by Risk Level",
        ["All", "High", "Medium", "Low"]
    )

    if risk_filter == "All":
        filtered_df = risk_df

    else:
        filtered_df = risk_df[
            risk_df["Risk_Level"] == risk_filter
        ]

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

    st.markdown("---")

    st.subheader("🔥 High Risk Cases")

    high_risk = risk_df[
        risk_df["Risk_Level"] == "High"
    ]

    st.dataframe(
        high_risk,
        use_container_width=True
    )


elif section == "Visualization":

    st.header("📈 Data Visualization")

    st.subheader("Risk Distribution")

    risk_counts = risk_df["Risk_Level"].value_counts()

    fig1 = px.bar(
        x=risk_counts.index,
        y=risk_counts.values,
        labels={
            "x": "Risk Level",
            "y": "Count"
        },
        title="Distribution of Risk Levels",
        text_auto=True
    )

    fig1.update_layout(
        template="plotly_dark",
        height=500
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    st.subheader("Orbit Distribution")

    orbit_counts = active_df["Orbit_Type"].value_counts()

    orbit_counts = orbit_counts.reindex(
        ["LEO", "MEO", "GEO"],
        fill_value=0
    )

    fig2 = px.pie(
        names=orbit_counts.index,
        values=orbit_counts.values,
        title="Satellite Orbit Distribution"
    )

    fig2.update_layout(
        template="plotly_dark",
        height=500
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    st.subheader("Altitude Distribution")

    fig3 = px.histogram(
        active_df,
        x="Altitude",
        nbins=20,
        title="Satellite Altitude Distribution"
    )

    fig3.update_layout(
        template="plotly_dark",
        height=500
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )


elif section == "Search & Reports":

    st.header("🔍 Search & Reports")

    sat_name = st.text_input(
        "Enter Satellite Name"
    )

    if sat_name:

        result_df = risk_df[
            risk_df["Satellite"].str.contains(
                sat_name,
                case=False,
                na=False
            )
        ]

        st.subheader("Search Results")

        st.dataframe(
            result_df,
            use_container_width=True
        )

    st.markdown("---")

    st.subheader("📥 Download High Risk Report")

    high_risk = risk_df[
        risk_df["Risk_Level"] == "High"
    ]

    csv = high_risk.to_csv(index=False)

    st.download_button(
        label="Download CSV Report",
        data=csv,
        file_name="high_risk_report.csv",
        mime="text/csv"
    )


st.markdown("---")

st.caption(
    "Space Debris Risk Analysis System | Developed using Python, Pandas, Plotly and Streamlit"
)