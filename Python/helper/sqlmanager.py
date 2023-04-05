import sqlalchemy as db
import os

metadata = db.MetaData()

Users = db.Table('Users', metadata,
            db.Column('Id', db.Integer(),primary_key = True, autoincrement=True),
            db.Column('telegramid', db.String(),primary_key = False),
            db.Column('Money', db.Float, nullable = False)
            )

def init():
    engine = db.create_engine('sqlite:///./userdata/data.sqlite')
    conn = engine.connect()
    metadata.create_all(engine)
    conn.close()

# Create User
def createuser(telegramid):
    engine = db.create_engine('sqlite:///./userdata/data.sqlite')
    conn = engine.connect()
    output = conn.execute("SELECT telegramid FROM Users WHERE telegramid =?", (telegramid,)).fetchone()
    print(output)
    if  output != None:
        return False
    
    query = db.insert(Users).values(telegramid = telegramid, Money = 0.0)
    conn.execute(query)
    conn.close()
    if not os.path.isdir("./userdata/" + str(telegramid)):
        os.mkdir("./userdata/" + str(telegramid))
    return True

# All users
def allusers():
    engine = db.create_engine('sqlite:///./userdata/data.sqlite')
    conn = engine.connect()
    output = conn.execute("SELECT telegramid FROM Users").fetchall()
    conn.close()
    return output