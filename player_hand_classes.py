# player_hand_classes.py

class Hand:
    """Represents a hand of cards for a player or dealer."""

    def __init__(self):
        self.cards = []
        self.bet = 0
        self.is_split = False
        self.can_split = False
        self.can_double = True

    def add_card(self, card):
        """Add a card to the hand."""
        self.cards.append(card)

        # Update split eligibility
        if len(self.cards) == 2:
            # Allow splitting if cards have the same rank
            self.can_split = (self.cards[0].rank == self.cards[1].rank)
        else:
            self.can_split = False  # Can't split after more than 2 cards

        # Disable double after first hit
        if len(self.cards) > 2:
            self.can_double = False

    def calculate_value(self):
        """Calculate the total value of the hand."""
        value = sum(card.rank for card in self.cards)

        # Adjust for Aces
        num_aces = sum(1 for card in self.cards if card.value == 'Ace')
        while value > 21 and num_aces:
            value -= 10  # Treat an Ace as 1 instead of 11
            num_aces -= 1

        return value

    def is_blackjack(self):
        """Check if the hand is a Blackjack."""
        return len(self.cards) == 2 and self.calculate_value() == 21

    def is_soft_hand(self):
        """Check if the hand is a soft hand (contains an Ace counted as 11)."""
        value = sum(card.rank for card in self.cards)
        num_aces = sum(1 for card in self.cards if card.value == 'Ace')
        return num_aces > 0 and value <= 21

    def __str__(self):
        return ", ".join(str(card) for card in self.cards)


class Player:
    """Represents a player in the Blackjack game."""

    def __init__(self, name, balance, age, wins=0, losses=0):
        self.name = name
        self.age = age
        self.balance = balance
        self.hands = []
        self.wins = wins
        self.losses = losses
        self.ties = 0  # Initialize ties to 0

    def place_bet(self, amount):
        """Place a bet for the player."""
        if amount > self.balance:
            raise ValueError("Insufficient funds to place this bet.")
        if amount <= 0:
            raise ValueError("Bet amount must be greater than zero.")
        self.balance -= amount
        hand = Hand()
        hand.bet = amount
        self.hands.append(hand)
        return hand

    def double_down(self, hand):
        """Double the bet for the current hand."""
        if not hand.can_double:
            raise ValueError("Cannot double down at this point.")

        if self.balance < hand.bet:
            raise ValueError("Insufficient funds to double down.")

        self.balance -= hand.bet
        hand.bet *= 2
        hand.can_double = False
        return hand

    def split_hand(self, hand):
        """Split a hand into two hands."""
        if not hand.can_split:
            raise ValueError("Cannot split this hand.")

        if self.balance < hand.bet:
            raise ValueError("Insufficient funds to split.")

        # Create a new hand with the second card
        split_hand = Hand()
        split_hand.add_card(hand.cards.pop())
        split_hand.bet = hand.bet
        split_hand.is_split = True

        # Deduct additional bet from balance
        self.balance -= hand.bet

        # Mark original hand as split
        hand.is_split = True

        # Add the new split hand
        self.hands.append(split_hand)
        return hand, split_hand

    def add_winnings(self, amount):
        """Add winnings to the player's balance."""
        self.balance += amount

    def reset_hands(self):
        """Clear player's hands between rounds."""
        self.hands = []

    def record_win(self):
        """Record a win."""
        self.wins += 1

    def record_loss(self):
        """Record a loss."""
        self.losses += 1

    def record_tie(self):
        """Record a tie."""
        self.ties += 1
