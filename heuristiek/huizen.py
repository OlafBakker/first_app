"""
AMSETLHEAGE: A city width several houses in it. There are three types of
houses; onefamily-house, bugalow or Maison. Each house has specific
width and height (length and it has a minimum freestanding. The goal of
amstelheage is to put the houses in such a position to optimalize the
total freestanding and total value of the grid. Amstelheage is 120 m
by 160 m.
"""
from Tkinter import *
import sys
import math

# Waarde van een pixel in meters
PIXEL = 0.2

master = Tk()
# 1 pixel = 20 cm
w = Canvas(master, width=800, height=600)
w.pack()

def radians((x1, y1), (x2, y2)):
        """
        Given two points calculates the angle between the point in respect to point
        1. The angles are given like in an unit circle.
        """
        deltaX = x2 - x1
        deltaY = y2 - y1
        
        # Can't divide through zero, so it's either plus a half pi or minus a half pi.
        if deltaX == 0:
                if deltaY > 0:
                        return -0.5*math.pi
                elif deltaY < 0:
                        return 0.5*math.pi
                else:
                        print "Points are the same."
                        sys.exit()
        
        elif deltaY == 0:
                return math.atan(float(deltaY) / float(deltaX))
        
        elif (deltaX > 0 and deltaY > 0) or (deltaX > 0 and deltaY < 0):        
                return -math.atan(float(deltaY) / float(deltaX))
                
        elif deltaX <= 0 and deltaY <= 0:
                return math.pi - math.atan(float(deltaY) / float(deltaX))
                
        elif deltaX <= 0 and deltaY >= 0:
                return -math.pi - math.atan(float(deltaY) / float(deltaX))
                
def degrees((x1, y1), (x2, y2)):
        return math.degrees(radians((x1, y1), (x2, y2)))

# print "Test1:", math.degrees(radians((50, 50), (100, 100)))
# print "Test2:", math.degrees(radians((100, 100), (50, 50)))
# print "Test3:", math.degrees(radians((50, 100), (100, 50)))
# print "Test4:", math.degrees(radians((100, 50), (50, 100)))
# print "Test5:", math.degrees(radians((50, 50), (100, 50)))
# print "Test6:", math.degrees(radians((50, 50), (50, 100)))
# print "Test6:", math.degrees(radians((50, 100), (50, 50)))

def distance((x1, y1), (x2, y2)):
        return ((x2 - x1)**2.0 + (y2 - y1)**2.0)**(0.5)
        
class House(object):
        
        def __init__(self, canvas, (x, y), space, minSpace, w, h, color, \
                                 orientation = False):
                """
                Initializes a "c" colored square with center (x, y) and surrounding
                space with width "space" (space is in meters).
                """
                # Coordinates, dimensions and name.
                self.x = x
                self.y = y
                self.width = float(w)
                self.height = float(h)
                self.name = (x, y)
        
                # Stops if space is less then minimum space
                if space < minSpace:
                        print "Space of", self.name, "needs to be at least", min, "meters."
                        sys.exit()
                
                global PIXEL
                canvas.create_rectangle(x - (w / 2.0 + space) / PIXEL, \
                                                                y - (h / 2.0 + space) / PIXEL, \
                                                                x + (w / 2.0 + space) / PIXEL, \
                                                                y + (h / 2.0 + space) / PIXEL, fill="grey")
                canvas.create_rectangle(x - w / (2.0 * PIXEL), y - h / (2.0 * PIXEL), \
                                                                x + w / (2.0 * PIXEL), y + h / (2.0 * PIXEL), \
                                                                fill=color)
        
        def getX(self):
                return self.x
        def getY(self):
                return self.y
        def getWidth(self):
                return self.width
        def getHeight(self):
                return self.height
                
        def calcCenterDist(self, other):
                "Calculates the distance between the centres of the houses"
                return ((self.x - other.getX())**2.0 + \
                                (self.y - other.getY())**2.0)**0.5
                
        def calcSpace(self, other):
                """
                Calculates the space between this house and the other hosue.
                """
                phi = degrees((self.x, self.y), (other.getX(), other.getY()))

                #[upper left, upper right, lower left, lower right]
                otherCorner = other.corners()
                selfCorner = self.corners()

                # other house is either above or below this house.
                if (selfCorner[0][0] <= otherCorner[0][0] <= selfCorner[1][0]) or \
                 (selfCorner[0][0] <= otherCorner[1][0] <= selfCorner[1][0]):

                 # Above this house (deltaY).
                 if phi >= 0 :
                                 return selfCorner[0][1] - otherCorner[2][1]
                 # Below this house (deltaY).
                 else:
                                 return otherCorner[0][1] - selfCorner[2][1]

                # other house is either of the lef or the right of this house.
                elif (selfCorner[0][1] <= otherCorner[0][1] <= selfCorner[2][1]) or \
                          (selfCorner[0][1] <= otherCorner[2][1] <= selfCorner[2][1]):

                 # Rigth of this house (deltaX).
                 if abs(phi) <= 90:
                                 return otherCorner[0][0] - selfCorner[1][0]
                 # Left of this house (deltaX).
                 else:
                                return selfCorner[0][0] - otherCorner[1][0]

                # Other house is diagonal of this house.
                else:
                        # Other house is diagonal to the right.
                        if abs(phi) <= 90:
                                # Other house is above this house.
                                if phi >= 0:
                                        return distance(selfCorner[1], otherCorner[2])
                                # Other house is below this house.
                                else:
                                        return distance(selfCorner[3], otherCorner[0])

                        # Other house is diagonal on the left
                        else:
                                # Other house is above this house.
                                if phi >= 0:
                                        return distance(selfCorner[0], otherCorner[3])
                                # Other house is below this house.
                                else:
                                        return distance(selfCorner[2], otherCorner[1])

        def corners(self):
                """
                Returns the coordinates of the corners in a list of tuples.
                [(upper left), (upper right), (lower left), (lower right)
                """
                return [(self.x - self.width / 2.0, self.y - self.height / 2.0), \
                                (self.x + self.width / 2.0, self.y - self.height / 2.0), \
                                (self.x - self.width / 2.0, self.y + self.height / 2.0), \
                                (self.x + self.width / 2.0, self.y + self.height / 2.0)]
        
        def isIn(self, (x, y)):
                "Returns true if given coordinates are in the house"
                return (self.x - self.width / 2.0 < x < self.x + self.width / 2.0) and \
                         (self.y - self.height / 2.0 < y < self.y + self.height / 2.0)
                        
        def houseIsIn(self, other):
                "Returns true if the other house is in this house."
                corner = other.corners()
                for c in corner:
                        if self.isIn(c):
                                return True
                return False

class OneFamilyHouse(House):
        """
        A onefamily-house with a width and height of 8 meters
        and a minimum feestanding of 2 meters, collored red.
        """
        def __init__(self, canvas, (x, y), space):
                House.__init__(self, canvas, (x, y), space, 2, 8, 8, "red")

        def calc_price(self)
                int SELL_PRICE = 285000
                int APPR_PRICE = SELL_PRICE * 0.03
                return oWorth = SELL_PRICE + (((self.space/0.2) - 2) * APPR_PRICE)

class Bungalow(House):
        """
        A bungalow with a width of 10 meters and a height of 7.5 meters
        and a minimum freestanding of 3 meters, collord blue.
        """
        def __init__(self, canvas, (x, y), space):
                House.__init__(self, canvas, (x, y), space, 3, 10, 7.5, "blue")

        def calc_price(self)
                int SELL_PRICE = 399000
                int APPR_PRICE = SELL_PRICE * 0.04 
                return bWorth = SELL_PRICE + (((self.space/0.2) - 3) * APPR_PRICE)


        def rotate(self)
                self.width = self.height
                self.height = self.width
                        
class Maison(House):
        """
        A Maison with a width of 11 meters and height 10.5 meters
        and a minimum freestanding of 6 meters, collored green.
        """
        def __init__(self, canvas, (x, y), space):
                House.__init__(self, canvas, (x, y), space, 6, 11, 10.5, "green")
                
        def calc_price(self)
                int SELL_PRICE = 610000
                int APPR_PRICE = SELL_PRICE * 0.06
                return mWorth = SELL_PRICE + (((self.space/0.2) - 6) * APPR_PRICE)

def callback(event):
        "Gives the coordinates when clicking with the mouse."
        print "clicked", event.x, event.y
# Applays callback on this canvas
w.bind("<Button-1>", callback)

O1 = OneFamilyHouse(w, (100, 100), 3)
Bungalow(w, (250, 250), 3)
M1 = Maison(w, (500, 500), 6)
M2 = Maison(w, (500, 100), 6)

print M1.calcSpace(M2)







mainloop()