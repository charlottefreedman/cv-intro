from numpy import sign
import cv2

directions = {
    -1 : "right",
    1: "left",
    0 : "forward"

}

strafe = {
    -1 : "right",
    1: "left",
    0 : "forward"

}




def get_lane_center(lane):
    
    if len(lane) == 2:
        center = (lane[0][1] + lane[1][1])/2 
        slope = (1/((1/lane[0][0] + 1/lane[1][0])/2))

        return (center, slope)
    
    return (0,0)

def get_center_line(center, slope, screen_height):
    if slope == 0:
        return [0,0,0, 0, 0, 0]
    topX = ((-1 * screen_height) + slope * center)/slope
    return [0,0,topX, 0, center, screen_height]

def draw_center(img, line):
    temp_img = img
    x1 = int(line[2])
    y1 =int(line[3])
    x2 = int(line[4])
    y2 =int(line[5])
    cv2.line(temp_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
    return temp_img    

def recommend_direction(center, slope, screenCenter, lane, cameraWidth):
    # check if midpoint is in the center of the screen if so go forward
    if center == None or slope == None:
        return directions[1]
    if center < 1000 and center > 750 and (sign(lane[0][0]) != sign(lane[1][0])):
        return "forward"
    else:
        diff = screenCenter - center
        return f"{directions[sign(slope)]} {diff * cameraWidth/110} degrees strafe {strafe[sign(diff)]}"
        