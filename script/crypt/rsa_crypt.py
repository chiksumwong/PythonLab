import os
from base64 import b64encode, b64decode

import Crypto
from Crypto.Cipher import PKCS1_OAEP, PKCS1_v1_5
from Crypto.Hash import SHA256, SHA512, SHA384, MD5
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15

from server.settings import BASE_DIR

SETTING_ROOT = os.path.join(BASE_DIR, 'server')


def rsa_key_generation(private_path="private.pem", public_path="public.pem"):
    # 1024, 2048, 4096
    key = RSA.generate(2048)

    private_key = key.export_key()
    file_out = open(private_path, "wb")
    file_out.write(private_key)
    file_out.close()

    public_key = key.publickey().export_key()
    file_out = open(public_path, "wb")
    file_out.write(public_key)
    file_out.close()

    print("Done")


def rsa_load_file(fn):
    key = None
    try:
        key = RSA.importKey(open(fn).read())
    except Exception as err:
        print('Error:', fn, err)
    return key


def get_max_length(rsa_key, encrypt=True):
    block_size = Crypto.Util.number.size(rsa_key.n) / 8
    reserve_size = 45  # 预留位为11
    if not encrypt:  # 解密时不需要考虑预留位
        reserve_size = 0
    max_length = block_size - reserve_size
    return max_length


# Handle Long Text Problem
def rsa_encrypt_long(message, public_key):
    message = message.encode('utf-8')  # string to bytes
    encrypt_result = b''
    max_length = get_max_length(public_key)
    max_length = int(max_length)
    cipher = PKCS1_OAEP.new(public_key)
    while message:
        input_data = message[:max_length]
        message = message[max_length:]
        out_data = cipher.encrypt(input_data)
        encrypt_result += out_data
    encrypt_result = b64encode(encrypt_result)
    return encrypt_result.decode("utf-8")  # bytes to string


def rsa_decrypt_long(cipher_text, private_key):
    decrypt_result = b""
    max_length = get_max_length(private_key, False)
    max_length = int(max_length)
    decrypt_message = b64decode(cipher_text)
    cipher = PKCS1_OAEP.new(private_key)
    while decrypt_message:
        input_data = decrypt_message[:max_length]
        decrypt_message = decrypt_message[max_length:]
        out_data = cipher.decrypt(input_data)
        decrypt_result += out_data
    return decrypt_result.decode('utf-8')  # bytes to string


# Between Server and Server
def rsa_encrypt(message, public_key):
    message = message.encode('utf-8')  # string to bytes
    cipher_text = ""
    try:
        cipher = PKCS1_OAEP.new(public_key)
        cipher_text = cipher.encrypt(message)
        cipher_text = b64encode(cipher_text)  # bytes to base64 (bytes)
    except Exception as err:
        print('RSA Encryption Error:', err)
    return cipher_text.decode("utf-8")  # bytes to string


def rsa_decrypt(cipher_text, private_key):
    cipher_text = b64decode(cipher_text)  # string to base64
    message = ""
    try:
        cipher = PKCS1_OAEP.new(private_key)
        message = cipher.decrypt(cipher_text)
    except Exception as err:
        print('RSA Decryption Error:', err)
    return message.decode('utf-8')  # bytes to string


def rsa_sign(message, private_key):
    message = message.encode('utf-8')  # string to bytes
    signature = ''
    try:
        signer = pkcs1_15.new(private_key)
        digest = SHA256.new(message)
        signature = signer.sign(digest)
        signature = b64encode(signature)  # bytes to base64
    except Exception as err:
        print('RSA Sign Error:', err)
    return signature.decode('utf-8')  # bytes to string


def rsa_verify(message, signature, public_key):
    message = message.encode('utf-8')  # string to bytes
    signature = b64decode(signature)  # string to base64
    try:
        signer = pkcs1_15.new(public_key)
        digest = SHA256.new(message)
        signer.verify(digest, signature)
        res = True
    except (ValueError, TypeError):
        res = False
    return res


# Between Frontend (Jsencrypt) and Backend
def rsa_encrypt_web(message, public_key):
    message = message.encode('utf-8')  # string to bytes
    cipher_text = ""
    try:
        cipher = PKCS1_v1_5.new(public_key)  # Cannot use "PKCS1_OAEP", it cannot decrypt at Jsencrypt
        cipher_text = cipher.encrypt(message)
        cipher_text = b64encode(cipher_text)  # bytes to base64 (bytes)
    except Exception as err:
        print('RSA Encryption Error:', err)
    return cipher_text.decode("utf-8")  # bytes to string


def rsa_decrypt_web(cipher_text, private_key):
    cipher_text = cipher_text.encode('utf-8')  # string to bytes
    cipher_text = b64decode(cipher_text)  # bytes to base64
    message = ""
    try:
        cipher = PKCS1_v1_5.new(private_key)  # Cannot use "PKCS1_OAEP", it cannot decrypt from Jsencrypt
        sentinel = None
        message = cipher.decrypt(cipher_text, sentinel)
    except Exception as err:
        print('RSA Decryption Error:', err)
    return message.decode('utf-8')  # bytes to string


# Functions
def get_msg(msg):
    path_b2 = os.path.join(SETTING_ROOT, "public_b.pem")
    encrypted = rsa_encrypt(msg, rsa_load_file(path_b2))
    return encrypted


def get_sign(msg):
    path_a1 = os.path.join(SETTING_ROOT, "private_a.pem")
    encrypted = rsa_encrypt(msg, rsa_load_file(path_a1))
    return encrypted


def decrypt_msg(encrypted):
    path_b1 = os.path.join(SETTING_ROOT, "private_b.pem")
    decrypted = rsa_decrypt(encrypted, rsa_load_file(path_b1))
    return decrypted


def verify_sign(msg, sign):
    path_a2 = os.path.join(SETTING_ROOT, "public_a.pem")
    verified = rsa_verify(msg, sign, rsa_load_file(path_a2))


# Generate the Keys
def gen_key():
    # Private and Public Key Generation
    rsa_key_generation("private_a.pem", "public_a.pem")
    rsa_key_generation("private_b.pem", "public_b.pem")


# Test Case
def case_server():
    msg = "testingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtesting"
    # As a Sender (A)
    # Encrypt
    path_a1 = os.path.join(SETTING_ROOT, "private_a.pem")
    path_a2 = os.path.join(SETTING_ROOT, "public_a.pem")
    path_b1 = os.path.join(SETTING_ROOT, "private_b.pem")
    path_b2 = os.path.join(SETTING_ROOT, "public_b.pem")

    encrypted = rsa_encrypt(msg, rsa_load_file("public_b.pem"))
    print(encrypted)

    # Sign
    signed = rsa_sign(msg, rsa_load_file("private_a.pem"))
    print(signed)

    # As a Receiver (B)
    # Decrypt
    decrypted = rsa_decrypt(encrypted, rsa_load_file("private_b.pem"))
    print(decrypted)
    # Verify
    verified = rsa_verify(decrypted, signed, rsa_load_file("public_a.pem"))
    print(verified)


def case_web():
    # As a Sender (A)
    msg = "Hello!"
    # Encrypt
    encrypted = rsa_encrypt_web(msg, rsa_load_file("public_b.pem"))
    print(encrypted)
    # Sign
    signed = rsa_sign(msg, rsa_load_file("private_a.pem"))
    print(signed)

    # As a Receiver (B)
    encrypted_msg = "oOYoigag50oMGplT5/vyMu3dUAe7dM5/zzrf1hCPMQkLj0J67kPBcm1tbQZO7KFz2xfxyKdunYOfYh6kysivb3GA9JNKsvZ5LtwQlV3qVznk/0TKC5N0n0vjXlY5ZNzKlyfoIeDb7BOHlkS7Vh8X8ErtPbsy50Pjmj2OHN734KyhmUdq8Hr9pNyK68BXjcJnqEIlQlTohyJXjaVA6ae+GvUBFHKiRmlNc2gPUYe7Al8rH+1uwY4IXJRzkhLzGheqo10eM60HHqWvfTOgGnlQj1HNgUTi+Ly4spwhgwuPvsCYPHW4QDR6ulvp3+uJKaUWJEfoyTsQwrG9VfmBdMOFsw=="
    signed_msg = "GhRotUd2jA3vNVjTtl23lIGho18NpddmdR6GTpDDQXi7rnYs80xBIZg5PE+Oy/ycDTHU1KUKR3ebvzuVBBlyIDO+BVsK/ixhyO7OeC6YHLaA9cyP2c1JrsGGU+fTW85o+MEqwGwkoukcrydGvFXZuvHMx6Zg1dchDxwMBv2gjhAqZPmqFXWKb47F5oeD6RIX2UNZNW+44LZksLM6/tt0xnvPB9doH7rkZAbqQUgzC5MpVosghUhm0bsrO1T+q6KnsoI7bsG7UZnkf/Ap3rX9CZ0SPE4xMKb7w3YbdKx/oirN/EGwQwVokGvT82K1HmqZ0A7cQC3mNsPgEj56j9ZIeQ=="
    # Decrypt
    decrypted = rsa_decrypt_web(encrypted_msg, rsa_load_file("private_b.pem"))
    print(decrypted)
    # Verify
    verified = rsa_verify(decrypted, signed_msg, rsa_load_file("public_a.pem"))
    print(verified)


def case_long():
    msg = "{'company_name_e':'ABCcompany','company_name_c':'\u4e2d\u6587\u516c\u53f8'','company_name_oe':'ABCcompany','company_name_oc':'\u4e2d\u6587\u516c\u53f8'','form_of_business':'corporate','registered_address':'KwunTong,HungToRd,58\u865f5\u6a1318\u5ba4CareerAndKensonIndustrialMansion','corresponding_address':'KwunTong,HungToRd,58\u865f5\u6a1318\u5ba4CareerAndKensonIndustrialMansion','business_registration_number':'RE2323','year_of_establishment':'2019','number_of_staff':'50','company_website':'www.company_abc.com','telephone_number':'34453333','fax_number':'33333333','email':'abc@example.com','services_description':'thisisnotdescription','major_customers':'MTR,HKE','certificates':'IS2132,IS2324','q_a':'1','q_a_y':'thisshowsomeinformaiton','q_b':'1','q_b_y':'thisshowsomeinformaiton','q_c':'1','q_c_y_a':'thisshowsomeinformaiton','q_c_y_b':'thisshowsomeinformaiton','q_d':'1','q_d_y':'thisshowsomeinformaiton','q_e':'1','q_e_y':'thisshowsomeinformaiton','printed_name':'sum','position':'CEO'}"
    encrypted = rsa_encrypt_long(msg, rsa_load_file("public_b.pem"))
    print(encrypted)

    # Sign
    signed = rsa_sign(msg, rsa_load_file("private_a.pem"))
    print(signed)

    # As a Receiver (B)
    # Decrypt
    decrypted = rsa_decrypt_long(encrypted, rsa_load_file("private_b.pem"))
    print(decrypted)

    # Verify
    verified = rsa_verify(decrypted, signed, rsa_load_file("public_a.pem"))
    print(verified)


if __name__ == '__main__':
    # gen_key()
    # case_server()

    # case_web()

    case_long()
