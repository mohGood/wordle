Solver assistant for Wordle

Game:
https://www.powerlanguage.co.uk/wordle/

Usage:
After the first guess, apply the necessary restrictions to the script.

Arguments:
  -h, --help            help
  -d DICTIONARY, --dictionary DICTIONARY
                        Words dictionary file
  -p PRESENT, --present PRESENT
                        All the letters we know are in the word, all in one string 
                        Default: ''
  -n NOT_PRESENT, --not-present NOT_PRESENT
                        All the letters we know are not in the word, all in one string
			Default: ''
  -r PATTERN, --pattern PATTERN
                        Regex pattern that must match the word.
			Default: "....."
  -i, --interactive     Run in interactive mode
  --no-interactive      Run in non-interactive mode
			(Default)

Example for interactive mode:

In interactive mode, you will be asked to enter the word that you tried in the game, and then the answer that the game gave you.

$ python wordle.py --interactive
running in interactive mode
Enter Wordle's answer as follows:
- '+' for: letter is in word and in correct spot (green)
- '?' for: letter is in word but not in correct spot (yellow)
- '-' for: letter is not in word (gray)

We continue until we reach five + signs.


Example for non-interactive mode:

In non-interactive mode, we have to pass all the constraints as parameters

Step 1

Guess a word in the game. 
ex: `saint`

wordle:
----+

This means that we know that the last letter is "t".
We also know that "s", "a", "i" and "n" do not exist in the word.

Step 2

Now we run the script

$ python wordle.py --present t --not-present sain --pattern "....t"

This time we choose one of the script words, for example:

ex: `crypt`

wordle:
-?--+

We now know that `r` is one of the letters in the solution, but not in the second position.
"C", "y" and "p" are not letters in the solution.

Step 3

We can run the solver again, this time with updated restrictions:

$ python wordle.py --present rt --not-present saincyp --pattern ".[^r]..t"

Choose one of the script words, for example:
`exert`

Wordle:
---?+

We now know even more: "r" is not in fourth place, "e" and "x" do not exist.

Step 4

$ python wordle.py --present rt --not-present saincypex --pattern ".[^r].[^r]t"

['Burut', 'Murut', 'robot']

We now have only three choices