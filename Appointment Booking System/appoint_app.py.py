from flask import Flask,render_template,request  #session
import mysql.connector as mysql
from twilio.rest import Client

db = mysql.connect(
    host = 'localhost',
    user = 'root',
    password = 'root',
    database='db'
)

cursor = db.cursor()

app=Flask(__name__)

@app.route('/')
def user_page(): #Handler
    return render_template('index.html')

@app.route('/admin')
def admin_page():
    cursor.execute(" SELECT * FROM DETAILS ")
    result = cursor.fetchall()
    db.commit()
    data = []
    for i in result:
        data.append(i)
    return render_template('admin.html',res = data)

# @app.route('/user')
# def result_page(): #Handler
#     return render_template('index.html')

@app.route('/collect',methods=['POST']) #Collect the data(Handler)  
def collectData():
    n = request.form['name']
    m = request.form['mob']
    dt = request.form['time']
    k=getdetails(n,m)
    if k:
        sql = 'DELETE FROM DETAILS WHERE name = %s'
        val = (n,)
        cursor.execute(sql,val)
        db.commit()
        storedata(n,m,dt)
        return render_template('index.html',res = (n+" "+"Request Sent"))
    else:
        storedata(n,m,dt)
        r = "Data Request Sent"
        return render_template('index.html',res=r)

@app.route('/getdata',methods=['GET','POST'])
def getdatafromdb():
    cursor.execute("SELECT * FROM DETAILS")
    result = cursor.fetchall()
    data = []
    for i in result:
        data.append(i)
    for i in data:
        print(i)
    return render_template('admin.html',res = data)

@app.route('/collectcheck',methods=['GET','POST'])
def checkstatus():
    mobnum = request.form['chkmob']
    print(mobnum)
    sql = 'SELECT * FROM DETAILS WHERE mobile = %s'
    val = (mobnum,)
    cursor.execute(sql,val)
    result = cursor.fetchone()
    if result:
        m = result[3]
        n = result[2]
        print(m)
        if m == "Approved":
            return render_template('index.html',res2 = m,res3="at",res4=n)
        elif m == 'Rejected':
            return render_template('index.html',res2 = m)
        else:
            return render_template('index.html',res2 = "Decision Pending")
    else:
        return render_template('index.html',res2 = "INVALID CREDITIONALS")

 
@app.route('/collectmob',methods=['POST']) #Collect the data(Handler)  
def collectData1():
        m = request.form['mob']
        st = request.form['status']
        print(st)
        if st == 'approve':
            k = 'Approved'
            sql = "UPDATE DETAILS SET status = %s WHERE mobile = %s"
            val = (k,m)
            cursor.execute(sql,val)
            db.commit()
            msg(k)
            return render_template('admin.html',res1=k)
        elif st == 'reject':
            kn = 'Rejected'
            sql = "UPDATE DETAILS SET status = %s WHERE MOBILE = %s"
            val = (kn,m)
            cursor.execute(sql,val)
            db.commit()
            msg(kn)
            return render_template('admin.html',res1=kn)
        elif st == "assign":
            dt = request.form['time']
            k = 'Approved'
            sql = "UPDATE DETAILS SET status = %s WHERE mobile = %s"
            val = (k,m)
            cursor.execute(sql,val)
            db.commit()
            sql = "UPDATE DETAILS SET datetime  = %s WHERE MOBILE = %s"
            val = (dt,m)
            cursor.execute(sql,val)
            db.commit()
            x = dt[8:10]+'-'+dt[5:7]+'-'+dt[0:4]+" , "+dt[11:]
            acc_sid = "AC5b1993aac683426f386a6975b4a2a2f1"
            auth_token = "6b6d0c571b5e8eba1b65bf297b2da8d0"
            client = Client(acc_sid, auth_token)

            client.messages.create(
                to = "whatsapp:+919347917379",
                from_ = "whatsapp:+14155238886",
                body = k+" at "+x)
            return render_template('admin.html',res1 = k)
       
def getdetails(name,mob):
    cursor.execute("SELECT * FROM details WHERE name = %s AND mobile = %s",(name,mob))
    result=cursor.fetchone()
    return result
    
def msg(x):
    acc_sid = "AC5b1993aac683426f386a6975b4a2a2f1"
    auth_token = "6b6d0c571b5e8eba1b65bf297b2da8d0"
    client = Client(acc_sid, auth_token)

    client.messages.create(
        to = "whatsapp:+919347917379",
        from_ = "whatsapp:+14155238886",
        body = x+", Please check the Status in Portal")

        
def storedata(name,mob,datetime): #Private function not a handler
    sql = "INSERT INTO DETAILS (name,mobile,datetime) VALUES (%s,%s,%s)"
    val = (name,mob,datetime)
    cursor.execute(sql,val)
    db.commit()

if __name__=="__main__":

    app.run(debug=True) 