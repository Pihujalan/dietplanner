# Drop unwanted columns
df = df.drop(columns=[f"Unnamed: {i}" for i in range(13, 19)], errors="ignore")

# Optionally drop City/State/Country if you don’t want location bias
df = df.drop(columns=["City", "State", "Country"], errors="ignore")

print("Remaining columns:", df.columns.tolist())