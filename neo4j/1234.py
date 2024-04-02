import uuid


for i in range(10000):
    print(i, uuid.uuid1(), sep=',')