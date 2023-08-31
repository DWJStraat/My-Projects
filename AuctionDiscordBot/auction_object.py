class Auction:
    def __init__(self):
        self.participants = []
        self.bid = 0
        self.winner = None
        self.item_name = None
        self.item_description = None

    def start(self, item_name: str, item_description: str, item_price: int):
        self.item_name = item_name
        self.item_description = item_description
        self.bid = item_price
        self.winner = None

    def participate(self, user_id: int):
        self.participants += [user_id]

    def leave(self, user_id: int):
        self.participants.remove(user_id)

    def bid_func(self, user_id: int, bid: int):
        if bid > self.bid:
            self.bid = bid
            self.winner = user_id
            if user_id not in self.participants:
                self.participants += [user_id]
            return True
        else:
            return False

    def end(self):
        return (self.winner, self.bid) if self.winner is not None else (None, None)

    def view(self):
        return self.item_name, self.item_description, self.bid, self.winner