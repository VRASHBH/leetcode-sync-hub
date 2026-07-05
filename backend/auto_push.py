from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

class SolutionHandler(FileSystemEventHandler):

    def on_created(self, event):
        if not event.is_directory:
            print(f"[CREATED] {event.src_path}")

    def on_modified(self, event):
        if not event.is_directory:
            print(f"[MODIFIED] {event.src_path}")

if __name__ == "__main__":

    observer = Observer()
    observer.schedule(SolutionHandler(), "solutions", recursive=False)

    observer.start()

    print("Watching solutions folder...")

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        observer.stop()

    observer.join()