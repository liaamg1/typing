"""Typing functions for main.py"""
from operator import itemgetter
import time
import random

def clear_console():
    """Clear the console."""
    print("\n" * 100)

def print_stats1(precision, precision_words, gross_wpm):
    """Print the current statistics."""
    #Only 5 arguments per function
    clear_console()
    print(f"Current Letter Precision: {precision}%")
    print(f"Current Word Precision: {precision_words}%")
    print(f"Current Gross WPM: {gross_wpm}")

def print_stats2(incorrect, elapsed_time, net_wpm, accuracy):
    """Print the current statistics."""
    print(f"Current Net WPM: {net_wpm}")
    print(f"Current accuracy: {accuracy}%")
    print(f"Elapsed Time: {elapsed_time}")
    print("Current Incorrect Letters:")
    incorrect_letters = dict(sorted(incorrect.items(), key=itemgetter(1, 0), reverse=True))

    for letter, count in incorrect_letters.items():
        print(f"'{letter}': {count} time(s)")
    print("Type the following lines:")

def animal_category(net_wpm):
    """Determine animal category based on net WPM."""
    categories = [
        (5, "Sloth"),
        (15, "Snail"),
        (30, "Manatee"),
        (40, "Human"),
        (50, "Gazelle"),
        (60, "Ostrich"),
        (70, "Cheetah"),
        (80, "Swordfish"),
        (90, "Spur-winged goose"),
        (100, "White-throated needletail"),
        (120, "Golden eagle"),
    ]
    
    for limit, animal in categories:
        if net_wpm <= limit:
            return animal
    return "Peregrine falcon"

def difficulty(level):
    """Run typing difficulty test and save score."""
    try:
        with open(level, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Error: The file '{level}' does not exist.")
        return
    except Exception as err:
        print(f"An error occurred while reading the file: {err}")
        return

    incorrect = {}
    wrong = 0
    input_count = 0
    input_count_words = 0
    wrong_words = 0
    user_count = 0

    # Initialize basic values
    precision = 0
    precision_words = 0
    gross_wpm = 0
    elapsed_time = "0m 0s"
    net_wpm = 0
    accuracy = "0%"
    start_time = time.time()

    print("Type the following lines:")
    for line in lines:
        line = line.strip()
        print_stats1(precision, precision_words, gross_wpm)
        print_stats2(incorrect, elapsed_time, net_wpm, accuracy)
        typed_line = input(f"{line}\n")

        input_words = typed_line.split()
        user_count += len(input_words)

        words = line.split()
        input_count += len(line.replace(" ", "").replace("\n", ""))
        input_count_words += len(words)

        for index, word in enumerate(words):
            input_word = input_words[index] if index < len(input_words) else ""
            max_length = max(len(word), len(input_word))
            for index2 in range(max_length):
                #check
                expected_char = word[index2] if index2 < len(word) else None
                typed_char = input_word[index2] if index2 < len(input_word) else None
                if expected_char is not None and (typed_char is None or expected_char != typed_char):
                    incorrect[expected_char] = incorrect.get(expected_char, 0) + 1
                    wrong += 1
            if word != input_word:
                wrong_words += 1

        # Calculate elapsed time
        time_seconds = time.time() - start_time

        minutes = int(time_seconds // 60)
        seconds = int(time_seconds % 60)

       
        if seconds >= 30:
            time_minutes = minutes + 1  #round up
        else:
            time_minutes = minutes  

        #atleast 1 minute
        time_minutes = max(1, time_minutes)

        
        gross_wpm = user_count / time_minutes
        net_wpm = gross_wpm - (wrong / time_minutes)
        accuracy = (net_wpm / gross_wpm) * 100 if gross_wpm > 0 else 0


        right = input_count - wrong
        precision = round((right / input_count) * 100, 2) if input_count > 0 else 0
        right_words = input_count_words - wrong_words
        precision_words = round((right_words / input_count_words) * 100, 2) if input_count_words > 0 else 0

        minutes = int(time_seconds // 60)
        seconds = int(time_seconds % 60)
        elapsed_time = f"{minutes}m {seconds}s"

        print_stats1(precision, precision_words, gross_wpm)
        print_stats2(incorrect, elapsed_time, net_wpm, accuracy)

    # Final results
    incorrect_letters2 = dict(sorted(incorrect.items(), key=itemgetter(1, 0), reverse=True))
    clear_console()
    print("Press Enter to see your result...")
    input()
    print("FINAL RESULT")
    print("---------------------------------")
    print(f"Final Letter Precision: {precision}%")
    print(f"Final Word Precision: {precision_words}%")
    
    print("Incorrect letters:")
    for letter, count in incorrect_letters2.items():
        print(f"'{letter}': {count} time(s)")
    print("---------------------------------")
    print(f"Total Time: {elapsed_time}")
    print(f"Final Gross WPM: {gross_wpm}")
    print(f"Final Net WPM: {net_wpm}")
    print(f"Final accuracy: {accuracy}")
    print(f"You type like a {animal_category(net_wpm)}")

    # Save score
    level_print = level.rstrip('.txt').capitalize()
    score_output = precision_words
    scores = []
    
    try:
        with open('score.txt', 'r', encoding='utf-8') as score_file:
            for line in score_file:
                level_name, name_score = line.strip().split(' | ')
                score_value = float(name_score.split(': ')[1].replace('%', ''))
                scores.append((level_name, score_value, name_score.split(': ')[0])) 
    except FileNotFoundError:
        print("Score file not found, creating a new one.")
    except Exception as err:
        print(f"An error occurred while reading the score file: {err}")
    
    name = input("Please enter your name to save your score! ")
    scores.append((level_print, float(score_output), name))  

    # Score sorting
    level_order = {"Hard": 3, "Medium": 2, "Easy": 1}
    sortable_scores = []
    
    for score in scores:
        try:
            sortable_scores.append((level_order[score[0]], score[0], score[1], score[2]))
        except KeyError:
            print(f"Warning: Level '{score[0]}' not found in level_order. Skipping.")

    sortable_scores.sort(key=itemgetter(0, 2), reverse=True)

    try:
        with open('score.txt', 'w', encoding='utf-8') as score_file:
            for score in sortable_scores:
                score_file.write(f"{score[1]} | {score[3]}: {score[2]}%\n")
    except Exception as err:
        print(f"An error occurred while saving the scores: {err}")

def view_score():
    """Function to view saved scores"""
    try:
        with open('score.txt', 'r', encoding='utf-8') as score_file:
            scores = score_file.readlines()
            for line in scores:
                print(line)
    except FileNotFoundError:
        print("No score file found.")
    except Exception as err:
        print(f"An error occurred while reading the score file: {err}")

def train(user_choice):
    """Print random characters for a training test."""
    if user_choice <= 0:
        print("Error: Training duration must be greater than zero.")
        return

    wrong = {}
    not_right = 0
    count = 0
    characters = 'abcdefghijlklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ,.-'
    end_time = time.time() + user_choice
    
    while time.time() < end_time:
        letter = random.choice(characters)
        clear_console()
        print(letter)
        user_input = input("").strip() 

    # Check if input length is valid
        if letter != user_input or user_input is None or len(user_input) > 1:
            wrong[letter] = wrong.get(letter, 0) + 1
            not_right += 1
        count += 1


    # Calculation
    percentage_wrong = (not_right / count) * 100 if count > 0 else 0
    wpm = count / (user_choice * 60)
    wrong_letters = dict(sorted(wrong.items(), key=itemgetter(1, 0), reverse=True))
    
    #display stats
    for letter, count in wrong_letters.items():
        print(f"'{letter}': {count} time(s)")
    print(f"Wrong: {percentage_wrong}%")
    print(f"Words per minute: {wpm}")
