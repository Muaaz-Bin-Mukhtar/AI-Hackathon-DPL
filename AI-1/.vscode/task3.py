import pandas as pd
import numpy as np
import ast

# ---------------------------
# 1. Load features
# ---------------------------
df = pd.read_csv("features_file.csv")

# Convert skills_set from string to Python set
def str_to_set(s):
    try:
        return set(ast.literal_eval(s))
    except:
        return set()

df["skills_set"] = df["skills_set"].apply(str_to_set)

print("🔹 Loaded features for scoring:")
print(df.head(), "\n")

# ---------------------------
# 2. Define student requirements
# ---------------------------
# Example: student wants these subjects and experience ~5 years
student_skills = {"math", "physics", "chemistry"}
student_experience = 5  # years
sigma = 2  # for Gaussian experience score

# ---------------------------
# 3. Scoring Functions
# ---------------------------

# 3a. Skills score using Jaccard similarity
def jaccard_score(tutor_skills, student_skills):
    if not tutor_skills:
        return 0.0
    intersection = tutor_skills & student_skills
    union = tutor_skills | student_skills
    return len(intersection) / len(union)

df["skills_score"] = df["skills_set"].apply(lambda s: jaccard_score(s, student_skills))

# 3b. Experience score (Gaussian)
df["exp_score"] = np.exp(-((df["years_num"] - student_experience) ** 2) / (2 * sigma ** 2))

# 3c. Rating score is already normalized in [0,1]; fill missing with 0
df["rating_score"] = df["rating_norm"].fillna(0)

# ---------------------------
# 4. Final weighted score
# ---------------------------
df["final_score"] = 0.5 * df["skills_score"] + 0.3 * df["exp_score"] + 0.2 * df["rating_score"]

# ---------------------------
# 5. Rank tutors
# ---------------------------
df_sorted = df.sort_values(by="final_score", ascending=False)

print("🔹 Top 10 tutors based on final score:")
print(df_sorted[["name", "skills_set", "years_num", "rating_norm", "final_score"]].head(10))

# ---------------------------
# 6. Save scored file
# ---------------------------
df_sorted.to_csv("scored_tutors.csv", index=False)
print("\n✅ Scored tutors saved as scored_tutors.csv")

# ---------------------------
# 7. Reflection (comments)
# ---------------------------
# - Important features for ranking: skills_score, exp_score, rating_score
# - Adding experience and rating improves ranking vs skills-only
# - Weights can be fixed or user-tunable depending on user preference
