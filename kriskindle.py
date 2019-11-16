import random
import json
from string import Template
from datetime import datetime
import getpass
import smtplib
import kriskindle_config as kk_config

mainMsgTemplate = Template('Dear $secretSanta,\nYou will be buying a present for $assigned this year!')

def writeEmail(assignedName, secretSantaName, secretSantaEmail):
    '''Creates the email body which will be 
    sent as the email to the secret santa
    to inform them who they will be buying
    a present for.
    '''
    currYear = datetime.now().year
    msg = "\r\n".join([
        "From: %s" % kk_config.KRIS_KINDLE_EMAIL,
        "To: %s" % secretSantaEmail,
        "Subject: Kris Kindle %s" %currYear,
        "",
        mainMsgTemplate.substitute(secretSanta=secretSantaName, assigned=assignedName)
    ])
    return msg


def loginSMTPEmail(serverAddress, accountEmail):
    '''Login to the email account on the specified 
    SMTP server and prompt the user for a password.

    Returns the SMTP server
    '''
    # conncect to SMTP server
    serverSMTP = smtplib.SMTP(serverAddress)
    serverSMTP.ehlo()
    serverSMTP.starttls()

    # login to the server
    password = getpass.getpass(
                    f"Enter password to login to {accountEmail}:\n"
                )
    serverSMTP.login(accountEmail, password)

    return serverSMTP


def assignSantas(participants):
    '''Shuffles participants and assigns names.

    After shuffle, names are assigned pointing
    to the next person in the list in a circular
    fashion so that the last points back to the first
    ensuring a chain of gift giving when taking turns.
    '''
    random.shuffle(participants)
    numParticipants = len(participants)

    for i in range(numParticipants):
        assignedName = participants[(i + 1) % numParticipants]['name']
        participants[i]['assigned'] = assignedName


def runKrisKindle(participants):
    '''
    Main function which runs the krisKindle
    process, shuffling the list of names
    and emails and then sending secret
    emails to each secret santa.
    '''
    assignSantas(participants)
    server = loginSMTPEmail(kk_config.SMTP_SERVER_ADDR, kk_config.KRIS_KINDLE_EMAIL)

    for ind in participants:
        emailContent = writeEmail(ind['assigned'], ind['name'], ind['email'])
        server.sendmail(kk_config.KRIS_KINDLE_EMAIL, ind['email'], emailContent)
        print(f"Sent email to \"{ind['name']}\" at email address \"{ind['email']}\"")
    
    # close connection
    server.close()


if __name__ == '__main__':
    with open("env/users.json") as users_file:
        users = json.load(users_file)
    
    runKrisKindle(users)
