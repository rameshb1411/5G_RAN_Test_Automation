import time
import datetime
import sys

def log(message):
    timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"[{timestamp}] [Core] {message}", flush=True)

if __name__ == '__main__':
    log("Starting Core simulator...")
    while True:
        log("Core: Handling signaling requests...")
        time.sleep(1)
