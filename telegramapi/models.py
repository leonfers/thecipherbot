import requests


class TelegramApi():
    service = None;
    bot_url = 'https://api.telegram.org/bot910195128:AAHacOdlZmh2kjNpc337RsN1KZci-ISk624/'

    def sendMessage(self, message, chat_id, reply_markup):
        json = {"text": message, "chat_id": chat_id}
        if reply_markup: json.__setitem__('reply_markup', reply_markup)
        r = requests.post(url=self.bot_url + 'sendMessage', json=json)
        print(json)

    @staticmethod
    def getService():
        if (TelegramApi.service is None):
            TelegramApi.service = TelegramApi()
        return TelegramApi.service

    @staticmethod
    def buildReplyMarkup():
        reply_markup = {"keyboard": [[{'text':'*enter*'}], [{'text':'overview'}], [{'text':'history'}], [{'text':'command'}], [{'text':'leave'}]],
                        'one_time_keyboard': True}
        return reply_markup
