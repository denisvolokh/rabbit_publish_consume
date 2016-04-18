#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='192.168.99.100'))
channel = connection.channel()

#channel.exchange_declare(exchange='test_exchange',
#                         type='fanout')

result1 = channel.queue_declare(exclusive=True)
queue_name1 = result1.method.queue

channel.queue_bind(exchange='test_exchange#1',
                   queue=queue_name1)

result2 = channel.queue_declare(exclusive=True)
queue_name2 = result2.method.queue

channel.queue_bind(exchange='test_exchange#2',
                   queue=queue_name2)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %r" % body)
    ch.basic_ack(method.delivery_tag)

channel.basic_consume(callback,
                      queue=queue_name1,
                      no_ack=False)

channel.basic_consume(callback,
                      queue=queue_name2,
                      no_ack=False)

channel.start_consuming()