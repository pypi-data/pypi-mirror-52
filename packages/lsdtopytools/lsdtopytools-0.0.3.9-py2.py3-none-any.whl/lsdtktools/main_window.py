from tkinter import *
from tkinter import PhotoImage, Canvas
import numpy as np
import pandas as pd
from PIL import Image, ImageTk
from matplotlib import cm

class Window(Frame):
  def __init__(self, master=None, width = 400, height = 300):
    Frame.__init__(self, master)               
    self.master = master
    self.width = width
    self.height = height
    self.init_window()
    # self.canvas = Canvas(self, width=width, height=height, bg="#000000")
    # self.canvas.pack(expand=YES, fill=BOTH)


  def init_window(self, title = "LSDTopoTools"):

    self.master.title(title)
    self.pack(fill=BOTH, expand=1)
    self.master.geometry("%sx%s"%(self.width,self.height))

  def plot_array(self, array):
    # im = Image.fromarray(np.array([[20,50,50,20],[35,35,250,2]]))
    # newarr = np.resize(array,(self.height,self.width))
    im = Image.fromarray(np.uint8(cm.gist_earth(array)*255))
    im.save("test.png")
    img = ImageTk.PhotoImage(im)
    # print(img)
    label = Label(image=img) 
    label.image = img # keep a reference!
    label.pack(expand = YES, fill=BOTH)


