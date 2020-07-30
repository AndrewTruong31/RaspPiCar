import motorControl as motor


motor.motorVals()

def findWeightedLine(center):
    if(len(center) > 0):
        seg1 = 0.05 * center[0][0]
    else:
        seg1 = 0

    if(len(center) > 1):
        seg2 = 0.1 * center[1][0]
    else:
        seg2 = 0

    if(len(center) > 2):
        seg3 = 0.5 * center[2][0]
    else:
        seg3 = 0

    if(len(center) > 3):
        seg4 = 0.35 * center[3][0]
    else:
        seg4 = 0

    sum = int(seg1 + seg2 + seg3 + seg4)
    sum -= 320 

    if(sum < 0):
        dir = "Go Left"
    if(sum >= 0):
        dir = "Go Right"

    print("Weighted Average: " + str(sum) + "   >   " + dir)


def printCenterPoints(center):
    print(str(center[0]) + " " + str(center[1]) + " " + str(center[2]) + " " + str(center[3]))
    print(center[0][1])