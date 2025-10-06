import pandas as pd

# 1. Load the CSV
df = pd.read_csv("data.csv")

# Inspect
print("🔹 First 5 rows of data:")
print(df.head(), "\n")
print("🔹 Info about dataset:")
print(df.info(), "\n")

# Cleaning
df["years_experience_clean"] = pd.to_numeric(
    df["years_experience"].str.replace(r"\D", "", regex=True),
    errors="coerce"
)

df["hourly_rate_clean"] = (
    df["hourly_rate"]
    .str.replace(r"[^\d.]", "", regex=True)
    .astype(float)
)

df["rating_clean"] = pd.to_numeric(df["rating"], errors="coerce")
df["subjects_clean"] = df["subjects"].str.strip().str.lower()

# Check out-of-range ratings
bad_ratings = df[(df["rating_clean"] < 1) | (df["rating_clean"] > 5)]
if not bad_ratings.empty:
    print("⚠️ Found out-of-range ratings:\n", bad_ratings[["rating"]], "\n")

# Reflection: % failed parsing
failed = df[["years_experience_clean", "hourly_rate_clean", "rating_clean"]].isna().mean() * 100
print("🔹 Percentage of rows that failed parsing:\n", failed)

# 👉 Save cleaned version for Task 2
df.to_csv("cleaned_file.csv", index=False)
print("✅ Cleaned file saved as cleaned_file.csv")
