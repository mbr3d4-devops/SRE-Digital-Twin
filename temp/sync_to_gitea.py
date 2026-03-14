import os
import base64
import json
import urllib.request
import urllib.error
import urllib.parse

# Gitea Configuration
GITEA_URL = "http://localhost:3000/api/v1"
GITEA_USER = "marcelo"
GITEA_PASS = "password123"
REPO = "target-app-infra"
BACKUP_DIR = "/home/marcelo/Documentos/projeto Digital Twin/temp"
GITEA_DEST_PATH = "project-backups"

AUTH = base64.b64encode(f"{GITEA_USER}:{GITEA_PASS}".encode()).decode()

def gitea_request(method, path, body=None):
    # Ensure path is properly formatted (no leading slash)
    path = path.lstrip("/")
    # URL encode the path to handle spaces and special characters
    encoded_path = urllib.parse.quote(path)
    url = f"{GITEA_URL}/repos/{GITEA_USER}/{REPO}/contents/{encoded_path}"
    headers = {
        "Authorization": f"Basic {AUTH}",
        "Content-Type": "application/json",
        "accept": "application/json"
    }
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req) as res:
            return res.status, json.loads(res.read().decode())
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read().decode())
        except:
            return e.code, str(e)
    except Exception as e:
        return 500, str(e)

def sync():
    if not os.path.exists(BACKUP_DIR):
        print(f"Error: {BACKUP_DIR} not found.")
        return

    # Walk through the backup directory recursively
    for root, dirs, files in os.walk(BACKUP_DIR):
        for filename in files:
            local_path = os.path.join(root, filename)
            
            # Calculate the relative path from BACKUP_DIR to the file
            rel_path = os.path.relpath(local_path, BACKUP_DIR)
            gitea_path = os.path.join(GITEA_DEST_PATH, rel_path)
            
            try:
                with open(local_path, "rb") as f:
                    content = base64.b64encode(f.read()).decode()
            except Exception as e:
                print(f"Failed to read {local_path}: {e}")
                continue
            
            print(f"Syncing {rel_path} to Gitea...")
            
            # Check if file exists to get SHA
            status, info = gitea_request("GET", gitea_path)
            
            body = {
                "content": content,
                "message": f"Backup auto-sync: {rel_path}",
                "branch": "main"
            }
            
            if status == 200:
                # Update
                body["sha"] = info["sha"]
                u_status, u_info = gitea_request("PUT", gitea_path, body)
                if u_status in [200, 201]:
                    print(f"✅ Updated {rel_path}")
                else:
                    print(f"❌ Failed to update {rel_path}: {u_info}")
            else:
                # Create
                c_status, c_info = gitea_request("POST", gitea_path, body)
                if c_status in [200, 201]:
                    print(f"✅ Created {rel_path}")
                else:
                    print(f"❌ Failed to create {rel_path}: {c_info}")

if __name__ == "__main__":
    sync()
