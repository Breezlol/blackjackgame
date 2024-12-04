# card_deck_classes.py

import random
import logging

class Card:
    """Represents a single playing card."""

    def __init__(self, suit, value):
        self.suit = suit
        self.value = value  # '2', '3', ..., '10', 'Jack', 'Queen', 'King', 'Ace'
        self.rank = self._get_rank()

    def _get_rank(self):
        """Convert card value to its rank for Blackjack scoring."""
        if self.value in ['Jack', 'Queen', 'King']:
            return 10
        elif self.value == 'Ace':
            return 11  # Ace initially counts as 11
        else:
            return int(self.value)

    def __str__(self):
        return f"{self.value} of {self.suit}"

class Deck:
    """Represents a multi-deck shoe used in casino Blackjack."""

    SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    VALUES = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

    def __init__(self, num_decks=6):
        """Initialize a shoe with multiple decks."""
        self.num_decks = num_decks
        self.cards = []
        self._create_shoe()

    def _create_shoe(self):
        """Create a shoe with multiple decks and shuffle it."""
        self.cards = []
        for _ in range(self.num_decks):
            for suit in self.SUITS:
                for value in self.VALUES:
                    self.cards.append(Card(suit, value))
        self.shuffle()

    def shuffle(self):
        """Shuffle the entire shoe."""
        random.shuffle(self.cards)

    def deal(self):
        """Deal a single card from the shoe."""
        total_cards = self.num_decks * len(self.SUITS) * len(self.VALUES)
        reshuffle_threshold = int(total_cards * 0.25)  # Reshuffle when 25% of the shoe remains
        if len(self.cards) <= reshuffle_threshold:
            logging.info("Reshuffling the shoe...")
            self._create_shoe()
        return self.cards.pop()
