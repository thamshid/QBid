import os

from settings import WHATSAPP_GROUP_ID, WHATSAPP_NUMBER, WHATSAPP_PASSWORD


def send_whatsapp_msg(number=WHATSAPP_NUMBER, password=WHATSAPP_PASSWORD, to_number=WHATSAPP_GROUP_ID, message=""):
    messages = [message[i:i + 100] for i in range(0, len(message), 100)]
    for msg in messages:
        os.system('yowsup-cli demos --send ' + to_number +' "' + msg + '" --login '+ number + ':' + password)
    return True

