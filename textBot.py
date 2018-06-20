from twilio.rest import Client
import sqlite3
from sqlite3 import Error

conn = sqlite3.connect("contacts.db")
c = conn.cursor()

def createContactDatabase():
    c.execute("""CREATE TABLE contacts (
                first text,
                last text,
                number text
            )""")
    
    conn.commit()


def addContact(firstName, lastName, num):
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
    if people == []:
        c.execute("SELECT * FROM contacts WHERE first=?",(lastName))
        people = c.fetchall()
        
    #contact still not found, asks if user wants to add it
    if people == []:
        yesNo = input("Contact not found. Would you like to add it?(y/n)\n")
        
        if yesNo.lower().strip() == "y" or yesNo.lower().strip() == "yes":
            num = input("Number for",firstName,lastName,"(no (), - or spaces)")
            yesNo = input("Is",num,"the correct number for",firstName,lastName + "? (y/n)")
            
            if yesNo.lower().strip() == "y" or yesNo.lower().strip() == "yes":
                addContact(firstName,lastName,num)
        

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
    
    