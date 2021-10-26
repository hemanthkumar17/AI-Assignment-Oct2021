from functools import cache
from random import randint

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
            self.winningPath = {"A": {(0, 0): None}, "B": {(0, 0): None}}
            self.__WINNINGPOLICY = {"A": 1, "B": -1}
            self.playGamePaths()
        

    def displayGameTree(self, stack = None):
        if stack == None:
            stack = self.piles
        print("="*33 + "\n|    PILE 1\t|   PILE 2\t|")
        for _currpile in range(self.n_stone+1, 0, -1):
            print(f"|\t{'0' if stack[0] >= _currpile else ''}\t|\t{'0' if stack[1] >= _currpile else ''}\t|")
        print("="*33)

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

    # Creates the game tree that the bot plays with itself to figure out the winning path
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
                # 
                if evalScore != self.__WINNINGPOLICY[player] and paths[-1].data == self.__WINNINGPOLICY[player]:
                    evalScore = self.__WINNINGPOLICY[player]
                    self.winningPath[player][piles] = paths[-1]
        return Node(evalScore, (tuple(piles), player), paths)
    
                # self.config[(tuple(piles), player)] = Node()

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
                if pile != 0 and pile != 1:
                    continue
                if stack[pile] < n:
                    continue
                stack[pile] -= n
                print(f"\n{currPlayer} removed {n} stones from the pile {pile}\n")
                currPlayer = "Bot"
            else:
                if self.winningPath["A"][tuple(stack)]:
                    move = self.winningPath["A"][tuple(stack)].config[0]
                    pile = 1 if self.piles[0] == move[0] else 0
                    n = stack[pile] - move[pile]
                    stack = list(move)  
                    print(f"\nThe {currPlayer} removed {n} stones from the pile {pile}\n")
                    currPlayer = "You"
                else:
                    print("Bot Concedes !!")
                    stack = [0, 0]
        if currPlayer == "Bot":
            print("Congratulations!! You Win")
        else:
            print("You lose :( Better luck next time!")

def main():
    game = GameTree(4)
    game.playWithHuman()

if __name__ == "__main__":
    main()