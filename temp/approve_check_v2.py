import psycopg2, urllib.request, time, json, base64, sys

print('STARTING APPROVAL CHECKER', flush=True)

# 1. Fetch Action ID
action_id = None
try:
    conn = psycopg2.connect(host='postgres-db.ai-ops.svc.cluster.local', port=5432, dbname='incidents', user='user', password='pass')
    cur = conn.cursor()
    cur.execute("SELECT action_id FROM incident_logs WHERE status='pending' ORDER BY created_at DESC LIMIT 1;")
    row = cur.fetchone()
    if row: action_id = row[0]
    cur.close(); conn.close()
except Exception as e:
    print('DB Error:', e, flush=True)

if not action_id:
    print('NO PENDING ACTION ID FOUND', flush=True)
else:
    print('APPROVING ACTION:', action_id, flush=True)
    # 2. Approve Fix
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:9091/approve?id={action_id}") as r:
            print('APPROVE STATUS:', r.getcode(), flush=True)
    except Exception as e:
        print('APPROVE ERROR:', e, flush=True)

    print('WAITING 25s for Archivist background thread (LLM generation + Gitea Upload)...', flush=True)
    time.sleep(25)

    # 3. Check Gitea
    print('GITEA POSTMORTEMS:', flush=True)
    url = 'http://gitea-http.gitops.svc.cluster.local:3000/api/v1/repos/marcelo/target-app-infra/contents/postmortems'
    creds = base64.b64encode(b'marcelo:password123').decode()
    try:
        import ssl
        ctx = ssl._create_unverified_context()
        req = urllib.request.Request(url, headers={'Authorization': 'Basic ' + creds})
        with urllib.request.urlopen(req, context=ctx) as r:
            files = json.loads(r.read().decode())
            for f in files: print(' - ' + f['path'] + ' (' + f['type'] + ')', flush=True)
    except Exception as e:
        print('GITEA FETCH ERROR:', e, flush=True)
