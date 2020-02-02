import requests


class TelegramApi():

    service = None;
    bot_url = 'https://api.telegram.org/bot910195128:AAHacOdlZmh2kjNpc337RsN1KZci-ISk624/'

    def sendMessage(self,message, chat_id):
        r = requests.post(url=self.bot_url + 'sendMessage', json={"text": message, "chat_id": chat_id})

    @staticmethod
    def getService():
        if(TelegramApi.service is None):
            TelegramApi.service = TelegramApi()
        return TelegramApi.service
