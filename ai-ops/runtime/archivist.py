import json, os, pika
from .messaging import get_mq_conn
from .thread_manager import ThreadManager

def callback(ch, method, props, body):
    try:
        tid = json.loads(body.decode())['trace_id']
        tm = ThreadManager()
        tm.r.set(f"archive:{tid}", body.decode(), ex=604800)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except: ch.basic_ack(delivery_tag=method.delivery_tag)

def run():
    conn = get_mq_conn(); ch = conn.channel()
    ch.queue_declare(queue='sre_archive', durable=True)
    ch.basic_consume(queue='sre_archive', on_message_callback=callback)
    ch.start_consuming()

if __name__ == "__main__":
    run()
