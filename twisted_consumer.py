# -*- coding:utf-8 -*-

import pika
from pika import exceptions
from pika.adapters import twisted_connection
from twisted.internet import defer, reactor, protocol,task


@defer.inlineCallbacks
def run(connection):

    channel = yield connection.channel()

    exchange = yield channel.exchange_declare(exchange='test_exchange',type='direct')

    queue = yield channel.queue_declare(queue='8031.level1', auto_delete=False, exclusive=False)

    yield channel.queue_bind(exchange='test_exchange',queue='8031.level1',routing_key='8031.level1')

    yield channel.basic_qos(prefetch_count=1)

    queue_object, consumer_tag = yield channel.basic_consume(queue='8031.level1',no_ack=False)

    l = task.LoopingCall(read, queue_object)

    l.start(0.01)


@defer.inlineCallbacks
def read(queue_object):

    ch,method,properties,body = yield queue_object.get()

    if body:
        print(body)

    yield ch.basic_ack(delivery_tag=method.delivery_tag)


parameters = pika.ConnectionParameters()
cc = protocol.ClientCreator(reactor, twisted_connection.TwistedProtocolConnection, parameters)
d = cc.connectTCP('192.168.99.100', 5672)
d.addCallback(lambda protocol: protocol.ready)
d.addCallback(run)
reactor.run()
