import json, os, urllib.request, base64, ssl, redis, pika, yaml, re, time
def get_redis():
    return redis.Redis(host=os.environ.get("REDIS_HOST", "redis-state"), port=6379, decode_responses=True)
def mq_publish(ch, q, msg):
    ch.queue_declare(queue=q, durable=True)
    ch.basic_publish(exchange='', routing_key=q, body=json.dumps(msg))
def clean_analyst_output(text):
    \"\"\"Garante layout de Março: Corta introduções e remove 'Thinking'.\"\"\"
    if "🔍" in text:
        text = text[text.find("🔍"):]
    text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    noise = ["Analyze", "Input", "Task", "Evaluate", "Internal Monologue"]
    lines = [l for l in text.split('\n') if not any(n in l for n in noise)]
    return "\n".join(lines).strip()
