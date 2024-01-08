from customtkinter import *
import tkinter
import random
import time
import threading
import requests
from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
#import cv2
from Adafruit_IO import MQTTClient
import paho.mqtt.client as mqtt



def up():
    print("Up")
    client.publish("mecanum-behavior", "up")

def left():
    print("Left")
    client.publish("mecanum-behavior", "left")

def right():
    print("Right")
    client.publish("mecanum-behavior", "right")

def down():
    print("Down")
    client.publish("mecanum-behavior", "down")

def automatic():
    print("Automatic")
    client.publish("mecanum-behavior", "auto")

set_appearance_mode("dark")
set_default_color_theme("dark-blue")

app = CTk()
app.geometry("1100x600")

CONTROL_BUTTON_COLOR = "#6600ff"
CONTROL_BUTTON_HOVER = "#4158D0"
CONRTROL_BUTTON_RADIUS = 30
controlFrame= CTkFrame(
    master=app,
    width=350,
    height=200,
    fg_color="transparent"
)

controlFrame.place(
    relx=0.4,
    rely=0.05
)

controlArmFrame = CTkFrame(
    master=app,
    width=250,
    height=200,
    fg_color="transparent"
)
controlArmFrame.place(
    relx=0.75,
    rely=0.05
)

def verticalArmEvent(verticalArmValue):
    print(verticalArmValue)
    client.publish(AIO_FEED_ID[2], str(int(verticalArmValue)))

verticalArmSlider = CTkSlider(
    master=controlArmFrame,
    width=250,
    height=20,
    progress_color="#666699",
    button_color="#ccccff",
    from_=0,
    to=90,
    command=verticalArmEvent,
    number_of_steps=90,
)
verticalArmSlider.place(
    relx=0,
    y=40,
    anchor="nw"
)

verticalArmLabel = CTkLabel(
    master=controlArmFrame,
    width=80,
    height=30,
    justify=tkinter.CENTER,
    fg_color="#ff5050",
    text="VERTICAL ARM",
    corner_radius=20,
)
verticalArmLabel.place(
    relx=0,
    rely=0,
    anchor="nw"
)

horizontalArmLabel = CTkLabel(
    master=controlArmFrame,
    width=80,
    height=30,
    justify=tkinter.CENTER,
    fg_color="#ff5050",
    text="HORIZONTAL ARM",
    corner_radius=20
)
horizontalArmLabel.place(
    relx=0,
    y=70,
    anchor="nw"
)

HORIZONTAL_ARM_0 = 0
HORIZONTAL_ARM_1 = 50
HORIZONTAL_ARM_2 = 45
def horizontalArmEvent(horizontalArmValue):
    # client.publish(AIO_FEED_ID[], "right")
    # global HORIZONTAL_ARM_0, HORIZONTAL_ARM_1, HORIZONTAL_ARM_2
    # HORIZONTAL_ARM_0 = HORIZONTAL_ARM_1
    # HORIZONTAL_ARM_1 = HORIZONTAL_ARM_2
    # HORIZONTAL_ARM_2 = int(horizontalArmValue)
    # if HORIZONTAL_ARM_0 == HORIZONTAL_ARM_1 and HORIZONTAL_ARM_1 == HORIZONTAL_ARM_2:
    client.publish(AIO_FEED_ID[3], str(int(horizontalArmValue)))

horizontalArmSlider = CTkSlider(
    master=controlArmFrame,
    width=250,
    height=20,
    progress_color="#666699",
    button_color="#ccccff",
    from_=0,
    to=90,
    command=horizontalArmEvent,
    number_of_steps=90
)
horizontalArmSlider.place(
    relx=0,
    y=110,
    anchor="nw"
)

straightButton = CTkButton(
    master=controlFrame,
    width=100,
    height=50, 
    text="UP",
    fg_color=CONTROL_BUTTON_COLOR,
    corner_radius=CONRTROL_BUTTON_RADIUS,
    hover_color=CONTROL_BUTTON_HOVER,
    command=up
)
straightButton.place(
    relx=0.5, 
    y=50/2,
    anchor="center"
)

downButton = CTkButton(
    master=controlFrame,
    width=100,
    height=50, 
    text="BACK",
    fg_color=CONTROL_BUTTON_COLOR,
    corner_radius=CONRTROL_BUTTON_RADIUS,
    hover_color=CONTROL_BUTTON_HOVER,
    command=down
)
downButton.place(
    relx=0.5, 
    y=70,
    anchor="n"
)

leftButton = CTkButton(
    master=controlFrame,
    width=100,
    height=50, 
    text="LEFT",
    fg_color=CONTROL_BUTTON_COLOR,
    corner_radius=CONRTROL_BUTTON_RADIUS,
    hover_color=CONTROL_BUTTON_HOVER,
    command=left
)
leftButton.place(
    x=5, 
    y=70
)


rightButton = CTkButton(
    master=controlFrame,
    width=100,
    height=50, 
    text="RIGHT",
    fg_color=CONTROL_BUTTON_COLOR,
    corner_radius=CONRTROL_BUTTON_RADIUS,
    hover_color=CONTROL_BUTTON_HOVER,
    command=right
)
rightButton.place(
    x=345, 
    y=70 + 50/2,
    anchor="e"
)

automaticButton = CTkButton(
    master=controlFrame,
    width=340,
    height=50, 
    text="AUTOMATIC",
    fg_color=CONTROL_BUTTON_COLOR,
    corner_radius=CONRTROL_BUTTON_RADIUS,
    hover_color=CONTROL_BUTTON_HOVER,
    command=automatic
)
automaticButton.place(
    relx=0.5, 
    y=140,
    anchor="n"
)

imageInfoFrame = CTkFrame(
    master=app,
    width=350,
    height=250,
    fg_color="transparent"
)
imageInfoFrame.place(
    relx=0.48,
    rely=0.45
)

imageInfoLabelsFrame = CTkFrame(
    master=app,
    width=80,
    height=250,
    fg_color="transparent"
)
imageInfoLabelsFrame.place(
    relx=0.4,
    rely=0.45
)

confidentScoreLabelsFrame = CTkFrame(
    master=app,
    width=80,
    height=250,
    fg_color="transparent"
)
confidentScoreLabelsFrame.place(
    relx=0.8,
    rely=0.45
)

confidentLeftBar = CTkProgressBar(
    master=imageInfoFrame,
    width=350,
    height=30,
    progress_color="#cc00cc"
)
confidentLeftBar.place(
    relx=0,
    rely=0,
    anchor="nw"
)

confidentRightBar = CTkProgressBar(
    master=imageInfoFrame,
    width=350,
    height=30,
    progress_color="#0000ff"
)
confidentRightBar.place(
    relx=0,
    y=50,
    anchor="nw"
)

confidentUpBar = CTkProgressBar(
    master=imageInfoFrame,
    width=350,
    height=30,
    progress_color="#00ff00"
)
confidentUpBar.place(
    relx=0,
    y=100,
    anchor="nw"
)

confidentStopBar = CTkProgressBar(
    master=imageInfoFrame,
    width=350,
    height=30,
    progress_color="#ff1a1a"
)
confidentStopBar.place(
    relx=0,
    y=150,
    anchor="nw"
)

confidentUturnBar = CTkProgressBar(
    master=imageInfoFrame,
    width=350,
    height=30,
    progress_color="#ff9933"
)
confidentUturnBar.place(
    relx=0,
    y=200,
    anchor="nw"
)

confidentLeftLabel = CTkLabel(
    master=imageInfoLabelsFrame,
    width=80,
    height=30,
    fg_color="#cc3300",
    text="LEFT",
    justify=tkinter.CENTER,
    corner_radius=20,
)
confidentLeftLabel.place(
    relx=0,
    rely=0,
    anchor="nw"
)

confidentRightLabel = CTkLabel(
    master=imageInfoLabelsFrame,
    width=80,
    height=30,
    fg_color="#cc3300",
    text="RIGHT",
    justify=tkinter.CENTER,
    corner_radius=20,
)
confidentRightLabel.place(
    relx=0,
    y=50,
    anchor="nw"
)

confidentUpLabel = CTkLabel(
    master=imageInfoLabelsFrame,
    width=80,
    height=30,
    fg_color="#cc3300",
    text="UP",
    justify=tkinter.CENTER,
    corner_radius=20,
)
confidentUpLabel.place(
    relx=0,
    y=100,
    anchor="nw"
)

confidentStopLabel = CTkLabel(
    master=imageInfoLabelsFrame,
    width=80,
    height=30,
    fg_color="#cc3300",
    text="STOP",
    justify=tkinter.CENTER,
    corner_radius=20,
)
confidentStopLabel.place(
    relx=0,
    y=150,
    anchor="nw"
)

confidentUturnLabel = CTkLabel(
    master=imageInfoLabelsFrame,
    width=80,
    height=30,
    fg_color="#cc3300",
    text="U-TURN",
    justify=tkinter.CENTER,
    corner_radius=20,
)
confidentUturnLabel.place(
    relx=0,
    y=200,
    anchor="nw"
)

confidentScoreLeftVar = StringVar()
confidentScoreLeftLabel = CTkLabel(
    master=confidentScoreLabelsFrame,
    width=80,
    height=30,
    textvariable=confidentScoreLeftVar,
    justify=tkinter.CENTER
)
confidentScoreLeftLabel.place(
    relx=0,
    rely=0,
    anchor="nw"
)

confidentScoreRightVar = StringVar()
confidentScoreRightLabel = CTkLabel(
    master=confidentScoreLabelsFrame,
    width=80,
    height=30,
    textvariable=confidentScoreRightVar,
    justify=tkinter.CENTER
)
confidentScoreRightLabel.place(
    relx=0,
    y=50,
    anchor="nw"
)

confidentScoreUpVar = StringVar()
confidentScoreUpLabel = CTkLabel(
    master=confidentScoreLabelsFrame,
    width=80,
    height=30,
    textvariable=confidentScoreUpVar,
    justify=tkinter.CENTER
)
confidentScoreUpLabel.place(
    relx=0,
    y=100,
    anchor="nw"
)

confidentScoreStopVar = StringVar()
confidentScoreStopLabel = CTkLabel(
    master=confidentScoreLabelsFrame,
    width=80,
    height=30,
    textvariable=confidentScoreStopVar,
    justify=tkinter.CENTER
)
confidentScoreStopLabel.place(
    relx=0,
    y=150,
    anchor="nw"
)

confidentScoreUturnVar = StringVar()
confidentScoreUturnLabel = CTkLabel(
    master=confidentScoreLabelsFrame,
    width=80,
    height=30,
    textvariable=confidentScoreUturnVar,
    justify=tkinter.CENTER
)
confidentScoreUturnLabel.place(
    relx=0,
    y=200,
    anchor="nw"
)

cameraFrame = CTkFrame(
    master=app,
    width=400,
    height=400
)
cameraFrame.place(
    relx=0.03,
    rely=0.05
)

controlCameraFrame = CTkFrame(
    master=app,
    width=400,
    height=100
)
controlCameraFrame.place(
    relx=0.03,
    rely=0.75
)

inputIPCamEntry = CTkEntry(
    master=controlCameraFrame,
    placeholder_text="Input IP of camera",
    #state="disabled",
    justify=tkinter.CENTER,
    width=400,
    height=50,
)
inputIPCamEntry.place(
    relx=0,
    rely=0,
    anchor="nw"
)

camSwitchVar = StringVar(value="off")
def takeCamIP():
    if camSwitchVar.get() == "on":
        global img_url
        img_url = "http://" + inputIPCamEntry.get() + "/capture"
        print(img_url)
onOffCamSwitch = CTkSwitch(
    master=controlCameraFrame,
    width=100,
    height=20,
    text="start/stop stream",
    fg_color="#cc0000",
    progress_color="#009900",
    command=takeCamIP,
    variable=camSwitchVar,
    onvalue="on",
    offvalue="off"
)
onOffCamSwitch.place(
    relx=0.5,
    rely=0.7,
    anchor="center"
)
AIresultFrame = CTkFrame(
    master=app,
    width=500,
    height=100
)
AIresultFrame.place(
    relx=0.4,
    rely=0.88
)

AIresultNameLabel = CTkLabel(
    master=AIresultFrame,
    width=100,
    height=50,
    text="AI RESULT",
    fg_color="#ff5050",
    font=("Helvetica", 17, "bold"),
    justify=tkinter.CENTER,
    corner_radius=20
)
AIresultNameLabel.place(
    relx=0,
    rely=0,
    anchor="nw"
)


##################### PROCESS #####################
AIO_KEY = "aio_AqXF50XhVsRavK3GlO6rBmd34V1V"
AIO_USERNAME = "Unray"
AIO_FEED_ID = ["aicamera", "mecanum-behavior", "vertical-arm", "horizontal-arm"]
BROKER_ADDRESS = "192.168.4.5"
CONFIDENCE = 0.1
OUPUT_PREDICT_SCORE = [0, 0, 0, 0, 0]
###### ADAFRRUIT ######
def connected(client):
    print("Connected to adafruit")
    for topic in AIO_FEED_ID:
        client.subscribe(topic)

def subscribe(client , userdata , mid , granted_qos):
    print("Subscribe successfully ...")

def disconnected(client):
    print("Disconnected ...")
    sys.exit (1)

def message(client , feed_id , payload):
    print("Send to adafruit " + payload)

# client = MQTTClient(AIO_USERNAME , AIO_KEY)
# client.on_connect = connected
# client.on_disconnect = disconnected
# client.on_message = message
# client.on_subscribe = subscribe
# client.connect()
# client.loop_background()

###########local brocker###########
def on_connect(client, userdata, flags, rc): 
    print("Connected to broker " + BROKER_ADDRESS)

def on_message(client, userdata, msg):
    print(f"From broker: (topic) {msg.topic} (payload) ({str(msg.payload)})")

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed: " "include message: "+ str(mid))

def on_publish(mosq, obj, mid):
    print(f"Mesage {mid} has been sent to broker")

# client = mqtt.Client()
# client.on_connect = on_connect
# client.on_message = on_message
# client.on_subscribe = on_subscribe
# client.on_publish = on_publish
# client.connect(BROKER_ADDRESS, 1883, 60)
# client.subscribe("test", 0)
# client.publish("test", "hello")
def mqttConnect():
    global client
    #client.loop_forever()
mqttThread = threading.Thread(target=mqttConnect)
mqttThread.start()


#img_url = 'http://192.168.98.215/capture'
img_url = 'http://192.168.1.6/capture'
#control_url = 'http://192.168.1.6/control?ai_camera='
counter = 0
MODEL_FOLDER = 'C://Users//PCPV//Desktop//Code//LogicDesign//model//'
model = load_model(MODEL_FOLDER + 'keras_model.h5')


def image_detector():
    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is
    # determined by the first position in the shape tuple, in this case 1.
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    # Replace this with the path to your image
    image = Image.open('Images//greenland_' + str(counter) +'.png')
    #resize the image to a 224x224 with the same strategy as in TM2:
    #resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.LANCZOS)

    #turn the image into a numpy array
    image_array = np.asarray(image)
    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    # Load the image into the array
    data[0] = normalized_image_array

    # run the inference
    prediction = model.predict(data)
    #get the 1D array
    output = prediction[0]
    global OUPUT_PREDICT_SCORE
    OUPUT_PREDICT_SCORE = output
    print(OUPUT_PREDICT_SCORE)
    #assign default value for max confidence
    max_index = 0
    max_confidence = output[0]
    #find the maximum confidence and its index
    for i in range(1, len(output)):
        if max_confidence < output[i]:
            max_confidence = output[i]
            max_index = i
    print(max_index, max_confidence)
    #take confidence
    global CONFIDENCE
    CONFIDENCE = max_confidence
    file = open(MODEL_FOLDER + "labels.txt",encoding="utf8")
    data = file.read().split("\n")
    print("AI Result: ", data[max_index])
    #client.publish("ai", data[max_index])
    return data[max_index]

#image = cv2.imread('Pics/greenland_' + str(counter) +'.png')
img0 = 0
img1 = 1
img2 = 2
img3 = -1
sendToAda = 0
pressCounter = 5
def imageProcess(imgResult):
    global img0, img1, img2, img3
    img0 = img1
    img1 = img2

    img2 = imgResult
    if img0 == img1 and img1 == img2:
        if img3 != img2:
            img3 = img2
            #if img2 > -1:
            global pressCounter
            pressCounter = 5
            return 1
        else:
            #if img3 > -1:
            pressCounter = pressCounter - 1
            print(f"counter :{pressCounter}")
            if pressCounter == 0:
                pressCounter = 5
                return 1
            #return 1#same pressed state -> use old data -> do not send to ada
    return -1 #do not send to ada
        
counter = 0

def main():
    print("Capturing...")
    while True:
        #counter = counter + 1
        if camSwitchVar.get() == "on":
            print("Capturing...", counter)
            global sendToAda
            response = requests.get(img_url)
            if response.status_code:
                fp = open('Images//greenland_' + str(counter) +'.png', 'wb')
                fp.write(response.content)
                fp.close()
                #image = cv2.imread('Pics//greenland_' + str(counter - 1) +'.png')
                #cv2.imshow('AI Camera', response.content)

                result = image_detector()
                print(result[0])
                if CONFIDENCE > 0.98:
                    sendToAda = imageProcess(int(result[0]))

                if sendToAda == 1:
                    client.publish(AIO_FEED_ID[0], result)
                    sendToAda = 0

                #requests.get(control_url + result)
        time.sleep(1)


def updateConfidentScore():
    while True:
        global OUPUT_PREDICT_SCORE
        upScore = OUPUT_PREDICT_SCORE[2]
        confidentUpBar.set(upScore)
        confidentScoreUpVar.set(str(round(upScore * 100, 3))+ " %")
        
        rightScore = OUPUT_PREDICT_SCORE[1]
        confidentRightBar.set(rightScore)
        confidentScoreRightVar.set(str(round(rightScore * 100, 3))+ " %")

        leftScore = OUPUT_PREDICT_SCORE[0]
        confidentLeftBar.set(leftScore)
        confidentScoreLeftVar.set(str(round(leftScore * 100, 3))+ " %")

        stopScore = OUPUT_PREDICT_SCORE[3]
        confidentStopBar.set(stopScore)
        confidentScoreStopVar.set(str(round(stopScore * 100, 3))+ " %")

        uturnScore = OUPUT_PREDICT_SCORE[4]
        confidentUturnBar.set(uturnScore)
        confidentScoreUturnVar.set(str(round(uturnScore * 100, 3))+ " %")
        time.sleep(0.3)

one = threading.Thread(target=updateConfidentScore)
mainThread = threading.Thread(target=main)
mainThread.start()
one.start()
app.mainloop()

print("hello")