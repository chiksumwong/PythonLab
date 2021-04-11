import hashlib
import json
import os

from config.settings import BASE_DIR
from script.loger import log_info, log_exc


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
    log_info('Gen md5 start')
    try:
        md5_list = []
        # gen md5 for each file
        for root, dirs, files in os.walk(root_path):
            for names in files:
                file_obj = {}
                filepath = os.path.join(root, names)
                md5 = md5_generate(filepath)
                print(filepath)

                # remove root_path
                filepath = filepath.replace(root_path+'\\', '')

                # Save md5 as dict
                file_obj[str(filepath)] = md5
                md5_list.append(file_obj)

        # to json file
        with open(os.path.join(root_path, 'result.json'), 'w+', encoding='utf-8') as f:
            data = {'md5_list': md5_list}
            json.dump(data, f)

        log_info('Gen md5 end')

    except IOError as e:
        log_exc(f'Load File Fail: {e}')


def verify_project_md5(root_path, md5_json):
    with open(md5_json) as json_file:
        data = json.load(json_file)
        data_arr = data['md5_list']
        for item in data_arr:
            for i in item:
                file_path = os.path.join(root_path, i)
                result = md5_check(file_path, item[i])
                if not result:
                    log_info(f'Md5 verify fail: {file_path}')


if __name__ == '__main__':
    gen_project_md5(BASE_DIR)
    verify_project_md5(BASE_DIR, os.path.join(BASE_DIR, 'result.json'))