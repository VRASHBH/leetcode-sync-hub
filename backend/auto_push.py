from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import time
import os

class SolutionHandler(FileSystemEventHandler):

    def on_created(self, event):

        if event.is_directory:
            return

        if not event.src_path.endswith((".cpp", ".py", ".java")):
            return

        print(f"[NEW] {event.src_path}")

        try:
            subprocess.run(["git", "add", "."], check=True)

            commit_message = f"Added {os.path.basename(event.src_path)}"

            subprocess.run(
                ["git", "commit", "-m", commit_message],
                check=True
            )

            subprocess.run(
                ["git", "push"],
                check=True
            )

            print("✅ GitHub Updated")

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