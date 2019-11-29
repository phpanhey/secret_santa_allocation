import random
import smtplib
import json


def sendMail(message, emailto):
    TO = emailto
    SUBJECT = 'weihnachtswichteln'
    TEXT = message

    sender = getConfig('src_email')
    password = getConfig('src_email_passwort')

    server = smtplib.SMTP('smtp.office365.com', 587)
    server.ehlo()
    server.starttls()
    server.login(sender, password)

    BODY = '\r\n'.join(['To: %s' % TO,
                        'From: %s' % sender,
                        'Subject: %s' % SUBJECT,
                        '', TEXT])

    try:
        server.sendmail(sender, [TO], BODY)
        print('email sent')
    except:
        print('error sending mail')

    server.quit()


def getConfig(config_key):
    with open('config.json', 'r') as file:
        return json.loads(file.read().replace('\n', ''))[config_key]


# script start
participants_emails = getConfig('participants_emails')
participant_names_shuffled = sorted(
    list(participants_emails.keys()), key=lambda k: random.random())

print(participant_names_shuffled)

for idx, participant_name in enumerate(participant_names_shuffled):
    message = 'Hallo ' + participant_name + ',\n\n' + 'dieses jahr beschenkst du ' + participant_names_shuffled[(idx + 1) % len(
        participant_names_shuffled)] + '.\n\n\n ps: die auslosung und das senden der mail wurde mit einem selbstgeschriebenen python script realisiert, schau hier:'
    sendMail(message, 'philipp.panhey@gmail.com')
