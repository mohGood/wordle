import argparse
import re
import shutil
import sys

def get_candidates(words, present, not_present, pattern):
    return [word for word in words if
            all([letter in word for letter in present]) and
            not any([letter in word for letter in not_present]) and
            pattern.match(word)
            ]

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    # https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def print_candidates(candidates):
    width = shutil.get_terminal_size().columns
    spacing_length = 2
    word_length = 5
    words_per_line = (width - word_length) // (word_length + spacing_length) + 1
    lines = chunks(candidates, words_per_line)
    spacing = " "*spacing_length
    for line in lines:
        print(spacing.join(line))

parser = argparse.ArgumentParser(
    description="Suggest solutions to Wordle based on some constraints.")
parser.add_argument('-d', '--dictionary',
                    default="dictionary.txt",
                    help="Dictionary file to use as the starting point. Default is '/usr/share/dict/words'.")
parser.add_argument('-p', '--present',
                    default="",
                    help="All letters that we know are in the word, all in one string. Default is '' (emtpy string).")
parser.add_argument('-n', '--not-present',
                    default="",
                    help="All letters that we know are not in the word, all in one string. Default is '' (emtpy string).")
parser.add_argument('-r', '--pattern',
                    default=".....",
                    help="Regex pattern we know the word must match. Default is '.....'.")
parser.add_argument('-i', '--interactive',
                    dest='interactive',
                    action='store_true',
                    help="Run in interactive mode.")
parser.add_argument('--no-interactive',
                    dest='interactive',
                    action='store_false',
                    help="Run in non-interactive mode (default).")
args = parser.parse_args()

# read the dictionary file, filter out those which are five characters long:
lines = []
with open(args.dictionary) as f:
    lines = f.read().splitlines()
words = [line for line in lines if len(line) == 5]

# set parameters
present = [char for char in args.present] # letters that we know are in the word
not_present = [char for char in args.not_present]  # letters we know are not in the word
pattern = re.compile(args.pattern)

if args.interactive:
    print("running in interactive mode")
    print("Enter Wordle's answer as follows:")
    print("- '+' for: letter is in word and in correct spot (green)")
    print("- '?' for: letter is in word but not in correct spot (yellow)")
    print("- '-' for: letter is not in word (grey)")
    word_pattern = re.compile("^[a-z]{5}$")
    wordle_pattern = re.compile("^[+-?]{5}$")
    pattern_list = [ 
        {"yes": ".", "no": [] } ,
        {"yes": ".", "no": [] } ,
        {"yes": ".", "no": [] } ,
        {"yes": ".", "no": [] } ,
        {"yes": ".", "no": [] } ,
    ]
    while True:
        while True:
            prompt = "What is your word?"
            word = input(f"{prompt : <25} ")
            if word_pattern.match(word):
                break
            print(" Word must be exactly five characters long!")
        while True:
            prompt = "What is Wordle's answer?"
            answer = input(f"{prompt : <25} ")
            if wordle_pattern.match(answer):
                break
            print(" Wordle answer must be five times [+-?]!")

        if answer == "+++++":
            print("Congratulations!")
            break

        word = [letter for letter in word]
        answer = [symbol for symbol in answer]
        for letter, symbol, pattern_unit in zip(word, answer, pattern_list):
            if symbol == '-':
                not_present.append(letter)
            if symbol == '+':
                present.append(letter)
                pattern_unit['yes'] = letter
            if symbol == '?':
                present.append(letter)
                pattern_unit['no'].append(letter)

        pattern = []
        for pattern_unit in pattern_list:
            if len(pattern_unit['no']) > 0 and pattern_unit['yes'] == '.':
                pattern.append(f"[^{''.join(pattern_unit['no'])}]")
            else:
                pattern.append(pattern_unit['yes'])

        pattern = "".join(pattern)
        pattern = re.compile(pattern)

        candidates = get_candidates(words, present, not_present, pattern)
        print("May I suggest the following options:")
        print_candidates(candidates)

    sys.exit(0)

# filter words with all() and not any()
candidates = get_candidates(words, present, not_present, pattern)
print_candidates(candidates)
