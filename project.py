import json
import random
from dataclasses import dataclass


MAX_WRONG_ANSWERS = 3


def load_flags(filepath: str) -> dict:
    """
    Load flag data from a JSON file.

    The JSON is expected to have keys 'easy', 'medium', and 'hard',
    each mapping to a list of objects with 'country' and 'description'.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Basic validation of structure
    for key in ("easy", "medium", "hard"):
        if key not in data or not isinstance(data[key], list):
            raise ValueError(f"Missing or invalid '{key}' list in JSON file.")
    return data


def _level_to_key(level: int) -> str:
    """
    Internal helper: map numeric level to JSON key.

    1 -> 'easy', 2 -> 'medium', 3 -> 'hard'
    """
    mapping = {1: "easy", 2: "medium", 3: "hard"}
    if level not in mapping:
        raise ValueError(f"Invalid level: {level}. Expected 1, 2, or 3.")
    return mapping[level]


def select_country_by_level(level: int, flags_data: dict) -> dict:
    """
    Select a random flag entry for a given difficulty level.

    Parameters:
        level: 1 (easy), 2 (medium), 3 (hard)
        flags_data: dict loaded from flags.json

    Returns:
        A dictionary like {"country": ..., "description": ...}
    """
    key = _level_to_key(level)
    level_flags = flags_data.get(key, [])
    if not level_flags:
        raise ValueError(f"No flags available for difficulty '{key}'.")
    return random.choice(level_flags)


def get_flag_description(country: str, flags_data: dict) -> str | None:
    """
    Return the description for a given country from the flags_data.

    If the country is not found, return None.
    """
    normalized_target = country.strip().lower()
    for level_flags in flags_data.values():
        for entry in level_flags:
            if entry.get("country", "").strip().lower() == normalized_target:
                return entry.get("description")
    return None


def check_answer(user_answer: str, correct_country: str) -> bool:
    """
    Check if the user's answer matches the correct country.

    Comparison is case-insensitive and ignores leading/trailing spaces.
    """
    if user_answer is None:
        return False
    return user_answer.strip().lower() == correct_country.strip().lower()


@dataclass
class FlagQuestion:
    """
    Represents a single flag question at a given difficulty level.
    """
    country: str
    description: str
    level: int

    def ask_and_check(self) -> bool:
        """
        Ask the user to guess the country based on the flag description.

        Returns:
            True if the user guesses correctly, False otherwise.
        """
        level_names = {1: "Easy", 2: "Medium", 3: "Hard"}
        level_name = level_names.get(self.level, f"Level {self.level}")

        print(f"\n{level_name} flag:")
        print(f"Description: {self.description}")
        user_guess = input("Your guess (country name): ")

        if check_answer(user_guess, self.country):
            print("Correct!")
            return True
        else:
            print(f"Incorrect. The correct answer was: {self.country}")
            return False


def main() -> None:
    """
    Main entry point for the flag guessing game.

    Rules:
    - The game attempts to go through levels 1 (easy), 2 (medium), 3 (hard).
    - You only move up a level if you answer the current level correctly.
    - If you reach a total of 3 wrong answers, the game is over.
    - If you answer correctly at all three levels, you win.
    """
    try:
        flags_data = load_flags("flags.json")
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
        print(f"Error loading flags: {e}")
        return

    print("Welcome to the Flag Guessing Game!")
    print("You will try to guess flags at three difficulty levels: easy, medium, and hard.")
    print(f"You can make at most {MAX_WRONG_ANSWERS} wrong answers in total.\n")

    levels = (1, 2, 3)
    current_level_index = 0
    wrong_answers = 0
    correct_answers = 0

    # Loop until we either finish all levels or reach max wrong answers.
    while current_level_index < len(levels) and wrong_answers < MAX_WRONG_ANSWERS:
        level = levels[current_level_index]

        # One flag per difficulty for this run: choose it once and reuse if needed.
        entry = select_country_by_level(level, flags_data)
        question = FlagQuestion(
            country=entry["country"],
            description=entry["description"],
            level=level,
        )

        # Ask the question. If wrong, stay on the same level and increment wrong counter.
        is_correct = question.ask_and_check()
        if is_correct:
            correct_answers += 1
            current_level_index += 1  # advance to next difficulty
        else:
            wrong_answers += 1
            if wrong_answers < MAX_WRONG_ANSWERS and current_level_index < len(levels):
                print(
                    f"Wrong answers so far: {wrong_answers}/{MAX_WRONG_ANSWERS}. "
                    "You will stay at the same difficulty level and try again."
                )

    # End-of-game messages
    if correct_answers == len(levels):
        print("\nCongratulations, you won!")
    elif wrong_answers >= MAX_WRONG_ANSWERS:
        print(f"\nGame over! You reached {wrong_answers} wrong answers.")
    else:
        # This case would only happen if something unexpected breaks the loop
        print("\nGame ended before completion.")


if __name__ == "__main__":
    main()
