import json
from flask import Flask, jsonify, request
import requests
import json
import time

app = Flask(__name__)
@app.route("/hello", methods=["GET"])
def hello():
   return "DataParser is ready!!!"

@app.route("/", methods=["POST"])
def home():
   start_time = time.time()
   result=""
   try:
      req = request.get_json() 
      jsondata=req
      temp_data=jsondata.copy()
      del temp_data["BatteryData"]
      battery_data=jsondata.copy()
      del battery_data["TemperatureData"]
      temp_data=json.dumps(temp_data)
      battery_data=json.dumps(battery_data)
      headers = {
      'Content-Type': 'application/json',
      'Ce-Specversion': '1.0',
      'Ce-Type': 'temperature',
      'Ce-Source': 'poc',
      'Ce-Id': '1'
      }
      print(temp_data)

      #r = requests.post('http://broker-ingress.knative-eventing.svc.cluster.local/default/default', data=temp_data, headers=headers)
      r = requests.post('http://kafka-broker-ingress.knative-eventing.svc.cluster.local/default/my-demo-kafka-broker', data=temp_data, headers=headers)
      # response_time_temp = time.time()
      # response_difference_for_temp = response_time_temp -  start_time
      # print(response_difference_for_temp)
      
      if r.status_code != 200:
        print ("Error:", r.status_code)

      headers = {
        'Content-Type': 'application/json',
        'Ce-Specversion': '1.0',
        'Ce-Type': 'battery',
        'Ce-Source': 'poc',
        'Ce-Id': '1'
        }
      print(battery_data)
   
      r = requests.post('http://kafka-broker-ingress.knative-eventing.svc.cluster.local/default/my-demo-kafka-broker', data=battery_data, headers=headers)
      response_time = time.time()
      response_difference = response_time -  start_time
      print(response_difference)
      #r = requests.post('http://broker-ingress.knative-eventing.svc.cluster.local/default/default', data=battery_data, headers=headers)
      if r.status_code != 200:
            print ("Error:", r.status_code)

      result = {"message": "DataParser", "response_difference": response_difference}

   except Exception as err:
      result = {"message": "Error", "error": str(err)}
   return jsonify(result)

# driver function
if __name__ == '__main__':

   app.run(host="0.0.0.0",port=2000)