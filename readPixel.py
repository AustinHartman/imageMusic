from PIL import Image
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
from collections import OrderedDict
from PIL import Image


# open and load image
def setImage(file):
    img = Image.open(file)
    size = img.size
    if (size[0] * size[1] > 400):
        img = img.resize((16, 16), Image.ANTIALIAS)
    return img


def pixAvg(size, pix, w, h):
    sum = 1
    res = list(pix[w, h])
    if (w < 15):
        sum += 1
        res = [x+y for x, y in zip(list(pix[w+1, h]), res)]
    if (w > 0):
        sum += 1
        res = [x+y for x, y in zip(list(pix[w-1, h]), res)]
    if (h < 15):
        sum += 1
        res = [x+y for x, y in zip(list(pix[w, h+1]), res)]
    if (h > 0):
        sum += 1
        res = [x+y for x, y in zip(list(pix[w, h-1]), res)]

    return tuple([i/sum for i in res])



img = setImage('something.jpg')
size = img.size
pix = img.load()


# Red: length of note
# Green: frequency of note
# Blue: loudness of note

# takes in pixel frequency and determines the closest not ranging from c3-b4
def getClosestFrequency(greenVal):
    # can select different note freq array for diff range and/or flat sharp combo of notes
    note_frequencies = [131, 147, 165, 175, 196, 220, 247,
                        262, 294, 330, 349, 392, 440, 494]
    #note_frequencies = [82, 87, 98, 110, 123, 131]
    f = (greenVal/255)*(note_frequencies[-1]-note_frequencies[0]) + note_frequencies[0]

    prev = note_frequencies[0]
    for n in note_frequencies[1:]:
        if (f >= prev and f <= n):
            if (abs(f-prev) > abs(f-n)):
                return n
            else:
                return prev
        prev = n

    return note_frequencies[-1]


def getNoteLength(l):
    note_lengths = ((1, 0.9),
                    (0.5, 0.7),
                    (0.25, 0.5),
                    (0.125, 0.3),
                    (0.0625, 0.1))

    prev = note_lengths[0]
    for n in note_lengths[1:]:
        if (l <= prev[1] and l >= n[1]):
            if (abs(l-prev[1]) > abs(l-n[1])):
                return n[0]
            else:
                return prev[0]
        prev = n

    return note_lengths[-1][0]


# builds sinusoidal wave at certain frequency
def genWave(pix):
    r=pix[0]
    g=pix[1]
    b=pix[2]

    loudness = (b/255)*7900 + 100

    # sample rate also not factored in due to its impact on freq, will reimplement differently
    noteLength = getNoteLength(r/255) # sample rate
    fs = 44100
    f = getClosestFrequency(g) # the frequency of the signal
    x = range(fs) # the points on the x axis for plotting
    stopHere = int(len(x) * noteLength)

    # compute the value (amplitude) of the sin wave at the for each sample
    ### WAVE EQUATIONS
    # Note: many of these equations alter the notes frequency... i think
    #s = [ 8000*( np.sin( np.cos(2*np.pi*f * (i/fs))*3 ) ) for i in x]
    ### This one sounds like a bagpipe
    #s = [ 8000*( np.sin(   np.cos(np.cos(np.cos( 2*np.pi*f*(i/fs))*3 )*4 )*3 )*2  ) for i in x]
    ### arctic monkeys - this wave resembles their logo
    #s = [ 8000*( np.sin( np.cos((2*np.pi*f * (i/fs)) / 25) *np.sin(2*np.pi*f * (i/fs)) ) ) for i in x[:stopHere]]
    ### square wave - seems to create fuller less airy notes
    s = [ loudness * ( np.sin(2*np.pi*f * (i/fs)) + np.sin((2*np.pi*f * (i/fs))*3)/3 + np.sin((2*np.pi*f * (i/fs))*7)/7 \
        +np.sin((2*np.pi*f * (i/fs))*9)/9 ) for i in x[:stopHere]]
    # just dont use
    #s = [ 8000 * ( np.sin((2*np.pi*f * (i/fs)*25)) + np.sin(3*(2*np.pi*f * (i/fs))) + \
    #    np.sin(5*(2*np.pi*f * (i/fs))) ) for i in x]
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
i = 1
for w in range(size[0]):
    for h in range(size[1]):
        print(i)
        i+=1
        #p = pixAvg(size, pix, w, h)
        data = data + genWave(pix[w, h])

data = np.array(data)
data = data.astype(np.int16)

show_info("data", data)
wavfile.write('something.wav', 44100, data)
drawGraph(data[:100], "something.png")
