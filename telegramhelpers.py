import requests, os

API_TOKEN = os.getenv('API_TOKEN')

def sendMessage(user_id: str, text: str, max_retries: int = 1):
    url = f'https://api.telegram.org/bot{API_TOKEN}/sendMessage'
    payload = {
        "chat_id": user_id,
        "text": text
    }
    for i in range(max_retries):
        r = requests.get(url, params=payload)
        isOk = False
        try:
            isOk = r.json()["ok"] == True
        except:
            pass
        if isOk == True:
            return isOk
    return isOk