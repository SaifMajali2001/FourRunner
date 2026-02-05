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
