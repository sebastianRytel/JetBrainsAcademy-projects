print("H A N G M A N")
import random
word = random.choice(['python', 'java', 'kotlin', 'javascript'])
# word = random.choice(['javascript'])
word_as_list = list(word)
hypens = list(len(word) * '-') 
trials = 0
guessed_word = len(word) * '-'
guessed_letters = []
while True:
    play_or_exit = input("Type 'play' to play the game, 'exit' to quit: ")
    if play_or_exit == "play":
        while trials <= 8:
            print("""
"""+guessed_word)
            guessed_word.replace('-','')
            input_letter = input("Input a letter: ")
            if len(tuple(input_letter)) > 1 or input_letter == '':
                print("You should input a single letter")
                continue
            if input_letter in guessed_letters:
                print("You've already guessed this letter")
                continue
            guessed_letters.append(input_letter)
            start = 0
            if not input_letter.islower() or not input_letter.isalpha():
                print("Please enter a lowercase English letter")
                continue
            if input_letter not in word_as_list:
                print("That letter doesn't appear in the word")                                                                                                                                                 
                trials += 1
                if trials == 8:
                    print("You lost!")
                    break
            elif input_letter in word_as_list:
                for letter in word_as_list:
                    if input_letter  == letter:
                        index = word_as_list.index(letter, start)
                        hypens[index] = word[index]
                    start += 1
                if input_letter in guessed_word:
                    print("You've already guessed this letters")
                    trials += 1
                guessed_word = ''         
                for letter in hypens:
                    guessed_word += letter
                if guessed_word == word:
                    print(f'You guessed the word {guessed_word}!')
                    print("You survived!")
                    break
        else:
            print("You lost!")
            print()
    else:
        if play_or_exit == 'exit':
            quit()
