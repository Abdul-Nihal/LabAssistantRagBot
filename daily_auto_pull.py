import os
import subprocess
import time
from datetime import datetime

def git_pull():
    try:
        print(f"[{datetime.now()}] Running git pull in {os.getcwd()}...")
        result = subprocess.run(["git", "pull"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Success:\n{result.stdout}")
        else:
            print(f"Error:\n{result.stderr}")
    except Exception as e:
        print(f"Exception occurred: {e}")

if __name__ == "__main__":
    while True:
        git_pull()
        print("Waiting for 24 hours until next pull...\n")
        time.sleep(86400)  # Sleep for 24 hours (86400 seconds)
