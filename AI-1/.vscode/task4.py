import streamlit as st
import pandas as pd
import numpy as np

# Load the scored tutors file from Task 3
df = pd.read_csv("scored_tutors.csv")

st.title("🎓 Tutor Finder & Ranking System")

# ----------------- Sidebar Filters -----------------
st.sidebar.header("🔍 Filters")

# City filter
cities = st.sidebar.multiselect(
    "Select Cities", 
    options=df["city"].dropna().unique()
)

# Subject filter
subjects = st.sidebar.multiselect(
    "Select Subjects", 
    options=sorted({sub.strip().lower() for s in df["subjects_clean"].dropna() for sub in s.split(",")})
)

# Min years of experience
min_years = st.sidebar.slider("Minimum Years of Experience", 0, int(df["years_num"].max()), 0)

# Max hourly rate
max_rate = st.sidebar.slider("Maximum Hourly Rate", 0, int(df["rate_num"].max()), int(df["rate_num"].max()))

# Target experience (for Gaussian score)
target_years = st.sidebar.slider("Target Years (Experience Proximity)", 0, 20, 5)

# ----------------- Filtering -----------------
filtered_df = df.copy()

if cities:
    filtered_df = filtered_df[filtered_df["city"].isin(cities)]

if subjects:
    filtered_df = filtered_df[
        filtered_df["subjects_clean"].apply(
            lambda s: any(sub in s for sub in subjects) if isinstance(s, str) else False
        )
    ]

filtered_df = filtered_df[filtered_df["years_num"] >= min_years]
filtered_df = filtered_df[filtered_df["rate_num"] <= max_rate]

# ----------------- Recalculate Experience Score -----------------
def exp_proximity(y, t, sigma=2):
    return np.exp(-((y - t) ** 2) / (2 * sigma ** 2))

filtered_df["exp_score"] = filtered_df["years_num"].apply(lambda y: exp_proximity(y, target_years))

# ----------------- Final Score -----------------
filtered_df["final_score"] = (
    0.5 * filtered_df["skills_score"] +
    0.3 * filtered_df["exp_score"] +
    0.2 * filtered_df["rating_score"].fillna(0)
)

filtered_df = filtered_df.sort_values(by="final_score", ascending=False)

# ----------------- Display -----------------
st.subheader(f"Found {len(filtered_df)} matching tutors")

if len(filtered_df) == 0:
    st.warning("⚠️ No tutors match your filters.")
else:
    st.dataframe(
        filtered_df[["name", "subjects_clean", "years_num", "rate_num", "rating_clean", "final_score"]],
        use_container_width=True
    )

    # Expander for details
    for _, row in filtered_df.iterrows():
        with st.expander(f"📘 {row['name']} - {row['subjects_clean']}"):
            st.write(f"**City:** {row['city']}")
            st.write(f"**Experience:** {row['years_num']} years")
            st.write(f"**Hourly Rate:** {row['rate_num']}")
            st.write(f"**Rating:** {row['rating_clean']}")
            st.write(f"**Final Score:** {row['final_score']:.3f}")
            st.write(f"**Bio:** {row['bio']}")
