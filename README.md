Final Project – Flag Guessing Game  
Program developed by André Galhoz Valente
  
The Flag Guessing Game is a console-based quiz in which the user tries to identify countries from textual descriptions of their national flags. When the program starts, it loads all flag data from a JSON file and then guides the player through a sequence of flag questions with increasing difficulty.

The player is welcomed with a short introduction to the game and its rules:

1. The game uses three difficulty levels:  
◦  Level 1 (easy): most common and easily recognizable countries  
◦  Level 2 (medium): moderately well-known countries  
◦  Level 3 (hard): less familiar or more complex flags  
2. For each difficulty level, the program selects one flag description at random from the corresponding list in the JSON file.  
3. The player must guess the country name by typing it into the console when shown the description.  
4. Answers are checked in a case-insensitive way and ignore leading/trailing spaces.  
5. The game starts at the easy level. The player only advances to the next level if they guess the current country correctly.  
6. If the player guesses incorrectly, they stay on the same difficulty level, and the same flag is presented again.  
7. The player has a total of 3 lives (3 wrong answers). After each incorrect guess, the number of wrong answers increases.  
8. When the player reaches 3 wrong answers in total, the game ends immediately with a “Game over” message.  
9. If the player answers correctly at all three difficulty levels (easy, medium, hard) before losing all lives, the game prints:  
   “Congratulations, you won!”

All flag data is stored in a JSON file named flags.json. This file is organized into three keys: "easy", "medium", and "hard". Each key maps to a list of objects, where each object contains a country name and a textual description of its flag. This design satisfies the requirement to avoid hard-coding large data directly in the program and to read data from an external file instead.

The program is implemented in Python in a single main file, project.py, which contains the main() function and all required additional functions at the top level. The guessing logic is encapsulated in a simple class that represents an individual flag question and handles interaction with the user. Testing is done with pytest in a separate file, test_project.py, which includes unit tests for the three main helper functions.

Structure

•  def main()  
◦  Entry point of the program.  
◦  Loads the JSON data, explains the rules, manages the current difficulty level, counts wrong answers, and decides whether the player wins or loses.
•  def load_flags()  
◦  Reads flags.json from disk and validates that it contains "easy", "medium", and "hard" lists with country/description entries.
•  def select_country_by_level()  
◦  Given a difficulty level (1 for easy, 2 for medium, 3 for hard) and the loaded data, selects a random flag entry from the corresponding list.
•  def get_flag_description()  
◦  Given a country name and the loaded data, returns the corresponding flag description if the country exists, or None otherwise.
•  def check_answer()  
◦  Compares the player’s input with the correct country name in a case-insensitive way and returns True if they match, False otherwise.
•  class FlagQuestion  
◦  Attributes: country, description, and difficulty level.  
◦  Method: ask_and_check() displays the flag description to the user, reads their guess from the console, uses check_answer() to verify it, and prints whether the guess is correct or not.
•  test_project.py  
◦  Contains pytest unit tests for select_country_by_level, get_flag_description, and check_answer, using sample in-memory data that mimics the structure of flags.json.

