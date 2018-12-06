import ev3dev.ev3 as ev3
from ev3 import *
#added these ^ SK
from time import sleep
'''
The agv function will act as the "main" method for your system. dairy_land is a Factory object from the factory.py file.
dairy_land has an attribute "test_complete" that signals if you have completed all of the orders in the test file.
dairy_land.read_order() will return an Order object from the queue. Once you have successfully fulfilled an order to the
correct packer, you may call the order_complete function on the order object to mark it as complete.

IMPORTANT: each time you call the read_order() function, the order at the front of the queue is removed. Do not call the
read_order() function until the previous order has been fulfilled.
'''
def move(this_packer, this_bin):
    std_turn_X = 308.5157698 #this is the number of degrees the pulley must turn to move one space
    std_turn_Y = 358.098622 #this is the number of degrees the wheels are required to turn to move one space
    if this_packer is not None and this_bin is None:
        x_move = this_packer.x - self.x
        print(x_move)
        y_move = this_packer.y - self.y
        print(y_move)
    elif this_packer is None and this_bin is not None: 
        x_move = this_bin.x - self.x
        print(x_move)
        y_move = this_bin.y - self.y
    else:
        ev3.Sound.speak('Error I cannot detect my next move').wait()
    mA = LargeMotor('outA') #motor: pulley motor
    mB = LargeMotor('outB') #motor: wheel motor
    mC = LargeMotor('outC') #motor: wheel motor
    mA.run_to_rel_pos(position_sp=x_move*std_turn_X, speed_sp=100, stop_action="brake")
    mB.run_to_rel_pos(position_sp=y_move*std_turn_Y, speed_sp=100, stop_action="brake")
    mC.run_to_rel_pos(position_sp=y_move*std_turn_Y, speed_sp=100, stop_action="brake")
    #TODO: add "sleep while running method"
    sleep(3)
    ars.updateCurLocation(bin.x, bin.y)

def agv(dairy_land):

    #Initialize all of your objects before the while loop
    ars = ARS(1,1) #ARS will start at (0,0) on the coordinate plain every time
    r1 = Bin('red', 'r1', 1, 1)
    r2 = Bin('red', 'r2', 3, 1)
    r3 = Bin('red', 'r3', 3, 3)
    y1 = Bin('yellow', 'y1', 1, 5)
    y2 = Bin('yellow', 'y2', 1, 3)
    b1 = Bin('blue','b1', 3, 5)
    bins = [r1, r2, r3, y1, y2, b1]

    #TODO add packer coordinates
    p1 = Packer(1, 0, 7)
    p2 = Packer(2, 5, 7)
    p3 = Packer(3, 0, 0)
    packers = [p1, p2, p3]

    while not dairy_land.test_complete:
        # read an order:
        cur_order = dairy_land.read_order()
        # see if there is a valid order:
        if cur_order is not None:
            # fulfill the order:
            # bins --> an array that stores all of the bin objects you've created
            cur_bin = ars.find_nearest_bin(bins, packers[cur_order.packer - 1], cur_order.color)
            # cur_bin --> the closest bin returned from the find_nearest_bin function
            print(cur_bin.name) # SK test
            # Move robot to closest bin:
            move(None, cur_bin)
            sleep(3)
            print(packers[cur_order.packer - 1].region) # SK test
            # Move to correct packer:
            move(None, packers[cur_order.packer - 1])
            sleep(3)
            # Move bin to open (and optimal) spot
            move(None, cur_bin) #for now, assume we're taking bin back to its location
            cur_order.isComplete = True
        else:
            sleep(1)


class ARS():
    def __init__(self, x, y):
        self.x = x #SK - these are the initial coordinates of the ARS
        self.y = y

    def find_nearest_bin(self, bins, packer, color):
        dist = 20
        near_bin = bins[0]
        for this in bins:
            if this.color == color:
                # simply the total horizontal and vertical distance your system needs to travel depending on
                # how you track locations in your system, distance calculation will differ
                new_dist = abs(packer.x - this.x)+abs(packer.y - this.y)
                # makes sure that you are not trying to retrieve an empty bin
                if new_dist < dist & this.quantity > 0:
                    dist = new_dist
                    near_bin = this
        return near_bin

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


