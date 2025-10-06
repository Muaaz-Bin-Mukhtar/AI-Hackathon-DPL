import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import re

# ---------------------------
# 1. Load cleaned data
# ---------------------------
df = pd.read_csv("cleaned_file.csv")

print("🔹 Data loaded for feature extraction:")
print(df.head(), "\n")

# ---------------------------
# 2. Feature Extraction
# ---------------------------

# 2a. skills_set: split subjects into sets
df["skills_set"] = df["subjects"].apply(
    lambda x: set([s.strip().lower() for s in x.split(",")]) if isinstance(x, str) else set()
)

# 2b. years_num: extract numeric part, default 0 if missing
def extract_years(val):
    if pd.isna(val):
        return 0
    match = re.search(r"\d+", str(val))
    return int(match.group()) if match else 0

df["years_num"] = df["years_experience"].apply(extract_years)

# 2c. rate_num: numeric hourly rate, fill missing with 0
df["rate_num"] = pd.to_numeric(df["hourly_rate"].str.replace(r"[^\d.]", "", regex=True), errors="coerce").fillna(0)

# 2d. rating_norm: normalize rating to [0,1], clip invalid ratings first
df["rating_clean"] = pd.to_numeric(df["rating"], errors="coerce")
df["rating_clean"] = df["rating_clean"].clip(lower=1, upper=5)  # force all ratings between 1–5

scaler = MinMaxScaler()
df["rating_norm"] = scaler.fit_transform(df[["rating_clean"]])

# ---------------------------
# 3. Save feature-extracted file
# ---------------------------
df.to_csv("features_file.csv", index=False)

print("✅ Feature extraction complete → saved as features_file.csv")
print(df[["skills_set", "years_num", "rate_num", "rating_norm"]].head(), "\n")

# ---------------------------
# 4. Reflection (comments)
# ---------------------------
# - Important features for ranking: years_num, rate_num, rating_norm, skills_set
# - Keep raw + cleaned? Cleaned columns are used for analysis; raw can be kept for reference/debugging
