from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
import binascii
from Crypto.Signature import pkcs1_15

# генерация ключей в DER формате
key = RSA.generate(1024)
privk = key.export_key('DER', pkcs=8)
pubk = key.publickey().export_key('DER', pkcs=8)

# сохраним их в HEX представлении бинарных данных
print('private_hex=' + str(binascii.hexlify(privk)))
print('public_hex=' + str(binascii.hexlify(pubk)))

# приватный hex ключ
f_private = open('private.key.hex', 'wb')
f_private.write(binascii.hexlify(privk))
f_private.close()

# публичный hex ключ
f_public = open('public.key.hex', 'wb')
f_public.write(binascii.hexlify(pubk))
f_public.close()
