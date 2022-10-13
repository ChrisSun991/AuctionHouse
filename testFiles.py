import unittest
from OnlineAuction import OnlineAuction
from AuctionItems import AuctionItems
import pytest
testFile = "input.txt"


class Test(unittest.TestCase):

    def setUp(self) -> None:
        self.auction = OnlineAuction(testFile)

    def test_01_readTestFile(self):
        # Test on reading the input file and also classifying the instructions
        self.auction.readAndClass()
        assert len(self.auction.auction_order) > 1, "Reading and classification error"
        assert isinstance(self.auction.auction_order, list), "auction orders should be a list of instructions"

    def test_02_faultyInstructions(self):
        instruction = []
        with pytest.raises(ValueError, match=r"Wrong instruction format"):
            self.auction.dataClass(instruction)

    def test_03_faultyInstructions(self):
        instruction = ['10','SELL','abalaba', '20']
        with pytest.raises(ValueError, match=r"Wrong instruction format"):
            self.auction.dataClass(instruction)

    def test_04_addItem(self):
        item_to_sell = [999,250,'SELL','iphone',1000,1200]
        auction_item = self.auction.item._make(item_to_sell)
        self.auction.processOrders(auction_item)
        testItem = AuctionItems('iphone',auction_item)
        assert testItem, self.auction.all_auction_items['iphone']

    def test_05_addItemFalse(self):
        item_to_sell = [1000,233,'BID','iphone',1000,1200]
        auction_item = self.auction.item._make(item_to_sell)
        with pytest.raises(ValueError, match=r"Wrong Format for selling"):
            self.auction.processOrders(auction_item)
        # testItem = AuctionItems('iphone',auction_item)

    def test_06_valid(self):
        item_to_sell = [999,250,'SELL','iphone',1000,1200]
        auction_item = self.auction.item._make(item_to_sell)
        self.auction.processOrders(auction_item)

        item_to_bid = [1001,256,'BID','iphone',1200]
        auction_bid = self.auction.bids._make(item_to_bid)
        assert self.auction.validBidAction(auction_bid), True

    def test_07_valid_false_reservePrice(self):
        item_to_sell = [999,250,'SELL','iphone',1000,1200]
        auction_item = self.auction.item._make(item_to_sell)
        self.auction.processOrders(auction_item)

        item_to_bid = [1001,256,'BID','iphone',900]
        auction_bid = self.auction.bids._make(item_to_bid)
        assert not self.auction.validBidAction(auction_bid), True

    def test_08_valid_false_bidPrice(self):
        item_to_sell = [999,250,'SELL','iphone',1000,1200]
        auction_item = self.auction.item._make(item_to_sell)
        self.auction.processOrders(auction_item)

        item_to_bid_1 = [1001,256,'BID','iphone',1100]
        auction_bid_1 = self.auction.bids._make(item_to_bid_1)
        self.auction.processOrders(auction_bid_1)

        item_to_bid_2 = [1002, 199, 'BID', 'iphone', 1050]
        auction_bid_2 = self.auction.bids._make(item_to_bid_2)
        assert not self.auction.validBidAction(auction_bid_2), True

    def test_09_valid_false_timestamp(self):
        item_to_sell = [999,250,'SELL','iphone',1000,1200]
        auction_item = self.auction.item._make(item_to_sell)
        self.auction.processOrders(auction_item)

        item_to_bid_1 = [1001,256,'BID','iphone',1100]
        auction_bid_1 = self.auction.bids._make(item_to_bid_1)
        self.auction.processOrders(auction_bid_1)

        item_to_bid_2 = [1000, 199, 'BID', 'iphone', 1200]
        auction_bid_2 = self.auction.bids._make(item_to_bid_2)
        assert not self.auction.validBidAction(auction_bid_2), True

    def test_10_valid_true_timestamp(self):
        item_to_sell = [999,250,'SELL','iphone',1000,1200]
        auction_item = self.auction.item._make(item_to_sell)
        self.auction.processOrders(auction_item)

        item_to_bid_1 = [1001,256,'BID','iphone',1100]
        auction_bid_1 = self.auction.bids._make(item_to_bid_1)
        self.auction.processOrders(auction_bid_1)

        item_to_bid_2 = [1002, 199, 'BID', 'iphone', 1200]
        auction_bid_2 = self.auction.bids._make(item_to_bid_2)
        assert self.auction.validBidAction(auction_bid_2), True

    def test_11_valid_false_close_time(self):
        item_to_sell = [999,250,'SELL','iphone',1000,1200]
        auction_item = self.auction.item._make(item_to_sell)
        self.auction.processOrders(auction_item)

        item_to_bid_1 = [1001,256,'BID','iphone',1100]
        auction_bid_1 = self.auction.bids._make(item_to_bid_1)
        self.auction.processOrders(auction_bid_1)

        item_to_bid_2 = [1202, 199, 'BID', 'iphone', 1200]
        auction_bid_2 = self.auction.bids._make(item_to_bid_2)
        assert not self.auction.validBidAction(auction_bid_2), True

    def test_12_bidItemFalse(self):
        item_to_sell = [999,250,'SELL','iphone',1000,1200]
        auction_item = self.auction.item._make(item_to_sell)
        self.auction.processOrders(auction_item)

        item_to_bid = [1000,233,'SELL','iphone',1000]
        auction_item_1 = self.auction.bids._make(item_to_bid)
        with pytest.raises(ValueError, match=r"Wrong Format for bidding"):
            self.auction.processOrders(auction_item_1)
        # testItem = AuctionItems('iphone',auction_item)

    def test_13_heartbeats1(self):
        item_to_sell = [999,250,'SELL','iphone',1000,1200]
        auction_item = self.auction.item._make(item_to_sell)
        self.auction.processOrders(auction_item)

        item_to_bid_2 = [1002, 199, 'BID', 'iphone', 1200]
        auction_bid_2 = self.auction.bids._make(item_to_bid_2)
        self.auction.processOrders(auction_bid_2)

        item_heartbeat = [1200]
        heartbeat_item = self.auction.hearbeat_type._make(item_heartbeat)
        self.auction.processOrders(heartbeat_item)
        assert self.auction.all_auction_items['iphone'].price_paid, 1200
        assert self.auction.all_auction_items['iphone'].status, 'SOLD'
        assert self.auction.all_auction_items['iphone'].highestBidder, 1002
        assert self.auction.all_auction_items['iphone'].lowest, 1200
        assert self.auction.all_auction_items['iphone'].highest, 1200

    def test_14_heartbeats2(self):
        item_to_sell = [999,250,'SELL','iphone',1000,1200]
        auction_item = self.auction.item._make(item_to_sell)
        self.auction.processOrders(auction_item)

        item_to_bid_1 = [1001,256,'BID','iphone',1100]
        auction_bid_1 = self.auction.bids._make(item_to_bid_1)
        self.auction.processOrders(auction_bid_1)

        item_to_bid_2 = [1002, 199, 'BID', 'iphone', 1350]
        auction_bid_2 = self.auction.bids._make(item_to_bid_2)
        self.auction.processOrders(auction_bid_2)

        item_heartbeat = [1200]
        heartbeat_item = self.auction.hearbeat_type._make(item_heartbeat)
        self.auction.processOrders(heartbeat_item)
        assert self.auction.all_auction_items['iphone'].price_paid, 1350
        assert self.auction.all_auction_items['iphone'].status, 'SOLD'
        assert self.auction.all_auction_items['iphone'].highestBidder, 1002
        assert self.auction.all_auction_items['iphone'].lowest, 1100
        assert self.auction.all_auction_items['iphone'].highest, 1350
        assert self.auction.all_auction_items['iphone'].total_bid_count, 2

    def test_15_heartbeats3(self):
        item_to_sell = [999,250,'SELL','iphone',1000,1200]
        auction_item = self.auction.item._make(item_to_sell)
        self.auction.processOrders(auction_item)

        item_to_bid_1 = [1001,256,'BID','iphone',1100]
        auction_bid_1 = self.auction.bids._make(item_to_bid_1)
        self.auction.processOrders(auction_bid_1)

        item_to_bid_2 = [1002, 199, 'BID', 'iphone', 900]
        auction_bid_2 = self.auction.bids._make(item_to_bid_2)
        self.auction.processOrders(auction_bid_2)

        item_to_bid_3 = [1003, 200, 'BID', 'iphone', 1350]
        auction_bid_3 = self.auction.bids._make(item_to_bid_3)
        self.auction.processOrders(auction_bid_3)

        item_heartbeat = [1200]
        heartbeat_item = self.auction.hearbeat_type._make(item_heartbeat)
        self.auction.processOrders(heartbeat_item)
        # assert self.auction.all_auction_items['iphone'].price_paid, 1350
        # assert self.auction.all_auction_items['iphone'].status, 'SOLD'
        # assert self.auction.all_auction_items['iphone'].highestBidder, 1002
        assert self.auction.all_auction_items['iphone'].lowest, 900
        # assert self.auction.all_auction_items['iphone'].highest, 1350
        assert self.auction.all_auction_items['iphone'].total_bid_count, 3

    def test_16_heartbeats4(self):
        item_to_sell = [999,250,'SELL','iphone',1000,1200]
        auction_item = self.auction.item._make(item_to_sell)
        self.auction.processOrders(auction_item)

        item_heartbeat = [1200]
        heartbeat_item = self.auction.hearbeat_type._make(item_heartbeat)
        self.auction.processOrders(heartbeat_item)
        assert (self.auction.all_auction_items['iphone'].price_paid ==  0.0), True
        assert self.auction.all_auction_items['iphone'].status, 'UNSOLD'
        assert (self.auction.all_auction_items['iphone'].highestBidder == ''), True
        # assert self.auction.all_auction_items['iphone'].lowest, 900
        assert (self.auction.all_auction_items['iphone'].highest ==  0), True
        assert (self.auction.all_auction_items['iphone'].total_bid_count == 0), True

    def test_17_wrongFormat(self):
        item = [999,250]
        with pytest.raises(ValueError, match=r"Wrong instruction format!"):
            self.auction.processOrders(item)

