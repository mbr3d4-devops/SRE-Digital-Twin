import json
import urllib.request
import urllib.error
import time

# Configuration
RC_URL = "http://rocketchat.127.0.0.1.nip.io"
ADMIN_USER = "admin"
ADMIN_PASS = "sre-admin-2026"
CHANNELS = ["ops-warroom", "ops-security", "ops-history"]
OUTPUT_FILE = "/tmp/rocketchat_hooks.json"

def rc_request(path, method="GET", body=None, headers=None):
    if headers is None:
        headers = {}
    headers["Content-Type"] = "application/json"
    
    url = f"{RC_URL}{path}"
    data = json.dumps(body).encode() if body else None
    
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req) as res:
            return json.loads(res.read().decode())
    except urllib.error.HTTPError as e:
        try:
            return json.loads(e.read().decode())
        except:
            return {"status": "error", "message": str(e)}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def login():
    print(f"Logging in as {ADMIN_USER}...")
    res = rc_request("/api/v1/login", "POST", {"user": ADMIN_USER, "password": ADMIN_PASS})
    if res.get("status") == "success":
        data = res.get("data", {})
        return data.get("authToken"), data.get("userId")
    else:
        print(f"Login failed: {res.get('message')}")
        return None, None

def create_channel(name, token, user_id):
    headers = {"X-Auth-Token": token, "X-User-Id": user_id}
    print(f"Checking/Creating channel #{name}...")
    
    # Check if exists
    res = rc_request(f"/api/v1/channels.info?roomName={name}", "GET", headers=headers)
    if res.get("success"):
        print(f"Channel #{name} already exists.")
        return res["channel"]["_id"]
    
    # Create
    res = rc_request("/api/v1/channels.create", "POST", {"name": name}, headers=headers)
    if res.get("success"):
        print(f"Channel #{name} created.")
        return res["channel"]["_id"]
    else:
        print(f"Failed to create channel #{name}: {res.get('error')}")
        return None

def main():
    token, user_id = login()
    if not token:
        return

    # Ensure channels exist
    for name in CHANNELS:
        create_channel(name, token, user_id)
        
    # Export Credentials for Orchestrator (keeping filename for backwards compatibility)
    creds = {
        "RC_TOKEN": token,
        "RC_USER_ID": user_id
    }
    
    with open(OUTPUT_FILE, "w") as f:
        json.dump(creds, f, indent=2)
    print(f"Success! API Credentials saved to {OUTPUT_FILE}")
    print(json.dumps(creds, indent=2))

if __name__ == "__main__":
    # Give RC a moment to settle if just restarted
    time.sleep(2)
    main()
