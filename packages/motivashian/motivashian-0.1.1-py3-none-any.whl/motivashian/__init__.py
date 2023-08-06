from mss import mss
import tkinter as tk
from PIL import Image, ImageTk
import imageio
import numpy as np
import time
from playsound import playsound
import multiprocessing

path_files = __file__+"/../"

def sound():
    playsound(path_files+'doitnow.mp3')

def make_mask(imarray):
    R,G,B = imarray[:,:,0], imarray[:,:,1], imarray[:,:,2]
    mask = (G < 100) |  (R>G) | (B>G)
    return mask

root = tk.Tk()
root.wm_attributes("-topmost", True)
root.wm_attributes("-fullscreen", True)

video = imageio.get_reader(path_files+'doitnow.mkv')
nb_frame = video.count_frames()
fps = video.get_meta_data()['fps']
dt_video = 1/fps #time interval between two frames

with mss() as sct:
    sct_img = sct.grab(sct.monitors[0])
    background = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")

def stream(ind):
    t0 = time.time()

    if ind+1 > nb_frame: #Close if end of video is reached
        root.destroy()
        return

    imv = video.get_data(ind)

    mask = make_mask(imv)
    frame = background.copy()
    frame.paste(Image.fromarray(imv), (0,0), Image.fromarray(mask))

    imTk = ImageTk.PhotoImage(frame)
    label.config(image=imTk)
    label.image = imTk

    dt = time.time() - t0
    jump = int(1 + dt // dt_video) #If the video is not render suficiently fast will skip frames
    dt_wait = jump*dt_video - dt
    root.after(int(dt_wait*1000), stream, ind+jump)

label = tk.Label(root)
label.pack()

start_t = time.time()

player = multiprocessing.Process(target=sound) # create process
player.start()
stream(0)
root.mainloop()
video.close()
player.terminate()
