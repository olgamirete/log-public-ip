import requests
from datetime import datetime

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
        with open('backup', 'r', encoding='utf-8') as f:
            old_ip = f.read()
    except FileNotFoundError:
        old_ip = ''

    if old_ip != new_ip:
        # Public IP has changed from old_ip to new_ip.
        with open('backup', 'w', encoding='utf-8') as f:
            f.write(new_ip)
        with open('log', 'a', encoding='utf-8') as f:
            f.write(f'{iso_timestamp}: {new_ip}\n')
    else:
        # Public IP hasn't changed.
        pass
else:
    with open('log', 'a', encoding='utf-8') as f:
        f.write(f'{iso_timestamp}: could not find public ip.\n')
