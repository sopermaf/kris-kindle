import csv
import getpass
import itertools
import os
import random
import smtplib
from datetime import datetime
from string import Template

mainMsgTemplate = Template(
    "Dear $secretSanta,\nYou will be buying a present for $assigned this year!"
)

KRIS_KINDLE_EMAIL = os.environ["KRIS_KINDLE_EMAIL"]
SMTP_SERVER_ADDR = os.environ.get("SMTP_SERVER_ADDR", "smtp.gmail.com")


def writeEmail(assignedName, secretSantaName, secretSantaEmail):
    """Creates the email body which will be
    sent as the email to the secret santa
    to inform them who they will be buying
    a present for.
    """
    currYear = datetime.now().year
    msg = "\r\n".join(
        [
            f"From: {KRIS_KINDLE_EMAIL}",
            f"To: {secretSantaEmail}",
            f"Subject: Kris Kindle {currYear}",
            "",
            mainMsgTemplate.substitute(
                secretSanta=secretSantaName, assigned=assignedName
            ),
        ]
    )
    return msg


def loginSMTPEmail(serverAddress, accountEmail):
    """Login to the email account on the specified
    SMTP server and prompt the user for a password.

    Returns the SMTP server
    """
    # conncect to SMTP server
    serverSMTP = smtplib.SMTP(serverAddress)
    serverSMTP.ehlo()
    serverSMTP.starttls()

    # login to the server
    password = getpass.getpass(f"Enter password to login to {accountEmail}:\n")
    serverSMTP.login(accountEmail, password)

    return serverSMTP


def assignSantas(participants):
    """Shuffles participants and assigns names.

    After shuffle, names are assigned pointing
    to the next person in the list in a circular
    fashion so that the last points back to the first
    ensuring a chain of gift giving when taking turns.
    """
    # ensures not in order of input file
    random.shuffle(participants)

    # shifts one ahead in participants names for cirucular gift exchange
    names = itertools.cycle(p["name"] for p in participants)
    next(names)

    for person, assigned in zip(participants, names):
        person["assigned"] = assigned

    # ensure output doesn't reveal the circular order
    random.shuffle(participants)


def runKrisKindle(participants):
    """
    Main function which runs the krisKindle
    process, shuffling the list of names
    and emails and then sending secret
    emails to each secret santa.
    """
    server = loginSMTPEmail(SMTP_SERVER_ADDR, KRIS_KINDLE_EMAIL)

    assignSantas(participants)

    for ind in participants:
        emailContent = writeEmail(ind["assigned"], ind["name"], ind["email"])
        server.sendmail(KRIS_KINDLE_EMAIL, ind["email"], emailContent)
        print(f"Sent email to \"{ind['name']}\" at email address \"{ind['email']}\"")

    # close connection
    server.close()


if __name__ == "__main__":
    with open("users.csv") as users_file:
        users = list(csv.DictReader(users_file))

    runKrisKindle(users)
