import redis, os

def get_redis():
    return redis.Redis(host=os.environ.get("REDIS_HOST", "redis-state"), port=6379, decode_responses=True)

class ThreadManager:
    def __init__(self):
        self.r = get_redis()
    
    def set_thread(self, tid, tmid):
        self.r.set(f"tmid:{tid}", tmid, ex=86400)
    
    def get_thread(self, tid):
        return self.r.get(f"tmid:{tid}")
    
    def save_evidence(self, tid, evidence):
        self.r.set(f"evidence:{tid}", evidence, ex=3600)
    
    def get_evidence(self, tid):
        return self.r.get(f"evidence:{tid}") or "{}"

    def save_analysis(self, tid, laudo):
        self.r.set(f"analysis:{tid}", laudo, ex=3600)
    
    def get_analysis(self, tid):
        return self.r.get(f"analysis:{tid}") or "Sem laudo."
