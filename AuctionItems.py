from collections import namedtuple
import math


class AuctionItems:
    def __init__(self, name, data):
        self.name = name
        self.addedTime = data.timestamp
        self.owner = data.user_id
        self.reserve_price = data.reserve_price
        self.close_time = data.close_time
        self.all_bids = []
        self.price_paid = 0.0  # should be the price paid by the auction winner
        # (0.00 if the item is UNSOLD), as a number to two decimal places
        self.status = 'UNSOLD'  # 'SOLD' or 'UNSOLD depending on auction outcome, default 'UNSOLD'
        self.total_bid_count = int(0)  # number of 'valid' bids received for the item
        self.highest = int(0)  # The highest bid received for the item as a number to 2 dp
        self.lowest = math.inf  # The Lowest bid placed on the item as a number to 2 dp
        self.highestBidder = ""

    def setStatus(self, status):
        if status == 'SOLD' or status == "UNSOLD":
            self.status = status

    def getFullData(self):  # this matches with the output requried
        return "{0}|{1}|{2}|{3}|{4}|{5}|{6}|{7}".format(self.close_time,
                                                        self.name,
                                                        self.highestBidder,
                                                        self.status,
                                                        self.price_paid,
                                                        self.total_bid_count,
                                                        self.highest,
                                                        self.lowest)

    def printDataTable(self):
        print("{:<10} {:<10} {:<8} {:<8} {:<15} {:<12} {:<12} {:<10}".format(self.close_time,
                                                        self.name,
                                                        self.highestBidder,
                                                        self.status,
                                                        self.price_paid,
                                                        self.total_bid_count,
                                                        self.highest,
                                                        self.lowest))
