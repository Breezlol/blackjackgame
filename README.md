
## Table of contents

- [Description of the program](#description-of-the-program)
- [How to run the program](how-to-run-the-program)
- [Gameplay instructions](gameplay-instructions)
- [License](license)

## Description of the program

- This program is a Python game of the classic casino game Blackjack. It allows you to play rounds against a virtual dealer.  The rules are shown uppon running the program. The goal of the game is to have a hand value of 21 or as close as possible without exceeding it. While also having a higher total than the dealer. In Blackjack, number cards are worth their face value. The face cards Jack, Queen, King are worth 10. Aces can be counted as either 1 or 11 wheich is dependant on which value is more advantageous to the hand. Players have options to  hit (taking another card), stand (ending their turn), doubling down, or split pairs. The program manages the deck as well. It shuffles the cards when 25% of the shoe remains. It also handles betting and player balances and keeps track of game statistics like wins, losses, and ties.

## How to run the program

- **Python 3.7** or higher.
  
**Download the ZIP File**:

**Extract the ZIP File**:
- Locate the downloaded ZIP file on your computer.
- Right-click the file and select **Extract All...** or use your preferred file extraction tool.
- Choose a destination folder where you want the project files to be extracted.
- Open the IDE of your choice and ooen the folder that you have extracted the files into.
- Make sure that the .txt files are in the same directory, so the program can read and write them.
- Run Main.py
- The game uses Python's standard libraries and does not require external packages.
 
## Gameplay instructions
- The game starts with a welcome message.
- You will be prompted to view the instructions; enter yes or no
- A list of available players from players.txt will be displayed.
- Enter the number corresponding to the player you wish to select.
- Place a Be, minimum bet is 5$ maximum is 500$, ensure you have suffiecient balance
- **Play a round**
   - You and the dealer are dealt two cards
   - Your and the dealer's value is displayed
   - choose h or hit to hit
   - choose s or stand to pass your play
   - choose d or double down to double your bet and take ONLY one more card and end your turn
   - Given you have 2 hands of the same value you can choose p, sp or split to split the hand
   - The dealer plays according to the rules. Stand on sll 17s and hit soft 17 (Example: 6 and Ace)
   - The outcome of the round is displayed upon choosing your move
   - You are prompted to play another round or exit.
   - The game end of you run out of funds.
   - Game results are saved to blackjack_results.txt
   - Player data is updated in players.txt
   - To refil a player balance you have to input the balance in the players.txt file the systanx is name, age, balance, wins, losses
## License
This project is licensed under the MIT License. See the LICENSE file for details.


 
