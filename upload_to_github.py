import os
import subprocess
import json
import requests
from datetime import datetime

# ---------------- CONFIGURATION ---------------- #
GITHUB_USERNAME = "rameshb1411"  # Replace with your GitHub username
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # Set this as an environment variable
LOCAL_REPO_PATH = r"C:\Users\Ramesh1\PycharmProjects\PythonProject2\5G_RAN_Test_Project"
LOG_FILE = os.path.join(LOCAL_REPO_PATH, "upload_log.txt")
NEW_REPO_NAME = "5G_RAN_Test_Automation"
GITHUB_API_URL = "https://api.github.com/user/repos"
GITHUB_REPO_URL = f"https://github.com/{GITHUB_USERNAME}/{NEW_REPO_NAME}.git"


# ---------------- LOGGING FUNCTION ---------------- #
def log_message(message):
    """Logs messages to a file and prints them with UTF-8 encoding."""
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    log_entry = f"{timestamp} {message}\n"

    try:
        with open(LOG_FILE, "a", encoding="utf-8") as log_file:
            log_file.write(log_entry)
    except Exception as log_error:
        print(f"❌ ERROR: Failed to write log: {log_error}")

    print(message)


# ---------------- CHECK IF REPO EXISTS ---------------- #
def repo_exists():
    """Checks if the GitHub repository already exists."""
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(f"https://api.github.com/repos/{GITHUB_USERNAME}/{NEW_REPO_NAME}", headers=headers)
    return response.status_code == 200


# ---------------- CREATE NEW REPO IF NEEDED ---------------- #
def create_github_repo():
    """Creates a new GitHub repository if it does not exist."""
    if repo_exists():
        log_message(f"✅ Repository '{NEW_REPO_NAME}' already exists. Proceeding with upload.")
        return

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {"name": NEW_REPO_NAME, "private": False}

    response = requests.post(GITHUB_API_URL, headers=headers, data=json.dumps(data))

    if response.status_code == 201:
        log_message(f"✅ Repository '{NEW_REPO_NAME}' created successfully!")
    elif response.status_code == 422:
        log_message(f"⚠️ Repository creation failed: {response.json()}")
    else:
        log_message(f"❌ ERROR: Unable to create repository: {response.json()}")


# ---------------- UPDATE ENVIRONMENT VARIABLE ---------------- #
def update_env_variable():
    """Updates the Windows environment variable to store the repo name."""
    os.system(f'setx GITHUB_REPO "{NEW_REPO_NAME}"')
    log_message(f"✅ Updated environment variable: GITHUB_REPO={NEW_REPO_NAME}")


# ---------------- GIT SETUP & FILE UPLOAD ---------------- #
def git_setup_and_upload():
    """Handles git initialization, commits, and uploads to GitHub."""
    os.chdir(LOCAL_REPO_PATH)

    # Initialize git if not already initialized
    if not os.path.exists(os.path.join(LOCAL_REPO_PATH, ".git")):
        log_message("ℹ️ Initializing new Git repository...")
        subprocess.run(["git", "init"], check=True)
        subprocess.run(["git", "branch", "-M", "main"], check=True)
        subprocess.run(["git", "remote", "add", "origin", GITHUB_REPO_URL], check=True)

    # Pull the latest changes (if repo exists)
    try:
        subprocess.run(["git", "pull", "origin", "main", "--allow-unrelated-histories"], check=True)
    except subprocess.CalledProcessError:
        log_message("⚠️ No previous commits found, skipping pull.")

    # Add and commit changes
    subprocess.run(["git", "add", "."], check=True)

    # Get the latest version number
    version = get_latest_version() + 1
    commit_message = f"Automated upload: version {version}"
    subprocess.run(["git", "commit", "-m", commit_message], check=True)

    # Push to GitHub
    subprocess.run(["git", "push", "-u", "origin", "main"], check=True)
    log_message(f"✅ Code successfully uploaded to GitHub! (Version {version})")


# ---------------- TRACK VERSION CONTROL ---------------- #
def get_latest_version():
    """Gets the latest version number from the commit history."""
    try:
        output = subprocess.check_output(["git", "log", "--pretty=format:%s"], text=True)
        versions = [int(line.split("version")[-1]) for line in output.split("\n") if "version" in line]
        return max(versions) if versions else 0
    except Exception:
        return 0  # No previous versions found


# ---------------- MAIN EXECUTION ---------------- #
try:
    log_message("🚀 Starting GitHub upload automation...")

    # Step 1: Create a new repo if it doesn’t exist
    create_github_repo()

    # Step 2: Update environment variable
    update_env_variable()

    # Step 3: Upload code to GitHub
    git_setup_and_upload()

    log_message("🎉 Upload process completed successfully!")
except Exception as e:
    log_message(f"❌ ERROR: Unexpected error: {e}")
