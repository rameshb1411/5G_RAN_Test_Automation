import subprocess
import time
import os
import threading

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
GNB_SCRIPT = os.path.join(SCRIPT_DIR, "gnb_simulator.py")
UE_SCRIPT = os.path.join(SCRIPT_DIR, "ue_simulator.py")
CORE_SCRIPT = os.path.join(SCRIPT_DIR, "core_simulator.py")
TEST_SUITE = os.path.join(SCRIPT_DIR, "test_suite.robot")
LOG_FILE = os.path.join(SCRIPT_DIR, "all_console_logs.txt")

def start_component(script, name):
    print(f"🔄 Starting {script}...\n")
    proc = subprocess.Popen(
        ["python", script],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        bufsize=1
    )
    return proc

def read_logs(process, name, stop_event, log_file):
    while not stop_event.is_set():
        line = process.stdout.readline()
        if line:
            output_line = f"[{name}] {line.strip()}"
            print(output_line, flush=True)
            log_file.write(output_line + "\n")
            log_file.flush()
    for line in process.stdout:
        output_line = f"[{name}] {line.strip()}"
        print(output_line, flush=True)
        log_file.write(output_line + "\n")
        log_file.flush()

stop_event = threading.Event()

with open(LOG_FILE, "w", encoding="utf-8") as log_file:
    gnb_process = start_component(GNB_SCRIPT, "gNB")
    ue_process = start_component(UE_SCRIPT, "UE")
    core_process = start_component(CORE_SCRIPT, "Core")

    gnb_thread = threading.Thread(target=read_logs, args=(gnb_process, "gNB", stop_event, log_file))
    ue_thread = threading.Thread(target=read_logs, args=(ue_process, "UE", stop_event, log_file))
    core_thread = threading.Thread(target=read_logs, args=(core_process, "Core", stop_event, log_file))

    gnb_thread.start()
    ue_thread.start()
    core_thread.start()

    # Wait until "ALL_SIBS_BROADCASTED" is detected in gNB logs
    def wait_for_all_sibs():
        while True:
            line = gnb_process.stdout.readline()
            if "ALL_SIBS_BROADCASTED" in line:
                print("[Test Runner] Detected ALL_SIBS_BROADCASTED. Proceeding with tests.", flush=True)
                log_file.write("[Test Runner] Detected ALL_SIBS_BROADCASTED. Proceeding with tests.\n")
                log_file.flush()
                break
    wait_for_all_sibs()

    print("🚀 Running test cases...\n")
    log_file.write("🚀 Running test cases...\n")
    log_file.flush()
    test_process = subprocess.run(["robot", TEST_SUITE], capture_output=True, text=True)

    print("📜 Test Output:")
    print(test_process.stdout)
    print("🛑 Test Errors:")
    print(test_process.stderr)

    log_file.write("📜 Test Output:\n")
    log_file.write(test_process.stdout + "\n")
    log_file.write("🛑 Test Errors:\n")
    log_file.write(test_process.stderr + "\n")
    log_file.flush()

    stop_event.set()

    gnb_process.terminate()
    ue_process.terminate()
    core_process.terminate()

    gnb_process.wait()
    ue_process.wait()
    core_process.wait()

    gnb_thread.join()
    ue_thread.join()
    core_thread.join()

    print("✅ All components and tests completed.")
    log_file.write("✅ All components and tests completed.\n")
    log_file.flush()
