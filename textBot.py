from twilio.rest import Client
import sqlite3

conn = sqlite3.connect("contacts.db")
c = conn.cursor()

account_sid = "AC51fecec263256437b0ad0f8c196ed679"
#auth_token = ""
#client = Client(account_sid, auth_token)
#
#tnum = ""

def easyCommand(command):
    return command.strip().lower()

def createContactTable():
    c.execute("""CREATE TABLE IF NOT EXISTS contacts (
                first text,
                last text,
                number text
            )""")
    
    conn.commit()

def addContact():
    print("Adding Contact")
    firstName = input("First Name:")
    lastName = input("Last Name:")
    firstName.strip()
    lastName.strip()
    num = input("Number for " + firstName +" "+ lastName + "(no (), - or spaces): ")
    
    yesNo = easyCommand(input("Is " + num + " the correct number for " + firstName +" "+ lastName + "? (y/n)"))
    if yesNo == "y" or yesNo == "yes":
        c.execute("INSERT INTO contacts VALUES (?,?,?)",(firstName,lastName,num))
        conn.commit()
    
    
def getContact(firstName,lastName):
    c.execute("SELECT * FROM contacts WHERE first=? AND last=?",(firstName,lastName))
    people = c.fetchall()
        
    #contact not found
    if len(people) == 0:
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
    
    #if multiple contacts witht the same name are found
    else:
        print(len(people),"contacts found. Please select the number corresponding to the contact you want.")
        for i in range(0,len(people)):
            print(i," | ",people[i][0],"\t",people[i][1],"\t",people[i][2])
        print(len(people)," | ", "contact not found")
        choice = int(input())
        if choice >= 0 and choice < i:
            sendMessage(people[choice][2])
        elif choice == i:
            yesNo = easyCommand(input("Would you like to add a contact?"))
            if yesNo == "y" or yesNo == "yes":
                addContact()
            
def sendMessage(num):
    print("text")
    #message = client.messages.create(
    #    to=, 
    #    from_=tnum,
    #    body=)
    return None

#used for sending pregenerated quotes
class Quote:
    def __init__(self, text):
        conn = sqlite3.connect("quotes.db")
        c = conn.cursor()
        c.execute("INSERT INTO contacts VALUES (?)",(text))
        conn.commit()


if __name__ == '__main__':
    createContactTable()
    
    print("What would you like to do?")
    print("0 | Get Contact To Send a Message To \n"
          "1 | Add Contact  \n"
          "2 | See Contact List  \n"
          )
    choice = int(input())
    if choice == 0:
        first = input("Enter the first name of the contact. ")
        last = input("Enter the last name of the contact. ")
        getContact(first,last)
    if choice == 1:
        addContact()
    
    

    
    