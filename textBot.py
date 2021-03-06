from twilio.rest import Client
import sqlite3
import quoteManager

conn1 = sqlite3.connect("contacts.db")
c1 = conn1.cursor()

#-----------------------------------MUST-ENTER-TWILIO-ACCOUNT-DETAILS--------------------------
#account_sid = "AC51fecec263256437b0ad0f8c196ed679"
#auth_token = ""
#client = Client(account_sid, auth_token)
#
#tnum = ""

def easyCommand(command):
    return command.strip().lower()

def createContactTable():
    c1.execute("""CREATE TABLE IF NOT EXISTS contacts (
                first text,
                last text,
                number text
            )""")
    
    conn1.commit()

def addContact():
    print("Adding Contact")
    firstName = input("First Name:")
    lastName = input("Last Name:")
    firstName.strip()
    lastName.strip()
    num = input("Number for " + firstName +" "+ lastName + "(no (), - or spaces): ")
    
    yesNo = easyCommand(input("Is " + num + " the correct number for " + firstName +" "+ lastName + "? (y/n) "))
    if yesNo == "y" or yesNo == "yes":
        c1.execute("INSERT INTO contacts VALUES (?,?,?)",(firstName,lastName,num))
        conn1.commit()
    
    
def getContact(firstName,lastName):
    c1.execute("SELECT * FROM contacts WHERE first=? AND last=?",(firstName,lastName))
    people = c1.fetchall()
        
    #contact not found
    if len(people) == 0:
        yesNo = easyCommand(input("Contact not found. Would you like to add one?(y/n) "))
        
        if yesNo == "y" or yesNo == "yes":
            addContact()
                
    elif len(people) == 1:
        yesNo = easyCommand(input("Contact " + people[0][0] +" "+people[0][1] + " at "+people[0][2]+"?(y/n) "))
        if yesNo == "y" or yesNo == "yes":
            sendMessage(people[0][2])
        else:
            yesNo = easyCommand(input("Would you like to add a new contact?(y/n) "))
            addContact()
    
    #if multiple contacts witht the same name are found
    else:
        print(len(people),"contacts found. Please select the number corresponding to the contact you want. ")
        for i in range(0,len(people)):
            print(i," | ",people[i][0],"\t",people[i][1],"\t",people[i][2])
        print(len(people)," | ", "contact not found")
        choice = int(input())
        if choice >= 0 and choice < len(people):
            sendMessage(people[choice][2])
        elif choice == len(people):
            yesNo = easyCommand(input("Would you like to add a contact?(y/n) "))
            if yesNo == "y" or yesNo == "yes":
                addContact()
            
            
def showContacts():
    c1.execute("SELECT * FROM contacts")
    people = c1.fetchall()
    for i in people:
        print(i[0],"\t",i[1],"\t",i[2])

        
def deleteContact():
    c1.execute("SELECT rowid,* FROM contacts")
    people = c1.fetchall()
    for p in people:
        print(p[0],": ",p[1],"\t",p[2],"\t",p[3])
    idToDelete = int(input("Select the number corresponding to the contact you would like to delete. "))
    c1.execute("DELETE FROM contacts WHERE rowid=?",(idToDelete,))
    conn1.commit()
    

def sendMessage(num):
    print("0 | Send normal message \n"
          "1 | Send quote from database "
          )
    choice = input()
    if choice == '0':
        message = input("Message: ")
    if choice == '1':
        message = quoteManager.getQuote()
    print(message)
        
#-------------------------------------------UNCOMMENT-REGION-FOR-USE-----------------------------
#    message = client.messages.create(
#        to=num, 
#        from_=tnum,
#        body=message)



if __name__ == '__main__':
    createContactTable()
    quoteManager.createQuoteTable()
    
    print("Welcome to TextBot!")
    
    while True:
        print("\nWhat would you like to do?")
        print("0 | Send Message \n"
              "1 | Add Contact  \n"
              "2 | See Contact List  \n"
              "3 | Delete Contact  \n"
              "4 | Save a Quote  \n"
              "5 | Show Quotes  \n"
              "6 | Delete Quote  "
              )
        choice = input()
        
        if choice == '0':
            first = input("Enter the first name of the contact. ")
            last = input("Enter the last name of the contact. ")
            getContact(first,last)
            
        elif choice == '1':
            addContact()
            
        elif choice == '2':
            showContacts()
            
        elif choice == '3':
            deleteContact()
            
        elif choice == '4':
            q = input("Quote: ")
            quoteManager.storeQuote(q)
            
        elif choice == '5':
            quoteManager.showQuotes()
            
        elif choice == '6':
            quoteManager.deleteQuote()
            
        else:
            break
        
    conn1.close()
    quoteManager.conn2.close()
            