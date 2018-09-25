from PIL import Image
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt

# open and load image
img = Image.open('anotherPainting.jpg')
pix = img.load()
size = img.size

# Red: length of note
# Green: frequency of note
# Blue: loudness of note
note_frequencies = [131, 147, 165, 175, 196, 220, 247,
                    262, 294, 330, 349, 392, 440, 494]

# takes in pixel frequency and determines the closest not ranging from c3-b4
def getClosest(f):
    prev = note_frequencies[0]
    for n in note_frequencies[1:]:
        if (f >= prev and f <= n):
            if (abs(f-prev) > abs(f-n)):
                return n
            else:
                return prev
        prev = n

    return note_frequencies[-1]

# builds sinusoidal wave at certain frequency
def genWave(pix):
    r=pix[0]
    g=pix[1]
    b=pix[2]

    # currently loudness not factored in, so blueness doesn't relate to loudness
    loudness = (b/255)*7900 + 100

    # sample rate also not factored in due to its impact on freq, will reimplement differently
    l = (r/255)*4500 + 500 # sample rate
    fs = 44100
    f = getClosest( 370*(g/255) + 130) # the frequency of the signal
    x = np.arange(fs) # the points on the x axis for plotting
    # compute the value (amplitude) of the sin wave at the for each sample
    ### WAVE EQUATIONS
    # Note: many of these equations alter the notes frequency... i think
    #s = [ 8000*( np.sin( np.cos(2*np.pi*f * (i/fs))*3 ) ) for i in x]
    ### This one sounds like a bagpipe
    #s = [ 8000*( np.sin(   np.cos(np.cos(np.cos( 2*np.pi*f*(i/fs))*3 )*4 )*3 )*2  ) for i in x]
    ### arctic monkeys - this wave resembles their logo
    s = [ 8000*( np.sin( np.cos((2*np.pi*f * (i/fs)) / 25) *np.sin(2*np.pi*f * (i/fs)) ) ) for i in x]
    ### square wave - seems to create fuller less airy notes
    #s = [ 8000 * ( np.sin(2*np.pi*f * (i/fs)) + np.sin((2*np.pi*f * (i/fs))*3)/3 + np.sin((2*np.pi*f * (i/fs))*7)/7 \
    #    +np.sin((2*np.pi*f * (i/fs))*9)/9 ) for i in x]
    # just dont use
    #s = [ 8000 * ( np.sin((2*np.pi*f * (i/fs)*25)) + np.sin(3*(2*np.pi*f * (i/fs))) + \
    #    np.sin(5*(2*np.pi*f * (i/fs))) ) for i in x]
    #s = np.array(s)
    #s = s.astype(np.int16)
    return s

def show_info(aname, a):
    print ("Array:", aname)
    print ("shape:", a.shape)
    print ("dtype:", a.dtype)
    print ("min, max:", a.min(), a.max())

def drawGraph(data, file):
    x = np.arange(len(data))
    fig, ax = plt.subplots()
    ax.plot(x, data)
    ax.grid()
    fig.savefig(file)


print("this might take a few minutes...")

data = []
# traverse the img pixel by pixel left to right
for w in range(size[0]):
    for h in range(size[1]):
        data = data + genWave(pix[w,h])

data = np.array(data)
data = data.astype(np.int16)

show_info("data", data)
wavfile.write('pic2.wav', 44100, data)
drawGraph(data[:500], "pic2.png")
