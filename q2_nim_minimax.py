
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
    f = open("output.txt", "w")
    def __init__(self, n_stone: int = 3):
        self.n_stone = n_stone
        self.winningPath = {}
        self.__WINNINGPOLICY = {"A": 1, "B": -1}
    
    def playGamePaths(self):
        self.piles = [self.n_stone]*2
        initNode = {}
        for player in ["A", "B"]:
            initNode[player] = self.createGameTree(self.piles, player)
            print("-"*50 + "\n" + str(initNode[player]))
            path = self.winningPath
            print("-"*50 + "\nWinningPath\n" + "-"*50)
            for config in self.winningPath:
                print(config)
                print(str(self.winningPath[config]))
                print("="*50)
            for node in [path[(tuple(self.piles), player)]]:
                if node == None:
                    break
                print(str(node))
                path = node
                print(node[0])

    def createGameTree(self, piles, player):
        nextPlayer = "A" if player == "B" else "B"      # The next player after this turn
        evalScore = -1 if player == "A" else 1          # If no winning path is found at this config, the player will lose
        paths = []
        self.winningPath[tuple(piles), player] = None
        for pile in range(2):                           # The player picks a pile to remove stones from
            for stones in range(1, piles[pile]+1):    # The player picks 1...leftover number of stones from the pile picked
                newPile = piles.copy()
                newPile[pile] -= stones
                self.winningPath[(tuple(newPile), player)] = "None"
                if newPile[0] == 0 and newPile[1] == 0:
                    paths.append(Node(1 if player == "A" else -1, ((0, 0), nextPlayer)))
                else:
                    paths.append(self.createGameTree(newPile, nextPlayer))
                self.f.write(str(paths[-1]))
                self.f.write("\nWinning Path next node: " + self.winningPath[tuple(newPile), player] + "\n" + "-"*50)
                if evalScore != self.__WINNINGPOLICY[player] and paths[-1].data == self.__WINNINGPOLICY[player]:
                    evalScore = self.__WINNINGPOLICY[player]
                    self.winningPath[tuple(piles), player] = paths[-1]
        return Node(evalScore, (tuple(piles), player), paths)
    
                # self.config[(tuple(piles), player)] = Node()



def main():
    game = GameTree()
    game.playGamePaths()
    game.f.close()
if __name__ == "__main__":
    main()