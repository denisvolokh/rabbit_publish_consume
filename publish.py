__author__ = 'barmalei4ik'

import pika
import time

parameters = pika.URLParameters('amqp://guest:guest@192.168.99.100:5672/%2F')

connection = pika.BlockingConnection(parameters)

channel = connection.channel()

channel.exchange_declare(exchange='test_exchange',
                         type='fanout')

for x in range(0, 100000):
    print x
    channel.publish(exchange="test_exchange",
                    routing_key="8031.level1",
                    body='message body value ' + str(x))
    #channel.basic_publish('test_exchange',
    #                      'test_routing_key',
    #                      'message body value ' + str(x))
    time.sleep(.001)

connection.close()