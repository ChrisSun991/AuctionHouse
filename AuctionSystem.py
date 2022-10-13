import argparse
from OnlineAuction import OnlineAuction


def main():
    arguments = argparse.ArgumentParser()
    arguments.add_argument('--filename', type=str, default='input.txt')
    print("-----------------------------WELCOME TO THE ONLINE AUCTION-----------------------------")
    args = arguments.parse_args()

    auction = OnlineAuction(args.filename)
    print("---------------------------------instructions received---------------------------------")
    print("-------------------------------------AUCTION START-------------------------------------")

    auction.readAndClass()
    auction.processInstructionsList()
    print("----------------------------------------SUMMARY----------------------------------------")
    print('{:<8} {:<8} {:<8} {:<8} {:<8} {:<8} {:<8} {:<8}'.format('Close_Time', 'Item_Name', 'Winner', 'Status', 'Price_Paid', 'Total_Bid_Count', 'Highest_Price', 'Lowest_Price'))
    auction.returnAuctionValuesAsList()
    print("------------------------------------AUCTION CLOSED-------------------------------------")
    auction.writeOutput()


if __name__ == '__main__':
    main()
