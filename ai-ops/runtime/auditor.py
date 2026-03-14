import json, os, pika
from .messaging import get_mq_conn, send_to_rocket
from .thread_manager import ThreadManager

def callback(ch, method, props, body):
    try:
        ctx = json.loads(body.decode()); tid = ctx['trace_id']
        tm = ThreadManager(); r = tm.r
        if r.get(f"status:{tid}") == "resolved" and not r.get(f"prompt_sent:{tid}"):
            prompt = "✅ **Sistema Estabilizado Técnico.**\nMarcelo, informe:\n1. O que foi feito?\n2. Como foi feito?\n3. Por quê foi feito?"
            send_to_rocket("auditor", prompt, tmid=tm.get_thread(tid))
            r.set(f"prompt_sent:{tid}", "true", ex=3600)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"[AUDITOR ERROR] {e}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

def run():
    conn = get_mq_conn(); ch = conn.channel()
    ch.queue_declare(queue='sre_audit', durable=True)
    ch.basic_consume(queue='sre_audit', on_message_callback=callback)
    ch.start_consuming()

if __name__ == "__main__":
    run()
