# word.py

import random

def random_words():
    # Read words from dictionary.txt
    with open("dictionary.txt", "r", encoding="utf-8") as file:
        words = []

        for line in file:
            clean_line = line.strip()
            if clean_line:
                words.append(clean_line)

    # Shuffle the list of words
    random.shuffle(words)
    return words

def type_word(word):
    progress = 0
    # call display words

    while progress < len(word):
        letter = input(f"Next letter ({progress+1}/{len(word)}): ")

        # Only take first typed character
        if not letter:
            continue
        letter = letter[0]

        if letter == word[progress]:
            progress += 1
            # print("Correct!")
        else:
            progress = 0
            # print("Wrong letter! Progress reset.")
    
    # call move function
