import time
import pika
import sys

from controls import Controller

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='logs', exchange_type='fanout')

result_queue = channel.queue_declare(queue='', exclusive=True)
queue_name = result_queue.method.queue
channel.queue_bind(exchange='logs', queue=queue_name)
try:
    type_m = str(sys.argv[1]).lower()
except Exception:
    type_m = 'debug'

types = ['debug', 'info', 'warning', 'error']
if type_m == 'info':
    types = types[1:]
elif type_m == 'warning':
    types = types[2:]
elif type_m == 'error':
    types = types[3]
else:
    pass


def callback(ch, method, properties, body):
    body = eval(body.decode())
    if body['type'] in types:
        print("{} - {}\n".format(time.ctime(), body['message']))
        Controller.create_or_update(body['type'], body['message'])
        Controller.send_email(body['type'], body['message'])
        print(" [X] Email sent")
    else:
        print("Accion no permitida")
    print('[x] Received')
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print("-------------------------------------------------------------------------")


channel.basic_consume(queue=queue_name, on_message_callback=callback)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
