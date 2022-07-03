import numpy as np
import matplotlib.pyplot as plt
from poly2d import *


# get the surface fit class and initialize for 64 x 64 chip
p2d = poly2d(64,64)


###
# Read in two frames, N frames apart
inframe = 0
N = 13
indat= np.fromfile('/Users/hg/data/process_hyti/scan_1000_sub', dtype=np.uint16).reshape(2000,512,320)
frame0 = indat[inframe,:,:]
frame1 = indat[inframe+N,:,:]

# extract the 64 x 64 subscene from each of the two frames
frame0_sub = frame0[300:364,140:204]
frame1_sub = frame1[300:364,140:204]

# fit a 2d surface to each subscene, then subtract that surface from the subscene to get a zero meaned, detrended image
p2d.fit(frame0_sub)
f0 = frame0_sub - p2d.zfit
p2d.fit(frame1_sub)
f1 = frame1_sub - p2d.zfit


f = plt.figure()
f.add_subplot(1,2,1)
plt.imshow (f0)
f.add_subplot(1,2,2)

# get the fft, take the complex conjugate the 1st, then multiply the two resulting complex arrays
fft0 = np.fft.fft2(f0)
fft0c = np.conj(fft0)
fft1 = np.fft.fft2(f1)
fcross = fft0c * fft1
# inverse fft
ifcross = np.fft.ifft2(fcross)

# find the location of the maximum  array.
maxloc = np.argmax(np.abs(ifcross))

print (maxloc/64.)
yoffset = int (maxloc/64.)
ave_y = float(yoffset) / N
xoffset = maxloc - (yoffset * 64)
ave_x = float (xoffset) / N
print ('Xoffset : ', ave_x)
print ('Yoffset : ', ave_y)
plt.imshow(f1)
plt.show()