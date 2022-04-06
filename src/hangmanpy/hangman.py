#!/usr/bin/env python3

import random, os, time, sys

IN_IPYTHON = True

try:
    from IPython import display
except:
    IN_IPYTHON = False
    
IN_COLAB = 'google.colab' in sys.modules
GAME_DEBUG = False

WORDS_PATH = 'words'
HANGMAN_PATH = 'hangman_frames.txt'


def clear_screen():
  if IN_IPYTHON and IN_COLAB:
      display.clear_output()
  else:
    if sys.platform == 'win32':
      os.system('cls')
    else:
      os.system('clear')


def files_list(input_path):
    result_files = []
    for f in os.scandir(input_path):
      if f.is_file and f.name.endswith(".txt"):
        result_files.append(f.path)
    return result_files
    

def read_words():
  words_path = WORDS_PATH
  content = []
  words_files_list = files_list(words_path)
  for wf in words_files_list:
    with open(wf, "r") as f:
      content.extend(f.read().split())
  return content


def read_hangman_frames():
    hangman_path = HANGMAN_PATH
    hangman_frames = []
    with open(hangman_path, "r") as f:
        hangman_frames.extend(f.read().split('\n\n'))
    return hangman_frames


def print_hangman(hangman_frames, attempts):
    print(hangman_frames[attempts])


def peak_random_word(words):
  return random.choice(words)


def print_word_state(word, word_chars, not_word_chars):
    for c in word:
      if c in word_chars:
        print(c, end='')
      else:
        print('_', end='')
      print(' ', end='')
    print()

    delim = ', '
    print(delim.join(not_word_chars))

    print()


def check_game_state(word, word_chars, attempts):
    all_guessed = True
    for c in word:
      if c not in word_chars:
        all_guessed = False

    if all_guessed:
      return False

    if attempts >= 6:
      return False
    
    return True


def game_loop(word, hangman_frames):
  game_running = True
  attempts = 0
  word_chars = []
  not_word_chars = []

  clear_screen()

  while game_running:

    if GAME_DEBUG:
      print(word)

    print_hangman(hangman_frames, attempts)
    print_word_state(word, word_chars, not_word_chars)
    print(attempts)

    input_char = input('Character: ')[0].lower()

    time.sleep(0.1)
    clear_screen()

    if not input_char.isalpha() or input_char == '':
      print('Unexpected symbol!')
      continue

    if input_char in word_chars:
      continue

    if input_char in word:
      word_chars.append(input_char)
    else:
      if input_char not in not_word_chars:
        not_word_chars.append(input_char)
        attempts += 1

    game_running = check_game_state(word, word_chars, attempts)

  print_hangman(hangman_frames, attempts)
  print_word_state(word, word_chars, not_word_chars)


def continue_prompt():
    continue_game = True
    while True:
        continue_input = input('Continue[y/n]: ').lower()[0]
        if continue_input == 'y':
            continue_game = True
            break
        elif continue_input == 'n':
            continue_game = False
            break
        else:
            continue

    return continue_game


def main():
  try:
    words = read_words()
    word = peak_random_word(words)
    hangman_frames = read_hangman_frames()

    continue_game = True
    while continue_game:
        game_loop(word, hangman_frames)
        continue_game = continue_prompt()


  except KeyboardInterrupt:
    print("Quiting game...")


if __name__ == '__main__':
  main()
