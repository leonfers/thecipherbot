import requests

bot_url = 'https://api.telegram.org/bot910195128:AAHacOdlZmh2kjNpc337RsN1KZci-ISk624/'


def sendMessage(message, chat_id):
    r = requests.post(url=bot_url + 'sendMessage', json={"text": message, "chat_id": chat_id})
    print(r.status_code)
    print(r.reason)
    print(r.json())