#!/usr/bin/env python3

import sys

# Sample dictionary of Swiss German sentences keyed by canton.
# Each canton has key sentences in its dialect.
# NOTE: These are purely illustrative and do not accurately reflect real dialects.
DIALECT_DICTIONARY = {
    "Zurich": {
        "How are you?": "Wiemer gahts dir?",
        "I like eating pizza.": "Ich ha gärn Pizza ässe.",
    },
    "Bern": {
        "How are you?": "Wie geit’s der?",
        "I like eating pizza.": "I ha gärn Pizza ässä.",
    },
    "Basel": {
        "How are you?": "Wia goots dir?",
        "I like eating pizza.": "I mag gärn Pizza ässe.",
    },
}

# High German reference sentences that map to the keys in DIALECT_DICTIONARY.
HIGH_GERMAN_SENTENCES = [
    "How are you?",
    "I like eating pizza.",
]

def naive_distance(str1: str, str2: str) -> int:
    """
    A naive distance function. 
    Returns a simple sum of the absolute difference in length 
    plus character-by-character mismatches for the overlapping range.
    """
    # For demonstration, a very simple approach:
    # 1. Count character mismatches in the overlapping region.
    # 2. Add difference in length.
    distance = 0
    min_len = min(len(str1), len(str2))
    for i in range(min_len):
        if str1[i] != str2[i]:
            distance += 1
    distance += abs(len(str1) - len(str2))
    return distance

def choose_canton() -> str:
    """
    Let the user choose a canton from the dictionary.
    """
    cantons = list(DIALECT_DICTIONARY.keys())
    print("\nAvailable Cantons:")
    for i, canton in enumerate(cantons, start=1):
        print(f"{i}. {canton}")
    choice = input("Select a canton by number: ").strip()
    
    try:
        index = int(choice) - 1
        if 0 <= index < len(cantons):
            selected_canton = cantons[index]
            print(f"\nYou selected: {selected_canton}")
            return selected_canton
        else:
            print("Invalid number. Returning to main menu.")
            return ""
    except ValueError:
        print("Invalid input. Returning to main menu.")
        return ""

def translation_mode(canton: str):
    """
    Shows a High German sentence and asks for translation into the chosen Swiss German dialect.
    """
    if not canton:
        print("No canton chosen yet.")
        return
    
    print("\n=== Translation Mode ===")
    for sentence in HIGH_GERMAN_SENTENCES:
        print(f"\nHigh German: {sentence}")
        user_translation = input("Your dialect translation: ")
        print(f"You said: {user_translation}")

def test_mode():
    """
    Allows the user to input their dialect sentences, 
    then tries to guess which canton’s dialect is closest.
    """
    print("\n=== Test Mode ===")
    print("Enter a sentence in your dialect (or type 'exit' to stop):")
    
    user_sentences = []
    while True:
        text = input("> ").strip()
        if text.lower() == "exit":
            break
        elif text:
            user_sentences.append(text)
    
    if not user_sentences:
        print("No sentences entered. Returning to main menu.")
        return
    
    # For each user sentence, compute distance to each canton’s known sentences.
    # Then sum or average distances to find the best match.
    canton_scores = {c: 0 for c in DIALECT_DICTIONARY.keys()}
    total_count = 0
    
    # We'll compare each user sentence to each known dialect sentence in the dictionary.
    for user_text in user_sentences:
        total_count += 1
        for canton, translations in DIALECT_DICTIONARY.items():
            # We do a best-match approach for each user sentence 
            # to the best of the canton’s known translations.
            best_local_distance = float('inf')
            for sample_sentence in translations.values():
                dist = naive_distance(user_text.lower(), sample_sentence.lower())
                best_local_distance = min(best_local_distance, dist)
            
            # Add that best local distance to the canton’s cumulative score
            canton_scores[canton] += best_local_distance
    
    # Now find which canton has the smallest cumulative distance
    best_canton = None
    best_score = float('inf')
    for canton, score in canton_scores.items():
        if score < best_score:
            best_score = score
            best_canton = canton
    
    print("\nYour dialect might be closest to:", best_canton)
    print("Detailed scores:")
    for canton, score in canton_scores.items():
        print(f"  {canton}: {score}")

def main():
    current_canton = ""
    
    while True:
        print("\n=== Swiss German Dialect CLI ===")
        print("1. Choose Canton")
        print("2. Translation Mode (translate from High German to selected dialect)")
        print("3. Test Mode (guess which canton your dialect is closest to)")
        print("4. Quit")
        
        choice = input("Enter your choice: ").strip()
        
        if choice == "1":
            current_canton = choose_canton()
        elif choice == "2":
            translation_mode(current_canton)
        elif choice == "3":
            test_mode()
        elif choice == "4":
            print("Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
