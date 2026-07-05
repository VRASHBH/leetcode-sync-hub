import sqlite3
import os

# Database clear
conn = sqlite3.connect("database/solutions.db")
cur = conn.cursor()

cur.execute("DELETE FROM solutions")

conn.commit()
conn.close()

print("✅ Database Cleared")

# Solutions folder clear
folders = [
    "solutions/Easy",
    "solutions/Medium",
    "solutions/Hard"
]

for folder in folders:
    if os.path.exists(folder):
        for file in os.listdir(folder):
            path = os.path.join(folder, file)

            if os.path.isfile(path):
                os.remove(path)

print("✅ Solutions Deleted")

# README reset
with open("README.md", "w", encoding="utf-8") as f:
    f.write("""# 🚀 LeetCode Sync Hub

## 📊 Statistics

| Difficulty | Count |
|------------|--------|
| Easy | 0 |
| Medium | 0 |
| Hard | 0 |

## 🎯 Total Solved

0

## 🕒 Last Updated

-
""")

print("✅ README Reset")

print("\n🚀 Project Reset Complete!")