'''
/************************************************************************
 MIT License

 Copyright (c) 2018 Harsh Kakashaniya,Koyal Bhartia, Aalap Rana

 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:

 The above copyright notice and this permission notice shall be included in all
 copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 SOFTWARE.
 *************************************************************************/

/**
 *  @file    Challenge.py
 *  @author  Harsh Kakashaniya, Koyal Bhartia and Aalap Rana
 *  @date    13/3/2019
 *  @version 1.0
 *
 *  @brief Project 2,Lane Detection
 *
 *  @section DESCRIPTION
 *
 *  This is code has 3 parts,
 1. Pre Processing of image
 2. Perceptive transform
 3. Histogram for lane
 4. Integrate all 3 parts and  take inverse transfrorm
 *
 */
 '''
import argparse
import numpy as np
import os, sys
from numpy import linalg as LA
from numpy import linalg as la
from matplotlib import pyplot as plt
import math
from PIL import Image
import random

try:
    sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
except:
    pass
import cv2
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
# @brief Function for converting gray scale to binary
#
#  @param Matrix
#
#  @return Matrix
#
def binary(A):
    for i in range(0,len(A)):
        for j in range(0,len(A[0])):
            if (A[i,j]>230):
                A[i,j]=255
            else:
                A[i,j]=0
    return A
# @brief Function for taking perspective transform
#
#  @param Image Matrix
#
#  @return Transformed Matrix
#
def perspective_view(image):
    #sequence tl,tr,br,bl
    dst1 = np.array([
        [0,720],
        [0, 0],
        [1280,0],
        [1280,720]], dtype = "float32")

    source=np.array([
        [0+150,720-80],
        [0+570, 450],
        [1280-570,450],
        [1280-50,720-80]], dtype = "float32")


    M1,status = cv2.findHomography(source, dst1)

    warp1 = cv2.warpPerspective(image, M1, (1280,720))
    #warp2=cv2.medianBlur(warp1,3)
    blur=cv2.GaussianBlur(warp1.copy(),(5,5),0)
    smooth=cv2.addWeighted(blur,1.5,warp1,-0.5,0)
    #bin=binary(warp1)
    return smooth

def lanedetect(image):
    count=0
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if(image[i,j]==255):
                count=count+1
        if (count>10):
            break
    return count
# @brief Function for get back inverse perspective transform
#
#  @param Image Matrix
#
#  @return Transformed Matrix
#
def inverseperceptive(image):
    dst1 = np.array([
        [0,720],
        [0, 0],
        [1280,0],
        [1280,720]], dtype = "float32")

    source=np.array([
        [0+150,720-80],
        [0+570, 450],
        [1280-570,450],
        [1280-50,720-80]], dtype = "float32")



    M1,status = cv2.findHomography(dst1,source,)
    warp1 = cv2.warpPerspective(image.copy(), M1, (1280,720))
    warp2=cv2.medianBlur(warp1,3)

    return warp2
# @brief Function for Undistorting image
#
#  @param Image Matrix
#
#  @return Transformed Matrix
#
def Undistort(image):
    dist = np.mat([ -2.42565104e-01 , -4.77893070e-02 , -1.31388084e-03 , -8.79107779e-05,
        2.20573263e-02])

    K = np.mat([[  1.15422732e+03 , 0.00000000e+00  , 6.71627794e+02],
     [  0.00000000e+00 ,  1.14818221e+03  , 3.86046312e+02],
     [  0.00000000e+00 ,  0.00000000e+00  , 1.00000000e+00]])

    destination = cv2.undistort(image, K, dist, None, K)

    return destination
# @brief Function for Extracting ROI
#
#  @param Image Matrix
#
#  @return Transformed Matrix
#
def ExtractROI(image):
    black=np.zeros((360,1280))

    # Crop image
    imageROI = image[360:720,0:1280]
    black=np.concatenate((black, imageROI), axis=0)
    return black
# @brief Function for yellow lane detection
#
#  @param Image Matrix, length and width of ROI
#
#  @return Transformed Matrix
#
def Yellowlane(image):

    hls = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)
    #lower = np.array([20, 100, 100])
    #upper = np.array([25, 255, 255])
    one=hls[:,:,1]
    two=hls[:,:,2]
    black=np.zeros((720,1280))
    for i in range(two.shape[0]):
        for j in range(two.shape[1]):
            if (two[i,j]>50):
                black[i,j]=255
    #ROI=ExtractROI(black)
    #clahe = cv2.createCLAHE(clipLimit=25.0, tileGridSize=(4,4))
    #cl12 = clahe.apply(two)

    #cl13=cv2.GaussianBlur(cl12,(9,9),0)
    #cl14 = cv2.inRange(cl13, 200, 255)

    #imageROI = black[400:720,0:1280]
    #HLS=cv2.bitwise_and(black,two)
    #lower = np.array([20, 120, 80])
    #upper = np.array([45, 200, 255])
    #mask = cv2.inRange(two, lower, upper)
    #HLS=cv2.bitwise_and(hls,hls,mask=mask)
    #bgr = cv2.cvtColor(HLS, cv2.COLOR_HLS2BGR)
    #gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    #transform_y=perspective_view(gray)
    #bit=cv2.bitwise_and(image,image,mask=mask).astype(np.uint8)
    #ROI=ExtractROI(mask)
    transform_y=perspective_view(black)
    return transform_y
#@brief Function for White lane detection
#
#  @param Image Matrix
#
#  @return Transformed Matrix
#
def Whitelane(image):
    kernel_size = 5
    blur_gray = cv2.GaussianBlur(image,(kernel_size, kernel_size),0)
    mask = cv2.inRange(blur_gray, 180, 255)
    #edges = cv2.Canny(gray,100,200)
    return mask
# @brief Function for getting Hough lines on image
#
#  @param Image Matrix and original image
#
#  @return Transformed Matrix
#
def Hough_lines(image,Original):
    width,height=image.shape
    #print(np.shape(image),"image")
    #print(np.shape(Original),"ORIG")

    edges = cv2.Canny(image, 100, 200)
    rho = np.ceil(np.sqrt(width*width+height*height))
    theta = np.pi/60
    threshold = 6
    min_line_length = 30
    max_line_gap = 25
    line_image = np.copy(Original) * 0
    lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]),min_line_length, max_line_gap)

    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(line_image,(x1,y1),(x2,y2),(255,0,0),5)

    #lines_edges = cv2.addWeighted(lines, 0.8, line_image, 1, 0)
    return line_image
# @brief Function for getting Histogram Silding
#
#  @param Image Matrix
#
#  @return left lane and right lane points
#
def Histogram(image):
    leftlane=[]
    rightlane=[]
    for j in range(10):
        c=72*(10-j)
        d=72*(9-j)
        for i in range(20):
            a=64*(i)
            b=64*(i+1)
            img=image[d:c,a:b]
            hist=lanedetect(img)
            if(hist>5 and i<10):
                leftlane=np.append(leftlane,[(c+d)/2,(a+b)/2])
            if(hist>4 and 20-i<10):
                rightlane=np.append(rightlane,[(c+d)/2,(a+b)/2])
    rangeleft=int(leftlane.shape[0]/2)
    rangeright=int(rightlane.shape[0]/2)

    left=np.reshape(leftlane,[rangeleft,2])
    right=np.reshape(rightlane,[rangeright,2])

    print(np.shape(left))
    print(np.shape(right))

    try:
        if(rightlane==[]):
            raise ValueError

    except ValueError:
        rightlane=np.append(rightlane,leftlane[0])
        rightlane=np.append(rightlane,leftlane[1]+800)
    rangeright=int(rightlane.shape[0]/2)
    right=np.reshape(rightlane,[rangeright,2])

    return image,left,right
# @brief Function for ploting on unwraped image
#
#  @param Image Matrix, Orignal Matrix, left lane, right lane
#
#  @return Transformed Matrix,slope
#
def plotlines(image,Original,left,right,polyfit_old,count):
    flag=1

    if(right.shape[0]>2):
        flag=0

    left_fit = np.polyfit(left[:,0], left[:,1], 2)
    right_fit = np.polyfit(right[:,0], right[:,1], 2)

    if (flag==0):
        left_fit[2]=right_fit[2]-700
        ploty = np.linspace(0, image.shape[0]-1, image.shape[0])
        left_fitx = right_fit[0]*ploty*ploty + right_fit[1]*ploty + left_fit[2]
        right_fitx =right_fit[0]*ploty*ploty + right_fit[1]*ploty + right_fit[2]
        center_line=(left_fit[0]*ploty*ploty+right_fit[0]*ploty*ploty)/2 + (left_fit[1]*ploty+right_fit[1]*ploty)/2 + (left_fit[2]+right_fit[2])/2
        black=Original*0
        for i in range(ploty.shape[0]):
            y=int(ploty[i])
            x_l=int(left_fitx[i])
            x_r=int(right_fitx[i])
            x_c=int(center_line[i])
            koko=(x_r-x_l)
            for i in range(koko):
                if(x_l+i>1280-1 or x_l+i<0 ):
                    break
                black[y,x_l+i]=[0,0,51]
        print('right')

    if (flag==1):
        right_fit[2]=left_fit[2]+700
        ploty = np.linspace(0, image.shape[0]-1, image.shape[0])
        left_fitx = left_fit[0]*ploty*ploty + left_fit[1]*ploty + left_fit[2]
        right_fitx =left_fit[0]*ploty*ploty + left_fit[1]*ploty + right_fit[2]
        center_line=(left_fit[0]*ploty*ploty+left_fit[0]*ploty*ploty)/2 + (left_fit[1]*ploty+left_fit[1]*ploty)/2 + (left_fit[2]+right_fit[2])/2
        black=Original*0
        for i in range(ploty.shape[0]):
            y=int(ploty[i])
            x_l=int(left_fitx[i])
            x_r=int(right_fitx[i])
            x_c=int(center_line[i])
            koko=(x_r-x_l)
            for i in range(koko):
                if(x_l+i>1280-1 or x_l+i<0 ):
                    break
                black[y,x_l+i]=[0,0,51]
        print('left')

    slope=(math.atan((right_fitx[720-50]-right_fitx[50])/620))*180/np.pi
    print(slope)
    polyfit_old=left_fit
    return black,slope,polyfit_old
# @brief Function for text input in the Image
#
#  @param Image Matrix, slope
#
#  @return Transformed Matrix
#
def Text(image,slope):
    slp=round(slope,2)
    info="Angle of turning is: "+str(np.abs(slp))+' degrees'
    cv2.putText(image,info,(350,100),cv2.FONT_HERSHEY_SIMPLEX,1,(51,0,0),3,cv2.LINE_AA)
    if(slp>0):
        cv2.putText(image,'Turn LEFT',(540,200),cv2.FONT_HERSHEY_SIMPLEX,1,(0,51,102),3,cv2.LINE_AA)
    elif(slp<0):
        cv2.putText(image,'Turn RIGHT',(540,200),cv2.FONT_HERSHEY_SIMPLEX,1,(51,102,0),3,cv2.LINE_AA)
    else:
        cv2.putText(image,'Go STRAIGHT',(540,200),cv2.FONT_HERSHEY_SIMPLEX,1,(51,0,102),3,cv2.LINE_AA)


    return image
#-------------------------------------------------------------------------------
def Imageprocessor(path):
    vidObj = cv2.VideoCapture(path)
    count = 0
    success = 1
    img_array=[]
    while (success):
        if (count==0):
            success, image = vidObj.read()
        width,height,layers=image.shape
        size = (width,height)
        image=Undistort(image)
        undist_img=image.copy()
        gray =cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        #image_y=Yellowlane(undist_img)
        transform_w=perspective_view(gray)
        image_w=Whitelane(transform_w)
        image_y=Yellowlane(undist_img)
        final_transform=image_w+image_y
        final_transform_original=final_transform.copy()
        Histo,leftlane,rightlane=Histogram(final_transform_original)
        if (count==0):
            back=[0,0]
        tr_with_lines,slope,back_n=plotlines(final_transform_original,undist_img,leftlane,rightlane,back,count)
        back=back_n

        global_lines=inverseperceptive(tr_with_lines)
        gray_merge=cv2.bitwise_or(undist_img,global_lines)
        result=cv2.addWeighted(undist_img,1,global_lines,1,0)
        Final=Text(result,slope)

        count += 1
        print(count)
        #cv2.imwrite('%d.jpg' %count,Final)
        img_array.append(Final)
        success, image = vidObj.read()

    return img_array,size

#video file
def video(img_array,size):
    video=cv2.VideoWriter('video.avi',cv2.VideoWriter_fourcc(*'DIVX'), 16.0,size)
    for i in range(len(img_array)):
        video.write(img_array[i])
    video.release()
# main
if __name__ == '__main__':

    # Calling the function
    Image,size=Imageprocessor('challenge_video.mp4')
    video(Image,size)
