import cv2
import numpy as np
import matplotlib.pyplot as plt

def get_x_int(elem):
    return elem[1]

def detect_lines(img, threshold1=50, threshold2=150, apertureSize=3, 
                 minLineLength=100, maxLineGap=10):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # convert to grayscale
    edges = cv2.Canny(gray, threshold1, threshold2, apertureSize) # detect edges
    lines = cv2.HoughLinesP(
                edges,
                rho = 1,
                theta = np.pi/180,
                threshold = 100,
                minLineLength=minLineLength,
                maxLineGap=maxLineGap
        ) # detect lines
    return lines

def draw_lines(img, lines, color=(0, 102, 255)):
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(img, (x1, y1), (x2, y2), color, 2)

    return img

def get_slopes_intercepts(lines): #only X-intercept
    slopes = []
    xInts = []
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
                xInt = ((slope * x1) - y1) / slope

        slopes.append(slope)
        xInts.append(xInt)

    return (slopes, xInts)

def detect_lanes(lines):
    lanes = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        deltaY = abs(y2 - y1)
        if x2 == x1:
            slope = None
            xInt = x1
        else:
            slope = (y2 - y1)/(x2 - x1)
            if y2 == y1:
                xInt = None
            else:
                xInt = ((slope * x1) - y1) / slope
        if slope != None and xInt != None and deltaY != 0:
            lanes.append([slope, xInt, x1, y1, x2, y2])
        
    cleanedLines = []
    for line in lanes:
        canAdd = True
        for cleanedLine in cleanedLines:
            if abs(cleanedLine[1] - line[1]) < 0.1:
                canAdd = False

        if canAdd:
            cleanedLines.append(line)

    sorted_lines = []
    sorted_lines = cleanedLines
    sorted_lines.sort(key=get_x_int)

    dist1 = abs(sorted_lines[1][1] - sorted_lines[0][1])
    dist2 = abs(sorted_lines[2][1] - sorted_lines[1][1])
    pairs = []

    if dist1 > dist2:
        sorted_lines.pop(0)
    if len(sorted_lines) % 2 != 0:
        sorted_lines.pop(len(sorted_lines) - 1)
    if len(sorted_lines) >= 2:
        for i in range(0, len(sorted_lines)-1, 2):
            pairs.append([sorted_lines[i], sorted_lines[i+1]])

    return pairs

def draw_lanes(img, lanes):
    temp = img
    for lines in lanes:
        for line in lines:
            x1 = line[2]
            y1 = line[3]
            x2 = line[4]
            y2 = line[5]
            cv2.line(img, (x1, y1), (x2, y2), (0, 102, 255), 2)
    return temp

        


