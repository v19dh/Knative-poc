from flask import Flask, request
import mysql.connector
import json
from cloudevents.http import from_http
import time

app = Flask(__name__)
is_dev=False
@app.route("/hello", methods=["GET"])
def display_databases():
    result=""
    try:
        conn=GetDBConnection()
        print(conn)
        c=conn.cursor()
        c.execute('show databases;')
        result=c.fetchall()
        conn.close()
    except Exception as err:
        result = err
    return f'<h1>Hello - {result} </h1>'

@app.route("/service", methods=["GET"])
def display_service_status():
    return "Temperature service is running"

@app.route("/", methods=["POST"])
def home():
    start_time = time.time()
    # result=""
    if request.method.upper() == "GET":
        return "Welcome to Knative world!"
    try:
        event = from_http(request.headers, data=request.get_data())
        bdata=event.data
        if type(bdata)==bytes:
            bdata=eval(bdata.decode())
        print(bdata)
        id = bdata["BeaconId"]
        msg=f"Alert for beacon Id {id}"
        dt = bdata["Date"]
        volt=bdata['BatteryData']['Voltage']
        if volt<=2000 or volt>=3000:
            print('Sending alert..')
            UpdateDatabase(id,dt,volt,msg)
            response_time = time.time()
            response_difference = response_time -  start_time
            print(response_difference)

        responseData = {
        "data":{ "result":"success" },
        "datacontenttype": "application/json; charset=utf-8",
        "id": "MESSAGE_ID",
        "source": "//cloudaudit.googleapis.com/projects/PROJECT_ID/logs/data_access",
        "specversion": "1.0",
        "type": "reply",
        "response_difference" : response_difference
        }
        response = app.response_class(
            status=200,
            mimetype='application/cloudevents+json',
            response=json.dumps(responseData))
        return response
    except Exception as err:
        result = err
    return f'<h1>Hello - {result} </h1>'

def UpdateDatabase(id, dt, volt, msg):
    conn = GetDBConnection()
    cur = conn.cursor()
    cmd=f"INSERT INTO BatteryAlerts (Id,Date_time,batteryvoltage,Message) values ('{id}','{dt}','{volt}','{msg}')"
    print(cmd)
    cur.execute(cmd)
    conn.commit()
    print("executed....")
    conn.close()  

def GetDBConnection():
    if is_dev:
        conn=mysql.connector.connect(host='127.0.0.1', database='poc', user='dinesh', password='dinesh')
    else:
        conn=mysql.connector.connect(host='knative-poc-db.cojyo4snq6mh.us-east-1.rds.amazonaws.com', database='eksclusterdatabase', user='admin', password='knativerds',ssl_disabled=True)
    return conn

if __name__ == "__main__":
    import sys
    if (len(sys.argv) > 1):
        is_dev = True
    app.run(host='0.0.0.0',port=9000)