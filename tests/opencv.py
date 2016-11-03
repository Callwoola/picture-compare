import numpy as np
from matplotlib import pyplot as plt
import cv2

img = cv2.imread('/Users/liyang/Downloads/mQxZL0pz69ZbmfR8pSw70c7lmQgt4SI-3-fhhnxP9hUVLmIJSHmFsGWE_sifAkQv.jpg@1o.png',0)
edges = cv2.Canny(img,100,200)

plt.subplot(121),plt.imshow(img,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(edges,cmap = 'gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

plt.show()
