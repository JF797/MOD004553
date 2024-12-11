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
                runningGame(HARDMODE)
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
    
    
def runningGame(HARDMODE):
    print("Game starting")
    selectedWordList, selectedWord, desiredWordLength = pickWordFromWordList('dictionary.txt')
    guessingArray=[] # Requires initialising first
    print(f'for ref - selected word: {selectedWord}')
    correctlyGuessedLetters=0
    numberOfGuesses=len(selectedWord)*2

    
    def createGuessingArray(desiredWordLength):
        for letter in range(0, desiredWordLength):
            guessingArray.append('_')
        return guessingArray

    def displayGuessingArray(guessingArray):
        for letter in guessingArray:
            print(letter, end=" ")

    def checkIfGuessedLetterIsInWord(guessOption, selectedWord):
        if guessOption in selectedWord:
            return True
        else:
            return False
        
    def guessedCorrectly(guessOption, selectedWord, guessingArray):
        guessedLetterPosition=selectedWord.find(guessOption)
        guessingArray[guessedLetterPosition]=guessOption
        return guessingArray
    
    def guessedCorrectlyMultiple(guessOption, selectedWord, guessingArray):
        duplicateCharacters = 0
        for x in range(0, len(selectedWord)):
            if selectedWord[x] == guessOption:
                guessingArray[x] = guessOption
                duplicateCharacters += 1
        return guessingArray, duplicateCharacters

    def checkForMultipleLettersInWordForGuess(guessOption, selectedWord):
        if selectedWord.count(guessOption) > 1:
            return True
        else:
            return False
    
    def checkIfWordHasBeenGuessedCorrectly(guessingArray, selectedWord):
        if (''.join(guessingArray)) == selectedWord:
            return True
        else:
            return False

    # Used for hardmode function
    def recalculateWordList(selectedWordList, guessingArray, wordListBank):
        # Iterate through all the words in the selected word list
        for words in selectedWordList:
            # By default, set all words as matched, and then if they don't reach the criterion, don't include them.
            wordMatched=True
            # For each word, check to make sure these do not match the remaining letters in a word we are looking for
            for wordLengthCounter in range(len(guessingArray)):
                if guessingArray[wordLengthCounter] != '_' and guessingArray[wordLengthCounter] != words[wordLengthCounter]:
                    wordMatched = False
                    break 
            # All the remaining matches are added to an additional word list bank
            if wordMatched == True:
                wordListBank.append(words)
        return wordListBank
    
    # Used for hardmode function
    def findMostUniqueWordBasedOnCharacterCost(wordListBank, guessingArray):
        frequencyDictionary={}
        for word in wordListBank:
            for letters in word:
                if letters in frequencyDictionary:
                    frequencyDictionary[letters] += 1
                else:
                    frequencyDictionary[letters] = 1

        # To avoid words being chosen with duplicate characters that have been guessed, give these letters a higher cost
        def findLetterCosts(word):
            letterCost=0
            for letters in word:
                letterCost += (1/(frequencyDictionary[letters] + 1))
            return letterCost
        
        mostUniqueWord=min(wordListBank, key=findLetterCosts)
        return mostUniqueWord

    guessingArray = createGuessingArray(desiredWordLength)

    # Array for guessed letters, as we cannot compare this to the guessingArray as the user shouldn't be able to guess the same wrong answer twice.
    guessedLetters=[]
    wordListBank=[]


    while numberOfGuesses != 0:
        duplicateCharacters = 0
        displayGuessingArray(guessingArray)
        print(f'Remaining Guesses: {numberOfGuesses}')
        guessOption=input("Please guess a letter.\n>>> ").lower()

        # Validate user input for a-z characters using regex
        if not re.match("^[a-z]*$", guessOption) or len(guessOption) > 1 or guessOption == "":
            print("Only single character letters of a-z are allowed")
        
        # Finish the game if the number of guesses reaches 0
        elif numberOfGuesses == 0:
            print('Sorry, you have no more guesses')
            break

        # Check if that letter has already been guessed
        elif guessOption in guessedLetters:
            print(f'The letter: {guessOption} has already been guessed. But you wont lose a point')

        # Criterion after input has been validated
        else:
            numberOfGuesses-=1

            # Check to see if the guessed letter is in the word
            if checkIfGuessedLetterIsInWord(guessOption, selectedWord) == True:
                print("correct")
                
                # Add the correctly guessed letter to the guessing array if there are multiple instances
                if checkForMultipleLettersInWordForGuess(guessOption, selectedWord) == True:
                    guessingArray, duplicateCharacters=guessedCorrectlyMultiple(guessOption, selectedWord, guessingArray)
                
                # Otherwise just add it once
                else:   
                    guessingArray=guessedCorrectly(guessOption, selectedWord, guessingArray)
                    correctlyGuessedLetters+=1

                if HARDMODE == True:
                    wordListBank=recalculateWordList(selectedWordList, guessingArray, wordListBank)
                    nextPossibleWord=findMostUniqueWordBasedOnCharacterCost(wordListBank, guessingArray)
                    print(f'most unique next word: {nextPossibleWord}')
                    print(wordListBank)
                    if nextPossibleWord != selectedWord:
                        selectedWord = nextPossibleWord
                        print("Computer has changed the word")

            else:
                print(f'The letter: {guessOption} is not in this word. Try again.')

            
            if checkIfWordHasBeenGuessedCorrectly(guessingArray, selectedWord) == True:
                print(f'You won! The word was: {selectedWord}')
                print('The game will now exit')
                exit()
            


        # Add the guessed letter to the guessedLetters array for checking
        guessedLetters.append(guessOption)

    print("Game over: you are out of guesses!")










    displayGuessingArray(guessingArray)



   


    

def main(HARDMODE):
    introduction(HARDMODE)
    getMenuOption(HARDMODE)



main(HARDMODE)