import os
from flask import Flask,render_template,make_response,jsonify,request
from dotenv import load_dotenv
from mongofunctions import mongoFuncs
from userfuncs import userfuncs
# from flask.ext.bcrypt import Bcrypt

if os.getenv('environment')!='PROD':
    load_dotenv()

app = Flask(__name__)
srcmongoobj=mongoFuncs(app,os.getenv('MONGODB'))
targetmongoobj=mongoFuncs(app,os.getenv('TARGETDB'))


@app.route('/')
def index():
    return os.getenv('environment')

@app.route('/querydata')
def queryData():

    resp=None
    try:

        otptlst=[]
        print('-------------------------')
        otpt = targetmongoobj.emptyTable('users')
        # for v in otpt:
        #     otptlst.append(v)
        print(otpt)
    except Exception as e:
        print(e)


    resp = make_response(jsonify(done='done'), 200)
    return resp

@app.route('/syncdb')
def syncData():
    
    resp=None
    isValid=True

    
    try:
       
        usr = request.authorization.username
        pswrd = request.authorization.password
        isValid=userfuncs.validate_login(usr,pswrd)
        
        if isValid:
            pass
        else:
            
            print('Error: Auth Failed..')
            raise Exception('Auth Failed')
    except Exception as e:
        print(f'error: {e}')
        isValid = False
        resp=make_response(jsonify(error=str(e)), 401)

    

    if isValid:
        
        progress = []
        try:

            for collname in srcmongoobj.collectionNames:
                otpt = srcmongoobj.getAllTable(collname)
                targetmongoobj.emptyTable(collname)
                inserted = targetmongoobj.insertData(collname, otpt)
                progress.append(collname)
            resp = make_response(jsonify(status='completed',progress=progress), 200)
        except Exception as e:
            print(f'error: {e}')
            resp=make_response(jsonify(error=str(e),progress=progress), 500)

    

    return resp

@app.route('/upsert')
def upsertData():
    pass


if __name__=='__main__':
    app.run(host='0.0.0.0')