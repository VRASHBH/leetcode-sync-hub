from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import sqlite3
import time
import os
from datetime import datetime

DB_PATH = "database/solutions.db"

SUPPORTED_EXTENSIONS = {
    ".cpp": "C++",
    ".py": "Python",
    ".java": "Java",
    ".sql": "SQL",
    ".js": "JavaScript"
}


def update_readme():

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM solutions")
    total = cur.fetchone()[0]

    cur.execute(
        "SELECT COUNT(*) FROM solutions WHERE difficulty='Easy'"
    )
    easy = cur.fetchone()[0]

    cur.execute(
        "SELECT COUNT(*) FROM solutions WHERE difficulty='Medium'"
    )
    medium = cur.fetchone()[0]

    cur.execute(
        "SELECT COUNT(*) FROM solutions WHERE difficulty='Hard'"
    )
    hard = cur.fetchone()[0]

    cur.execute("""
    SELECT language, COUNT(*)
    FROM solutions
    GROUP BY language
    ORDER BY COUNT(*) DESC
    """)

    language_stats = cur.fetchall()

    conn.close()

    language_section = ""

    for lang, count in language_stats:
        language_section += f"- {lang}: {count}\n"

    content = f"""# 🚀 LeetCode Sync Hub

## 📊 Statistics

Total Solved: {total}

🟢 Easy: {easy}
🟡 Medium: {medium}
🔴 Hard: {hard}

## 💻 Languages

{language_section}

## 🔄 Auto Synced

Last Updated:
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

    with open(
        "README.md",
        "w",
        encoding="utf-8"
    ) as f:
        f.write(content)

    print("✅ README Updated")


def save_to_database(
    filename,
    difficulty,
    language
):

    problem_name = os.path.splitext(filename)[0]

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

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
        language
    ))

    conn.commit()
    conn.close()

    print("✅ Database Updated")

    return True


class SolutionHandler(FileSystemEventHandler):

    def process_file(self, file_path):

        if os.path.isdir(file_path):
            return

        ext = os.path.splitext(file_path)[1]

        if ext not in SUPPORTED_EXTENSIONS:
            return

        filename = os.path.basename(file_path)

        language = SUPPORTED_EXTENSIONS[ext]

        if "Easy" in file_path:
            difficulty = "Easy"

        elif "Medium" in file_path:
            difficulty = "Medium"

        elif "Hard" in file_path:
            difficulty = "Hard"

        else:
            difficulty = "Unknown"

        print(f"\n📄 New Solution Found")
        print(f"File: {filename}")
        print(f"Difficulty: {difficulty}")
        print(f"Language: {language}")

        try:

            inserted = save_to_database(
                filename,
                difficulty,
                language
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

    def on_created(self, event):
        self.process_file(event.src_path)

    def on_modified(self, event):
        self.process_file(event.src_path)


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