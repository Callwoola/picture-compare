#coding:utf-8


import cv2
import numpy as np
from matplotlib import pyplot as plt
def test_2():
    # http://docs.opencv.org/3.1.0/d4/dc6/tutorial_py_template_matching.html
    # find 找图例子
    img_rgb = cv2.imread('origin_material.jpg')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('find.png',0)
    w, h = template.shape[::-1]

    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where( res >= threshold)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
    cv2.imwrite('res.png',img_rgb)



def test_one():
    img = cv2.imread('orgin_brick.jpg',0)
    img2 = img.copy()
    img2 = img.copy()
    template = cv2.imread('brick.png',0)
    w, h = template.shape[::-1]

    # All the 6 methods for comparison in a list
    methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
               'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
    for meth in methods:
        img = img2.copy()
        method = eval(meth)

        # Apply template Matching
        res = cv2.matchTemplate(img,template,method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
            bottom_right = (top_left[0] + w, top_left[1] + h)

        cv2.rectangle(img,top_left, bottom_right, 255, 2)
        plt.subplot(121),plt.imshow(res,cmap = 'gray')
        plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
        plt.subplot(122),plt.imshow(img,cmap = 'gray')
        plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
        plt.suptitle(meth)
        plt.show()

def test_3():
    import urllib2
    import io

    url = "http://i.gzdmc.net/images/bd2888edd41a951de1ab8cbfb33c82e2.jpg@1e_400w_400h_1c_0i_1o_90Q_1x.png";
    res = urllib2.urlopen(url)
    # save data into Bytes
    imimage = io.BytesIO(res.read())

    nparr = np.fromstring(imimage.read(), np.uint8)
    img = cv2.imdecode(nparr, cv2.CV_LOAD_IMAGE_COLOR)
    print dir(img)
    height, width, channels = img.shape
    print height
    print width
    print channels
    # img = cv2.imread()
    mask = np.zeros(img.shape[:2],np.uint8)

    bgdModel = np.zeros((1,65),np.float64)
    fgdModel = np.zeros((1,65),np.float64)

    rect = (0, 0, height - 1 ,width - 1)
    cv2.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)
    mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
    img = img*mask2[:,:,np.newaxis]
    
    plt.imshow(img),plt.colorbar(),plt.show()

    # # newmask is the mask image I manually labelled
    # newmask = cv2.imread('orgin_brick.jpg',0)
    # # whereever it is marked white (sure foreground), change mask=1
    # # whereever it is marked black (sure background), change mask=0
    # mask[newmask == 0] = 0
    # mask[newmask == 255] = 1
    # mask, bgdModel, fgdModel = cv2.grabCut(img,mask,None,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_MASK)
    # mask = np.where((mask==2)|(mask==0),0,1).astype('uint8')
    # img = img*mask[:,:,np.newaxis]
    # plt.imshow(img),plt.colorbar(),plt.show()
def test_find_cycle():    
    cap = cv2.VideoCapture(0)

    while(1):
        
        # Take each frame
        _, frame = cap.read()
        
        # Convert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # define range of blue color in HSV
        lower_blue = np.array([110,50,50])
        upper_blue = np.array([130,255,255])
        
        # Threshold the HSV image to get only blue colors
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        
        # Bitwise-AND mask and original image
        res = cv2.bitwise_and(frame,frame, mask= mask)
        
        cv2.imshow('frame',frame)
        cv2.imshow('mask',mask)
        cv2.imshow('res',res)
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break        
    cv2.destroyAllWindows()
test_3()
