import pika
import sys
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='logs', exchange_type='fanout')

command = {'type': str(sys.argv[1]).lower(), 'message': ' '.join(sys.argv[2:])}

channel.basic_publish(exchange='logs', routing_key='', body=json.dumps(command))

print("[X] Sent")

connection.close()
