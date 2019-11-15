import random
import json
from string import Template

emailMsgTemplate = Template('Dear $secretSanta,\nYou will be buying a present for $assigned this year!')


def writeEmail(assignedName, secretSantaName):
    '''Creates the email body which will be 
    sent as the email to the secret santa
    to inform them who they will be buying
    a present for.
    '''
    return emailMsgTemplate.substitute(
                secretSanta=secretSantaName,
                assigned=assignedName,
            )


def sendEmail(emailAddr, emailContent):
    '''
    Send an email to the to the specified
    address with the specified content
    '''
    pass


def assignSantas(participants):
    '''Shuffles participants and assigns names.
    Changes dictionary in place.
    '''
    random.shuffle(participants)

    numParticipants = len(participants)
    for i in range(0, numParticipants):
        assignedIndex = i + 1 if i + 1 < numParticipants else 0
        assignedName = participants[assignedIndex]['name']
        participants[i]['assigned'] = assignedName
        

def runKrisKindle(participants):
    '''
    Main function which runs the krisKindle
    process, shuffling the list of names
    and emails and then sending secret
    emails to each secret santa.
    '''
    assignSantas(participants)

    for ind in participants:
        emailContent = writeEmail(ind['assigned'], ind['name'])
        print(emailContent)
        # send
    

        

    

if __name__ == '__main__':
    with open("env/users.json") as users_file:
        users = json.load(users_file)
    
    runKrisKindle(users)
