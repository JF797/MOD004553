# assignment MOD004553.
# word guessing game

# imports
import time


# difficulties. If 0 then 'Easy' mode is selected
HARDMODE=False

# def showInstructions():
    
    

def showGameMenu():
    print("""Please select from one of the following options
          1 - Begin game.
          2 - Show information.
          3 - Choose difficulty.
          4 - Exit game.""")



# introduction to the code, this will run as soon as the program starts.
def introduction():
    print("Welcome to the word guessing game!")
    print(f'CURRENT DIFFICULTY MODE: {"EASY" if HARDMODE == False else "HARD"}')
    

def changeDifficulty(currentDifficulty):
    print(f"""Please select a difficulty for the game
          1 - Easy.
          2 - Hard.
          3 - Go back
          Currently selected: {'EASY' if currentDifficulty == False else 'HARD'} """)
    difficultyChoice = input("Please select an option.\n>>> ")
    match difficultyChoice:
        case "1":
            if currentDifficulty == False:
                print ("Difficulty mode already selected")
            else:
                return HARDMODE = False
        case "2":
            if currentDifficulty == True:
                print ("Difficulty mode already selected")
            else:
                return HARDMODE = True
        case "3":
            return


def getMenuOption(menuChoice, HARDMODE):
    match menuChoice:
        case "1":
            print(" Game starting")
            
        case "2":
            print("Show information")
            
        case "3":
            print("Choose difficultiy")
            HARDMODE = changeDifficulty(HARDMODE)
            main()
            
        case "4":
            print("Exit game")
            exit()
        case _:
            print("Not a valid option")
            getMenuOption(menuChoice)
    

def main():
    introduction()
    showGameMenu()
    menuChoice = input("Please select an option.\n>>> ")
    menuChoice = getMenuOption(menuChoice, HARDMODE)
    
main()