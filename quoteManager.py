#used for creating and sending pregenerated quotes
import sqlite3

conn2 = sqlite3.connect("quotes.db")
c2 = conn2.cursor()

def createQuoteTable():
    c2.execute("""CREATE TABLE IF NOT EXISTS quotes (
                quote text
            )""")
    conn2.commit()
    
def storeQuote(text):
    c2.execute("INSERT INTO quotes VALUES (?)",(text,))
    conn2.commit()

def showQuotes():
    c2.execute("SELECT * FROM quotes")
    quotes = c2.fetchall()
    for q in quotes:
        print(q[0])
        
def deleteQuote():
    c2.execute("SELECT rowid,* FROM quotes")
    quotes = c2.fetchall()
    for q in quotes:
        print(q[0],": ",q[1])
    idToDelete = int(input("Select the number corresponding to the quote you would like to delete."))
    c2.execute("DELETE FROM quotes WHERE rowid=?",(idToDelete,))