import os
import requests
import subprocess
import time

# Configuration
LOCAL_REPO_PATH = r"C:\Users\Ramesh1\PycharmProjects\PythonProject2\5G_RAN_Test_Project"
NEW_REPO_NAME = "5G_RAN_Test_Automation"  # Change repo name if needed

# Get GitHub credentials from environment variables
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if not all([GITHUB_USERNAME, GITHUB_TOKEN]):
    raise ValueError("Missing required environment variables. Set GITHUB_USERNAME and GITHUB_TOKEN.")

# Define GitHub API URLs
repo_api_url = f"https://api.github.com/user/repos"
repo_check_url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{NEW_REPO_NAME}"
git_repo_url = f"https://{GITHUB_USERNAME}:{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{NEW_REPO_NAME}.git"

# Step 1: Check if the GitHub repository exists
response = requests.get(repo_check_url, auth=(GITHUB_USERNAME, GITHUB_TOKEN))

if response.status_code == 200:
    print(f"✅ Repository '{NEW_REPO_NAME}' already exists. Proceeding with upload.")
elif response.status_code == 404:
    # Step 2: Create the repository if it doesn't exist
    print(f"🚀 Creating new GitHub repository: {NEW_REPO_NAME}...")
    repo_data = {"name": NEW_REPO_NAME, "private": False}  # Set to True for private repo
    create_response = requests.post(repo_api_url, json=repo_data, auth=(GITHUB_USERNAME, GITHUB_TOKEN))

    if create_response.status_code == 201:
        print("✅ Repository created successfully!")
        time.sleep(5)  # Give GitHub time to create the repo
    else:
        print(f"❌ Failed to create repository: {create_response.json()}")
        exit(1)
else:
    print(f"❌ Error checking repository: {response.json()}")
    exit(1)

# Step 3: Update Environment Variable with the new repository name
env_var_command = f'setx GITHUB_REPO "{NEW_REPO_NAME}"'
subprocess.run(env_var_command, shell=True, check=True)
print(f"✅ Updated environment variable: GITHUB_REPO={NEW_REPO_NAME}")

# Step 4: Navigate to the local project directory
if not os.path.exists(LOCAL_REPO_PATH):
    print(f"❌ Error: Local repository path '{LOCAL_REPO_PATH}' does not exist.")
    exit(1)

os.chdir(LOCAL_REPO_PATH)

# Step 5: Initialize Git (if not already initialized)
if not os.path.exists(os.path.join(LOCAL_REPO_PATH, ".git")):
    print("🔧 Initializing local Git repository...")
    subprocess.run(["git", "init"], check=True)
    subprocess.run(["git", "remote", "add", "origin", git_repo_url], check=True)
else:
    # Ensure correct remote origin
    subprocess.run(["git", "remote", "set-url", "origin", git_repo_url], check=True)

# Step 6: Pull latest changes (if repo is not empty)
try:
    subprocess.run(["git", "fetch", "origin"], check=True)
    subprocess.run(["git", "pull", "origin", "main", "--allow-unrelated-histories"], check=True)
except subprocess.CalledProcessError:
    print("ℹ️ First-time upload, no previous commits found.")

# Step 7: Add, Commit, and Push changes
print("📤 Uploading files to GitHub...")
subprocess.run(["git", "add", "."], check=True)
commit_message = f"Automated upload: version {len(os.listdir(LOCAL_REPO_PATH))}"
subprocess.run(["git", "commit", "-m", commit_message], check=True)
subprocess.run(["git", "branch", "-M", "main"], check=True)
subprocess.run(["git", "push", "-u", "origin", "main"], check=True)

print("✅ Code successfully uploaded to GitHub!")
