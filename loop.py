import time
import requests
import json
from time import sleep
import logging
import subprocess

logging.basicConfig(filename='./history_from_{}.log'.format(time.time()))

MY_KEY = # input your robot key here
NUM_GPU = 4

url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=" + MY_KEY
headers = {"Content-Type": "text/plain"}

def send(msg):
    data = {
      "msgtype": "text",
      "text": {
         "content": msg,
         "mentioned_list":[],
         "mentioned_mobile_list":[]
      }
    }
    r = requests.post(url=url, headers=headers, json=data)
    #logging.info
    print("\nSend 1 message: "+r.text)

def get_nvidia_smi():
    msg = ""
    _output = subprocess.check_output(["nvidia-smi"]).decode("utf-8").split()
    for i,idx in enumerate([59+j*27 for j in range(NUM_GPU)]):
        if int(_output[idx][:-3]) < 100:
            msg += "GPU {} free:\n{}\n".format(i, ''.join(_output[idx:idx+3]))
        else:
            msg += "GPU {} busy:\n{}\n".format(i, ''.join(_output[idx:idx+3]))
    return msg

check_every_s = float(input("check every () minute?")) * 60
send("hello. will send you gpu status every {} minute".format(check_every_s / 60))

#while input("\ncontinue?")!='n':
while True:
    send(get_nvidia_smi())
    sleep(check_every_s)
