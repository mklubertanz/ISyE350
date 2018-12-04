#!/usr/bin/python3
"""
Factory script for ISyE 350.

Running this script will spwan two threads - generator and agv. The generator
thread will generate the orders. The agv thread will run the agv function
implemented by the student.

Usage
-----
You can either run from the terminal

    $ python3 factory.py

or run this file from the ev3 brick.
"""

import time
from time import sleep
import sys
import threading
import queue
import random
# from typing import Tuple
import ev3dev.ev3 as ev3
import agv


# Class for orders and its operations
class Order(object):
    """
    Order class to provide basic operations on orders.

    Provides methods to create orders, get the quantities from the order,
    announces the order, notify order completetion etc. Many basic operations
    are overloaded to a sensible defaults (look at the documentation).

    """

    PENDING_ORDER = 0

    def __init__(self, packer, color):
        """
        Initialize an Order object with the number of red, blue and yellow SKUs

        Raises
        ----------
        an order can only come from one bin e.g. r + b + y <= 1

        Parameters
        ----------
        color :
            Color of cheese order calls for
        packer :
            Packer order is to be brought to

        Examples
        --------
        To generate an order from a red bin to Packer 1
            order = Order(packer = 1, color = 'red')

        or
            order = Order(1, 'red')

        """

        self.color = color
        self.packer = packer
        self.isComplete = False
        self.start_time = time.time()
        self.finish_time = None


    def announce(self):
        """speaks out the order"""
        ev3.Sound.speak(self.__repr__()).wait()

    def order_complete(self):
        """Marks the order as completed"""
        self.isComplete = True
        Order.PENDING_ORDER -= 1
        self.finish_time = time.time()

    def __repr__(self):
        return "Packer: "+str(self.packer)+", Color: "+self.color


# order generator. can replace in future keeping the signature
def generate_order(factory):
    ev3.Sound.speak('Generating Orders').wait()

    try:
        scenario = open(factory.test_scenario)
    except:
        print("Unable to open the", factory.test_scenario, "file")
        factory.test_complete = True
        exit()

    order = None
    for line in scenario:
        x = line.split(',')
        x[2] = x[2].strip()
        inter_arrival_time = int(x[0])
        packer = int(x[1])
        color = x[2]
        #inter_arrival_time, packer, color = [x for x in line.split(',')]
        time.sleep(inter_arrival_time)
        order = Order(packer, color)
        Order.PENDING_ORDER += 1
        # appends each order into the factory object's order_log []
        factory.order_log.append(order)
        # What is buffer method do?
        factory.buffer.put(order)


    no_of_orders = len(factory.order_log)
    cum_retrieval_time = 0
    no_of_bins = 0
    # test start is at the time of the first order in the order log
    test_start = factory.order_log[0].start_time
    test_end = 0

    # What exactly is this doing?
    while Order.PENDING_ORDER != 0:
        time.sleep(1)

    # Creates this factory log for each order in the order log
    for i, order in enumerate(factory.order_log):
        if test_end < order.finish_time:
            test_end = order.finish_time

        cum_retrieval_time += (order.finish_time - order.start_time)
        no_of_bins += 1

        factory.log.write('\nOrder Number {}\n'.format(i+1))
        factory.log.write(str(order))
        factory.log.write('\n')
        factory.log.write('Arrival Time    : {:.2f}\n'.format(order.start_time - test_start))
        factory.log.write('Completion Time : {:.2f}\n'.format(order.finish_time - test_start))
        factory.log.write('Retrieval Time  : {:.2f}\n'.format(order.finish_time - order.start_time))

    # Creates this overall summary for all of the orders in the order log
    factory.log.write('\nSummary:\n')
    factory.log.write('Total Run Time                    : {:.2f}\n'.format(test_end - test_start))
    factory.log.write('Average Retrieval Time            : {:.2f}\n'.format(cum_retrieval_time/no_of_orders))
    factory.log.write('Average Throughput (blocks/minute): {:.2f}\n'.format(no_of_bins/(test_end - test_start)*60))

    factory.test_complete = True
    exit()


# wrapper for factories buffer and end of order
class Factory(object):
    def __init__(self, log_name, test_scenario=None):
        self.buffer = queue.Queue()
        self.test_scenario = test_scenario
        self.order_log = []
        self.test_complete = False #students check test_complete, if true, exit
        self.log = log_name

    # read order for agv
    def read_order(self):
        if not self.buffer.empty():
            return self.buffer.get()
        else:
            return None


if __name__ == '__main__':
    # Student configuration
    group_name = 'YOUR_GROUP_NAME_HERE'

    # (Option I) if you want to run a test scenario modify the below line
    test_scenario = 'testcase1.test'

    # log name or optionally choose to set your own log file name
    log_name = 'report_{test_scenario}.log'.format(test_scenario=test_scenario)
    # DON'T EDIT ANYTHING BEYOND THIS

    # open file
    log = open(log_name, 'w')
    log.write('Group Name: {group_name}\n'.format(group_name=group_name))
    # Create factory object
    dairy_land = Factory(log, test_scenario=test_scenario)

    # create threads
    generator = threading.Thread(target=generate_order, args=(dairy_land, ))
    agv = threading.Thread(target=agv.agv, args=(dairy_land, ))

    # start threads
    generator.start()
    agv.start()

    # wait for threads
    generator.join()
    agv.join()

    # close log
    log.close()
