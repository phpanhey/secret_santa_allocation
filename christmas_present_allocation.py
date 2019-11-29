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


def writeFile(file_name, string):
    filehandle = open(file_name, 'w')
    filehandle.write(string)
    filehandle.close()


# script start
participants_emails = getConfig('participants_emails')
participant_names_shuffled = sorted(
    list(participants_emails.keys()), key=lambda k: random.random())

writeFile('present_allocation.json', json.dumps(participant_names_shuffled))

for idx, participant_name in enumerate(participant_names_shuffled):
    message = 'hallo ' + participant_name + ',\n es weihnachtet sehr.\n' + 'dieses jahr beschenkst du ' + participant_names_shuffled[(idx + 1) % len(
        participant_names_shuffled)] + '.\n\nbis naechstes jahr,\ndein python script.\n\n\n ps: es weiss niemand, wer wem was schenkt, denn die auslosung wurde ueber ein python script realisiert. wenn du sehen willst wie das funktioniert, schaue hier: \n https://github.com/phpanhey/secret_santa_allocation/blob/master/christmas_present_allocation.py'
    sendMail(message, participants_emails[participant_name])
