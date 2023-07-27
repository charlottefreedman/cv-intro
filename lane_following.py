from numpy import sign

directions = {
    -1 : "right",
    1 : "left",
    0 : "forward"
}

def get_lane_center(pairs):
    if int((len(pairs))/2) - 1 > 0:
        if (len(pairs) % 2) == 0:
            middle_lane = pairs[int((len(pairs))/2) - 1]
        else:
            middle_lane = pairs[int((len(pairs) + 1)/2) - 1]
    else:
        return (None, None)
    center = (middle_lane[0][1] + middle_lane[1][1])/2
    slope = (middle_lane[0][0] + middle_lane[1][0])/2
    return(center, slope)

def recommend_direction(center, slope, screenCenter):
    if center == None or slope == None:
        return directions[0]
    elif abs(screenCenter - center) < 50:
        return directions[0]
    else:
        return directions[sign(slope)]