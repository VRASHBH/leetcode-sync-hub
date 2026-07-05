from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import sqlite3
import time
import os

DB_PATH = "database/solutions.db"
from datetime import datetime

def update_readme():

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM solutions")
    total = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM solutions WHERE difficulty='Easy'")
    easy = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM solutions WHERE difficulty='Medium'")
    medium = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM solutions WHERE difficulty='Hard'")
    hard = cur.fetchone()[0]

    conn.close()

    content = f"""# 🚀 LeetCode Sync Hub

Total Solved: {total}

Easy: {easy}
Medium: {medium}
Hard: {hard}

Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
"""

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)

    print("✅ README Updated")

def save_to_database(filename, difficulty):

    problem_name = filename.replace(".cpp", "")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Duplicate check
    cur.execute("""
    SELECT COUNT(*)
    FROM solutions
    WHERE problem_name = ?
    """, (problem_name,))

    exists = cur.fetchone()[0]

    if exists:
        print("⚠️ Solution Already Exists")
        conn.close()
        return False

    cur.execute("""
    INSERT INTO solutions(
        problem_name,
        difficulty,
        language
    )
    VALUES(?,?,?)
    """, (
        problem_name,
        difficulty,
        "C++"
    ))

    conn.commit()
    conn.close()

    print("✅ Database Updated")

    return True

class SolutionHandler(FileSystemEventHandler):

    def on_created(self, event):

        if event.is_directory:
            return

        if not event.src_path.endswith(".cpp"):
            return

        filename = os.path.basename(event.src_path)

        # Difficulty Detection
        if "Easy" in event.src_path:
            difficulty = "Easy"
        elif "Medium" in event.src_path:
            difficulty = "Medium"
        elif "Hard" in event.src_path:
            difficulty = "Hard"
        else:
            difficulty = "Unknown"

        print(f"[NEW] {filename}")
        print(f"Difficulty: {difficulty}")

        try:

            inserted = save_to_database(
                filename,
                difficulty
            )

            if not inserted:
                return

            update_readme()

            subprocess.run(
                ["git", "add", "."],
                check=True
            )

            subprocess.run(
                [
                    "git",
                    "commit",
                    "-m",
                    f"Added {filename}"
                ],
                check=True
            )

            subprocess.run(
                ["git", "push"],
                check=True
            )

            print("🚀 GitHub Updated")

        except Exception as e:
            print("❌ Error:", e)

if __name__ == "__main__":

    observer = Observer()

    observer.schedule(
        SolutionHandler(),
        "solutions",
        recursive=True
    )

    observer.start()

    print("🚀 Watching solutions folder...")

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        observer.stop()

    observer.join()