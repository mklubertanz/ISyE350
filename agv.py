import time
from time import sleep
'''
The agv function will act as the "main" method for your system. dairy_land is a Factory object from the factory.py file.
dairy_land has an attribute "test_complete" that signals if you have completed all of the orders in the test file.
dairy_land.read_order() will return an Order object from the queue. Once you have successfully fulfilled an order to the
correct packer, you may call the order_complete function on the order object to mark it as complete. Kalley 

IMPORTANT: each time you call the read_order() function, the order at the front of the queue is removed. Do not call the
read_order() function until the previous order has been fulfilled.
'''
def agv(dairy_land):
    
    #Initialize all of your objects before the while loop
    ars = ARS()
    #TODO update this based on our expected demand (ie how many bins of each color do we need?)
    #we need 3 Reds, 2 Yellows and 1 Blue
    #TODO update coordinates
    r1 = Bin('red', 'r1', __, __)            #Top right
    r2 = Bin('red', 'r2', __, __)            #Middle left
    r3 = Bin('red', 'r3', __, __)            #Bottom right
    y1 = Bin('yellow', 'y1', __, __)         #Top left
    y2 = Bin('yellow','y2', __, __)          #Middle right
    b1 = Bin('blue','b1', __, __)            #Bottom left
    bins = [r1, r2, r3, y1, y2, b1]

    p1 = Packer(1, __, __)                   #Top left
    p2 = Packer(2, __, __)                   #Top right
    p3 = Packer(3, __, __)                   #Bottom left
    
    while not dairy_land.test_complete:
        # read an order:
        cur_order = dairy_land.read_order()
        # see if there is a valid order:
        if cur_order is not None:
            # fulfill the order:
            # bins --> an array that stores all of the bin objects you've created
            cur_bin = ars.find_nearest_bin(bins, cur_order.packer, cur_order.color)
            # cur_bin --> the closest bin returned from the find_nearest_bin function
            print(cur_bin) # SK test 
            
            # TODO implement code below...
            # Move robot to closest bin:
                # call function that activates motors and moves system
                # 
                # update system location
            
            # Pause while cheese is loaded:
            
            
            # Move to correct packer:
            
            
            
            
            # Move bin to open (and optimal) spot
            
                # update bin to new location
            
            
                
            
            print(cur_order) #SK this is an error check...not sure what cur_order object will print
            
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
                #^SK added this...can we just assume we take the bin back to where it was?
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
    def __init__(self, cur_x, cur_y):
        # Here is where you can initialize motors and sensors
        # For example...
        # self.mB = LargeMotor('B')
        self.cur_x = cur_x
        self.cur_y = cur_y

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
        
    def move_to_packer(self, bin, packer):
        # TODO
        PlaySound(soundBeepBeep);
        
        
        #keep track of how many units system moves in x and y direction

    def updateCurLocation(x, y): #SK this is a function I’ve added
        #x is distance system has traveled in x dir (will be positive or negative)
        #y is distance system has traveled in y dir (will be positive or negative)
        # implement function here
        cur_x = cur_x + x
        cur_y = cur_y + y
        
        
        

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
    ars = ARS()
    # TODO update this based on our expected demand (ie how many bins of each color do we need?)
    # TODO update coordinates
    r1 = Bin('red', 'r1', __, __)
    r2 = Bin('red', 'r2', __, __)
    y1 = Bin('yellow', 'y1', __, __)
    y2 = Bin('yellow', 'y2', __, __)
    b1 = Bin('blue','b1', __, __)
    b2 = Bin('blue','b2', __, __)
    bins = [r1, r2, y1, y1, b1, b2]

    p1 = Packer(1, __, __)
    p2 = Packer(2, __, __)
    p3 = Packer(3, __, __)
    
    while not dairy_land.test_complete:
        # read an order:
        cur_order = dairy_land.read_order()
        # see if there is a valid order:
        if cur_order is not None:
            # fulfill the order:
            # bins --> an array that stores all of the bin objects you've created
            cur_bin = ars.find_nearest_bin(bins, cur_order.packer, cur_order.color)
            # cur_bin --> the closest bin returned from the find_nearest_bin function
            print(cur_bin) # SK test 
            
            # TODO implement code below...
            # Move robot to closest bin:
                # call function that activates motors and moves system
                # update system location
            
            # Pause while cheese is loaded:
            
            
            # Move to correct packer:
            
            
            
            
            # Move bin to open (and optimal) spot
            
                # update bin to new location
            
            
                
            
            print(cur_order) #SK this is an error check...not sure what cur_order object will print
            
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
                #^SK added this...can we just assume we take the bin back to where it was?
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
    def __init__(self, cur_x, cur_y):
        # Here is where you can initialize motors and sensors
        # For example...
        # self.mB = LargeMotor('B')
        self.cur_x = cur_x
        self.cur_y = cur_y

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
        
    def move_to_packer(self, bin, packer):
        # TODO
        
        
        
        #keep track of how many units system moves in x and y direction

    def updateCurLocation(x, y): #SK this is a function I’ve added
        #x is distance system has traveled in x dir (will be positive or negative)
        #y is distance system has traveled in y dir (will be positive or negative)
        # implement function here
        cur_x = cur_x + x
        cur_y = cur_y + y
        
        
        

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


