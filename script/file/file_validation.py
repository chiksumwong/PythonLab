import os

import magic


def file_name_length_checking(file_path):
    file_name = os.path.basename(file_path)
    file_name_length = len(file_name)
    print('File Name:', file_name)
    print('File Name Length:', file_name_length)
    if 0 < file_name_length <= FILE_VALID_LENGTH:
        return True
    else:
        return False


def file_size_checking(file_path):
    file_size = os.path.getsize(file_path)
    print('File Size:', file_size)
    if 0 < file_size <= FILE_VALID_SIZE:
        return True
    else:
        return False


def file_type_checking(file_path):
    file_type = magic.from_file(file_path, mime=True)
    print('File Type:', file_type)

    if file_type in FILE_VALID_EXTENSIONS:
        return True
    else:
        return False


if __name__ == '__main__':
    # File Validation Setting
    FILE_VALID_LENGTH = 100
    FILE_VALID_SIZE = 1024 * 1024 * 20  # 20MB
    FILE_VALID_EXTENSIONS = [
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/excel",
        "application/vnd.ms-excel",
        "application/x-excel",
        "application/x-msexcel",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "text/csv",
        "text/comma-separated-values",
        "image/jpeg",
        "image/pjpeg",
        "image/bmp",
        "image/x-windows-bmp",
        "image/tiff",
        "image/x-tiff",
        "image/svg+xml",
        "image/png",
        "image/gif",
        "application/pdf",
        "application/mspowerpoint",
        "application/powerpoint",
        "application/vnd.ms-powerpoint",
        "application/x-mspowerpoint",
        "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        "application/mspowerpoint",
        "application/vnd.ms-powerpoint",
        "image/jpeg",
        "image/pjpeg",
        "application/rtf",
        "application/x-rtf",
        "text/richtext",
        "text/plain",
        "audio/mpeg3",
        "audio/x-mpeg-3",
        "video/mpeg",
        "video/x-mpeg",
        "audio/aiff",
        "audio/x-aiff",
        "video/mp4",
        "application/mp4",
        "audio/wav",
        "audio/x-wav",
        "audio/x-ms-wma",
        "audio/aiff",
        "audio/x-aiff",
        "video/quicktime",
        "application/x-troff-msvideo",
        "video/avi",
        "video/msvideo",
        "video/x-msvideo",
        "audio/mpeg",
        "video/mpeg",
        "audio/mpeg",
        "video/mpeg",
        "audio/mpeg",
        "video/mpeg",
        "video/x-ms-wmv",
        "application/x-compressed",
        "application/x-zip-compressed",
        "application/zip",
        "multipart/x-zip",
        "application/x-compress",
        "application/x-compressed",
        "application/x-7z-compressed",
        "application/rar",
        "application/x-rar-compressed",
        "audio/m4a",
        "audio/x-m4a",
        "message/rfc822 eml",
        "message/rfc822",
        "application/vnd.ms-outlook",
        "application/CDFV2",
        "application/vnd.ms-office"
    ]

    # File Validation
    file_name_length_checking('file_path')
    file_size_checking('file_path')
    file_type_checking('file_path')
