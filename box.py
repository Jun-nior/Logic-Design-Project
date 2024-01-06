import tkinter as tk
import PIL
from PIL import Image, ImageTk, ImageOps
import cv2
from urllib.request import urlopen
import numpy as np
from tkinter import messagebox, Canvas
from keras.models import load_model
import time
import requests
import threading

def up():
    print("Up")

def left():
    print("Left")

def right():
    print("Right")

def down():
    print("Down")

def automatic():
    print("Automatic")


def print_AI_result():
    AI_result=image_detector()
    command, confident_score=AI_result
    AI_stream.delete(1.0, tk.END)
    cs_stream.delete(1.0, tk.END)
    AI_stream.insert(tk.END, "AI Result: " + command)
    cs_stream.insert(tk.END, f"Confident score:  + {confident_score}")
    


# Flag to determine whether to update the video or not
streaming = False
first_time = True
streaming_lock = threading.Lock()
# check ip address function
def check_ip():
    global first_time
    if first_time:
        input_ip=entry_var.get()
        if input_ip == '192.168.2.43':
            toggle_stream()
            first_time=False
        else:
            messagebox.showerror("Invalid IP Address", "Please enter a valid IP address.")
    else:
        toggle_stream()


# Function to start/stop the video stream
def toggle_stream():
    global streaming
    with streaming_lock:
        streaming = not streaming

# Function to update the displayed video frame
def update_video():
    if streaming:
        # Replace this URL with the actual URL for your ESP32 camera stream
        url = "http://192.168.2.43/capture"
        
        # Read the video frame from the ESP32 camera
        img_resp = urlopen(url)
        img_arr = np.array(bytearray(img_resp.read()), dtype=np.uint8)
        frame = cv2.imdecode(img_arr, -1)

        # Convert the OpenCV BGR image to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Convert the NumPy array to a Tkinter-compatible PhotoImage
        image = Image.fromarray(rgb_frame)
        photo = ImageTk.PhotoImage(image=image)

        # Update the canvas with the new video frame
        canvas.config(image=photo)
        canvas.image = photo

        #give prediction and print the result
        # prediction()
        # print_AI_result()
        time.sleep(1)
        
        

    # Schedule the next update after a delay (in milliseconds)
    canvas.after(1, update_video)
    

img_url = 'http://192.168.2.43/capture'
control_url = 'http://192.168.2.43/control?ai_camera='
counter = 0
model = load_model('C://Trung Main//231//Logic Design Project//trained_signs//keras_model.h5')

def image_detector():
    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is
    # determined by the first position in the shape tuple, in this case 1.
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    # Replace this with the path to your image
    image = Image.open('Image//greenland_' + str(counter) +'.png')
    #resize the image to a 224x224 with the same strategy as in TM2:
    #resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(image, size, PIL.Image.Resampling.LANCZOS)

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
    #assign default value for max confidence
    max_index = 0
    max_confidence = output[0]
    #find the maximum confidence and its index
    for i in range(1, len(output)):
        if max_confidence < output[i]:
            max_confidence = output[i]
            max_index = i
    print(max_index, max_confidence)
    file = open("C://Trung Main//231//Logic Design Project//trained_signs//labels.txt",encoding="utf8")
    data = file.read().split("\n")
    print("AI Result: ", data[max_index])
    #client.publish("ai", data[max_index])
    return data[max_index],max_confidence

#image = cv2.imread('Pics/greenland_' + str(counter) +'.png')

counter = 0
def prediction():
    global streaming
    while True:
        while streaming:
            print("Capturing...", counter)
            #counter = counter + 1
            response = requests.get(img_url)
            if response.status_code:
                fp = open('Image//greenland_' + str(counter) +'.png', 'wb')
                fp.write(response.content)
                fp.close()
                #image = cv2.imread('Pics//greenland_' + str(counter - 1) +'.png')
                #cv2.imshow('AI Camera', response.content)
                result = image_detector()
                print_AI_result()
                # requests.get(control_url + result)

            time.sleep(1)

# Create the main window
root = tk.Tk()

# Set the size of the window to 1000x500
root.geometry("1000x500")

# Create a frame with size 320x240
frame_video = tk.Frame(root, width=320, height=240, bd=2, relief=tk.SOLID)
frame_video.pack_propagate(False)
frame_video.place(relx=0.25, rely=0.4, anchor="center")  # Center the frame
# frame_video.pack()

# Create a canvas inside the frame
canvas = tk.Label(frame_video, width=320, height=240)
canvas.pack()


# Create an Entry widget for the IP address
frame_ip=tk.Frame(root)
frame_ip.place(relx=0.25, rely=0.7, anchor="center")

entry_var = tk.StringVar()
entry_ip = tk.Entry(frame_ip, width=20, textvariable=entry_var)
entry_ip.grid(row=0, column=0, padx=5)


# Create a frame for the button
frame_button = tk.Frame(root)
frame_button.pack(pady=10)
frame_button.place(relx=0.25, rely=0.8, anchor="center")

# Create a button to start/stop the video stream
btn_toggle_stream = tk.Button(frame_button, text="Start/Stop Stream", command=check_ip)
btn_toggle_stream.pack()

# button up
frame_up = tk.Frame(root)
frame_up.pack(pady=10)
frame_up.place(relx=0.75, rely=0.3, anchor="center")
up_stream = tk.Button(frame_up, text="Up", command=up, width=10)
up_stream.pack()

#button down
frame_down = tk.Frame(root)
frame_down.pack(pady=10)
frame_down.place(relx=0.75, rely=0.4, anchor="center")
down_stream = tk.Button(frame_down, text="Down", command=down, width=10)
down_stream.pack()

#button left
frame_left = tk.Frame(root)
frame_left.pack(pady=10)
frame_left.place(relx=0.65, rely=0.4, anchor="center")
left_stream = tk.Button(frame_left, text="Left", command=left, width=10)
left_stream.pack()

#button right
frame_right = tk.Frame(root)
frame_right.pack(pady=10)
frame_right.place(relx=0.85, rely=0.4, anchor="center")
right_stream = tk.Button(frame_right, text="Right", command=right, width=10)
right_stream.pack()

#button automatic
frame_automatic = tk.Frame(root)
frame_automatic.pack(pady=10)
frame_automatic.place(relx=0.75, rely=0.5, anchor="center")
automatic_stream = tk.Button(frame_automatic, text="Automatic Run", command=automatic, width=40)
automatic_stream.pack()

#print AI result
frame_ai=tk.Frame(root)
frame_ai.pack(pady=10)
frame_ai.place(relx=0.75, rely=0.6, anchor="center")
AI_stream = tk.Text(frame_ai, height=1, width=30)
AI_stream.pack()

#print confident score
frame_cs=tk.Frame(root)
frame_cs.pack(pady=10)
frame_cs.place(relx=0.75, rely=0.7, anchor="center")
cs_stream = tk.Text(frame_cs, height=1, width=30)
cs_stream.pack()

# Call the update_video function to start displaying the video feed
update_video_thread = threading.Thread(target=update_video)
prediction_thread = threading.Thread(target=prediction)

update_video_thread.start()
prediction_thread.start()


# Run the Tkinter event loop
root.mainloop()

