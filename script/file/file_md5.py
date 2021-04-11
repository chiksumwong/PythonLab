import hashlib


def md5_generate(file_path):
    md5_hash = hashlib.md5()
    file = None

    try:
        file = open(file_path, "rb")
    except IOError:
        print("Reading file has problem:", file_path)

    content = file.read()
    md5_hash.update(content)
    digest = md5_hash.hexdigest()
    return digest


def md5_check(file_path, md5):
    md5_hash = hashlib.md5()

    file = None
    try:
        file = open(file_path, "rb")
    except IOError:
        print("Reading file has problem:", file_path)

    content = file.read()
    md5_hash.update(content)
    digest = md5_hash.hexdigest()

    if md5 == digest:
        print("MD5 Verified")
        return True
    else:
        print("MD5 Verification Failed")
        return False


def gen_project_md5(root_path):
    pass


def verify_project_md5(root_path, md5):
    pass


if __name__ == '__main__':
    pass
