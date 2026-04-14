import random

def load_words():
    """Load all 5-letter words from dictionary.txt."""
    with open("dictionary.txt", "r", encoding="utf-8") as file:
        words = []
        for line in file:
            clean = line.strip()
            if clean and len(clean) == 5:
                words.append(clean.lower())
    return words


def assign_words(directions, word_pool):
    """
    Given a list of directions (e.g. ['up', 'down', 'right']),
    assign a random word to each such that no two words share the same first letter.
    Returns a dict like {'up': 'crane', 'down': 'brave', 'right': 'gloom'}
    """
    assigned = {}
    used_letters = set()

    # Shuffle word pool so picks are random
    pool = word_pool.copy()
    random.shuffle(pool)

    for direction in directions:
        for word in pool:
            if word[0] not in used_letters:
                assigned[direction] = word
                used_letters.add(word[0])
                pool.remove(word)
                break

    return assigned