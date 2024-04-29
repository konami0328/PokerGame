import random


class Cards:
    def __init__(self, suit: str, num: str):
        self._suit = suit
        self._num = num

    def score_of_card(self):
        # create a method that evaluates score of every card
        # if the num is an integer from 2 to 10, the score is itself
        # if the num is J, Q, K, the score is 10
        # if the num is A, the score is 1
        if self._num in ['2', '3', '4', '5', '6', '7', '8', '9', '10']:
            return int(self._num)
        elif self._num in ['J', 'Q', 'K']:
            return 10
        else:
            return 1

    def __repr__(self):
        return self._num + ' of ' + self._suit

    @property
    def suit(self):
        return self._suit

    @suit.setter
    def suit(self, suit):
        if suit in ['Heart', 'Spade', 'Club', 'Diamond']:
            self._suit = suit
        else:
            print("That's not a valid suit.")

    @property
    def num(self):
        return self._num

    @num.setter
    def num(self, num):
        if num in ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']:
            self._num = num
        else:
            print("That's not a valid number.")


class Deck:
    def __init__(self, num_of_deck=4):
        suits = ['Heart', 'Spade', 'Club', 'Diamond']
        nums = ['A', 'J', 'Q', 'K', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        # num_of_deck attribute defines how many decks will be generated, default 4 decks
        self.num_of_deck = num_of_deck
        # _cards attribute is a list contains all the card objects
        self._cards = [Cards(s, n) for s in suits for n in nums] * self.num_of_deck
        # once a deck instance is created, the cards will be shuffled automatically
        random.shuffle(self._cards)
        # print(self._cards)

    # once the deal method is called, it will return two things:
    # 1. the first element of the card list, which is the dealt card
    # 2. after dealing the first card, the left card list
    @property
    def deal(self):
        dealt_card = self._cards[0]
        self._cards.pop(0)
        return dealt_card, self._cards


class Players:
    def __init__(self, id: int, score=0, deck=Deck(4), num_of_players=None, dealt_cards_list=None):  # don't set dealt_cards_list as []
        self.id = id
        self.score = score
        self.deck = deck
        self.num_of_players = num_of_players  # the number of players input by the user
        self.dealt_cards_list = dealt_cards_list  # each player's dealt card list

    @staticmethod
    def generate_players(num_of_players):
        # generate a list of Player instances based on the number of players.
        return [Players(i) for i in range(1, num_of_players + 1)]

    @property
    def bust_check(self):
        # This method checks if the player’s score exceeds 21
        if self.score > 21:
            return True
        else:
            return False

    @property
    def winner_check(self):
        # This method checks if the player reaches 21 scores
        if self.score == 21:  # reach 21
            return True
        else:
            return False

    @property
    def blackjack_check(self):
        # This method checks if the player gets a blackjack
        num_list = []
        if len(self.dealt_cards_list) == 2:
            num_list.extend([self.dealt_cards_list[0].num, self.dealt_cards_list[1].num])
            if ['A', '10'] == num_list or ['A', 'J'] == num_list or ['A', 'Q'] == num_list or ['A', 'K'] == num_list:
                return True
        else:
            return False

    def hit(self):
        # the hit method means the player choose to be dealt a card
        # the dealt card will be appended to the dealt_cards_list
        # the score of the player will be updated
        # hit method prints the player's score after his score is updated
        dealt_card, self.deck._cards = self.deck.deal
        if self.dealt_cards_list is None:
            self.dealt_cards_list = []
        self.dealt_cards_list.append(dealt_card)
        self.score += dealt_card.score_of_card()
        if self.bust_check is True:
            print(f'The dealt card is {dealt_card}. The score of player {self.id} is {self.score}. The score of player {self.id} is busted.')
        else:
            print(f'The dealt card is {dealt_card}. The score of player {self.id} is {self.score}.')

    def stand(self):
        # the stand method means the player choose not to hit, just print the score
        print(f'The score of player {self.id} is {self.score}.')

    def choose(self, choice):
        # when the player choose input 'hit', call the hit method
        if choice == 'hit':
            return self.hit()
        # when the player choose input 'stand' while his score is less than 17, stand method is not allowed to be called
        # print the warning, and automatically call the hit method
        elif choice == 'stand':
            if self.score < 17:
                print('You cannot stand when your score is less than 17.')
                return self.hit()
            # when the player choose input 'stand' while his score is more than 17
            # call the stand method
            else:
                return self.stand()

    # The game is over when:
    # 1. only one player is left in the game; or
    # 2. one player reaches exact 21 scores or blackjack.
    @classmethod
    def game(self):
        players_list = Players.generate_players(self.num_of_players)

        def num_of_remaining_players(players_list):  # return the number of players who are still in the game
            return sum(1 for player in players_list if player.bust_check is False)

        while num_of_remaining_players(players_list) > 1:
            for i in range(len(players_list)):
                if players_list[i].bust_check is False:
                    while True:
                        try:
                            move = str(input(f"Now is player {players_list[i].id}'s turn. "
                                             f"Please input your move."
                                             f"You can only input 'hit' or 'stand'."))
                            if move in ['hit', 'stand']:
                                break
                            else:
                                print("Invalid input. You can only input 'hit' or 'stand'")
                        except ValueError:
                            print("Invalid input. You can only input 'hit' or 'stand'")

                    players_list[i].choose(move)

                    if players_list[i].blackjack_check is True:
                        print(f'Player {players_list[i].id} got a blackjack. You win.')
                        # print(players_list[i].dealt_cards_list)
                        return

                    if players_list[i].winner_check is True:
                        print(f'Player {players_list[i].id} reached 21 scores. You win.')
                        # print(players_list[i].dealt_cards_list)
                        return

                    # print(num_of_remaining_players(players_list))
                    if num_of_remaining_players(players_list) == 1:
                        print(f'Game over.')
                        return


while True:
    try:
        # input the number of players
        Players.num_of_players = int(input('How many players are engaged in the game? Please input a number from 2 to 6: '))
        if Players.num_of_players in [2, 3, 4, 5, 6]:
            break
        else:
            print("Invalid input. Please input a number from 2 to 6.")
    except ValueError:
        print("Invalid input. Please enter a valid integer between 2 and 6.")


# while True:
#     try:
#         # input the number of decks
#         Deck.num_of_deck = int(input('How many decks do you want to use? Please input an integer.'))
#         if Deck.num_of_deck >= 1:
#             break
#         else:
#             print("Invalid input. Please input a number greater than 1.")
#     except ValueError:
#         print("Invalid input. Please enter a valid integer.")


Players.game()