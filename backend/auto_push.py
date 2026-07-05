from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import sqlite3
import time
import os

DB_PATH = "database/solutions.db"


def save_to_database(filename):

    problem_name = filename.replace(".cpp", "")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO solutions(
        problem_name,
        difficulty,
        language
    )
    VALUES(?,?,?)
    """, (
        problem_name,
        "Easy",
        "C++"
    ))

    conn.commit()
    conn.close()

    print("✅ Database Updated")


class SolutionHandler(FileSystemEventHandler):

    def on_created(self, event):

        if event.is_directory:
            return

        if not event.src_path.endswith(".cpp"):
            return

        filename = os.path.basename(event.src_path)

        print(f"[NEW] {filename}")

        try:

            save_to_database(filename)

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
        recursive=False
    )

    observer.start()

    print("🚀 Watching solutions folder...")

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        observer.stop()

    observer.join()