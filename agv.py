
from ev3dev.ev3 import *
#added this ^ SK
import time
from time import sleep
'''
The agv function will act as the "main" method for your system. dairy_land is a Factory object from the factory.py file.
dairy_land has an attribute "test_complete" that signals if you have completed all of the orders in the test file.
dairy_land.read_order() will return an Order object from the queue. Once you have successfully fulfilled an order to the
correct packer, you may call the order_complete function on the order object to mark it as complete.

IMPORTANT: each time you call the read_order() function, the order at the front of the queue is removed. Do not call the
read_order() function until the previous order has been fulfilled.
'''
def agv(dairy_land):
    
    #Initialize all of your objects before the while loop
    ars = ARS(0,0) #ARS will start at (0,0) on the coordinate plain every time
    # TODO verify coordinates
    r1 = Bin('red', 'r1', 3, 5)
    r2 = Bin('red', 'r2', 1, 3)
    r3 = Bin('red', 'r3', 3, 1)
    y1 = Bin('yellow', 'y1', 1, 5)
    y2 = Bin('yellow', 'y2', 3, 3)
    b1 = Bin('blue','b1', 1, 1)
    bins = [r1, r2, r3, y1, y1, b1, b2]

    #TODO add packer coordinates
    p1 = Packer(1, 0, 0)
    p2 = Packer(2, 0, 6)
    p3 = Packer(3, 4, 6)
    
    while not dairy_land.test_complete:
        # read an order:
        cur_order = dairy_land.read_order()
        # see if there is a valid order:
        if cur_order is not None:
            # fulfill the order:
            # bins --> an array that stores all of the bin objects you've created
            cur_bin = ars.find_nearest_bin(bins, cur_order.packer, cur_order.color)
            # cur_bin --> the closest bin returned from the find_nearest_bin function
            print(cur_bin.name) # SK test 
            # Move robot to closest bin:
            move_to_bin(cur_bin)
            # Pause while cheese is loaded:
            #TODO add method that makes ARS sleep for a few seconds
            
            # Move to correct packer:
            move_to_packer(cur_bin, cur_order.packer)          
            # Move bin to open (and optimal) spot
            move_to_bin(cur_bin) #for now, assume we're taking bin back to its location
            '''
            Begin ARS logic here. Again, this will serve as your main method. After you read an order in the queue,
            your first step should be to determine which packer requires the order and for which type of cheese the
            order is for.
            Each Order object has the following attributes:
            packer: an integer (1, 2 or 3) representing which packer the order is for
            color: a string ('red', 'yellow' or 'blue') representing the color bin to retrieve for the order
            See Order class in factory.py for more details...
            Once you understand how to access attributes of each order object, you need to find out where the closest
            bin is to retrieve for the order
            The next step after finding the nearest bin is obviously to move that bin from its location to the packer
            associated with the order. Depending on whether you are using a robot to move bins to the packers or have 
            a system built that transports the bins to the packers, your logic will differ slightly. 
            Robot:
                1. Move robot to closest bin
                2. Move robot from closest bin to correct packer
                3. Move bin back to open spot 
            System:
                1. Transport closest bin to correct packer
            '''
            """
            The rest is for YOU to complete. Always be aware and make sure to update locations of objects when moving 
            around the grid. Remember, you cannot bring a bin to a grid location that is already occupied by another
            bin. You should create a variable that keeps track of the location of empty spots in your grid. Once you've 
            completed an order be sure to call the order_complete() function on your cur_order and read the next order in.
            """
        else:
            sleep(1)

 

class ARS():
    def __init__(self, x, y):
        #TODO: verify which motor is which
        self.mA = LargeMotor('A') #motor:
        self.mB = LargeMotor('B') #motor:
        self.mC = LargeMotor('C') #motor:
        self.x = x #SK - these are the initial coordinates of the ARS
        self.y = y

'''
In the ARS class you can define different functions to help your system retrieve inventory bins for
each packer. Some examples to help get you started are below.
'''
    def find_nearest_bin(self, bins, packer, color):
        dist = 20
        for i in bins:
            if bins[i].color == color:
                # simply the total horizontal and vertical distance your system needs to travel depending on
                # how you track locations in your system, distance calculation will differ
                new_dist = abs(packer.x - bins[i].x)+abs(packer.y - bins[i].y)
                # makes sure that you are not trying to retrieve an empty bin
                if new_dist < dist & bins[i].quantity > 0:
                    dist = new_dist
                    index = i
        return(bins[index])

    def move_to_bin(self, bin):
        # TODO
        std_turn_X = #this is the number of degrees the pulley must turn to move one space 
        std_turn_Y = 358.098622 #this is the number of degrees the wheels are required to turn to move one space
        x_move = bin.x - self.x
        y_move = bin.y - self.y
        
        #TODO verify motors
        mA.move(x_move*std_turn_X)
        mB.move(y_move*std_turn_Y)
        mC.move(y_move*std_turn_Y)
        
        #!/usr/bin/env python3 - what's this? -SK
        updateCurLocation(bin.x, bin.y)
        
       
    
    def move_to_packer(self, bin, packer):
        # TODO
        std_turn_X = #this is the number of degrees the pulley must turn to move one space 
        std_turn_Y = 361.9114 #this is the number of degrees the wheels are required to turn to move one space
        x_move = packer.x - self.x
        y_move = packer.y - self.y
        
        #TODO verify motors
        mA.move(x_move*std_turn_X)
        mB.move(y_move*std_turn_Y)
        mC.move(y_move*std_turn_Y)
        
        #!/usr/bin/env python3 - what's this? -SK
        updateCurLocation(bin.x, bin.y)
        

    def updateCurLocation(self, x, y): #SK this is a method I’ve added
        self.x = x
        self.y = y
        
        
        

'''
Here are a couple of classes you may want to use to help organize your inventory grid. You are not required to use
any of these classes or you can build more classes to help organize. It is up to you. My functions/implementation is
based off of these classes.
'''
class Bin():
    def __init__(self, color, name, x, y):
        self.color = color
        # You may use any method for tracking location of bins, packers or grid locations
        # In this example I simply used x and y coordinates
        self.name = name
        self.x = x
        self.y = y
        self.quantity = 3
        self.replenish_cost = 0

    #TODO: delete these methods if they're not used    
    def getColor():
        return color

    def getX():
        return x
 
    def getY():
        return y

    # call this function when you have ran out of inventory
    def replenish(self):
        Sound.speak("Replenishing empty bin at location...")
        self.quantity = 3
        self.replenish_cost += 10


class Packer():
    def __init__(self, region, x, y):
        self.region = region
        self.x = x
        self.y = y


