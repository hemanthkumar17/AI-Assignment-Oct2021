from functools import cache
from random import randint

# A node class of the game, showing a particular config and possible choices
# A bot will hold an evaluation data to check if it can win from that config or not
class Node():
    def __init__(self, data: int, config: tuple, children: list = []):
        self.children = children
        self.data = data
        self.config = config

    def __str__(self):
        if self.children:
            string = f"\nCurrent configuration: {self.config}\nEvaluation Score: {self.data}\nPossible Configuration paths: {str([{child.config: child.data} for child in self.children])}\n"
            return string
        else:
            return f"\nCurrent configuration: {self.config}\nEvaluation Score: {self.data}\nNo possible paths from this point\n"

class GameTree():
    def __init__(self, n_stone: int = 3):
        with open("output.txt", "w") as f:
            self.f = f
            self.n_stone = n_stone
            self.winningPath = {"A": {(0, 0): None}, "B": {(0, 0): None}}   # Contains a map of all the winning paths
            self.__WINNINGPOLICY = {"A": 1, "B": -1}
            self.playGamePaths()
        
    # Displays the nim game stacks
    def displayGameTree(self, stack = None):
        if stack == None:
            stack = self.piles
        print("="*33 + "\n|    PILE 1\t|   PILE 2\t|")
        for _currpile in range(self.n_stone+1, 0, -1):
            print(f"|\t{'0' if stack[0] >= _currpile else ''}\t|\t{'0' if stack[1] >= _currpile else ''}\t|")
        print("="*33)

    # Runs a simulation where the bot plays with another bot to map the winning path
    def playGamePaths(self, consoleOutput = False):
        self.piles = tuple([self.n_stone]*2)
        initNode = {}
        for player in ["A", "B"]:
            initNode[player] = self.createGameTree(self.piles, player)
        if consoleOutput:
            print("-"*50 + "\nWinningPath\n" + "-"*50)
        for initPlayer in ["A", "B"]:
            if consoleOutput:
                print("="*50 + f"\nWinning Map for player {initPlayer}\n")
            self.f.write("\n" + "="*40 + f"\nWinning Map for player {initPlayer}\n")
            for config in self.winningPath[initPlayer]:
                if self.winningPath[initPlayer][config]:
                    self.f.write(f"{config}: {self.winningPath[initPlayer][config].config[0]}\n")
                else:
                    if consoleOutput:
                        print(f"{config}: No winning path")
                    self.f.write(f"{config}: No winning Config\n")

    # Creates the game tree that the bot plays with itself to figure out the winning path, recursively calling
    # functools.cache is placed to apply dynamic programming to accomodate faster mapping (Does not have to play the same move twice)
    @cache
    def createGameTree(self, piles, player):
        nextPlayer = "A" if player == "B" else "B"      # The next player after this turn
        evalScore = -1 if player == "A" else 1          # If no winning path is found at this config, the player will lose
        paths = []
        if tuple(piles) not in self.winningPath[player]:
            self.winningPath[player][piles] = None
        for pile in range(2):                           # The player picks a pile to remove stones from
            for stones in range(1, piles[pile]+1):      # The player picks 1...leftover number of stones from the pile picked
                newPile = list(piles)
                newPile[pile] -= stones
                newPile = tuple(newPile)
                if newPile[0] == 0 and newPile[1] == 0:     # If the game is over, the evaluation is done to decide who won and a leaf node is created   
                    paths.append(Node(1 if player == "A" else -1, ((0, 0), nextPlayer)))
                else:                                       # Plays the move to change config from piles->newPile and waits for the next player to play
                    paths.append(self.createGameTree(newPile, nextPlayer))
                self.f.write(str(paths[-1]))
                self.f.write("\nWinning Path next node: " + str(self.winningPath[nextPlayer][newPile]) + "\n" + "-"*50)
                # If a winning path has already been found, the eval score does not need a change
                # If the path jus traversed is the winning path, we update the winningPath and set the data of current node
                if evalScore != self.__WINNINGPOLICY[player] and paths[-1].data == self.__WINNINGPOLICY[player]:
                    evalScore = self.__WINNINGPOLICY[player]
                    self.winningPath[player][piles] = paths[-1]
        if not self.winningPath[player][piles]:
            self.winningPath[player][piles] = paths[0]
        return Node(evalScore, (tuple(piles), player), paths)
    
    # The bot plays with the human via console input
    # A coin toss decides if the human or the bot goes first
    def playWithHuman(self):
        stack = list(self.piles)
        currPlayer = "You" if randint(0, 1) else "Bot"
        print(f"{currPlayer} won the toss!\n{currPlayer} First")
        while stack != [0, 0]:
            self.displayGameTree(stack)
            if currPlayer == "You":
                pile, n = input("\nChoose a pile to remove from followed by the number of stones: ").split()
                pile = int(pile) - 1
                n = int(n)
                if pile != 0 and pile != 1: # Invalid pile number([1, 2] should be the only possible input of the user)
                    continue
                if stack[pile] < n:         # Not enough stones to remove
                    continue
                stack[pile] -= n
                print(f"\n{currPlayer} removed {n} stones from the pile {pile}\n")
                currPlayer = "Bot"
            else:
                if self.winningPath["A"][tuple(stack)]:
                    move = self.winningPath["A"][tuple(stack)].config[0]
                    pile = 1 if stack[0] == move[0] else 0
                    n = stack[pile] - move[pile]

                stack = list(move)  
                print(f"\nThe {currPlayer} removed {n} stones from the pile {pile}\n")
                currPlayer = "You"
                    
        if currPlayer == "Bot":
            print("Congratulations!! You Win")
        else:
            print("You lose :( Better luck next time!")
    
    def playWithBot(self):
        stack = list(self.piles)
        currPlayer = "Bot1" if randint(0, 1) else "Bot2"
        print(f"{currPlayer} won the toss!\n{currPlayer} First")
        while stack != [0, 0]:
            self.displayGameTree(stack)
            if currPlayer == "Bot1":
                move = self.winningPath["A"][tuple(stack)].config[0]
                pile = 1 if stack[0] == move[0] else 0
                n = stack[pile] - move[pile]

                stack = list(move)  
                print(f"\nThe {currPlayer} removed {n} stones from the pile {pile}\n")
                currPlayer = "Bot2"
            else:
                move = self.winningPath["A"][tuple(stack)].config[0]
                pile = 1 if stack[0] == move[0] else 0
                n = stack[pile] - move[pile]

                stack = list(move)  
                print(f"\nThe {currPlayer} removed {n} stones from the pile {pile}\n")
                currPlayer = "Bot1"
                    
        if currPlayer == "Bot1":
            print("Bot1 Wins")
        else:
            print("Bot2 Wins")

def main():
    game = GameTree(4)      # Creates and trains the bot
    p = input("Do you wanna play?(Y/N) ")
    if p == 'Y':
        game.playWithHuman()    # A game between the human and the bot is initiated
    else:
        game.playWithBot()

if __name__ == "__main__":
    main()