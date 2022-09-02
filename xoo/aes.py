import os

# pip install pycryptodome
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

from xoo.settings import XOO_AES_KEY

block_size = 32


def encrypt(text: str, key: str = XOO_AES_KEY, ) -> str:
    aes = AES.new(key.encode('utf-8'), AES.MODE_ECB)
    secure = aes.encrypt(pad(text.encode('utf-8'), block_size))
    return secure.hex()


def decrypt(secure: str, key: str = XOO_AES_KEY, ) -> str:
    aes = AES.new(key.encode('utf-8'), AES.MODE_ECB)
    text = unpad(aes.decrypt(bytes.fromhex(secure)), block_size)
    return text.decode('utf-8')


if __name__ == '__main__':
    tests = [
        '18888888888',
        '420325199909083355-xadfghjklqwex',
    ]
    for test in tests:
        x = encrypt(test)
        print(test, '->', x, len(x))
        y = decrypt(x)
        print(y)
    key = '物华天宝人杰地灵'
    print(decrypt(encrypt("老子服了这个老六", key), key))
