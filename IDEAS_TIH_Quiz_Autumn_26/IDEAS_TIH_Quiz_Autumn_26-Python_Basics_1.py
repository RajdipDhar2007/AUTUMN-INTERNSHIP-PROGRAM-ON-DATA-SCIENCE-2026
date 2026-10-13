#!/usr/bin/env python3
"""
IDEAS TIH Quiz Autumn 26 - Python Basics 1 - interactive terminal quiz
---------------------------------------------------------------
Run:   python python_basics_1_quiz.py

* 30 multiple-choice questions, 60 minutes in total.
* Type A, B, C or D and press Enter to answer.
  Type S to skip a question, Q to finish the quiz early.
* After each answer you are told how long you took.
* Right/wrong is revealed only at the end, in a results table,
  together with your total score, percentage and time taken.

Only the Python standard library is used (Python 3.7+).
"""

import os
import sys
import time
import textwrap

TITLE = "IDEAS TIH Quiz Autumn 26 - Python Basics 1"
TIME_LIMIT = 60 * 60          # seconds
OPTION_KEYS = ("A", "B", "C", "D")

QUESTIONS = [{'q': 'What will be the output of the following code?',
  'code': 'a = 16754\npi = 3.14\na = a - pi\na = int(a)\nprint(a)',
  'opts': {'A': '16750.86', 'B': '16751', 'C': '16750', 'D': 'Error'},
  'ans': 'C',
  'expl': 'The variable a initially holds the integer value 16754. We subtract the value of pi '
          '(3.14), which updates a to the floating-point number 16750.86. In Python, the int() '
          'function converts a float to an integer by truncating the decimal part, not by '
          'rounding. Therefore, 16750.86 becomes 16750, which is then printed.'},
 {'q': 'Consider the following code. What is printed?',
  'code': 'is_this_class_interseting = True\n'
          'is_this_class_interseting = int(is_this_class_interseting)\n'
          'print(is_this_class_interseting)',
  'opts': {'A': 'True', 'B': 'False', 'C': '1', 'D': '0'},
  'ans': 'C',
  'expl': 'In Python, the boolean value True is internally represented as the integer 1, and False '
          'is represented as the integer 0. When we cast the boolean True using the int() '
          'function, it returns 1.'},
 {'q': 'What will be the output of the following statement?',
  'code': "name = 'Gukesh Dommaraju'\nprint(name[1:-5])",
  'opts': {'A': 'ukesh Domm', 'B': 'ukesh Domma', 'C': 'ukesh Dom', 'D': 'Gukesh'},
  'ans': 'A',
  'expl': "Slicing [start:stop] starts at index 1 ('u') and stops before index -5. 'Gukesh "
          "Dommaraju' has 16 characters, so -5 is index 11 ('a'). The slice covers indices 1 to "
          "10, giving 'ukesh Domm'. (The original answer key said B, but running the code prints "
          "'ukesh Domm'.)"},
 {'q': 'What will be the output?',
  'code': "myList = ['Harry', 'Hermione', 'Ron', 'Draco', 'Snape']\nprint(myList[::-1])",
  'opts': {'A': "['Snape', 'Draco', 'Ron', 'Hermione', 'Harry']",
           'B': "['Harry', 'Hermione', 'Ron']",
           'C': "['Draco', 'Snape']",
           'D': 'Error'},
  'ans': 'A',
  'expl': 'The slicing syntax [::-1] leaves the start and stop indices blank (meaning it covers '
          'the entire list) and sets the step size to -1. A negative step size means the list is '
          'traversed in reverse order. This is a common Python shortcut for reversing lists or '
          'strings.'},
 {'q': 'Which statement about the following code is correct?',
  'code': 'try:\n'
          '    print(numerator // denominator)\n'
          'except ZeroDivisionError:\n'
          "    print('Trying to reach infinity?')",
  'opts': {'A': 'The except block executes every time',
           'B': 'The code prevents program crash due to division by zero',
           'C': 'try is used only for loops',
           'D': 'Integer division cannot cause errors'},
  'ans': 'B',
  'expl': 'The try-except block is used to catch and handle exceptions in Python. Here, if the '
          'denominator is 0, the division operation raises a ZeroDivisionError. Instead of '
          'stopping the program with a fatal crash, the flow transfers to the except block which '
          'smoothly prints a warning message.'},
 {'q': 'What will be the output of the following loop?',
  'code': 'for i in range(5):\n    print(i)',
  'opts': {'A': '1 2 3 4 5', 'B': '0 1 2 3 4', 'C': '0 1 2 3 4 5', 'D': 'Infinite loop'},
  'ans': 'B',
  'expl': 'The range(n) function generates a sequence of numbers starting from 0 by default, up to '
          'but not including the number n. Therefore, range(5) yields the sequence 0,1,2,3,4, '
          'which is printed iteratively by the loop.'},
 {'q': 'What does the following statement do?',
  'code': "new_text = original_text.replace('serious', 'sirius')\nprint(new_text)",
  'opts': {'A': "Removes the word 'serious'",
           'B': "Replaces all occurrences of 'serious' with 'sirius'",
           'C': "Finds the word 'sirius'",
           'D': 'Converts the string into lowercase'},
  'ans': 'B',
  'expl': 'The replace(old, new) method in Python creates a new string where all occurrences of '
          "the substring 'old' are replaced by the substring 'new'. Here, every instance of "
          "'serious' inside original_text is swapped for 'sirius' and assigned to new_text."},
 {'q': 'In a palindrome checking program, which concept would be most useful?',
  'code': '',
  'opts': {'A': 'Integer division',
           'B': 'Nested lists',
           'C': 'String reversal/slicing',
           'D': 'File handling'},
  'ans': 'C',
  'expl': 'A palindrome is a word or phrase that reads the exact same way backwards as forwards '
          "(e.g., 'madam'). By far the easiest way to check this in Python is to reverse the "
          'original string using slicing operations, such as text == text[::-1]. Thus, string '
          'reversal and slicing are the most useful concepts.'},
 {'q': 'What will be the value of `fact` after execution?',
  'code': 'num = 4\nfact = 1\nfor i in range(1, num+1):\n    fact = fact * i\nprint(fact)',
  'opts': {'A': '4', 'B': '10', 'C': '24', 'D': '120'},
  'ans': 'C',
  'expl': 'This program mathematically calculates the factorial of a given number, which is 4! in '
          'this case. The loop iterates with i taking values 1,2,3, and 4. Initially fact is 1. '
          'The steps are: 1 x 1=1; 1 x 2=2; 2 x 3=6; 6 x 4=24. So, the final value is 24.'},
 {'q': 'What is the purpose of `f` in the following statement?',
  'code': "print(f'Area of the rectangle = {area}')",
  'opts': {'A': 'It converts text into float',
           'B': 'It creates a formatted string',
           'C': 'It defines a function',
           'D': 'It performs file handling'},
  'ans': 'B',
  'expl': "Placing an 'f' before a string literal defines an f-string (formatted string literal) "
          'in modern Python. This enables direct, readable string formatting where we can inject '
          'the values of Python expressions or variables, like {area}, directly inside the curly '
          'braces of the string.'},
 {'q': 'What does the following code snippet output?',
  'code': 'value = 5.0\nprint(type(value))',
  'opts': {'A': "<class 'int'>",
           'B': "<class 'float'>",
           'C': "<class 'double'>",
           'D': "<class 'decimal'>"},
  'ans': 'B',
  'expl': 'The type() function in Python returns the class type of the object passed to it. Since '
          'the variable value is initialized with a decimal point (5.0), Python automatically '
          'assigns it the float data type.'},
 {'q': 'Determine the output of the given arithmetic expression.',
  'code': 'result = 2 ** 3\nprint(result)',
  'opts': {'A': '6', 'B': '8', 'C': '9', 'D': '16'},
  'ans': 'B',
  'expl': 'In Python, the double asterisk operator ** represents exponentiation. The expression '
          'computes 2 raised to the power of 3, which mathematically evaluates to 8.'},
 {'q': 'What is the result of executing the following statement?',
  'code': "print('Py' + 'thon')",
  'opts': {'A': 'Py thon', 'B': 'Python', 'C': 'Py+thon', 'D': 'Error'},
  'ans': 'B',
  'expl': 'The addition operator +, when used with string operands, performs concatenation. It '
          'merges the two strings end-to-end without inserting any additional spaces or '
          "characters, resulting in 'Python'."},
 {'q': 'What does the following logical evaluation return?',
  'code': 'print(10 > 9 and 5 < 3)',
  'opts': {'A': 'True', 'B': 'False', 'C': 'None', 'D': 'Error'},
  'ans': 'B',
  'expl': 'The expression contains two relational conditions combined with the logical and '
          'operator. While 10>9 evaluates to True, 5<3 evaluates to False. True and False results '
          'in False.'},
 {'q': 'Identify the output of the following indexing operation.',
  'code': 'lst = [10, 20, 30]\nprint(lst[1])',
  'opts': {'A': '10', 'B': '20', 'C': '30', 'D': 'Index out of bounds'},
  'ans': 'B',
  'expl': 'Python uses zero-based indexing for sequences such as lists. The element at index 0 is '
          '10, the element at index 1 is 20, and the element at index 2 is 30. Therefore, lst[1] '
          'accesses 20.'},
 {'q': 'What is printed upon executing this code block?',
  'code': "d = {'a': 1, 'b': 2}\nprint(d['a'])",
  'opts': {'A': '1', 'B': '2', 'C': "'a'", 'D': 'KeyError'},
  'ans': 'A',
  'expl': 'Dictionaries in Python store data as key-value pairs. Using bracket notation with a '
          "valid key retrieves the corresponding value. Passing the key 'a' to the dictionary d "
          'returns its associated value, 1.'},
 {'q': 'Evaluate the output of the given set definition and measurement.',
  'code': 's = {1, 1, 2}\nprint(len(s))',
  'opts': {'A': '1', 'B': '2', 'C': '3', 'D': 'Error'},
  'ans': 'B',
  'expl': 'A set in Python is an unordered collection of unique elements. When duplicate values (1 '
          'and 1) are provided during initialization, the set automatically removes duplicates. '
          'The final set is 1,2, which has a length of 2.'},
 {'q': 'What does the following string method invocation accomplish?',
  'code': "text = ' hello '\nprint(text.strip())",
  'opts': {'A': "' hello '", 'B': "'hello '", 'C': "' hello'", 'D': "'hello'"},
  'ans': 'D',
  'expl': 'The strip() method is used to remove leading and trailing whitespace characters from a '
          "string. Calling it on ' hello ' eliminates the spaces at both ends, yielding 'hello'."},
 {'q': 'Identify the result of executing this tuple assignment.',
  'code': 't = (1, 2)\nt[0] = 3',
  'opts': {'A': 't becomes (3, 2)',
           'B': 't becomes [3, 2]',
           'C': 'TypeError is raised',
           'D': 'SyntaxError is raised'},
  'ans': 'C',
  'expl': 'Tuples in Python are immutable data structures. This means their contents cannot be '
          'altered, added, or removed after creation. Attempting to reassign an index, such as '
          't[0] = 3, raises a TypeError.'},
 {'q': 'What does the membership test output?',
  'code': "print('a' in 'car')",
  'opts': {'A': 'True', 'B': 'False', 'C': '1', 'D': '0'},
  'ans': 'A',
  'expl': 'The in keyword acts as a membership operator. It checks if a specified substring exists '
          "within a target string. Since the character 'a' is present in the string 'car', the "
          'expression evaluates to the boolean value True.'},
 {'q': 'Analyze the basic conditional statement below. What is the output?',
  'code': "if 5 > 2:\n    print('yes')",
  'opts': {'A': 'No output', 'B': 'yes', 'C': 'True', 'D': 'False'},
  'ans': 'B',
  'expl': 'The if statement evaluates the boolean condition 5>2. Since 5 is mathematically greater '
          'than 2, the condition is true. The block of code indented under the if statement '
          "executes, printing 'yes'."},
 {'q': 'Calculate the final output of this loop accumulation.',
  'code': 's = 0\nfor i in [1, 2]:\n    s += i\nprint(s)',
  'opts': {'A': '1', 'B': '2', 'C': '3', 'D': '0'},
  'ans': 'C',
  'expl': 'The variable s is initialized to 0. The for loop iterates over the elements in the list '
          '[1,2]. During the first iteration, 1 is added to s. During the second iteration, 2 is '
          'added. The final accumulated sum is 0+1+2=3.'},
 {'q': 'Observe the output of string repetition combined with casting.',
  'code': 'print(str(10) * 2)',
  'opts': {'A': '20', 'B': "'1010'", 'C': "'20'", 'D': 'Error'},
  'ans': 'B',
  'expl': "The str() function casts the integer 10 into the string '10'. When the multiplication "
          'operator * is applied to a string and an integer n, Python repeats the string n times. '
          "Therefore, '10' multiplied by 2 concatenates the string to itself, resulting in "
          "'1010'."},
 {'q': 'Evaluate the result of the following slice notation.',
  'code': 'lst = [1, 2, 3, 4, 5]\nprint(lst[1:4:2])',
  'opts': {'A': '[2, 3]', 'B': '[2, 4]', 'C': '[1, 3]', 'D': '[3, 5]'},
  'ans': 'B',
  'expl': 'The slicing syntax [start:stop:step] defines list traversal. Parsing starts at index 1 '
          '(element 2) and proceeds up to, but not including, index 4 (element 5). A step size of '
          '2 skips every other element. Indices 1 and 3 are extracted, producing [2,4].'},
 {'q': 'What does the dictionary `get()` method return in this context?',
  'code': "d = {'x': 10}\nprint(d.get('y', 0))",
  'opts': {'A': '10', 'B': 'None', 'C': '0', 'D': 'KeyError'},
  'ans': 'C',
  'expl': 'The get(key, default) method retrieves the value associated with the specified key. If '
          'the key is absent from the dictionary, it returns the provided default argument instead '
          "of raising an error. The key 'y' does not exist in d, so the method returns 0."},
 {'q': 'Distinguish between identity and equality based on the code below.',
  'code': 'a = [1, 2]\nb = [1, 2]\nprint(a is b)',
  'opts': {'A': 'True', 'B': 'False', 'C': '1', 'D': 'Error'},
  'ans': 'B',
  'expl': 'The is keyword in Python checks for object identity (whether two references point to '
          'the exact same memory location), whereas == checks for value equality. Although a and b '
          'hold identical contents, lists are mutable objects, so Python allocates separate memory '
          'blocks for each assignment. Thus, a is b evaluates to False.'},
 {'q': 'Analyze how variable scope affects the output of this program.',
  'code': 'def f():\n    x = 10\n\nx = 5\nf()\nprint(x)',
  'opts': {'A': '10', 'B': '5', 'C': 'None', 'D': 'NameError'},
  'ans': 'B',
  'expl': 'Variables assigned inside a function are local to that function unless explicitly '
          'declared global. When f() is executed, the assignment x = 10 only modifies a local '
          'variable named x. The global variable x initialized to 5 outside the function remains '
          'unaffected. Printing it yields 5.'},
 {'q': 'What output is produced by the control flow within this loop?',
  'code': 'for i in range(3):\n    if i == 1:\n        continue\n    print(i)',
  'opts': {'A': '0 1 2', 'B': '1 2', 'C': '0 2', 'D': '0'},
  'ans': 'C',
  'expl': 'The continue statement causes a loop to skip the rest of its current iteration and '
          'advance to the next element. The loop ranges over 0,1,2. During iteration 0, it prints '
          '0. During iteration 1, the condition evaluates to true, triggering continue, bypassing '
          'the print statement. During iteration 2, it prints 2. Output is 0 followed by 2.'},
 {'q': 'Predict the result of chaining string split and join methods.',
  'code': "result = '-'.join('a b'.split())\nprint(result)",
  'opts': {'A': 'a b', 'B': 'a-b', 'C': 'a- -b', 'D': "['a', '-', 'b']"},
  'ans': 'B',
  'expl': "The split() method by default divides a string by whitespace, converting 'a b' into a "
          "list ['a', 'b']. Next, the join() method uses the string '-' as a separator to "
          "concatenate the items in the list. This joins 'a' and 'b' with a hyphen, producing "
          "'a-b'."},
 {'q': 'Examine the exception handling logic. What is the execution flow?',
  'code': "try:\n    1 / 0\nexcept ZeroDivisionError:\n    pass\nfinally:\n    print('done')",
  'opts': {'A': 'ZeroDivisionError crash', 'B': 'No output', 'C': 'done', 'D': 'SyntaxError'},
  'ans': 'C',
  'expl': 'The try block attempts a division by zero, which raises a ZeroDivisionError. The except '
          'block catches this exception and executes pass. The finally block executes upon '
          "completion of the try/except structure. Thus, 'done' is printed."}]


# ----------------------------------------------------------------- colours
def _supports_colour():
    if os.environ.get("NO_COLOR") or not sys.stdout.isatty():
        return False
    if os.name == "nt":
        os.system("")          # enables ANSI escape codes on Windows 10+
    return True

_COLOUR = _supports_colour()

def c(text, code):
    return f"\033[{code}m{text}\033[0m" if _COLOUR else text

BOLD, DIM, GREEN, RED, YELLOW, CYAN = "1", "2", "32", "31", "33", "36"


# ----------------------------------------------------------------- helpers
def fmt_time(seconds):
    """Under a minute -> 'x.y sec', otherwise 'x.y min'."""
    if seconds < 60:
        return f"{seconds:.1f} sec"
    return f"{seconds / 60:.1f} min"

def clock(seconds):
    seconds = max(0, int(seconds))
    return f"{seconds // 60:02d}:{seconds % 60:02d}"

def clear_screen():
    if sys.stdout.isatty():
        os.system("cls" if os.name == "nt" else "clear")

def timed_input(prompt, deadline):
    """
    Read one line, but give up when the deadline passes.
    Returns the typed text, or None if time ran out.
    """
    sys.stdout.write(prompt)
    sys.stdout.flush()
    remaining = deadline - time.time()
    if remaining <= 0:
        return None

    # Consoles such as IDLE are not real terminals: fall back to plain input()
    # and check the clock afterwards.
    if not sys.stdin.isatty():
        try:
            text = input()
        except EOFError:
            return None
        return None if time.time() > deadline else text

    if os.name == "nt":
        import msvcrt
        chars = []
        while True:
            if time.time() >= deadline:
                print()
                return None
            if msvcrt.kbhit():
                ch = msvcrt.getwch()
                if ch in ("\r", "\n"):
                    print()
                    return "".join(chars)
                if ch == "\x03":
                    raise KeyboardInterrupt
                if ch == "\b":
                    if chars:
                        chars.pop()
                        sys.stdout.write("\b \b")
                        sys.stdout.flush()
                elif ch in ("\x00", "\xe0"):
                    msvcrt.getwch()          # ignore arrow/function keys
                else:
                    chars.append(ch)
                    sys.stdout.write(ch)
                    sys.stdout.flush()
            else:
                time.sleep(0.03)
    else:
        import select
        ready, _, _ = select.select([sys.stdin], [], [], remaining)
        if not ready:
            print()
            return None
        line = sys.stdin.readline()
        return None if line == "" else line.rstrip("\n")


# ----------------------------------------------------------------- display
def show_question(i, q, deadline, answered_count):
    clear_screen()
    left = deadline - time.time()
    timer = c(f"Time left {clock(left)}", RED if left < 300 else CYAN)
    print(c(TITLE, BOLD))
    print(f"Question {i + 1} of {len(QUESTIONS)}   |   {timer}   |   "
          f"{answered_count} answered")
    print("-" * 70)
    print()
    for line in textwrap.wrap(q["q"], 70):
        print(c(line, BOLD))
    print()
    if q["code"]:
        for line in q["code"].splitlines():
            print("    " + c(line, YELLOW))
        print()
    for key in OPTION_KEYS:
        lines = q["opts"][key].splitlines() or [""]
        print(f"  {c(key + ')', BOLD)} {lines[0]}")
        for extra in lines[1:]:
            print(f"     {extra}")
    print()


# ----------------------------------------------------------------- results
def one_line(text, width):
    text = text.replace("\n", " / ")
    return text if len(text) <= width else text[: width - 3] + "..."

def print_results(answers, total_taken, time_up):
    clear_screen()
    n = len(QUESTIONS)
    score = sum(1 for q, a in zip(QUESTIONS, answers) if a and a["chosen"] == q["ans"])
    answered = sum(1 for a in answers if a and a["chosen"])
    pct = score / n * 100

    print(c(f"{TITLE}  -  RESULTS", BOLD))
    print()
    if time_up:
        print(c("Time is up! Unanswered questions are marked 'Not answered'.", RED))
        print()

    w_no, w_opt, w_rem, w_time = 5, 26, 12, 10
    widths = (w_no, w_opt, w_opt, w_rem, w_time)
    sep = "+" + "+".join("-" * (w + 2) for w in widths) + "+"

    def row(cells, colours=None):
        out = []
        for k, (cell, w) in enumerate(zip(cells, widths)):
            padded = cell.rjust(w) if k in (0, 4) else cell.ljust(w)
            if colours and colours[k]:
                padded = c(padded, colours[k])
            out.append(" " + padded + " ")
        return "|" + "|".join(out) + "|"

    print(sep)
    print(row(["Q.No.", "Correct option", "Chosen option", "Remark", "Time taken"]))
    print(sep)
    for i, (q, a) in enumerate(zip(QUESTIONS, answers)):
        correct = one_line(f"{q['ans']}) {q['opts'][q['ans']]}", w_opt)
        chosen_key = a["chosen"] if a else None
        if chosen_key:
            chosen = one_line(f"{chosen_key}) {q['opts'][chosen_key]}", w_opt)
            if chosen_key == q["ans"]:
                remark, colour = "Right", GREEN
            else:
                remark, colour = "Wrong", RED
        else:
            chosen, remark, colour = "-", "Not answered", DIM
        taken = fmt_time(a["time"]) if a else "-"
        print(row([str(i + 1), correct, chosen, remark, taken],
                  [None, None, None, colour, None]))
    print(sep)
    print(row(["", "Total score", f"{score} / {n}", "", ""]))
    print(row(["", "Percentage", f"{pct:.2f}%", "", ""]))
    print(row(["", "Total time taken", f"{fmt_time(total_taken)} ({clock(total_taken)})", "", ""]))
    print(sep)
    print()
    print(f"  Right: {c(score, GREEN)}   Wrong: {c(answered - score, RED)}   "
          f"Not answered: {n - answered}")
    print()
    print(c(f"  Total score : {score} / {n}", BOLD))
    print(c(f"  Percentage  : {pct:.2f}%", BOLD))
    print(c(f"  Time taken  : {fmt_time(total_taken)} ({clock(total_taken)} of 60:00)", BOLD))
    print()


def print_explanations(answers):
    print()
    for i, (q, a) in enumerate(zip(QUESTIONS, answers)):
        chosen = a["chosen"] if a else None
        tag = ("Not answered" if not chosen
               else "Right" if chosen == q["ans"] else "Wrong")
        colour = DIM if not chosen else GREEN if chosen == q["ans"] else RED
        print("=" * 70)
        print(c(f"Q{i + 1}. {q['q']}", BOLD) + "  [" + c(tag, colour) + "]")
        if q["code"]:
            print()
            for line in q["code"].splitlines():
                print("    " + c(line, YELLOW))
        print()
        ans_text = q["opts"][q["ans"]].replace("\n", " / ")
        print(c(f"Correct answer: {q['ans']}) {ans_text}", GREEN))
        if chosen and chosen != q["ans"]:
            print(c(f"Your answer   : {chosen}) {q['opts'][chosen].replace(chr(10), ' / ')}", RED))
        print()
        for line in textwrap.wrap(q["expl"], 70):
            print(line)
        print()


# ----------------------------------------------------------------- main
def main():
    clear_screen()
    print(c(TITLE, BOLD))
    print()
    print(f"  Questions  : {len(QUESTIONS)}")
    print("  Time limit : 60 minutes (the quiz ends automatically)")
    print("  Marking    : 1 mark per correct answer, no negative marking")
    print()
    print("  Type A, B, C or D and press Enter to answer.")
    print("  Type S to skip a question, Q to finish early.")
    print("  You'll find out what you got right at the end.")
    print()
    try:
        input("Press Enter to start...")
    except EOFError:
        return

    start = time.time()
    deadline = start + TIME_LIMIT
    answers = [None] * len(QUESTIONS)
    time_up = False
    quit_early = False

    for i, q in enumerate(QUESTIONS):
        shown = time.time()
        answered_count = sum(1 for a in answers if a and a["chosen"])
        show_question(i, q, deadline, answered_count)

        while True:
            left = deadline - time.time()
            reply = timed_input(f"Your answer (A/B/C/D, S=skip, Q=finish) "
                                f"[{clock(left)} left]: ", deadline)
            if reply is None:
                time_up = True
                answers[i] = {"chosen": None, "time": deadline - shown}
                break
            reply = reply.strip().upper()
            if reply in OPTION_KEYS:
                took = time.time() - shown
                answers[i] = {"chosen": reply, "time": took}
                print(c(f"\n  Answered in {fmt_time(took)}", YELLOW))
                break
            if reply == "S":
                took = time.time() - shown
                answers[i] = {"chosen": None, "time": took}
                print(c(f"\n  Skipped after {fmt_time(took)}", DIM))
                break
            if reply == "Q":
                confirm = timed_input("Finish the quiz now? (y/n): ", deadline)
                if confirm is None:
                    time_up = True
                    answers[i] = {"chosen": None, "time": deadline - shown}
                    break
                if confirm.strip().lower().startswith("y"):
                    answers[i] = {"chosen": None, "time": time.time() - shown}
                    quit_early = True
                    break
                continue
            print(c("  Please type A, B, C or D (or S to skip, Q to finish).", RED))

        if time_up or quit_early:
            break

        if i < len(QUESTIONS) - 1:
            nxt = timed_input("  Press Enter for the next question...", deadline)
            if nxt is None:
                time_up = True
                break

    end = deadline if time_up else time.time()
    total_taken = min(TIME_LIMIT, end - start)
    print_results(answers, total_taken, time_up)

    try:
        more = input("Show explanations for every question? (y/n): ")
    except EOFError:
        more = "n"
    if more.strip().lower().startswith("y"):
        print_explanations(answers)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nQuiz interrupted.")