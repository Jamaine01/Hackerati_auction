import sqlite3

conn = sqlite3.connect('auction.db', check_same_thread = False)
db = conn.cursor()


#starts the auction by initiating an item and price in database
def auction_setup(item, reserve_price):
	db.execute('''
		INSERT INTO auction(ItemName, ReservedPrice) VALUES(?,?)
		''', (item, reserve_price))
	conn.commit()

#bidder specifies auction and places bid
def make_bid(item, bidder, bid_price):
	db.execute('''
		INSERT INTO auction(ItemName, Buyer, Bid) VALUES(?,?,?)
		''', (item, bidder, bid_price))
	conn.commit()

#check for item to bid on
def check_item(item,):
	db.execute('''
		SELECT ItemName FROM auction WHERE ItemName = ?
		''', (item,))
	return db.fetchall()

#pulls entires to determine winner, highest bid, and if auction was a success
def pull_bids(item_final,):
	db.execute('''
		SELECT Buyer, Bid FROM auction WHERE ItemName = ?
		''', (item_final,))
	return db.fetchall()

#auctioner initiate the auction
item = raw_input('Enter item for auction: ')
price = raw_input('Enter reserved price: ').replace('$', '').replace(',', '')

#enter specs into database
auction_setup(item, price)

#bidder specify what item they're bidding for
bid_item = raw_input('What item would you like to bid on?...')

#checks database to see if item exist in auction
check = check_item(bid_item)

#checks if item in auction then proceeds to bid process
if len(check) >= 1:
	while True:
		take_bid = raw_input('Accept a bid?...')
		if take_bid == 'no':
			break
		else:
			bidder_bid = raw_input('Bid Item: ')
			bidder_name = raw_input('Enter Name: ')
			bidder_price = raw_input('Bid Price: ').replace('$', '').replace(',', '')
			#places bid in database
			make_bid(item, bidder_name, bidder_price)

bids = pull_bids(item)

#turn bids into a dictionary to reverse key, value pair to value, key pair
#turns bids into tuple to sort tuple by value first and return highest bidder

bids_dict = dict(bids)
bids_dict_reversed = dict((v,k) for k,v in bids_dict.iteritems())

#into tuple 
bids_tup = bids_dict_reversed.items()

#highest bidder
highest_bid = max(bids_tup)
winner = highest_bid[1]
paid = highest_bid[0]

print 'Winner: ', winner, '\n', 'Paid: ', paid

if paid >= price:
	print 'Auction Success!'
else:
	print 'Auction Failed...'



