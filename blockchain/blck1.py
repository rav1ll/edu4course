from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
import binascii
from Crypto.Signature import pkcs1_15
import time
import requests
import json
from traitlets.traitlets import Bool

# загружаем приватный ключ
f_private = open('private.key.hex', 'r')
keystr = binascii.unhexlify(f_private.read())
key = RSA.import_key(keystr)
print(key.publickey().exportKey)
# initialize library by public key
signer = pkcs1_15.new(key)


class Block:
    def __init__(self, index, data, previous_hash):
        self.index = index
        self.timestamp = time.time()
        self.data = data
        self.previous_hash = previous_hash
        self.data_signature = self.sign_data()
        self.hash = self.calculate_hash()
        self.arbiter_signature, self.ts = self.sign_by_arbiter()

    def calculate_hash(self):
        sha = SHA256.new()
        sha.update((str(self.index) + str(self.timestamp) + str(self.data) + str(self.data_signature) + str(
            self.previous_hash)).encode('utf-8'))
        return sha.hexdigest()

    def sign_data(self):
        with open('private.key.hex', 'rb') as f_private:
            private_key_hex = binascii.unhexlify(f_private.read())
            private_key = RSA.import_key(private_key_hex)
        data = (str(self.index) + str(self.data)).encode('utf-8')
        signature = pkcs1_15.new(private_key).sign(SHA256.new(data))
        return signature

    def sign_by_arbiter(self):
        json = requests.get('http://itislabs.ru/ts?digest=' + self.hash).json()
        print(json)
        sign = bytes.fromhex(json['timeStampToken']['signature'])
        ts = (json['timeStampToken']['ts'])
        print(ts)

        return sign, ts

    def validate_block_hash(self):
        data = (str(self.index) + str(self.timestamp) + str(self.data) + str(self.data_signature) + str(
            self.previous_hash)).encode('utf-8')
        calculated_hash = SHA256.new(data).hexdigest()
        return self.hash == calculated_hash

    def validate_block_signature(self, public_key):
        data = (str(self.index) + str(self.data)).encode('utf-8')
        h = SHA256.new(data)
        try:
            pkcs1_15.new(public_key).verify(h, self.data_signature)
            return True
        except (ValueError, TypeError):
            return False

    def validate_block(self):
        r = requests.get('http://itislabs.ru/ts/public')
        arbiter_public = r.content

        sha = SHA256.new()

        keystr = binascii.unhexlify(arbiter_public)
        key = RSA.import_key(keystr)
        signer = pkcs1_15.new(key)

        token = self.ts.encode('utf-8') + binascii.unhexlify(self.calculate_hash())
        sha.update(token)

        try:
            signer.verify(sha, self.arbiter_signature)
            print('подпись действительна')
        except ValueError:
            pass

    @staticmethod
    def validate_chain(blockchain, public_key):
        for i in range(1, len(blockchain)):
            if not blockchain[i].validate_block_hash():
                return False, blockchain[i].index
            if not blockchain[i].validate_block_signature(public_key):
                return False, blockchain[i].index
            if blockchain[i].previous_hash != blockchain[i - 1].hash:
                return False, blockchain[i].index
        return True, None


def create_genesis_block():
    return Block(0, "Genesis Block", "0")


def create_new_block(previous_block, data):
    index = previous_block.index + 1
    new_block = Block(index, data, previous_block.hash)

    return new_block


def get_block_info(index, blockchain):
    if 0 <= index < len(blockchain):
        block = blockchain[index]
        print(f"Информация в блоке #{block.index}:")
        print(f"Хеш: {block.hash}")
        print(f"Предыдущий Хеш: {block.previous_hash}")
        print(f"Данные: {block.data}")
        print(f"Временная метка: {block.timestamp}")
    else:
        print("Блок с указанным индексом не найден в блокчейне.")


def create_blockchain():
    blockchain = [create_genesis_block()]
    previous_block = blockchain[0]

    return blockchain, previous_block


def add_blocks(blockchain, previous_block):
    num_blocks_to_add = int(input("Введите количество блоков, которые вы хотите добавить: "))

    for i in range(num_blocks_to_add):
        data = input("Введите данные для блока #" + str(i + 1) + ": ")
        new_block = create_new_block(previous_block, data)
        blockchain.append(new_block)
        previous_block = new_block
        print(f"Блок #{new_block.index} добавлен в блокчейн!")
        print(f"Хеш блока: {new_block.hash}\n")


def watch_block(blockchain):
    block_index = int(input("Введите индекс блока, который вы хотите просмотреть: "))
    get_block_info(block_index, blockchain)
    return block_index


def write_blockchain():
    create = create_blockchain()
    previous_block = create[1]
    blockchain = create[0]

    add_blocks(blockchain, previous_block)

    block_index = watch_block(blockchain)
    blockchain[block_index].arbiter_signature

    blockchain[block_index].validate_block()

    validate(blockchain)

    blocks = []
    for i in range(len(blockchain)):
        block = blockchain[i]

        blocks.append({'index': block.index,
                       'hash': block.hash,
                       'prev_hash': block.previous_hash,
                       'block_data': block.data,
                       'timestamp': block.timestamp})

    with open("blockchain.json", "w") as file:
        # Записываем отформатированный словарь в файл в формате JSON
        json.dump(blocks, file)


def main():
    param = int(input())
    if param == 1:
        write_blockchain()
    else:
        with open("blockchain.json", "r") as file:
            # Записываем отформатированный словарь в файл в формате JSON
            json_str = file.read()
        my_dict = json.loads(json_str)

        for item in my_dict:
            index = item['index']
            hash = item['hash']
            prev_hash = item['prev_hash']
            block_data = item['block_data']
            timestamp = item['timestamp']
            new_block = Block(index, block_data, prev_hash)
            new_block.timestamp = timestamp
            new_block.hash = hash
            if index == 0:
                blockchain = []

            blockchain.append(new_block)

        print(blockchain)

        block_index = watch_block(blockchain)

        blockchain[block_index].validate_block()

        validate(blockchain)


def validate(blockchain):
    with open('public.key.hex', 'rb') as f_public:
        public_key_hex = binascii.unhexlify(f_public.read())
        public_key = RSA.import_key(public_key_hex)

    block_to_validate_index = int(input("Введите индекс блока, который нужно провалидировать: "))
    if 0 <= block_to_validate_index < len(blockchain):
        block_to_validate = blockchain[block_to_validate_index]
        is_block_hash_valid = block_to_validate.validate_block_hash()
        is_block_signature_valid = block_to_validate.validate_block_signature(public_key)
        if not is_block_hash_valid:
            print("Хэш неверен")
        if is_block_hash_valid and is_block_signature_valid:
            print("Хеш и подпись блока верны.")
        else:
            print("Хеш или подпись блока не верны.")
    else:
        print("Блок с указанным индексом не найден в блокчейне.")

    is_blockchain_valid, invalid_block_index = Block.validate_chain(blockchain, public_key)

    if is_blockchain_valid:
        print("Хеши и подписи всего блокчейна верны.")
    else:
        print(
            f"Хеши или подписи всего блокчейна не верны. Индекс первого блока с неверным хешом или подписью: {invalid_block_index}")


if __name__ == "__main__":
    main()
