import os
from dotenv import load_dotenv

load_dotenv()

# proxy settings
HOST = os.getenv('PROXY_HOST')
PORT = os.getenv('PROXY_PORT')
LOGIN = os.getenv('PROXY_LOGIN')
PASSWORD = os.getenv('PROXY_PASSWORD')

PROXY_URL=f"socks5://{LOGIN}:{PASSWORD}@{HOST}:{PORT}"

USER_AGENT='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'

headers = {'User-Agent': USER_AGENT}
proxies = {"https":PROXY_URL}

# data storage settings
DATA_FOLDER='parse_data'
ERROR_FOLDER='errors_data'
ERROR_FILENAME='errors.txt'
ERROR_FILEPATH=f'{ERROR_FOLDER}/{ERROR_FILENAME}'


# .csv file with links to parse
TARGET_LINKS_FILEPATH = 'habr.csv'