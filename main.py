import os
import json
import time
import requests
from datetime import datetime

#set these variables before running the script

global TOKEN
global URL
global SECRET_WEBHOOK_TOKEN
#TOKEN = "your telegram token from @BotFather"
#URL = "your webhook url"
#SECRET_WEBHOOK_TOKEN = "your secret token for X-Telegram-Bot-Api-Secret-Token"

def menu():
    print("webhook helper. reply with a choice (number)\n\n\
1) set webhook to url from bot_credentials\n\
2) delete current webhook\n\
3) delete current webhook and drop pending updates\n\
4) get webhook info")
    user_choice = int(input("\nyour choice: "))
    if user_choice == 1:
        setWebhook()
    elif user_choice == 2:
        deleteWebhook()
    elif user_choice == 3:
        deleteWebhook(drop_pending_updates=True)
    elif user_choice == 4:
        getWebhookInfo()
    else:
        os.system("clear")
        print("huh? try again.")
        time.sleep(1.5)
        os.system("clear")
        menu()
        

def setWebhook():
    set_webhook = requests.post(
        'https://api.telegram.org/bot{token}/setWebhook'.format(
            token = TOKEN
        ),
        headers={"Content-Type": "application/json"},
        json={
            "url": URL,
            "secret_token": SECRET_WEBHOOK_TOKEN
            }
    )
    response = set_webhook.json()
    print("\nsetWebhook request sent. Response status code: {status_code}".format(status_code=set_webhook.status_code))
    print("\nreadable setWebhook json response:\n\n", json.dumps(response, indent=4))


def deleteWebhook(drop_pending_updates = False):
    delete_webhook = requests.post(
        'https://api.telegram.org/bot{token}/deleteWebhook'.format(
            token = TOKEN
        ),
        headers={"Content-Type": "application/json"},
        json={"drop_pending_updates": drop_pending_updates}
    )
    response = delete_webhook.json()
    if not drop_pending_updates:
        print("\ndeleteWebhook request sent. Response status code: {status_code}".format(status_code=delete_webhook.status_code))
    elif drop_pending_updates:
        print("\ndeleteWebhook request sent (with drop_pending_updates == True). \
Response status code: {status_code}".format(status_code=delete_webhook.status_code))
    print("\nreadable deleteWebhook json response:\n\n", json.dumps(response, indent=4))


def getWebhookInfo():
    get_webhook_info = requests.post(
        'https://api.telegram.org/bot{token}/getWebhookInfo'.format(
            token = TOKEN
        ),
        headers={"Content-Type": "application/json"}
    )
    response = get_webhook_info.json()
    if response["result"]["url"] == '':
        print("\nwebhook is not set.")
    elif "last_error_date" in response["result"]:
        readable_date = datetime.fromtimestamp(response["result"]["last_error_date"]).strftime("%Y-%m-%d %H:%M:%S")
        timestamp = response["result"]["last_error_date"]
        response["result"]["last_error_date"] = "{r_d} (timestamp: {ts})".format(
            r_d = readable_date,
            ts = timestamp
        )
    print("\nreadable getWebhookInfo json response:\n\n", json.dumps(response, indent=4))


try:
    menu()
except KeyboardInterrupt:
    print("\n\n\nchange da world, my final message. goodbye...")
except NameError:
    print("\nerror: please, specify your Telegram token and webhook url as global TOKEN and URL variables")
