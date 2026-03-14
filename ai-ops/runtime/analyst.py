import json, os, pika
from .messaging import get_mq_conn, send_to_rocket
from .thread_manager import ThreadManager
from .llm_gateway import call_llm
from ..evidence_engine.normalizer import package_evidence
from ..renderer.forensic_markdown import render

def callback(ch, method, props, body):
    try:
        ctx = json.loads(body.decode())
        tid = ctx.get('trace_id', 'unknown')
        tm = ThreadManager()
        tmid = ctx.get('thread_id') or tm.get_thread(tid)
        
        alert_raw = tm.get_evidence(tid)
        alert = json.loads(alert_raw)
        labels = alert.get('labels', {})
        pod, ns = labels.get('pod', 'N/A'), labels.get('namespace', 'default')
        
        # Operational: Evidence Collection
        enriched = package_evidence(pod, ns)
        
        # Cognitive: Reasoning
        input_data = f"ALERTA: {alert_raw}\n\nEVIDENCIAS ENRIQUECIDAS:\n{enriched}"
        raw_ai = call_llm("analyst", input_data, trace_id=tid)
        
        # UI: Rendering
        try:
            data = json.loads(raw_ai)
            laudo = render(data)
        except:
            laudo = raw_ai
        
        send_to_rocket("analyst", laudo, tmid=tmid)
        tm.save_analysis(tid, laudo)
        
        # Next Step: Warden
        conn = get_mq_conn(); ch_out = conn.channel()
        ch_out.queue_declare(queue='sre_warden', durable=True)
        ch_out.basic_publish(exchange='', routing_key='sre_warden', body=json.dumps(ctx))
        conn.close()
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"[ANALYST ERROR] {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

def run():
    conn = get_mq_conn(); ch = conn.channel()
    ch.queue_declare(queue='sre_tasks', durable=True)
    ch.basic_consume(queue='sre_tasks', on_message_callback=callback)
    ch.start_consuming()

if __name__ == "__main__":
    run()
