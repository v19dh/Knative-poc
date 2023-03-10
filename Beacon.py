# from itertools import count
# import json,random,datetime,json,time,sys,radar,requests
# import http.client
# import json
# import logging
# import time


# # Set up the logging module
# logging.basicConfig(filename='BeaconSimulator', level=logging.INFO,
#                     format='%(asctime)s %(levelname)s %(message)s')

# Start_time = time.time()
# logging.info(f"Request {Start_time}")
# def Generate(beacon_id,n):
#     count=0
#     for i in range(n):
#         count+=1
#         def d():
#             return str(radar.random_datetime(start='2021-05-24T00:00:00', stop='2022-05-24T23:59:59'))
#         k=d()
#         l={'BeaconId': beacon_id,

#                 'Date':k,
#                 'TemperatureData':{'Temperature':random.randint(-30,140)},
#                 'BatteryData':{'Voltage':random.randint(1000,4000)}}
#         RequestToParser(l)
#         print (f"Data {count} posted to Parser")

# def RequestToParser(data):
#     conn = http.client.HTTPConnection("a45e75ea43fad4eba928eb9297c897f4-449558930.us-east-1.elb.amazonaws.com")
#     payload = json.dumps(data)
#     headers = {
#     'Content-Type': 'application/json',
#     'HOST': 'dataparserservice.default.34.199.164.178.sslip.io'
#     }
#     conn.request("POST", "/", payload, headers)
#     res = conn.getresponse()
#     data = res.read()
#     print(data.decode("utf-8"))



# if __name__ == '__main__':
#     n=len(sys.argv) 
#     if n > 1:
#         Generate(int(sys.argv[1]), int(sys.argv[2]))
#     else:
#         Generate(1,1)








# # datafunction()

# # for i in range(0,n):

# #     # if i==n:

# #         print(datafunction())

# #         time.sleep(sleeptime)
#------------------------------------------------------------------------------------
# import json
# import random
# import time
# import http.client
# import logging
# import sys
# import radar
# import multiprocessing

# # Set up the logging module
# logging.basicConfig(filename='BeaconSimulator', level=logging.INFO,
#                     format='%(asctime)s %(levelname)s %(message)s')

# Start_time = time.time()
# logging.info(f"Request {Start_time}")

# def generate_data(beacon_id, n):
#     for i in range(n):
#         timestamp = str(radar.random_datetime(start='2021-05-24T00:00:00', stop='2022-05-24T23:59:59'))
#         data = {
#             'BeaconId': beacon_id,
#             'Date': timestamp,
#             'TemperatureData': {'Temperature': random.randint(-30, 140)},
#             'BatteryData': {'Voltage': random.randint(1000, 4000)}
#         }
#         process_data(data)

# def process_data(data):
#     conn = http.client.HTTPConnection("a45e75ea43fad4eba928eb9297c897f4-449558930.us-east-1.elb.amazonaws.com")
#     payload = json.dumps(data)
#     headers = {
#         'Content-Type': 'application/json',
#         'HOST': 'dataparserservice.default.34.199.164.178.sslip.io'
#     }
#     conn.request("POST", "/", payload, headers)
#     res = conn.getresponse()
#     data = res.read()
#     print(data.decode("utf-8"))
  

# if __name__ == '__main__':
#     n = len(sys.argv)
#     if n > 2:
#         beacon_id = int(sys.argv[1])
#         n_requests = int(sys.argv[2])
#     else:
#         beacon_id = 1
#         n_requests = 1
        
#     processes = []
#     for i in range(n_requests):
#         process = multiprocessing.Process(target=generate_data, args=(beacon_id, 1))
#         processes.append(process)
#         process.start()
        
#     for process in processes:
#         process.join()





import json
import random
import time
import http.client
import logging
import sys
import radar
import multiprocessing
import datetime


# Set up the logging module
logging.basicConfig(filename='BeaconSimulator', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')

Start_time = time.time()





def generate_data(beacon_id, n):
    for i in range(n):
        timestamp = str(radar.random_datetime(start='2021-05-24T00:00:00', stop='2022-05-24T23:59:59'))
        data = {
            'BeaconId': beacon_id,
            'Date': timestamp,
            'TemperatureData': {'Temperature': random.randint(-30, 140)},
            'BatteryData': {'Voltage': random.randint(1000, 4000)}
        }
        process_data(data)

def process_data(data):
    conn = http.client.HTTPConnection("a45e75ea43fad4eba928eb9297c897f4-449558930.us-east-1.elb.amazonaws.com")
    payload = json.dumps(data)
    headers = {
        'Content-Type': 'application/json',
        'HOST': 'dataparserservice.default.34.199.164.178.sslip.io'
    }
    conn.request("POST", "/", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    now = datetime.datetime.now()
    print("Current date and time:", now)
    logging.info(f"Request {Start_time}")
 

if __name__ == '__main__':
    n = len(sys.argv)
    if n > 2:
        beacon_id = int(sys.argv[1])
        n_requests = int(sys.argv[2])
    else:
        beacon_id = 1
        n_requests = 1
        
    processes = []
    batch_size = 1000  # Send requests in batches of 1000
    
    for i in range(0, n_requests, batch_size):
        batch_end = min(i + batch_size, n_requests)
        batch_size = batch_end - i
        process = multiprocessing.Process(target=generate_data, args=(beacon_id, batch_size))
        processes.append(process)
        process.start()
        
    for process in processes:
        process.join()


