import urllib.request, json, base64, ssl
print("=== Checking Gitea Post-Mortems ===")
url = 'http://gitea-http.gitops.svc.cluster.local:3000/api/v1/repos/marcelo/target-app-infra/contents/postmortems'
creds = base64.b64encode(b'marcelo:password123').decode()
ctx = ssl._create_unverified_context()
req = urllib.request.Request(url, headers={'Authorization': 'Basic ' + creds})
try:
    with urllib.request.urlopen(req, context=ctx) as r:
        if r.getcode() == 200:
            files = json.loads(r.read().decode())
            print("Files Found:")
            for f in files: print(" -", f['path'], f['type'])
        else:
            print("Unexpected DB Code:", r.getcode())
except Exception as e:
    err_body = ""
    try: err_body = e.read().decode()
    except: pass
    print("Error fetching from Gitea API:", e)
    if err_body: print("Response:", err_body)
