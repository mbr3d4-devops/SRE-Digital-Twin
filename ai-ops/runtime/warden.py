import json, os, pika
from .messaging import get_mq_conn, send_to_rocket
from .thread_manager import ThreadManager
from .llm_gateway import call_llm

def callback(ch, method, props, body):
    try:
        ctx = json.loads(body.decode())
        tid = ctx['trace_id']
        tm = ThreadManager()
        tmid = tm.get_thread(tid)
        analise = tm.get_analysis(tid)
        
        raw_ai = call_llm("warden", f"ANALISE: {analise}", trace_id=tid)
        
        try:
            data = json.loads(raw_ai)
            veredito = data.get('veredito', 'REPROVADO').upper()
            justificativa = data.get('justificativa', raw_ai)
        except:
            veredito = "REPROVADO"
            justificativa = raw_ai
        
        send_to_rocket("warden", justificativa, tmid=tmid)
        
        if veredito == "REPROVADO":
            ch.basic_ack(delivery_tag=method.delivery_tag); return
        
        conn = get_mq_conn(); ch_out = conn.channel()
        ch_out.queue_declare(queue='sre_audit', durable=True)
        ch_out.basic_publish(exchange='', routing_key='sre_audit', body=json.dumps(ctx))
        conn.close()
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"[WARDEN ERROR] {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

def run():
    conn = get_mq_conn(); ch = conn.channel()
    ch.queue_declare(queue='sre_warden', durable=True)
    ch.basic_consume(queue='sre_warden', on_message_callback=callback)
    ch.start_consuming()

if __name__ == "__main__":
    run()
