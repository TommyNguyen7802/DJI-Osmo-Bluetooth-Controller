import os
import json
import paramiko

LOG_FILE = "transfer_log.txt"

def load_log():
    """Create log file if it doesn't exist."""
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            f.write("")
        print(f"Created new log file: {LOG_FILE}")
    """Load list of previously transferred files."""
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            return set(line.strip() for line in f if line.strip())
    return set()

def update_log(filename):
    """Append a new filename to the log."""
    with open(LOG_FILE, "a") as f:
        f.write(filename + "\n")

def transfer_new_videos():
    # Load configuration
    with open("config.json") as f:
        cfg = json.load(f)

    hostname = cfg["host"]
    port = cfg["port"]
    username = cfg["user"]
    password = cfg["password"]
    local_dir = cfg["local_dir"]
    remote_dir = cfg["remote_dir"]
    print(f"{local_dir}")
    # Load log of already transferred files
    transferred = load_log()

    # Connect to server
    with paramiko.SSHClient() as client:
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, port, username, password)
        sftp = client.open_sftp()

        # Iterate over files in local_dir
        for filename in os.listdir(local_dir):
            local_path = os.path.join(local_dir, filename)
            remote_path = os.path.join(remote_dir, filename)

            # Skip if already transferred or not a file
            if filename in transferred or not os.path.isfile(local_path):
                continue

            sftp.put(local_path, remote_path)
            print(f"Uploaded: {local_path} → {remote_path}")

            update_log(filename)

        print("\nFiles on server:")
        files = sftp.listdir(remote_dir)
        for f in files:
            print("-", f)

        sftp.close()
