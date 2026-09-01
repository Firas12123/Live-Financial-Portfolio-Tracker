import sqlite3

class Database:
    def __init__(self, db_name="Portfolio.db"):
        self.db_name = db_name
        self.connection, self.cursor = self.db_sync()
    
    def db_sync(self):
        connection = sqlite3.connect(self.db_name)  # create the database and table
        cursor = connection.cursor()
        command1 = ("""CREATE TABLE IF NOT EXISTS portfolio(
                           buy_id INTEGER PRIMARY KEY,
                           symbol TEXT,
                           amount_invested FLOAT,
                           share_price FLOAT)""")
        cursor.execute(command1)
        connection.commit()
        return connection, cursor
    
    def db_assign(self, symbol, purchases):  # assign variables inputed into the database table
        for amount_invested, share_price in purchases:
            self.cursor.execute("INSERT INTO portfolio(symbol, amount_invested, share_price) VALUES(?,?,?)",(symbol, amount_invested, share_price))
            self.connection.commit()
    
    def db_clear_symbol(self,symbol):  # removes the row if we call to replace it
        self.cursor.execute("DELETE FROM portfolio WHERE symbol = ?", (symbol,))
        self.connection.commit()
    
    def df_reset(self):
        choice = input("Press [D] to confirm resetting your portfolio [ANY OTHER KEY] to return to the main menu\n").lower()
        if choice.strip() == "d":
            self.cursor.execute("DELETE FROM portfolio")
            self.connection.commit()
            print("Your table has been deleted")
    