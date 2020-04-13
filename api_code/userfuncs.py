import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from dotenv import load_dotenv
from werkzeug.security import check_password_hash,generate_password_hash

class userfuncs:

    def __init__(self,username,pswrd):
        self.username=username
        self.password=pswrd

    def insert_user(self):
        engine = create_engine(os.getenv("DATABASE_URL"))
        db = scoped_session(sessionmaker(bind=engine))
        hash = generate_password_hash(self.password)
        print(hash)
        print(check_password_hash(hash, 'c1234'))
        try:
            # execquery=db.execute("SELECT * FROM users").fetchall()
            insertqry=db.execute("INSERT INTO users (username,pssword,userstatus) VALUES (:usr,:pswrd,:sttus)",{"usr":self.username,"pswrd":hash,"sttus":"active"})
            # print(execquery)
            db.commit()
        except Exception as e:
            print (e)
    @staticmethod
    def validate_login(usrnme,psswrd):
        engine = create_engine(os.getenv("DATABASE_URL"))
        db = scoped_session(sessionmaker(bind=engine))
        usrqry=db.execute("SELECT * FROM users WHERE username=:username",{"username":usrnme}).fetchall()
        if len(usrqry)==0:
            raise Exception('Auth Failed')
        else:
            # print(usrqry)
            for rw in usrqry:
                validpass=check_password_hash(rw['pssword'], psswrd)
                print(validpass)
                return validpass


if __name__=='__main__':
    if os.getenv('environment') != 'PROD':
        load_dotenv()
    try:
        userfuncs.validate_login('test1','test1')
    except Exception as e:
        print(e)

