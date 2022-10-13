from collections import namedtuple
import csv
from AuctionItems import AuctionItems
from decimal import *


class OnlineAuction:
    def __init__(self, auctionData=""):  # initialise
        self.auctionData = auctionData
        self.all_auction_items = {}
        self.closing_times = {}

        self.bids = namedtuple('bidItems', 'timestamp user_id action item bid_amount')
        self.item = namedtuple('items', 'timestamp user_id action item reserve_price close_time')
        self.hearbeat_type = namedtuple('heartbeat', 'timestamp')
        self.auction_order = []
        self.activeItems = {}

    def dataClass(self, data):  # data classification for each instruction line in data
        # print(data)
        if len(data) == 1:  # heartbeat
            self.auction_order.append(self.hearbeat_type._make(data))
        elif len(data) == 5:  # Bid
            self.auction_order.append(self.bids._make(data))  # generate new bids from data
        elif len(data) == 6:  # Sell
            self.auction_order.append(self.item._make(data))  # generate new item from data
        else:
            raise ValueError("Wrong instruction format")

    # current timestamp strictly larger than the last one and placed within auctioning time
    def checkTime(self, instr_timestamp, item):
        check = True  # initialise
        # First check the timestamp ( This may be useless but just a precaution check)
        if item.all_bids:  # if there are existing bids in the list, else skip as theres no point comparing an empty
            # list, it just gives you an error :)
            if Decimal(instr_timestamp) > Decimal(
                    item.all_bids[-1].timestamp):  # cast to decimal for comparison purposes
                check &= True
                # print("Auction instruction placed for item {0} in a reasonable time".format(item.name))
            else:
                check &= False
                print("INVALID BID: Auction instruction NOT placed for item {0} in a reasonable time".format(item.name))

        # Now check if its within auction time, if its False from the last one, do nothing, its already invalid
        if check:
            if Decimal(instr_timestamp) < Decimal(item.close_time):
                check &= True
                # print("Auction instruction is within item close time")
            else:
                check &= False
                print("INVALID BID: Auction instruction is out of item {0} 's close time".format(item.name))

        # Code alternatives : reverse the decimal comparison, and reverse the check &(s) so that else can be removed,
        # same but depends what looks cleaner I guess.
        return check

    # current bid is strictly greater than the last bid of the item, and the bid is also larger than the reserve bid
    # price
    def checkPrice(self, price, item):
        # check if current bid is strictly greater than the last bid of the item
        check = True  # initialise
        if item.all_bids:
            if Decimal(price) > Decimal(item.all_bids[-1].bid_amount):
                check &= True
                # print("Price placed on item {0} is larger than the last bid price".format(item.name))
            else:
                check &= False
                # print( "INVALID BID: Price placed on item {0} is smaller or equal to the last bid price".format(
                #(item.name))
        # the bid is also larger than the reserve bid price
        if check:
            if Decimal(price) >= Decimal(item.reserve_price):
                check &= True
                # print("Check Successful: Price placed on item {0} is larger than the reserve price".format(item.name))
            else:
                check &= False
                # print("INVALID BID: Price placed on item {0} is smaller than the reserve price".format(item.name))
        return check

    def validBidAction(self, bid):  # combine check by applying the two functions above , can of course using them
        # separately, this just helps to apply everything all at once

        check = True
        if self.all_auction_items:  # if list of items in the auction is not empty
            if bid.item in self.all_auction_items.keys():  # if item is added to the auction already
                if self.checkPrice(bid.bid_amount, self.all_auction_items[bid.item]) and self.checkTime(bid.timestamp,
                                                                                                        self.all_auction_items[
                                                                                                            bid.item]):
                    check &= True
                    # print("valid bid")
                else:
                    check &= False
                    # print("INVALID BID: invalid price or timestamp")
            else:
                # print("INVALID BID: item not in auction")
                check = False
        else:
            # print("INVALID BID: No items is under auction yet")
            check = False
        return check

    def processheartBeats(self, item_name):  # closes the items that are at this heartbeat (filtered before calling)
        item = self.all_auction_items[item_name]
        if item.all_bids:
            if len(item.all_bids) >= 2:  # based on example output, we return the 2nd highest bid price
                item.price_paid = item.all_bids[-2].bid_amount
                # item.setStatus('SOLD')
            else:
                item.price_paid = item.reserve_price
            item.setStatus('SOLD')
            item.highestBidder = item.all_bids[-1].user_id
            print("item {0} is sold for {1} to user {2}".format(item.name, item.price_paid, item.highestBidder))
        else:
            # item.price_paid = 0.0
            item.setStatus('UNSOLD')
            print("item {0} is not sold, item is now closed for auction".format(item.name))
        self.all_auction_items[item_name] = item
        self.activeItems.pop(item.name)

    def addCloseRecords(self, heartbeat, item_name):  # records the closing times of all auction items
        if int(heartbeat) not in self.closing_times:
            self.closing_times[int(heartbeat)] = list()
        self.closing_times[int(heartbeat)].append(item_name)

    def processOrders(self, instructions):
        if isinstance(instructions, self.item):  # register a new item to the auction,
            # also records its closing time separately for when dealing with heartbeats
            if instructions.action == 'SELL':
                self.all_auction_items[instructions.item] = AuctionItems(name=instructions.item, data=instructions)
                self.addCloseRecords(instructions.close_time, instructions.item)
                self.activeItems[instructions.item] = ""
                print("item {0} added".format(instructions.item))
            else:
                raise ValueError("Wrong Format for selling")
        elif isinstance(instructions, self.bids):  # Bidding action.
            if instructions.action == 'BID':
                price = instructions.bid_amount
                # first check if there exists the item that can be bid
                # and also if the item is active (meaning not closed)
                if instructions.item in self.all_auction_items.keys() and instructions.item in self.activeItems.keys():
                    auction_item = self.all_auction_items[instructions.item]
                    auction_item.total_bid_count += 1  # increment count (before valid or not based on suggested outputs)
                    if self.validBidAction(instructions):  # validation
                        auction_item.all_bids.append(instructions)  # if valid, add bid action
                        print("User {0} bid on item {1} successful, with price {2}".format(instructions.user_id,
                                                                                           instructions.item,
                                                                                           instructions.bid_amount))
                    else:
                        print("User {0}'s bid on item {1} is invalid".format(instructions.user_id, instructions.item))
                    # update prices if necessary
                    if Decimal(price) < Decimal(auction_item.lowest):
                        auction_item.lowest = Decimal(price)
                    if Decimal(price) > Decimal(auction_item.highest):
                        auction_item.highest = Decimal(price)
                    # update back into system
                    self.all_auction_items[instructions.item] = auction_item
            else:
                raise ValueError("Wrong Format for bidding")
        elif isinstance(instructions, self.hearbeat_type):  # heartbeat
            print("Auction Heartbeat @ time {0}".format(instructions.timestamp))
            #     heartbeat = instructions.timestamp
            if int(instructions.timestamp) in self.closing_times.keys():  # checks if any items are closing at the
                # current heartbeat
                if self.closing_times[int(instructions.timestamp)]:
                    for item in self.closing_times[int(instructions.timestamp)]:
                        self.processheartBeats(item)
        #
        else:
            print("invalid auction instruction")
            raise ValueError("Wrong instruction format!")

    def readAndClass(self):  # read file and map to classify
        with open(file=self.auctionData, newline='') as csvFile:
            csvLines = csv.reader(csvFile, delimiter='|')
            list(map(self.dataClass, csvLines))
        sorted(self.auction_order, key=lambda x: x[0])  # this is just to ensure that the inputs does not consist
        # unsorted timestamps

    def processInstructionsList(self):  # helper function to be called by the system
        list(map(self.processOrders, self.auction_order))

    def returnAuctionValuesAsList(self):  # returns table to be printed
        for i in self.all_auction_items:
            self.all_auction_items[i].printDataTable()

    def writeOutput(self):  # write output to text file
        lines = []
        for i in self.all_auction_items:
            lines.append(self.all_auction_items[i].getFullData())
        with open('AUCTION_RESULTS_' + self.auctionData, 'w') as f:
            for line in lines:
                f.write(line)
                f.write('\n')
