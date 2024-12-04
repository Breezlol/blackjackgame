# test_blackjack.py
import unittest
from card_deck_classes import Card, Deck
from player_hand_classes import Hand, Player
from Main import BlackjackGame

class TestCardDeckClasses(unittest.TestCase):

    def test_card_creation(self):
        card = Card('Hearts', 'Ace')
        self.assertEqual(card.suit, 'Hearts')
        self.assertEqual(card.value, 'Ace')
        self.assertEqual(card.rank, 11)

    def test_card_rank(self):
        card = Card('Spades', 'King')
        self.assertEqual(card.rank, 10)
        card = Card('Clubs', '7')
        self.assertEqual(card.rank, 7)

    def test_deck_creation(self):
        deck = Deck(num_decks=1)
        self.assertEqual(len(deck.cards), 52)
        suits = set(card.suit for card in deck.cards)
        values = set(card.value for card in deck.cards)
        self.assertEqual(suits, set(Deck.SUITS))
        self.assertEqual(values, set(Deck.VALUES))

    def test_deck_shuffle(self):
        deck1 = Deck(num_decks=1)
        deck2 = Deck(num_decks=1)
        self.assertNotEqual([card.value for card in deck1.cards], [card.value for card in deck2.cards])

    def test_deal_card(self):
        deck = Deck(num_decks=1)
        initial_count = len(deck.cards)
        card = deck.deal()
        self.assertIsInstance(card, Card)
        self.assertEqual(len(deck.cards), initial_count - 1)

class TestPlayerHandClasses(unittest.TestCase):

    def test_hand_add_card(self):
        hand = Hand()
        card = Card('Hearts', '5')
        hand.add_card(card)
        self.assertEqual(len(hand.cards), 1)
        self.assertEqual(hand.cards[0], card)

    def test_hand_value_no_aces(self):
        hand = Hand()
        hand.add_card(Card('Hearts', '5'))
        hand.add_card(Card('Diamonds', '9'))
        self.assertEqual(hand.calculate_value(), 14)

    def test_hand_value_with_aces(self):
        hand = Hand()
        hand.add_card(Card('Hearts', 'Ace'))
        hand.add_card(Card('Diamonds', '9'))
        self.assertEqual(hand.calculate_value(), 20)
        hand.add_card(Card('Clubs', '5'))
        self.assertEqual(hand.calculate_value(), 15)  # Ace counts as 11 -> 1

    def test_hand_blackjack(self):
        hand = Hand()
        hand.add_card(Card('Hearts', 'Ace'))
        hand.add_card(Card('Spades', 'King'))
        self.assertTrue(hand.is_blackjack())

    def test_player_place_bet(self):
        player = Player('TestPlayer', 1000, 30)
        hand = player.place_bet(100)
        self.assertEqual(player.balance, 900)
        self.assertEqual(hand.bet, 100)

    def test_player_insufficient_funds(self):
        player = Player('TestPlayer', 50, 30)
        with self.assertRaises(ValueError):
            player.place_bet(100)

    def test_player_double_down(self):
        player = Player('TestPlayer', 1000, 30)
        hand = player.place_bet(100)
        hand.add_card(Card('Hearts', '9'))
        hand.add_card(Card('Diamonds', '2'))
        player.double_down(hand)
        self.assertEqual(player.balance, 800)
        self.assertEqual(hand.bet, 200)
        self.assertFalse(hand.can_double)

    def test_player_split_hand(self):
        player = Player('TestPlayer', 1000, 30)
        hand = player.place_bet(100)
        hand.add_card(Card('Hearts', '8'))
        hand.add_card(Card('Diamonds', '8'))
        hand.can_split = True
        hand1, hand2 = player.split_hand(hand)
        self.assertEqual(len(player.hands), 2)
        self.assertEqual(player.balance, 800)
        self.assertEqual(hand1.bet, 100)
        self.assertEqual(hand2.bet, 100)
        self.assertEqual(len(hand1.cards), 1)
        self.assertEqual(len(hand2.cards), 1)

class TestBlackjackGame(unittest.TestCase):

    def setUp(self):
        self.game = BlackjackGame()
        self.game.round_number = 1  # Initialize round_number for tests
        # Mock player
        self.game.player = Player('TestPlayer', 1000, 30)
        self.game.dealer_hand = Hand()
        self.game.player.hands = []

    def test_player_wins(self):
        self.game.player.balance = 1000
        player_hand = self.game.player.place_bet(100)
        player_hand.add_card(Card('Hearts', '10'))
        player_hand.add_card(Card('Diamonds', '9'))  # 19

        self.game.dealer_hand.cards = [Card('Clubs', '7'), Card('Spades', '9')]  # Dealer 16

        # Simulate dealer's turn
        self.game._dealer_turn()

        # Resolve bets
        self.game._resolve_bets()

        # Expected balance: 1000 - 100 (bet) + 200 (payout) = 1100
        self.assertEqual(self.game.player.balance, 1100)  # Won $100

    def test_player_busts(self):
        self.game.player.balance = 1000
        player_hand = self.game.player.place_bet(100)
        player_hand.add_card(Card('Hearts', 'King'))
        player_hand.add_card(Card('Diamonds', '9'))
        player_hand.add_card(Card('Clubs', '5'))  # Bust (24)

        self.game.dealer_hand.cards = [Card('Clubs', '7'), Card('Spades', '9')]  # Dealer 16

        # No dealer turn needed since player busts
        self.game._resolve_bets()

        # Expected balance: 1000 - 100 (bet) = 900
        self.assertEqual(self.game.player.balance, 900)  # Lost $100

    def test_dealer_busts(self):
        self.game.player.balance = 1000
        player_hand = self.game.player.place_bet(100)
        player_hand.add_card(Card('Hearts', '8'))
        player_hand.add_card(Card('Diamonds', '9'))  # 17

        self.game.dealer_hand.cards = [Card('Clubs', '10'), Card('Spades', '6')]  # Dealer 16
        self.game.dealer_hand.add_card(Card('Hearts', 'Queen'))  # Dealer total: 26

        # Resolve bets
        self.game._resolve_bets()

        # Expected balance: 1000 - 100 (bet) + 200 (payout) = 1100
        self.assertEqual(self.game.player.balance, 1100)  # Won $100

    def test_push(self):
        self.game.player.balance = 1000
        player_hand = self.game.player.place_bet(100)
        player_hand.add_card(Card('Hearts', '10'))
        player_hand.add_card(Card('Diamonds', '7'))  # 17

        self.game.dealer_hand.cards = [Card('Clubs', '9'), Card('Spades', '8')]  # Dealer 17

        # Resolve bets
        self.game._resolve_bets()

        # Expected balance: 1000 - 100 (bet) + 100 (returned bet) = 1000
        self.assertEqual(self.game.player.balance, 1000)  # Bet returned

    def test_blackjack_payout(self):
        self.game.player.balance = 1000
        player_hand = self.game.player.place_bet(100)
        player_hand.add_card(Card('Hearts', 'Ace'))
        player_hand.add_card(Card('Diamonds', 'King'))  # Blackjack

        self.game.dealer_hand.cards = [Card('Clubs', '9'), Card('Spades', '8')]  # Dealer 17

        # Resolve bets
        self.game._resolve_bets()

        # Expected balance: 1000 - 100 (bet) + 250 (payout) = 1150
        self.assertEqual(self.game.player.balance, 1150)  # Won $150 (1.5x payout)

    def test_dealer_blackjack(self):
        self.game.player.balance = 1000
        player_hand = self.game.player.place_bet(100)
        player_hand.add_card(Card('Hearts', 'Ace'))
        player_hand.add_card(Card('Diamonds', 'King'))  # Player Blackjack

        self.game.dealer_hand.cards = [Card('Clubs', 'Ace'), Card('Spades', 'King')]  # Dealer Blackjack

        # Resolve bets
        self.game._resolve_bets()

        # Expected balance: 1000 - 100 (bet) + 100 (returned bet) = 1000
        self.assertEqual(self.game.player.balance, 1000)  # Push (tie)

if __name__ == '__main__':
    unittest.main()
