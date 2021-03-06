import RPi.GPIO as GPIO
import json
import paho.mqtt.client as mqtt
import time


thread = None

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

ir = 15
ir2 = 18

mqttc = mqtt.Client()
mqttc.connect("128.107.70.30") #<--- Please change IP to match the location of your MQTT broker
# 192.168.195.7 was IR 829 Broker
mqttc.loop_start()

GPIO.setup(ir, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(ir2, GPIO.IN, GPIO.PUD_DOWN)

start = 0
stop = 0

def data_collect():
    GPIO.add_event_detect(ir, GPIO.FALLING, callback=post_score, bouncetime=200)
    GPIO.add_event_detect(ir2, GPIO.RISING, callback=post_speed, bouncetime=200)

def post_score(channel):
    global start
    start = time.time();
    print("Start time is:")
    print(start);
    brokerMessage = {'Status': 'scored', 'Player': '2', 'Score': 1, 'Data': '0'}
    print("message sent")
    mqttc.publish("foosball/score", json.dumps(brokerMessage))

def post_speed(channel):
    global stop
    stop = time.time();
    print("Stop time is:")
    print(stop);
    if stop > start:
        elapsed = stop-start
        print("Elapsed time is:")
        print(elapsed)
        speed = .0345/elapsed #meters per second
        mph = 2.23694*speed #convert meters/s to mph
        print("posting speed")
        print(mph)
        brokerMessage = {'Status': 'speed', 'Speed':mph}
        mqttc.publish("foosball/speed", json.dumps(brokerMessage))

# while GPIO.input(ir)==0:
#     start = time.time();
#     print("Start time is:")
#     print(start);

# while GPIO.input(ir)==1:
#     print("speedRead is")
#     print(speedRead)
#     if speedRead is False:
        

if __name__ == '__main__':
    data_collect()
    print("started")
