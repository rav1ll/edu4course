import math
import random
import json
from Crypto.Signature import pkcs1_15
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
import binascii
import base64
import requests
import sys

def int_to_byte_array(value):
    return [
        (value >> 24) & 0xFF,
        (value >> 16) & 0xFF,
        (value >> 8) & 0xFF,
        value & 0xFF
    ]

def count_nonce(prevhash, data, sign):
    n = int('1' * 244, 2)
    mh = n + 1
    number = 0
    while mh >= n:

        # print(result)

        my_hasher = SHA256.new()
        my_hasher.update(bytearray(prevhash, 'utf-8') +
                         bytearray(str(data), 'utf-8') +
                         bytearray(sign, 'utf-8') +
                         number.to_bytes(4, sys.byteorder))

        mh = int(my_hasher.hexdigest(), 16)

        number += 1
    return number

def count_bitcoin():
    while True:
        with open("test_data_1000.csv", "r") as file:
            y_sum = 0
            for line in file:
                x1, x2, y = line.split(";")

                x1 = float(x1)
                x2 = float(x2)
                y = float(y)

                w11 = generate_random()
                w21 = generate_random()
                h11 = (count_func(x1 * w11 + x2 * w21))

                w12 = generate_random()
                w22 = generate_random()
                h12 = (count_func(x1 * w12 + x2 * w22))

                v11 = generate_random()
                v21 = generate_random()
                h21 = (count_func(h11 * v11 + h12 * v21))

                v12 = generate_random()
                v22 = generate_random()
                h22 = (count_func(h11 * v12 + h12 * v22))

                v13 = generate_random()
                v23 = generate_random()
                h23 = (count_func(h11 * v13 + h12 * v23))

                w1 = generate_random()
                w2 = generate_random()
                w3 = generate_random()
                y_ = (count_func(h21 * w1 + h22 * w2 + h23 * w3))

                y_sum += (y_ - y)**2

                f_private = open('public.key.hex', 'r')
                privkey = f_private.read()

            y_sum = round(y_sum, 11)
            if y_sum <= 0.4:
                var = {"w11": str(w11), "w12": str(w12), "w21": str(w21), "w22": str(w22),
                       "v11": str(v11), "v12": str(v12), "v13": str(v13), "v21": str(v21), "v22": str(v22), "v23": str(v23),
                       "w1": str(w1), "w2": str(w2), "w3": str(w3), "e": str(y_sum), "publickey": privkey}
                with open("optima", "w") as optima:
                    optima.write(str(var))
                return var

def creaete_key():
    key = RSA.generate(1024)
    privk = key.export_key('DER', pkcs=8)
    pubk = key.publickey().export_key('DER', pkcs=8)

    #print('private_hex=' + str(binascii.hexlify(privk)))
    #print('public_hex=' + str(binascii.hexlify(pubk)))

    # save private key as hex
    f_private = open('private.key.hex', 'wb')
    f_private.write(binascii.hexlify(privk))
    f_private.close()

    # save public key as hex
    f_public = open('public.key.hex', 'wb')
    f_public.write(binascii.hexlify(pubk))
    f_public.close()

def send_json():
    f_private = open('private.key.hex', 'r')
    keystr = binascii.unhexlify(f_private.read())
    key = RSA.import_key(keystr)

    signer = pkcs1_15.new(key)

    data = requests.get('http://itislabs.ru/nbc/chain').json()
    data = data[-1]

    prevhash = SHA256.new(
        bytes.fromhex(data['prevhash']) + json.dumps(data['data'], separators=(',', ':')).encode()
        + bytes.fromhex(data['signature']) + data['nonce'].to_bytes(4, byteorder='big')
    ).hexdigest()

    var = count_bitcoin()

    data_hasher = SHA256.new()
    data_hasher.update(bytearray(json.dumps(var, separators=(',', ':')).encode()))  # вычисляем хеш данных
    signed_data = signer.sign(data_hasher)  # подписываем полученный хеш от данных и фиксируем подпись
    signed_data = binascii.hexlify(signed_data).decode('utf-8')

    nonce = count_nonce(prevhash, var, signed_data)
    print(data['nonce'])
    print(nonce)


    block = {"prevhash": prevhash, "data": var, "signature": str(signed_data), "nonce": nonce}

    block_hash = SHA256.new(
        bytes.fromhex(block['prevhash']) + json.dumps(block['data'], separators=(',', ':')).encode()
        + bytes.fromhex(block['signature']) + block['nonce'].to_bytes(4, byteorder='big')
    ).hexdigest()

    while block_hash[:3] != '000' and block['nonce'] < 2 ** 32:
        block['nonce'] += 1
        block_hash = SHA256.new(
            bytes.fromhex(block['prevhash']) + json.dumps(block['data'], separators=(',', ':')).encode()
            + bytes.fromhex(block['signature']) + block['nonce'].to_bytes(4, byteorder='big')
        ).hexdigest()

    name_hasher = SHA256.new()
    name_hasher.update(bytearray(str("new string"), 'utf-8'))

    signed_name = signer.sign(name_hasher)
    signed_name = binascii.hexlify(signed_name).decode('utf-8')

    f_private = open('public.key.hex', 'r')
    privkey = f_private.read()

    block2 = {"autor": "Sussus amogus", "sign": signed_name, "publickey": privkey}

    result = requests.post("http://itislabs.ru/nbc/newblock/", json=block)
    print(result.text)
    result2 = requests.post('http://itislabs.ru/nbc/autor', json=block2)
    print(result2.text)

    print(block2)


def generate_random():
    return float(round(random.uniform(0, 0.3), 11))

def count_func(x):
    return 1/(1 + math.exp(-x))


#count_bitcoin()
creaete_key()
print(send_json())