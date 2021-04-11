from config.settings import ZIP_PASSWORD
from file_scaner import file_scan
from file_validation import file_name_length_checking, file_size_checking, file_type_checking
from file_zip import zip_encrypt, file_remove
from file_md5 import md5_generate
from script.loger import log_exc


def file_upload(zip_file_path, file_path, file):
    print('==================== Start File Validation ====================')
    # Save File Temporary (for virus scan, zip file)
    with open(file_path, 'wb+') as f:
        for chunk in file.chunks():
            f.write(chunk)

    # File Size Checking
    if not file_name_length_checking(file_path):
        log_exc('File Checking - Name Length Error, ' + file_path)
        # Remove the file
        file_remove(file_path)
        file_remove(zip_file_path)
        return {'error': 'File Name Length Fail'}

    # File Size Checking
    if not file_size_checking(file_path):
        log_exc('File Checking - File Size Error, ' + file_path)
        # Remove the file
        file_remove(file_path)
        file_remove(zip_file_path)
        return {'error': 'File Size Fail'}

    # File Type Checking
    if not file_type_checking(file_path):
        log_exc('File Checking - File Type Error, ' + file_path)
        # Remove the file
        file_remove(file_path)
        file_remove(zip_file_path)
        return {'error': 'File Type Fail'}

    # File Virus Scan
    if not file_scan(file_path):
        log_exc('File Checking - File Scan Error, ' + file_path)
        # Remove the file
        file_remove(file_path)
        file_remove(zip_file_path)
        return {'error': 'File Scan Fail'}

    # Gen MD5 Checksum
    md5 = md5_generate(file_path)

    # Zip File Encryption (Random the file name)
    if not zip_encrypt(zip_file_path, file_path, ZIP_PASSWORD):
        log_exc('File Checking - Zip Encrypt Error, ' + file_path)
        # Remove the file
        file_remove(file_path)
        file_remove(zip_file_path)
        return {'error': 'Zip Encryption Fail'}

    print('==================== End File Validation ====================')

    return {'md5': md5}


def file_download():
    pass
