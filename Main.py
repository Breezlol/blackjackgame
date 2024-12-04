import sys
import logging
from datetime import datetime
from card_deck_classes import Deck
from player_hand_classes import Player, Hand

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

class BlackjackGame:

    def __init__(self, output_file=None):
        self.deck = Deck()
        self.dealer_hand = Hand()
        self.player = None
        self.output_file = output_file or "blackjack_results.txt"
        self.players_info = self._load_players()
        self.round_number = 1  # Initialize round counter

    def _load_players(self):

        players = []
        try:
            with open('players.txt', 'r') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        parts = line.split(',')
                        if len(parts) == 5:
                            name, age, balance, wins, losses = parts
                            players.append({
                                'name': name.strip(),
                                'age': int(age.strip()),
                                'balance': float(balance.strip()),
                                'wins': int(wins.strip()),
                                'losses': int(losses.strip())
                            })
                        else:
                            print("Error: Each line in 'players.txt' must contain name, age, balance, wins, and losses separated by commas.")
                            sys.exit(1)
        except FileNotFoundError:
            print("Error: 'players.txt' file not found.")
            sys.exit(1)
        except ValueError:
            print("Error: 'players.txt' file contains invalid data.")
            sys.exit(1)
        return players

    def start_game(self):
        """Initialize the game with player information."""
        print("****************************************")
        print("**          Welcome to Blackjack      **")
        print("****************************************")

        # Offer instructions
        view_instructions = input("Would you like to view the instructions? (yes/no): ").lower()
        if view_instructions in ['yes', 'y']:
            self._show_instructions()

        # Present player options
        print("\nAvailable players:")
        for idx, player_info in enumerate(self.players_info, start=1):
            print(f"{idx}. {player_info['name']} (Age: {player_info['age']}) | Balance: {player_info['balance']}")

        # Ask the user to select a player
        while True:
            selection = input(f"Select player (1-{len(self.players_info)}): ")
            try:
                selection = int(selection)
                if 1 <= selection <= len(self.players_info):
                    selected_player_info = self.players_info[selection - 1]
                    break
                else:
                    print(f"Please enter a number between 1 and {len(self.players_info)}.")
            except ValueError:
                print("Please enter a valid number.")

        name = selected_player_info['name']
        age = selected_player_info['age']
        balance = selected_player_info['balance']
        wins = selected_player_info['wins']
        losses = selected_player_info['losses']

        self.player = Player(name, balance, age, wins, losses)
        self.round_number = 1  # Initialize round counter
        self._play_rounds()

    def _show_instructions(self):

        print("""
=== Blackjack Instructions ===
Objective:
Get as close to 21 without going over. Face cards are worth 10, Aces are worth 1 or 11.

Actions:
- Hit: Take another card.
- Stand: End your turn.
- Double Down: Double your bet and receive one more card.
- Split: If your first two cards are the same, you can split them into two hands.

Dealer Rules:
- Dealer must hit until their cards total 17 or higher.
- Dealer hits on a soft 17 (a hand totaling 17 with an Ace counted as 11).
""")

    def _play_rounds(self):

        while True:
            print("\n========================================")
            print(f"            ROUND {self.round_number}")
            print("========================================\n")
            # Reset for new round
            self.deck = Deck()
            self.dealer_hand = Hand()
            self.player.reset_hands()

            # Betting
            MIN_BET = 5
            MAX_BET = 500
            while True:
                print("----------------------------------------")
                bet_input = input(
                    f"Your current balance is ${self.player.balance:.2f}. Enter your bet (${MIN_BET}-${MAX_BET}): ")
                try:
                    bet = float(bet_input)
                    if bet < MIN_BET or bet > MAX_BET:
                        print(f"Bet must be between ${MIN_BET} and ${MAX_BET}.")
                        continue
                    if bet > self.player.balance:
                        print("Insufficient funds to place this bet.")
                        continue
                    current_hand = self.player.place_bet(bet)
                    break
                except ValueError:
                    print("Please enter a valid number.")

            # Initial deal
            current_hand.add_card(self.deck.deal())
            current_hand.add_card(self.deck.deal())
            self.dealer_hand.add_card(self.deck.deal())
            self.dealer_hand.add_card(self.deck.deal())

            # Display initial hands
            print("\n/// Dealing cards... Good Luck! ///\n")
            print("*************************")
            print(f"Your hand: {current_hand}")
            print(f"Your hand value: {current_hand.calculate_value()}")
            print("*************************\n")
            print(f"Dealer's visible card: {self.dealer_hand.cards[0]}")
            print(f"Dealer's visible card value: {self.dealer_hand.cards[0].rank}")

            # Player's turn for each hand (supporting multiple hands after split)
            for hand_index, hand in enumerate(self.player.hands):
                print("\n----------------------------------------")
                print(f"         PLAYING HAND {hand_index + 1}")
                print("----------------------------------------")
                self._player_turn(hand)

            # Dealer's turn
            self._dealer_turn()

            # Resolve bets
            self._resolve_bets()

            # Check if player has funds to continue
            if self.player.balance <= 0:
                print("\nYou have run out of funds. Game over.")
                break

            # Ask to continue
            play_again = input("\nWould you like to play another round? (yes/no): ").lower()
            if play_again not in ['yes', 'y']:
                break
            self.round_number += 1  # Increment round counter

        # End of game, save results
        self._save_game_results()
        self._update_player_data()

    def _player_turn(self, hand):
        """Handle player's turn for a single hand."""
        while True:
            hand_value = hand.calculate_value()
            if hand_value == 21:
                print("★★★ Blackjack! ★★★")
                break

            if hand_value > 21:
                print("Bust!")
                break

            # Prepare action options
            actions = ['(H)it', '(S)tand']
            valid_actions = ['h', 'hit', 's', 'stand']

            # Add double down option if available
            if hand.can_double and self.player.balance >= hand.bet:
                actions.append('(D)ouble down')
                valid_actions.extend(['d', 'double down'])

            # Add split option if available
            if hand.can_split and self.player.balance >= hand.bet:
                actions.append('S(P)lit')
                valid_actions.extend(['p', 'split', 'sp'])

            # Prompt for action
            action_prompt = f"Options: {', '.join(actions)}. What would you like to do? "
            action = input(action_prompt).lower()

            if action not in valid_actions:
                print("Invalid action. Please choose from the available options.")
                continue

            # Handle actions
            if action in ['h', 'hit']:
                hand.add_card(self.deck.deal())
                print("\n*************************")
                print(f"Your hand: {hand}")
                print(f"Hand value: {hand.calculate_value()}")
                print("*************************\n")
            elif action in ['s', 'stand']:
                break
            elif action in ['d', 'double down']:
                try:
                    self.player.double_down(hand)
                    hand.add_card(self.deck.deal())
                    print("\n--- Doubled Down! ---")
                    print("*************************")
                    print(f"Your hand: {hand}")
                    print(f"Hand value: {hand.calculate_value()}")
                    print("*************************\n")
                    break
                except ValueError as e:
                    print(e)
            elif action in ['p', 'split', 'sp']:
                try:
                    # Perform split
                    hand1, hand2 = self.player.split_hand(hand)

                    # Deal additional cards to each split hand
                    hand1.add_card(self.deck.deal())
                    hand2.add_card(self.deck.deal())

                    print("\n/// Hand Split! ///\n")
                    print(f"Hand 1: {hand1}")
                    print(f"Hand 2: {hand2}")
                    break
                except ValueError as e:
                    print(e)

    def _dealer_turn(self):

        print("\n========================================")
        print("            DEALER'S TURN")
        print("========================================")
        print(f"\nDealer's hand: {self.dealer_hand}")
        print(f"Dealer's hand value: {self.dealer_hand.calculate_value()}")

        # Dealer hits on 16 or less, hits on soft 17
        while True:
            dealer_value = self.dealer_hand.calculate_value()
            if dealer_value < 17:
                self.dealer_hand.add_card(self.deck.deal())
                print("\nDealer hits.")
                print(f"Dealer's new hand: {self.dealer_hand}")
                print(f"Dealer's hand value: {self.dealer_hand.calculate_value()}")
            elif dealer_value == 17 and self.dealer_hand.is_soft_hand():
                self.dealer_hand.add_card(self.deck.deal())
                print("\nDealer hits on soft 17.")
                print(f"Dealer's new hand: {self.dealer_hand}")
                print(f"Dealer's hand value: {self.dealer_hand.calculate_value()}")
            else:
                print("\nDealer stands.")
                break

        if self.dealer_hand.calculate_value() > 21:
            print("\nDealer busts!")

    def _resolve_bets(self):
        """Resolve bet outcomes for all hands."""
        print("\n=== Results for Round {} ===".format(self.round_number))
        print("----------------------------------------")

        dealer_value = self.dealer_hand.calculate_value()
        dealer_blackjack = self.dealer_hand.is_blackjack()

        for hand_index, player_hand in enumerate(self.player.hands):
            print(f"\n*** Hand {hand_index + 1} ***")
            player_value = player_hand.calculate_value()
            player_blackjack = player_hand.is_blackjack()

            print(f"Your hand: {player_hand}")
            print(f"Hand value: {player_value}")

            # Initialize total_payout to 0
            total_payout = 0

            # Check outcomes
            if player_blackjack and not dealer_blackjack:
                # Blackjack payout is 3:2 (1.5 times the bet)
                total_payout = player_hand.bet * 2.5  # Original bet + winnings
                print(f"Blackjack! You win ${player_hand.bet * 1.5:.2f}!")
                self.player.record_win()
            elif not player_blackjack and dealer_blackjack:
                print("Dealer has Blackjack. You lose.")
                self.player.record_loss()
            elif player_value > 21:
                print("Bust! You lose.")
                self.player.record_loss()
            elif dealer_value > 21:
                # Player wins, payout is 1:1
                total_payout = player_hand.bet * 2  # Original bet + winnings
                print(f"Dealer busts! You win ${player_hand.bet:.2f}!")
                self.player.record_win()
            elif player_value > dealer_value:
                # Player wins, payout is 1:1
                total_payout = player_hand.bet * 2  # Original bet + winnings
                print(f"You win ${player_hand.bet:.2f}!")
                self.player.record_win()
            elif player_value < dealer_value:
                print("Dealer wins. You lose.")
                self.player.record_loss()
            else:
                # Push (tie), player gets their bet back
                total_payout = player_hand.bet  # Return original bet
                print("Push (tie). Your bet is returned.")
                self.player.record_tie()

            # Update player's balance if there's a payout
            if total_payout > 0:
                self.player.add_winnings(total_payout)

        print("----------------------------------------")
        print(f"Your new balance is: ${self.player.balance:.2f}")
        print(f"Wins: {self.player.wins} | Losses: {self.player.losses} | Ties: {self.player.ties}")

    def _save_game_results(self):
        """Save game results to a text file."""
        try:
            with open(self.output_file, 'a') as f:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"Player: {self.player.name}\n")
                f.write(f"Ending Balance: ${self.player.balance:.2f}\n")
                f.write(f"Wins: {self.player.wins}\n")
                f.write(f"Losses: {self.player.losses}\n")
                f.write(f"Ties: {self.player.ties}\n")
                f.write(f"Timestamp: {timestamp}\n")
                f.write("=" * 30 + "\n")
            print(f"\nGame results saved to {self.output_file}")
        except IOError as e:
            print(f"Error saving game results: {e}")

    def _update_player_data(self):
        """Update player's data in 'players.txt'."""
        try:
            # Read all player data
            with open('players.txt', 'r') as f:
                lines = f.readlines()

            # Update the selected player's data
            with open('players.txt', 'w') as f:
                for line in lines:
                    parts = line.strip().split(',')
                    if parts[0] == self.player.name:
                        # Update balance and statistics
                        new_line = f"{self.player.name},{self.player.age},{self.player.balance},{self.player.wins},{self.player.losses}\n"
                        f.write(new_line)
                    else:
                        f.write(line)
            print("Player data updated successfully.")
        except Exception as e:
            print(f"Error updating player data: {e}")

def main():
    # Allow optional output file as command-line argument
    output_file = sys.argv[1] if len(sys.argv) > 1 else None

    game = BlackjackGame(output_file)
    game.start_game()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
