import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOG_DIR = os.path.join(BASE_DIR, 'log')

APP_ENV = 'DEV'

ZIP_PASSWORD = 'ab12345678'

if __name__ == '__main__':
    print(LOG_DIR)
