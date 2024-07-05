from imbox import Imbox
from datetime import datetime
import pandas as pd

username = 'italofarias071@gmail.com'

passwords = open('passwords/token', 'r').read()

host = "imap.gmail.com"


mail = Imbox(host, username=username, password=passwords, ssl=True)

messages = mail.messages(raw='has:attachment')



for (uid, message) in messages:

    print(message.subject)
    print(message.sent_from)
    print(message.sent_to)
    print(message.date)
    print(message.attachments)
    break