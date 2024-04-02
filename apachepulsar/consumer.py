import pulsar
from clickhouse_driver import Client
import pulsar
from pulsar.schema import *
from pulsar.schema import AvroSchema


class InfoSchema3(Record):
    id = Integer()
    data = String()
    timestamp = String()


myschema5 = AvroSchema(InfoSchema3)
# Настройки подключения к Apache Pulsar
pulsar_client = pulsar.Client('pulsar://localhost:6650')
pulsar_consumer = pulsar_client.subscribe(topic='my_topic',
                                          schema=myschema5,
                                          subscription_name='my-subscription')

# Настройки подключения к ClickHouse
clickhouse_client = Client(host='localhost', port=8123)

# Цикл получения сообщений из Apache Pulsar и записи их в ClickHouse
clickhouse_client.execute(
    'CREATE TABLE my_table (message_id int, message_data varchar, message_timestamp  varchar) ENGINE = Memory')
#     'INSERT INTO pulsar_data (message_id, message_data, message_timestamp) '
#     'VALUES (%(message_id)s, %(message_data)s, %(message_timestamp)s)',
#     data
# )
pulsar_consumer.acknowledge()
# print(111111)
# except:
