import requests
import json

class TelegramStats():


    def __init__(self, secret_key, group_key):
        '''
            secret_key : Your telegram bot
            group_key : Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        '''
        self.secret_key = secret_key
        self.group_key = group_key

    def get_msg(self):
        res = requests.get("https://api.telegram.org/bot{}/getUpdates".format(self.secret_key))
        return res.json()

    def send_msg(self, text):
        try:
            if isinstance(text, str) is False:
                text = json.dumps(text, ensure_ascii=False).encode('utf8')
            payload = {
                    "chat_id": "{}".format(self.group_key),
                    "text": str(text),
                }
            res = requests.post("https://api.telegram.org/bot{}/sendMessage".format(self.secret_key),data=payload)
            if res.status_code != requests.codes.ok:
                res = requests.post("https://api.telegram.org/bot{}/sendMessage".format(self.secret_key),data=payload)
            return res.json()
        except requests.exceptions.Timeout:
            # Maybe set up for a retry, or continue in a retry loop
            return {'failed': True}
        except requests.exceptions.TooManyRedirects:
            # Tell the user their URL was bad and try a different one
            return {'failed': True}
        except requests.exceptions.RequestException as e:
            return {'failed': True, 'msg': str(e)}