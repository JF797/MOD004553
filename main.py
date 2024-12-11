# assignment MOD004553.
# word guessing game

# imports
import time
import sys
import random
import os
import re


# difficulties. If 0 then 'Easy' mode is selected
HARDMODE=False

def clearScreen():
    if os.name == 'nt':
        print("clearing screen")
        os.system("cls")
    else:
        os.system("clear")

# Don't think this is required.
def generateWordLengthPossibility(words):
    longest = len(max(words, key=len))
    print(f'LONGEST: {max(words, key=len)}')
    shortest = len(min(words, key=len))
    print(f'SHORTEST: {min(words, key=len)}')
    return longest, shortest

def readDictionary(filename):
    print(f'Reading word list from file name: {filename}')
    wordList= []
    try:
        with open (filename, "r") as dictionaryFile:
            for word in dictionaryFile:
                wordList.append(word.strip())
        return wordList
    except(FileNotFoundError):
        print("File not found in directory of this program. Please correct this\nProgram will now exit.")
        sys.exit()


def generateSelectedWordList(desiredWordLength, wordList):
    selectedWordList = []
    for word in wordList:
        if len(word) == desiredWordLength:
            selectedWordList.append(word)
    return selectedWordList

def pickWordFromWordList(wordListFileName):
    wordList = readDictionary(wordListFileName)
    print("Computer is selecting a word length")
    # longestWordLength, shortestWordLength = generateWordLengthPossibility(wordList)
    # desiredWordLength=random.randint(shortestWordLength, longestWordLength)
    desiredWordLength=random.randint(4, 12)
    print(f'Word length selected: {desiredWordLength}')
    print(f'Generating word list from length')
    selectedWordList = generateSelectedWordList(desiredWordLength, wordList)
    print ("computer is choosing word from list")
    selectedWord = selectedWordList[random.randint(0, len(selectedWordList))]
    print (f'Selected Word: {selectedWord}')   
    return selectedWordList, selectedWord, desiredWordLength

def showInstructions():
    x = 0
    print(f"""The rules of the game are as follows:
          Player 1 - You.
          Player 2 - The computer.
          
          The computer  will choose a word from a set dictionary containing {x} words.
          Player 1 will then begin guessing the word that has been selected.
          Every correct letter guessed will reveal on the screen, allowing you to better guess the word.
          The game ends when either all the letters in the word have been guessed, or Player 1 has run out of guesses.
          The number of guesses will depend on the length of the word.
          
          Hard mode:
          Each turn, the computer will keep a list of "possible" words to choose from based on the length of the word.
          At any point in time, the computer can change the word selected from the named list, if the letters guessed will get them closer to losing.
          The idea of this is to prolong the game and make player 1 run out of guesses quicker.
          """)
    

def showGameMenu(HARDMODE):
    print(f'CURRENT DIFFICULTY MODE: {"HARD" if HARDMODE == True else "EASY"}')
    print("""Please select from one of the following options
          1 - Begin game.
          2 - Show rules.
          3 - Choose difficulty.
          4 - Exit game.""")
         


# introduction to the code, this will run as soon as the program starts.
def introduction(HARDMODE):
    print("Welcome to the word guessing game!")
    print(f'CURRENT DIFFICULTY MODE: {"HARD" if HARDMODE == True else "EASY"}')
    

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
                currentDifficulty = False
                print(f'Difficulty mode changed to {'EASY' if currentDifficulty == False else 'HARD'}')
        case "2":
            if currentDifficulty == True:
                print ("Difficulty mode already selected")
            else:
                currentDifficulty = True
                print(f'Difficulty mode changed to {'EASY' if currentDifficulty == False else 'HARD'}')
        case "3":
            return
    input("press enter to continue")
    return currentDifficulty


def getMenuOption(HARDMODE):
    menuIsSelected = False
    while menuIsSelected == False:
        clearScreen()
        showGameMenu(HARDMODE)
        menuChoice = input("Please select an option.\n>>> ")
        match menuChoice:
            case "1":
                menuIsSelected=True
                runningGame()
            case "2":
                showInstructions()
                input("press enter to continue")
                getMenuOption(HARDMODE)
            case "3":
                menuIsSelected=True
                HARDMODE = changeDifficulty(HARDMODE)
                getMenuOption(HARDMODE)
            case "4":
                menuIsSelected=True
                print("Exit game")
                sys.exit()
            case _:
                print("Not a valid option")
                continue
    
    
def runningGame():
    print("Game starting")
    selectedWordList, selectedWord, desiredWordLength = pickWordFromWordList('dictionary.txt')
    guessingArray=[] # Requires initialising first
    print(f'for ref - selected word: {selectedWord}')
    correctlyGuessedLetters=0

    
    def createGuessingArray(desiredWordLength):
        for letter in range(0, desiredWordLength):
            guessingArray.append('_')
        return guessingArray

    def displayGuessingArray (guessingArray):
        for letter in guessingArray:
            print(letter, end=" ")

    
    def playerGuess(guessedLetter, guessingArray, selectedWord, correctlyGuessedLetters):
        print(type(correctlyGuessedLetters))
        if guessedLetter in selectedWord:
            print(f'Correct! The letter {guessedLetter} is in this word')
            correctlyGuessedLetters=+1
            print(f'correctlyGuessedLetters={correctlyGuessedLetters}')   
            guessedLetterPosition=selectedWord.find(guessedLetter)
            guessingArray[guessedLetterPosition]=guessedLetter
            displayGuessingArray(guessingArray)
        else:
            print("Incorrect")


    
    
    guessingArray = createGuessingArray(desiredWordLength)
    displayGuessingArray(guessingArray)


    while correctlyGuessedLetters != desiredWordLength:
        guessOption=input("Please guess a letter.\n>>> ")
        playerGuess(guessOption, guessingArray, selectedWord, correctlyGuessedLetters)
        print(f'correctlyGuessedLetters={correctlyGuessedLetters}')


        if not re.match("^[a-z]*$", guessOption) or len(guessOption) > 1 or guessOption == "":
            print("Only single character letters of a-z are allowed")

    print("game over")









    displayGuessingArray(guessingArray)



   


    

def main(HARDMODE):
    introduction(HARDMODE)
    getMenuOption(HARDMODE)



main(HARDMODE)