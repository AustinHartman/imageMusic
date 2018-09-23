from PIL import Image
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt


img = Image.open('abstract.jpeg')
pix = img.load()
s = img.size

# Red: length of note
# Green: frequency of note
# Blue: loudness of note

def genWave(pix):
    r=pix[0]
    g=pix[1]
    b=pix[2]

    loudness = (b/255)*7900 + 100
    fs = (r/255)*4500 + 500 # sample rate
    f = 0.15666*fs*(g/255) + 0.01*fs # the frequency of the signal

    x = np.arange(fs) # the points on the x axis for plotting
    # compute the value (amplitude) of the sin wave at the for each sample
    s = [ loudness*(np.sin(2*np.pi*f * (i/fs))) for i in x]
    s = np.array(s)
    s = s.astype(np.int16)
    return s

def show_info(aname, a):
    print ("Array", aname)
    print ("shape:", a.shape)
    print ("dtype:", a.dtype)
    print ("min, max:", a.min(), a.max())
    print()

def drawGraph(data, file):
    x = np.arange(len(data))
    fig, ax = plt.subplots()
    ax.plot(x, data)
    ax.grid()
    fig.savefig(file)

data = np.array([])
data = data.astype(np.int16)
# traverse the img pixel by pixel left to right
for w in range(s[0]):
    for h in range(s[1]):
        data = np.concatenate([ data, genWave(pix[w,h]) ])

show_info("data", data)
wavfile.write('imgSong.wav', 5512, data)
drawGraph(data, "graph.png")
