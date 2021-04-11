import os
import random
import shutil
import string
from os.path import basename

import pyzipper


def zip_random_name(length=8):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str + '.zip'


def zip_encrypt(zip_file_path, file_path, password):
    try:
        # zip64 (not open) for large zip file (more than 4 GiB in size)
        with pyzipper.AESZipFile(zip_file_path,
                                 'w',
                                 compression=pyzipper.ZIP_LZMA,
                                 encryption=pyzipper.WZ_AES) as zf:
            zf.setpassword(password.encode('UTF-8'))
            zf.write(file_path, basename(file_path))  # create zip file then add that file with file path
            print("Zip Encryption Done!")
            return True
    except pyzipper.BadZipFile:
        print('Error: Zip file is corrupted')
        return False
    except pyzipper.LargeZipFile:
        print('Error: File size if too large')
        return False


def zip_decrypt(zip_file_name, folder_path, password):
    try:
        # zip64 (not open) for large zip file (more than 4 GiB in size)
        with pyzipper.AESZipFile(zip_file_name) as zf:
            zf.setpassword(password.encode('UTF-8'))
            zf.extractall(folder_path)  # extract all file in zip folder to that folder
            print("Zip Decryption Done!")
            return True
    except pyzipper.BadZipFile:
        print('Error: Zip file is corrupted')
        return False
    except pyzipper.LargeZipFile:
        print('Error: File size if too large')
        return False


def file_remove(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        print('Removed File:', file_path)
    else:
        print('The file does not exist:', file_path)


def files_remove(file_path):
    for the_file in os.listdir(file_path):
        print(the_file)
        path = os.path.join(file_path, the_file)
        try:
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    pass