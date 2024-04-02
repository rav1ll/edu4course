import pulsar
from pulsar.schema import *
from pulsar.schema import AvroSchema


class InfoSchema3(Record):
    id = Integer()
    data = String()
    timestamp = String()


myschema5 = AvroSchema(InfoSchema3)
client = pulsar.Client('pulsar://localhost:6650')

producer2 = client.create_producer(topic='my_topic',
                                   schema=myschema5,
                                   producer_name='my-subscription')

info_record2 = InfoSchema3()

info_record2.id = 12
info_record2.data = 'my message data'
info_record2.timestamp = '12381232731'
producer2.send(info_record2)
client.close()
