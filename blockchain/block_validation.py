import binascii

from Crypto.PublicKey import RSA
from traitlets.traitlets import Bool
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
    print(f"Хеши или подписи всего блокчейна не верны. Индекс первого блока с неверным хешом или подписью: {invalid_block_index}")