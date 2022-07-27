import requests
import os
from datetime import datetime
from telegramhelpers import sendMessage
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_MAX_RETRIES = 3
MY_USER_ID = os.getenv('MY_USER_ID')
REF = os.getenv('REF')
if REF == None or REF == '':
    REF = '(unknown)'

def get_previous_ip() -> str:
    previous_ip = ''
    try:
        base_path = os.path.dirname(__file__)
        with open(os.path.join(base_path, 'backup'), 'r', encoding='utf-8') as f:
            previous_ip = f.read()
    except FileNotFoundError:
        pass  # line previous_ip = '' still dominates
    return previous_ip

def get_current_ip() -> str:
    urls = [
        'https://ifconfig.me/ips',
        'https://ipecho.net/plain',
        'https://ipinfo.io/ip',
        'https://ident.me/',
        'https://api.ipify.org/'
    ]
    current_ip = ''
    for endpoint in urls:
        r = requests.get(endpoint)
        if r.status_code == 200:
            current_ip = r.text.strip()
            if current_ip != '':
                break
    return current_ip

def log_line(msg: str, logname: str = 'log') -> None:
    base_path = os.path.dirname(__file__)
    with open(os.path.join(base_path, logname), 'a', encoding='utf-8') as f:
        iso_timestamp = datetime.now().isoformat()
        f.write(f'{iso_timestamp}: {msg}\n')

def send_alert(msg: str) -> None:
    msg_status = sendMessage(
        user_id=MY_USER_ID,
        text=msg,
        max_retries=TELEGRAM_MAX_RETRIES)
    if msg_status != True:
        log_line('Could not send alert per Telegram. Alert: "{msg}".')

def backup_ip(ip: str) -> None:
    base_path = os.path.dirname(__file__)
    with open(os.path.join(base_path, 'backup'), 'w', encoding='utf-8') as f:
        f.write(ip)

def main():
    old_ip = get_previous_ip()
    current_ip = get_current_ip()
    if current_ip != '' and current_ip != old_ip:
        # Public IP has changed from old_ip to new_ip.
        backup_ip(current_ip)
        log_line(f'Public IP has changed from "{old_ip}" to "{current_ip}".')
        send_alert(f'Public IP of {REF} has changed from "{old_ip}" to "{current_ip}".')
    if current_ip == '':
        log_line('Could not retrieve the current IP.')
        send_alert('Could not find public ip.')

if __name__ == "__main__":
    main()
