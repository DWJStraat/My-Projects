import random


class player:
    def __init__(self, name):
        self.name = name
        self.hand = None
        self.ante = None
        self.bet = None
        self.winnings = None

    def draw(self, deck_class, amount):
        self.hand = deck_class.draw(amount)


class deck:
    def __init__(self):
        self.cards = None
        self.selected_colors = []
        self.all_colors = [
            'brass', 'bronze', 'copper', 'gold', 'silver',
            'black', 'blue', 'green', 'red', 'white', 'shadow',
            'cloud', 'ordning', 'stone', 'storm',
            'ettin', 'fire', 'frost', 'hill'
        ]
        self.discarded_cards = []

    def add_color(self, color):
        if color in self.all_colors:
            self.selected_colors.append(color)
            self.all_colors.remove(color)
        else:
            print(f'Invalid color: {color}')

    def build_main_deck(self):
        cards = []
        good_dragons = {
            'brass': [1, 2, 3, 4, 5, 7, 9],
            'bronze': [1, 3, 6, 7, 8, 9, 11],
            'copper': [1, 3, 5, 6, 7, 8, 10],
            'gold': [2, 4, 6, 8, 9, 11, 13],
            'silver': [2, 3, 6, 7, 8, 10, 12],

        }
        evil_dragons = {
            'black': [1, 2, 3, 5, 6, 7, 9],
            'blue': [1, 2, 4, 6, 7, 9, 11],
            'green': [1, 2, 4, 5, 6, 8, 10],
            'red': [2, 3, 6, 7, 8, 10, 12],
            'white': [1, 2, 3, 4, 5, 6, 8],
            'shadow': [2, 3, 4, 6, 7, 9, 11]
        }
        good_giants = {
            'cloud': [1, 3, 6, 7, 8, 9, 11],
            'ordning': [2, 5, 7, 8, 9, 11, 12],
            'stone': [1, 2, 4, 6, 7, 9, 10],
            'storm': [2, 4, 6, 8, 10, 11, 13]
        }
        evil_giants = {
            'ettin': [1, 2, 3, 4, 5, 6, 7],
            'fire': [1, 3, 5, 7, 8, 9, 11],
            'frost': [1, 3, 4, 6, 7, 9, 10],
            'hill': [1, 2, 3, 5, 6, 7, 8]

        }
        for color in self.selected_colors:
            if color in good_dragons:
                cards.append([color, good_dragons[color]])
            elif color in evil_dragons:
                cards.append([color, evil_dragons[color]])
            elif color in good_giants:
                cards.append([color, good_giants[color]])
            elif color in evil_giants:
                cards.append([color, evil_giants[color]])
            else:
                print(f'Invalid color: {color}')

            self.discarded_cards.append([color])
        self.cards = cards

    def draw(self, amount):
        drawn_cards = []
        try:
            for _ in range(amount):
                color_index = random.randint(0, len(self.cards) - 1)
                card_index = random.randint(0, len(self.cards[color_index][1]) - 1)
                color = self.cards[color_index][0]
                card = self.cards[color_index][1][card_index]
                drawn_cards.append([color,card])
                self.cards[color_index][1].remove(
                    card)
        except ValueError:
            print('Out of cards, shuffling')
            self.shuffle()
        print(drawn_cards)

    def shuffle(self):
        for color in self.discarded_cards:
            self.cards[self.discarded_cards.index(color)][1].extend(color[1:])
            self.discarded_cards[self.discarded_cards.index(color)] = [color,[]]


deck = deck()
deck.add_color('brass')
deck.add_color('bronze')
deck.add_color('copper')
deck.build_main_deck()
