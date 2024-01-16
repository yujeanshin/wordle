'''
[CS2] Wordle- Guess a five-letter secret word in at most six attempts.
'''
import random
# To install colorama, run the following command in your VS Code terminal:
# py -m pip install colorama
from colorama import Fore, Back, Style, init
init(autoreset=True) #Ends color formatting after each print statement
from wordle_wordlist import get_word_list
from itertools import combinations, permutations


def valid_guess(guess):
    valid = guess.isalpha() and len(guess) == 5
    return guess.upper(), valid

def get_feedback(guess: str, secret_word: str) -> str:
    '''Generates a feedback string based on comparing a 5-letter guess with the secret word. 
       The feedback string uses the following schema: 
        - Correct letter, correct spot: uppercase letter ('A'-'Z')
        - Correct letter, wrong spot: lowercase letter ('a'-'z')
        - Letter not in the word: '-'

       For example:
        - get_feedback("lever", "EATEN") --> "-e-E-"
        - get_feedback("LEVER", "LOWER") --> "L--ER"
        - get_feedback("MOMMY", "MADAM") --> "M-m--"
        - get_feedback("ARGUE", "MOTTO") --> "-----"

        Args:
            guess (str): The guessed word
            secret_word (str): The secret word
        Returns:
            str: Feedback string, based on comparing guess with the secret word
    '''
    guess, valid = valid_guess(guess)
    if not valid: return ""
    
    feedback = ["-"]*5
    secret_dict = {}
    for letter in secret_word:
        if letter in secret_dict.keys():
            secret_dict[letter] += 1
        else:
            secret_dict[letter] = 1
    
    for i in range(len(guess)):
        if guess[i] == secret_word[i]:
            feedback[i] = guess[i]
    
    for i in range(len(guess)):
        if feedback[i] == "-":
            if guess[i] in secret_dict.keys():
                count = 0
                for letter in feedback:
                    if letter.upper() == guess[i]:
                        count += 1
                if count < secret_dict[guess[i]]:
                    feedback[i] = guess[i].lower()
    
    feedback = "".join(feedback)
    return feedback

def format_guess(guess, secret_word):
    guess = guess.upper()
    feedback = get_feedback(guess, secret_word)
    result = ""
    for i in range(len(feedback)):
        if feedback[i] == "-":
            result += Back.BLACK + guess[i]
        elif feedback[i].isupper():
            result += Back.GREEN + guess[i]
        elif feedback[i].islower():
            result += Back.YELLOW + guess[i]
    return result

def make_dicts(word_list):
    # set up the dictionaries
    alphabet = "abcdefghijklmnopqrstuvwxyz".upper()
    lookup_dict = dict()
    freq_dict = dict()
    for letter in alphabet:
        freq_dict[letter] = 0
        for i in range(0, 5):
            lookup_dict[letter + str(i)] = set()

    for word in word_list:
        for i in range(0, 5):
            letter_key = word[i] + str(i)
            lookup_dict[letter_key].add(word)
            freq_dict[word[i]] += 1
    
    return lookup_dict, freq_dict

def get_freq_score(word, freq_dict):
    freq_score = 0
    for letter in word:
        freq_score += freq_dict[letter]
    
    return freq_score

def get_AI_guess(word_list: list[str], guesses: list[str], feedback: list[str]) -> str:
    '''Analyzes feedback from previous guesses (if any) to make a new guess
        Args:
            word_list (list): A list of potential Wordle words
            guesses (list): A list of string guesses, could be empty
            feedback (list): A list of feedback strings, could be empty
        Returns:
         str: a valid guess that is exactly 5 uppercase letters
    '''
    if guesses == []:
        return "IRATE"
    
    lookup_dict, freq_dict = make_dicts(word_list)
    green_keys = set()
    yellow_keys = set()
    black_keys = set()

    for word_num in range(len(guesses)):
        for i in range(0, 5):
            letter_key = guesses[word_num][i] + str(i)
            if feedback[word_num][i] == "-":
                black_keys.add(letter_key)
            elif feedback[word_num][i].isupper():
                green_keys.add(letter_key)
            elif feedback[word_num][i].islower():
                yellow_keys.add(letter_key)
    
    candidates = set(word_list)
    green_letters = set()
    if len(green_keys) != 0:
        for key in green_keys:
            candidates = candidates & lookup_dict[key]
            green_letters.add(key[0])

    yellow_letters = set()
    for key in yellow_keys:
        yellow_letters.add(key[0])
        candidates = candidates.difference(lookup_dict[key])
    
    black_letters = set()
    for key in black_keys:
        black_letters.add(key[0])
    
    greatest_freq_score = 0
    best_guess = ""
    for candidate in candidates:
        passed_yellow = True
        for yellow in yellow_letters:
            if yellow not in candidate:
                passed_yellow = False
                break
        if passed_yellow:
            if len(black_keys) == 0:
                freq_score = get_freq_score(candidate, freq_dict)
                if freq_score > greatest_freq_score:
                    best_guess = candidate
                    greatest_freq_score = freq_score
            
            passed_black = True
            for black_key in black_keys:
                if black_key[0] in yellow_letters or black_key[0] in green_letters:
                    if candidate in lookup_dict[black_key]:
                        passed_black = False
                        break
                else:
                    if black_key[0] in candidate:
                        passed_black = False
                        break
            if passed_black:
                freq_score = get_freq_score(candidate, freq_dict)
                if freq_score > greatest_freq_score:
                    best_guess = candidate
                    greatest_freq_score = freq_score

    
    return best_guess

def play_game():
    word_list = get_word_list()
    guesses = []
    feedback = []
    index = random.randint(0, len(word_list)-1)
    secret_word = word_list[index]
    guessed = False
    
    # MOIST, PREEN
    # secret_word = "PREEN"
    print("Welcome to Wordle!")
    print(f"secret_word: {secret_word}")
    num_guesses = 0
    while not guessed:
        print("Number of guesses:", num_guesses)
        guess = get_AI_guess(word_list, guesses, feedback)
        num_guesses += 1
        guesses.append(guess)
        feedback.append(get_feedback(guess, secret_word))
        print(format_guess(guess, secret_word))
        if guess == secret_word:
            print(f"success in {num_guesses} guesses!")
            break
        if num_guesses == 10:
            print("you took too long, bozo")
            print(f"the secret word was {secret_word}")
            break
    print("Thanks for playing!")
    return None

if __name__ == "__main__":
    # TODO: Write your own code to call your functions here
    # print(get_feedback("lever", "EATEN")) # --> "-e-E-"
    # print(get_feedback("LEVER", "LOWER")) # --> "L--ER"
    # print(get_feedback("MOMMY", "MADAM")) # --> "M-m--"
    # print(get_feedback("ARGUE", "MOTTO")) # --> "-----"
    
    print(play_game())
    # play_game()
    # print(format_guess("LEVER", "EATEN"))

    # ['E', 'A', 'R', 'O', 'T', 'L', 'I', 'S', 'N', 'C', 'U', 'Y', 'D', 'H', 'P', 'M', 'G', 'B', 'F', 'K', 'W', 'V', 'Z', 'X', 'Q', 'J']
    # {'A': 975, 'B': 280, 'C': 475, 'K': 210, 'S': 668, 'E': 1230, 'T': 729, 'Y': 424, 'O': 753, 'H': 387, 'R': 897, 'I': 670, 'D': 393, 'L': 716, 'U': 466, 'V': 152, 'N': 573, 'G': 310, 'P': 365, 'M': 316, 'F': 229, 'X': 37, 'W': 194, 'Z': 40, 'J': 27, 'Q': 29}
    
    # no words with top 5 letters, so we try EAROL, EARIT (ding ding, irate)

    
    # word_list = get_word_list()
    # print(make_dicts(word_list))
    # print(get_AI_guess(word_list, [], []))
    """
    letter_count = {}
    for word in word_list:
        for letter in word:
            if letter in letter_count.keys():
                letter_count[letter] += 1
            else:
                letter_count[letter] = 1
    
    counts = []
    for word in letter_count.keys():
        counts.append(letter_count[word])
    counts.sort(reverse=True)

    ordered_letters = []
    for count in counts:
        for letter in letter_count.keys():
            if letter_count[letter] == count:
                ordered_letters.append(letter)
                break

    print(letter_count)

    for perm in permutations(['E', 'A', 'R', 'I', 'T'], 5):
        perm = list(perm)
        perm = "".join(perm)
        if perm in word_list:
            print(perm)
    """
    pass