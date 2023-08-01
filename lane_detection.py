import cv2
import numpy as np
import matplotlib.pyplot as plt

def get_array_x_int(elem):
    return elem[1]

def detect_lines(img, threshold1=50, threshold2=150, apertureSize=3,minLineLength=100,maxLineGap=10):
    
    img = cv2.GaussianBlur(img, (9, 9), 0)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # convert to grayscale
    _,bw = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY)

    edges = cv2.Canny(bw, threshold1, threshold2, apertureSize) # detect edges
    lines = cv2.HoughLinesP(
                    edges,
                    rho=1,
                    theta=np.pi/180,
                    threshold =100,
                    minLineLength=minLineLength,
                    maxLineGap=maxLineGap,
            ) # detect lines
    return lines

def draw_lines(img, lines, color = (0, 255,0)):
    temp_img = img
    for line in lines:
        if type(line) == None:
            return img
        x1, y1, x2, y2 = line[0]
        cv2.line(temp_img, (x1, y1), (x2, y2), color, 2)

    return temp_img

    
def get_slopes_intercepts(lines, screen_height):
    slopes = []
    xints = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        if x2 == x1:
            slope = None
            xInt = x1
        else:
            slope = (y2 - y1)/(x2 - x1)
            if y2 == y1:
                xInt = None
            else:
                xInt = (screen_height-y1 + slope*x1)/slope

        slope.append(slope)
        xInt.append(xInt)

    return (slopes, xints)

def detect_lanes(lines, screen_height):

    #MERGE LINES
    lanes = []

    for line in lines:
        if type(line) != None:

            #print(line[0])
            x1, y1, x2, y2 = line[0]
            deltaY = y2 - y1
            if x2 == x1:
                slope = None
                xInt = x1
            else:
                slope = (y2 - y1)/(x2 - x1)
                if y2 == y1:
                    xInt = None
                else:
                    xInt = (screen_height - y1)/slope + x1
            if slope != None and xInt != None and deltaY != 0:
                lanes.append([slope, xInt, x1, y1, x2, y2])

    cleanedLines = []
    for line in lanes:
        canAdd = True
        for cleanedLine in cleanedLines:
            if abs(cleanedLine[0] - line[0]) < 0.5:
                canAdd = False

        if canAdd:
            cleanedLines.append(line)
    # DONE MERGING LINES
    #------
    # DELETE LINES NOT PART OF A LANE

    sorted_lines = cleanedLines
    sorted_lines.sort(key=get_array_x_int)
    if len(sorted_lines) > 2:  
        oneToZero = sorted_lines[1][1] - sorted_lines[0][1]
        twoToOne = sorted_lines[2][1] - sorted_lines[1][1]

        if(twoToOne < oneToZero):
            sorted_lines.pop(0)
        if len(sorted_lines) % 2 != 0:
            sorted_lines.pop(len(sorted_lines) - 1)
    # DONE DELETING LINES NOT IN LANE
    #------
    #PAIR LINES

    pairs = []
    if len(sorted_lines) >= 2:
        #pair 
        for i in range(0,len(sorted_lines)-1, 2):
            pairs.append([sorted_lines[i],sorted_lines[i+1]])
    #print(pairs)

    if len(pairs) > 0:
        if len(pairs) % 2 == 0: 
            center_lane = pairs[int((len(pairs))/2) -1]
        else:
            center_lane = pairs[int((len(pairs) + 1)/2) - 1]
        #print(center_lane)
    else:
        return []


    return center_lane

def draw_lanes(img, lanes):
    temp_img = img
    
    for line in lanes:
        if type(line) == None:
            return img
        x1 = line[2]#USING CONVENTION FROM DETECT_LANES
        y1 =line[3]
        x2 = line[4]
        y2 =line[5]
        cv2.line(temp_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
    return temp_img