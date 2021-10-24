import random

  
class Environment():
    # The geography of the environment includes A and B positions, each having a cleaniness status: clean or dirty
    def __init__(self, location_status = None):
        if location_status == None:
            location_status = {
                "A": "Clean",
                "B": "Clean"
            }
        self.location_status = location_status.copy()

    def __str__(self):
        return f"(Environment) A: {self.location_status['A']}  B: {self.location_status['B']}"

    def isClean(self, location):
        return True if self.location_status[location] == "Clean" else False


class Bot():
    # Simple reflex Vaccumm cleaner bot that does not have any precept history
    def __init__(self, environment: Environment = None) -> None:
        self.environment = environment
        self.score = 0
        self.position = "A"
        self.action = "None"
    
    def __str__(self):
        return f"The Bot is now at position: {self.position} and has a score of {self.score} in the environment:\n{str(self.environment)}\nLast Performed Action: {self.action}"
    
    def suck(self):
        self.action = f"Suck the dirt at {self.position}"
        self.environment.location_status[self.position] = "Clean"
        self.score += 1
    
    def move(self, direction):
        if direction == "R":
            self.action = "Move Right"
            self.position = "B"         # If at A, simply moves right to B. If at B, bumps at the wall and stays at B
        else:
            self.action = "Move Left"
            self.position = "A"         # If at B, simply moves left to A. If at A, bumps at the wall and stays at A
    
    def moveRandomly(self):
        self.move("R" if random.randint(0, 1) == 1 else "L")

    def runSimulation(self, environment: Environment, initPosition: str, showSimulationReport: bool = False, lifetime: int = 1000):
        self.environment = environment
        self.score = 0
        self.position = initPosition
        for _ in range(lifetime):
            if showSimulationReport:
                print(str(self))
            if self.environment.isClean(self.position):
                self.moveRandomly()
            else:
                self.suck()
        print("-"*50 + f"\nThe bot has completed simulation on the environment\n\n {str(self.environment)}\n\n and has achieved a performance score of {self.score}\n" + "-"*50)

POSSIBLE_CONFIGURATIONS = [
    {"A": "Clean", "B": "Clean"},
    {"A": "Dirty", "B": "Clean"},
    {"A": "Clean", "B": "Dirty"},
    {"A": "Dirty", "B": "Dirty"},
]

def main():
    vaccummBot = Bot()
    report = []
    print("-"*50)
    for initPos in ["A", "B"]:
        for configuration in POSSIBLE_CONFIGURATIONS:
            environment = Environment(configuration)
            print(f"Environment prepared for simulation: \n{str(environment)}")
            print(f"Bot set at the initial position:- {initPos}")
            print("Running Simulation on the environment")
            vaccummBot.runSimulation(environment = environment,initPosition = initPos)
            report.append([configuration, initPos, vaccummBot.score])
    # Generating report for the simulations done with the bot on different configurations and initial positions
    print("\nTEST REPORT:")
    for env, pos, score in report:
        print("-"*50 + f"\nSimulation of Vaccumm Bot starting at {pos} on [ (Configuration) {str(env)[1:-1]} ] scored {score} performance points")
    print("-"*50)

if __name__ == "__main__":
    main()