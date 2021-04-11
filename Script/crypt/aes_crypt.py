import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


class AesCrypt:
    def __init__(self, model, iv, encode_, key='abcdefghijklmnop'):
        self.encrypt_text = ''
        self.decrypt_text = ''

        self.encode_ = encode_

        self.key = self.add_16(key)
        self.iv = self.add_16(iv)
        self.model = {'ECB': AES.MODE_ECB, 'CBC': AES.MODE_CBC}[model]

        if model == 'ECB':
            self.aes = AES.new(self.key, self.model)  # Create an aes object
        elif model == 'CBC':
            self.aes = AES.new(self.key, self.model, self.iv)  # Create an aes object

    # Here the key length must be 16, 24 or 32, and the current 16-bit is enough.
    def add_16(self, par):
        par = par.encode(self.encode_)
        while len(par) % 16 != 0:
            par += b'\x00'
        return par

    # encryption
    def aes_encrypt(self, text):
        text = pad(text.encode('utf-8'), AES.block_size, style='pkcs7')
        self.encrypt_text = self.aes.encrypt(text)
        return base64.encodebytes(self.encrypt_text).decode().strip()

    # Decrypt
    def aes_decrypt(self, text):
        text = base64.b64decode(text)

        pt = unpad(self.aes.decrypt(text), AES.block_size)
        result = pt.decode("utf-8")

        return result


def aes_ecb_decrypt(text, key):
    try:
        text = base64.b64decode(text)
        key = key.encode("utf-8")

        while len(key) % 16 != 0:
            key += b'\x00'

        cipher = AES.new(key, AES.MODE_ECB)

        # AES.block_size = 16
        pt = unpad(cipher.decrypt(text), AES.block_size)
        result = pt.decode("utf-8")

        return result

    except ValueError as error:
        print("Incorrect Decryption: ", error)


def aes_ecb_encrypt(text, key):
    text = text.encode('utf-8')
    key = key.encode("utf-8")

    while len(key) % 16 != 0:
        key += b'\x00'

    cipher = AES.new(key, AES.MODE_ECB)

    ct_bytes = cipher.encrypt(pad(text, AES.block_size, style='pkcs7'))

    return base64.encodebytes(ct_bytes).decode().strip()


def aes_cbc_encrypt(text, key, iv):
    text = text.encode('utf-8')
    key = key.encode("utf-8")
    iv = iv.encode("utf-8")

    while len(key) % 16 != 0:
        key += b'\x00'

    while len(iv) % 16 != 0:
        iv += b'\x00'

    cipher = AES.new(key, AES.MODE_CBC, iv)

    ct_bytes = cipher.encrypt(pad(text, AES.block_size, style='pkcs7'))

    return base64.encodebytes(ct_bytes).decode().strip()


def aes_cbc_decrypt(text, key, iv):
    try:
        text = base64.b64decode(text)
        key = key.encode("utf-8")
        iv = iv.encode("utf-8")

        while len(key) % 16 != 0:
            key += b'\x00'

        while len(iv) % 16 != 0:
            iv += b'\x00'

        cipher = AES.new(key, AES.MODE_CBC, iv)

        # AES.block_size = 16
        pt = unpad(cipher.decrypt(text), AES.block_size)
        result = pt.decode("utf-8")

        return result

    except ValueError as error:
        print("Incorrect Decryption: ", error)


if __name__ == '__main__':
    # Class
    # AesCrypt Encrypt Example
    pr_ecb_c_e = AesCrypt('ECB', '', 'utf-8', 'abcdefghijklmnop')
    en_text = pr_ecb_c_e.aes_encrypt('123456789012345678901234567890')
    print('Class ECB Encrypt:', en_text)

    # AesCrypt Decrypt Example
    pr_ecb_c_d = AesCrypt('ECB', '', 'utf-8', 'abcdefghijklmnop')
    print('Class ECB Decrypt:', pr_ecb_c_d.aes_decrypt('M3q3c85LGdEj9k8iep/J16MmxhIQ7wDgXDKgcCr08Oc='))

    # AesCrypt Encrypt Example
    pr_cbc_c_e = AesCrypt('CBC', 'I8zyA4lVhMCaJ5Kg', 'utf-8', 'abcdefghijklmnop')
    en_text = pr_cbc_c_e.aes_encrypt('123456789012345678901234567890')
    print('Class CBC Encrypt:', en_text)

    # AesCrypt Decrypt Example
    pr_cbc_c_d = AesCrypt('CBC', 'I8zyA4lVhMCaJ5Kg', 'utf-8', 'abcdefghijklmnop')
    print('Class CBC Decrypt:', pr_cbc_c_d.aes_decrypt('6EZbi8MbHrcmEysaR1WqJX+R7ZlBWzL81AEZTsklfw0='))

    # Other
    # Decrypt Class - ECB
    pr_ecb = AesCrypt('ECB', '', 'utf-8', '1234567890123456')
    print('Web ECB Decrypt: ', pr_ecb.aes_decrypt('q6V+tjd/797mQueer75thw=='))

    # Decrypt Class - CBC
    pr_cbc = AesCrypt('CBC', 'I8zyA4lVhMCaJ5Kg', 'utf-8', '1234567890123456')
    print('Web CBC Decrypt: ', pr_cbc.aes_decrypt('TsCmO9Eg+uK8o+8b0keySQ=='))

    # Method
    # Encrypt Method - ECB
    print("Method ECB Encrypt: ", aes_ecb_encrypt("Asd^14556", "1234567890123456"))

    # Decrypt Method - ECB
    print("Method ECB Decrypt: ", aes_ecb_decrypt("q6V+tjd/797mQueer75thw==", "1234567890123456"))

    # Encrypt Method - CBC
    print("Method CBC Encrypt: ", aes_cbc_encrypt("Asd^14556", "1234567890123456", "I8zyA4lVhMCaJ5Kg"))

    # Decrypt Method - CBC
    print("Method CBC Decrypt: ", aes_cbc_decrypt("TsCmO9Eg+uK8o+8b0keySQ==", "1234567890123456", "I8zyA4lVhMCaJ5Kg"))
