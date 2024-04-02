import pulsar
from pulsar.schema import *
from pulsar.schema import AvroSchema


class InfoSchema3(Record):
    id = Integer()
    data = String()
    timestamp = String()


myschema5 = AvroSchema(InfoSchema3)
client = pulsar.Client('pulsar://localhost:6650')

consumer = client.subscribe(topic='example-topic',
                            schema=myschema5,
                            subscription_name='subs')

while True:
    msg = consumer.receive()
    print(msg.value())

client.close()
