import requests
import os
from datetime import datetime
from telegramhelpers import sendMessage
from dotenv import load_dotenv

MY_USER_ID = os.getenv('MY_USER_ID')

TELEGRAM_MAX_RETRIES = 3

base_path = os.path.dirname(__file__)

iso_timestamp = datetime.now().isoformat()

urls = [
    'https://ifconfig.me/ips',
    'https://ipecho.net/plain',
    'https://ipinfo.io/ip',
    'https://ident.me/',
    'https://api.ipify.org/'
]

new_ip = ''
for endpoint in urls:
    r = requests.get(endpoint)
    if r.status_code == 200:
        new_ip = r.text.strip()
        if new_ip != '':
            break

if new_ip != '':
    try:
        with open(os.path.join(base_path, 'backup'), 'r', encoding='utf-8') as f:
            old_ip = f.read()
    except FileNotFoundError:
        old_ip = ''

    if old_ip != new_ip:
        # Public IP has changed from old_ip to new_ip.
        with open(os.path.join(base_path, 'backup'), 'w', encoding='utf-8') as f:
            f.write(new_ip)
            msg_status = sendMessage(
                MY_USER_ID,
                f'Hey! Public ip has changed from "{old_ip}" to "{new_ip}".',
                TELEGRAM_MAX_RETRIES)
        with open(os.path.join(base_path, 'log'), 'a', encoding='utf-8') as f:
            f.write(f'{iso_timestamp}: New ip found: {new_ip}\n')
            if msg_status != True:
                f.write(
                    f'{iso_timestamp}: Could not alert per Telegram of new ip.\n')
    else:
        # Public IP hasn't changed.
        pass
else:
    with open(os.path.join(base_path, 'log'), 'a', encoding='utf-8') as f:
        f.write(f'{iso_timestamp}: could not find public ip.\n')
        msg_status = sendMessage(
            MY_USER_ID, 'Could not find public ip.', TELEGRAM_MAX_RETRIES)
        if msg_status != True:
            f.write(
                f'{iso_timestamp}: Could not alert per Telegram that ip couldn\'t be found.\n')
