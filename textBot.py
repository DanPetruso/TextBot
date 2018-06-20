from twilio.rest import Client
import sqlite3

conn = sqlite3.connect("contacts.db")
c = conn.cursor()

def easyCommand(command):
    return command.strip().lower()

def createContactDatabase():
    c.execute("""CREATE TABLE contacts (
                first text,
                last text,
                number text
            )""")
    
    conn.commit()


def addContact():
    firstName = input("First Name:")
    lastName = input("Last Name:")
    firstName.strip()
    lastName.strip()
    num = input("Number for",firstName,lastName,"(no (), - or spaces)")
            
    yesNo = easyCommand(input("Is",num,"the correct number for",firstName,lastName + "? (y/n)"))
    if yesNo == "y" or yesNo == "yes":
        c.execute("INSERT INTO contacts VALUES (?,?,?)",(firstName,lastName,num))
        conn.commit()
    
    
def getContact(firstName,lastName):
    #user only enters first name
    if lastName == "":
        c.execute("SELECT * FROM contacts WHERE first=?",(firstName))
    else:
        c.execute("SELECT * FROM contacts WHERE first=? AND last=?",(firstName,lastName))
    people = c.fetchall()
    
    #contact not found, checks if user entered lastName where firstName should have been
    if people == None:
        c.execute("SELECT * FROM contacts WHERE first=?",(lastName))
        people = c.fetchall()
        
    #contact still not found, asks if user wants to add it
    if people == None:
        yesNo = easyCommand(input("Contact not found. Would you like to add one?(y/n)\n"))
        
        if yesNo == "y" or yesNo == "yes":
            addContact()
                
    elif len(people) == 1:
        yesNo = easyCommand(input("Contact",people[0][0],people[0][1],"at",people[0][2]+"?"))
        if yesNo == "y" or yesNo == "yes":
            sendMessage(people[0][2])
        else:
            yesNo = easyCommand(input("Would you like to add a new contact?"))
            addContact()
            
    else:
        print(len(people),"contacts found. Please select the number corresponding to the contact you want.")
        for i in range(0,len(people)):
            print(i," | ",people[i][0],"\t",people[i][0],"\t",people[i][2])
        print(i+1," | ", "contact not found")
        choice = input()
        if choice >= 0 and choice < i:
            sendMessage(people[choice][2])
        elif choice == i:
            yesNo = easyCommand(input("Would you like to add a contact?"))
            if yesNo == "y" or yesNo == "yes":
                addContact()
            
def sendMessage(num):
    return None


if __name__ == '__main__':
    while True:
        print("What would you like to do?")
        print("0 | Send Message \n"
              "1 | Add Contact  \n"
              "2 | See Contact List  \n"
              )
        choice = input()
    
    
#account_sid = "AC51fecec263256437b0ad0f8c196ed679"
#auth_token = ""
#client = Client(account_sid, auth_token)
#
#tnum = ""
#
#message = client.messages.create(
#    to=, 
#    from_=tnum,
#    body=)
    
    