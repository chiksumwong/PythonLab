import clamd

from log.log import save_exception_log
from server.settings import APP_ENV


def file_scan(file_path):
    try:
        if APP_ENV == 'UAT' or APP_ENV == 'PROD':
            cd = clamd.ClamdUnixSocket(path='/var/run/clamd.scan/clamd.sock')

            print('Clamd PING:', cd.ping())
            print('Clamd Version:', cd.version())

            result = cd.scan(file_path)
            print('Clamd Scan Result:', result)

            if result.get(file_path)[0] == "OK":
                return True
            else:
                return False
        else:
            return True

    except Exception as e:
        save_exception_log(f'File Scan Fail: {e}')
        return True
