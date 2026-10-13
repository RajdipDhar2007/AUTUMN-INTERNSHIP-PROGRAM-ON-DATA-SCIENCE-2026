#!/usr/bin/env python3
"""
IDEAS TIH Quiz Autumn 26 - Python Basics 10 - interactive terminal quiz
---------------------------------------------------------------
Run:   python python_basics_10_quiz.py

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

TITLE = "IDEAS TIH Quiz Autumn 26 - Python Basics 10"
TIME_LIMIT = 60 * 60          # seconds
OPTION_KEYS = ("A", "B", "C", "D")

QUESTIONS = [{'q': 'What will the function isPrime(1) return based on the given implementation?',
  'code': '',
  'opts': {'A': 'True', 'B': 'False', 'C': 'None', 'D': 'Error'},
  'ans': 'A',
  'expl': 'Based on the specific implementation in the source, it returns True. Note that '
          'mathematically, 1 is not a prime number, but many basic programming implementations '
          'incorrectly flag it as prime if they only check for divisors from 2 up to the number '
          'without explicitly handling 1 as a special case.'},
 {'q': 'What is the output of the following code?',
  'code': "isEvenLambda = lambda x: 'Even' if x%2==0 else 'Odd'\nprint(isEvenLambda(56))",
  'opts': {'A': 'True', 'B': 'False', 'C': 'Even', 'D': 'Odd'},
  'ans': 'C',
  'expl': 'The lambda function uses an inline conditional statement to check if the variable x is '
          'divisible by 2 (i.e., x % 2 == 0). Since 56 is an even number, the remainder is 0, so '
          "the function returns the string 'Even'."},
 {'q': 'What will factorial(0) return in the recursive factorial program?',
  'code': '',
  'opts': {'A': '0', 'B': '1', 'C': 'Error', 'D': 'None'},
  'ans': 'B',
  'expl': 'In mathematics, the factorial of 0 (written as 0!) is defined as 1. In a standard '
          'recursive factorial program, checking if the input is 0 is the base case, and it '
          'returns 1 to stop the recursion from running indefinitely.'},
 {'q': 'In the Armstrong number program, what is the purpose of the statement below?',
  'code': 'l = len(str(n))',
  'opts': {'A': 'Converts number into float',
           'B': 'Counts the digits of the number',
           'C': 'Finds square root',
           'D': 'Reverses the number'},
  'ans': 'B',
  'expl': 'The function str(n) converts the integer n into a text string. The len() function then '
          'counts how many characters are in that string. Together, this combination is a quick '
          'trick in Python to count exactly how many digits are in a given number.'},
 {'q': 'What will be the output?',
  'code': 'myList = [1,2,3,4,5,6,7,8,7,7]\nmyList.remove(7)\nprint(myList)',
  'opts': {'A': 'All 7s are removed',
           'B': 'Only the first occurrence of 7 is removed',
           'C': 'Last occurrence of 7 is removed',
           'D': 'Error'},
  'ans': 'B',
  'expl': 'In Python, the remove(value) method on a list searches for the specified value and '
          'removes only its first occurrence from the left. It does not delete all copies of that '
          'value. Therefore, only the first 7 will be deleted.'},
 {'q': 'What does `myList.pop(7)` do?',
  'code': '',
  'opts': {'A': 'Removes the value 7 from the list',
           'B': 'Removes the last element',
           'C': 'Removes the element at index 7',
           'D': 'Clears the list'},
  'ans': 'C',
  'expl': 'The pop(index) method in Python removes the element located at the specified index and '
          'returns it. Contrast this with remove(value), which removes based on the actual value. '
          'Thus, pop(7) deletes the element sitting at index 7.'},
 {'q': 'Which data structure among the following does NOT allow modification after creation?',
  'code': '',
  'opts': {'A': 'List', 'B': 'Dictionary', 'C': 'Set', 'D': 'Tuple'},
  'ans': 'D',
  'expl': 'A Tuple is an immutable data structure in Python. Immutability means that once the '
          'tuple is created, you cannot change, add, or remove items from it. In contrast, Lists, '
          'Dictionaries, and Sets are all mutable.'},
 {'q': 'What will be the output of the following statement?',
  'code': 'print(round(0.49))',
  'opts': {'A': '0', 'B': '1', 'C': '0.49', 'D': 'Error'},
  'ans': 'A',
  'expl': 'The round() function mathematically rounds a floating-point number to the closest '
          'integer. Because 0.49 is less than 0.5, it is closer to 0 than it is to 1, so it rounds '
          'down to 0.'},
 {'q': 'Which statement about sets is correct based on the notebook?',
  'code': '',
  'opts': {'A': 'Sets allow duplicate values',
           'B': 'Sets maintain insertion order always',
           'C': 'Sets store only unique values',
           'D': 'Sets use indexing'},
  'ans': 'C',
  'expl': 'In Python, a Set is an unordered collection of items. Its primary mathematical '
          'characteristic is that it automatically removes duplicate elements, meaning it stores '
          'only unique values. Sets also do not support index-based access.'},
 {'q': 'What will be the output of the following recursive function call?',
  'code': 'power(2,3)',
  'opts': {'A': '5', 'B': '6', 'C': '8', 'D': '9'},
  'ans': 'C',
  'expl': 'The function call power(2, 3) mathematically calculates 2 raised to the power of 3. '
          'This evaluates to 2^3 = 2 x 2 x 2 = 8.'},
 {'q': 'What is the output of the following code snippet?',
  'code': 'multiply = lambda x, y: x * y\nprint(multiply(4, 5))',
  'opts': {'A': '9', 'B': '20', 'C': 'Error', 'D': 'None'},
  'ans': 'B',
  'expl': 'The code defines an anonymous lambda function that accepts two parameters, x and y, and '
          'returns their product. Passing 4 and 5 as arguments evaluates 4 multiplied by 5, '
          'resulting in 20.'},
 {'q': 'What does the following code utilizing the map function return?',
  'code': 'nums = [1, 2, 3]\nresult = list(map(lambda x: x**2, nums))\nprint(result)',
  'opts': {'A': '[1, 2, 3]', 'B': '[1, 4, 9]', 'C': '[2, 4, 6]', 'D': '[1, 8, 27]'},
  'ans': 'B',
  'expl': 'The map function applies the lambda function to each element of the list nums. The '
          'lambda squares each input (x^2). Thus, 1 becomes 1, 2 becomes 4, and 3 becomes 9.'},
 {'q': 'Determine the output of the filtering operation below.',
  'code': 'data = [10, 15, 20, 25]\n'
          'filtered_data = list(filter(lambda x: x % 10 == 0, data))\n'
          'print(filtered_data)',
  'opts': {'A': '[10, 15, 20, 25]', 'B': '[15, 25]', 'C': '[10, 20]', 'D': '[20]'},
  'ans': 'C',
  'expl': 'The filter function constructs an iterator from elements of the list for which the '
          'lambda returns True. The condition x % 10 == 0 evaluates to True only for elements '
          'divisible by 10, which are 10 and 20.'},
 {'q': 'How does the sorting operation modify the list of tuples?',
  'code': "pairs = [(1, 'c'), (3, 'a'), (2, 'b')]\n"
          'pairs.sort(key=lambda pair: pair[1])\n'
          'print(pairs)',
  'opts': {'A': "[(1, 'c'), (2, 'b'), (3, 'a')]",
           'B': "[(3, 'a'), (2, 'b'), (1, 'c')]",
           'C': "[(1, 'c'), (3, 'a'), (2, 'b')]",
           'D': 'Error'},
  'ans': 'B',
  'expl': 'The sort method is provided a key argument, which dictates the criterion for sorting. '
          'The lambda extracts the item at index 1 of each tuple (the string character). '
          "Therefore, the list is sorted alphabetically by 'a', 'b', and 'c'."},
 {'q': 'Evaluate the result of the following immediately invoked lambda function expression.',
  'code': 'result = (lambda x, y: (x + y) if x > y else (x - y))(5, 8)\nprint(result)',
  'opts': {'A': '13', 'B': '-3', 'C': '3', 'D': 'Syntax Error'},
  'ans': 'B',
  'expl': 'The lambda expression accepts two arguments. It checks if x > y. Here, x = 5 and y = 8. '
          'Since 5 > 8 is False, it executes the else clause, computing x - y, which is 5 - 8 = '
          '-3.'},
 {'q': 'What is the expected output when calling a lambda stored inside a dictionary?',
  'code': "ops = {'square': lambda x: x ** 2, 'cube': lambda x: x ** 3}\nprint(ops['cube'](3))",
  'opts': {'A': '6', 'B': '9', 'C': '27', 'D': 'KeyError'},
  'ans': 'C',
  'expl': "The dictionary ops stores lambda functions as values. Accessing ops['cube'] retrieves "
          'the function responsible for computing x^3. Passing 3 into it yields 3^3 = 27.'},
 {'q': 'What occurs structurally in Python if a recursive function operates continuously without a '
       'base case?',
  'code': '',
  'opts': {'A': 'Memory Leak',
           'B': 'RecursionError',
           'C': 'SyntaxError',
           'D': 'Infinite Loop without exception'},
  'ans': 'B',
  'expl': 'Python enforces a maximum recursion depth to prevent indefinite execution. If a base '
          'case is not met, the call stack exceeds this limit, and Python raises a '
          'RecursionError.'},
 {'q': 'Identify the logic error in the following recursive function.',
  'code': 'def countdown(n):\n    print(n)\n    countdown(n-1)',
  'opts': {'A': 'It lacks a return type definition.',
           'B': 'It lacks a base case.',
           'C': 'The parameter n is not an integer.',
           'D': 'print() cannot be used inside recursion.'},
  'ans': 'B',
  'expl': 'The function subtracts 1 from n and calls itself indefinitely. Because there is no '
          'conditional statement to stop the function (a base case, e.g., if n == 0:), it will '
          'execute until it exceeds the maximum recursion depth.'},
 {'q': 'Trace the execution of this recursive function to determine the output.',
  'code': 'def f(n):\n    if n <= 1:\n        return n\n    return f(n-1) + f(n-2)\nprint(f(4))',
  'opts': {'A': '2', 'B': '3', 'C': '4', 'D': '5'},
  'ans': 'B',
  'expl': 'This is the classic Fibonacci sequence calculation. To evaluate f(4), the program '
          'calculates f(3) + f(2). Expanding this: f(3) = f(2) + f(1) and f(2) = f(1) + f(0). With '
          'base cases f(1) = 1 and f(0) = 0, we find f(2) = 1, f(3) = 2, and finally f(4) = 2 + 1 '
          '= 3.'},
 {'q': 'What does this recursive function accomplish?',
  'code': 'def proc(s):\n'
          '    if len(s) == 0:\n'
          '        return s\n'
          '    else:\n'
          '        return proc(s[1:]) + s[0]',
  'opts': {'A': 'Sorts the string alphabetically.',
           'B': 'Reverses the string.',
           'C': 'Returns the first character.',
           'D': 'Truncates the string.'},
  'ans': 'B',
  'expl': 'The function takes a string s. If the string is empty, it returns it. Otherwise, it '
          'calls itself with the substring starting from index 1 (s[1:]) and appends the first '
          'character (s[0]) to the end of the returned result. This recursively constructs a '
          'reversed string.'},
 {'q': 'Determine the value printed by the mathematical recursive function below.',
  'code': 'def calc(n):\n'
          '    if n == 0:\n'
          '        return 0\n'
          '    return (n % 10) + calc(n // 10)\n'
          'print(calc(456))',
  'opts': {'A': '0', 'B': '10', 'C': '15', 'D': '456'},
  'ans': 'C',
  'expl': 'The function calculates the sum of the digits of a base-10 integer. Using modulo 10 (n '
          '% 10), it extracts the last digit. It then uses floor division (n // 10) to pass the '
          'remaining digits to the next recursive call. For 456, the sequence is 6 + 5 + 4 + 0 = '
          '15.'},
 {'q': 'In the verification of a 3-digit Armstrong number (where n = d_1d_2d_3), which '
       'mathematical condition must evaluate to true?',
  'code': '',
  'opts': {'A': 'n = d_1 + d_2 + d_3',
           'B': 'n = d_1^2 + d_2^2 + d_3^2',
           'C': 'n = d_1^3 + d_2^3 + d_3^3',
           'D': 'n = d_1 x d_2 x d_3'},
  'ans': 'C',
  'expl': 'By mathematical definition, an Armstrong number (or narcissistic number) for a given '
          'number of digits k is an integer such that the sum of its digits each raised to the '
          'power of k equals the number itself. For a 3-digit number, each digit must be raised to '
          'the power of 3.'},
 {'q': 'Examine the output of calling a function with a mutable default argument sequentially.',
  'code': 'def add_item(val, lst=[]):\n'
          '    lst.append(val)\n'
          '    return lst\n'
          '\n'
          'print(add_item(1))\n'
          'print(add_item(2))',
  'opts': {'A': '[1] followed by [2]',
           'B': '[1] followed by [1, 2]',
           'C': '[1, 2] followed by [1, 2]',
           'D': 'TypeError'},
  'ans': 'B',
  'expl': 'In Python, default arguments are evaluated exactly once at the time of function '
          'definition, not at each function call. Because a list is mutable, subsequent calls to '
          'add_item without explicitly passing a list will modify and return the exact same list '
          'object initialized during definition.'},
 {'q': 'Evaluate the outcome of the naive prime checking implementation when provided with a '
       'negative number.',
  'code': 'def is_prime(n):\n'
          '    for i in range(2, n):\n'
          '        if n % i == 0:\n'
          '            return False\n'
          '    return True\n'
          '\n'
          'print(is_prime(-5))',
  'opts': {'A': 'False', 'B': 'True', 'C': 'RecursionError', 'D': 'TypeError'},
  'ans': 'B',
  'expl': 'The function iterates from 2 up to n - 1. If n = -5, the range(2, -5) iterator is empty '
          'because the start is greater than the stop. Thus, the for loop does not execute, and '
          'the function immediately proceeds to return True. This highlights a logical flaw in '
          'basic algorithms not handling edge cases.'},
 {'q': 'When two distinct functions sequentially call each other in order to reach a base case, '
       'what is this specific architectural pattern termed?',
  'code': '',
  'opts': {'A': 'Tail Recursion',
           'B': 'Infinite Recursion',
           'C': 'Mutual Recursion',
           'D': 'Iterative Recursion'},
  'ans': 'C',
  'expl': 'Mutual recursion occurs when function A calls function B, and function B in turn calls '
          'function A. This is a common pattern in specific algorithmic designs, such as recursive '
          'descent parsers or determining parity (even/odd) via tandem functions.'},
 {'q': 'What distinguishes the append() method from the extend() method in list objects?',
  'code': 'lst1 = [1, 2]\nlst1.append([3, 4])\n\nlst2 = [1, 2]\nlst2.extend([3, 4])',
  'opts': {'A': 'append() creates a new list, extend() modifies in-place.',
           'B': 'append() adds the argument as a single element, extend() iterates over the '
                'argument appending each element.',
           'C': 'extend() is strictly used for tuples, append() for lists.',
           'D': 'Both execute the identical underlying operation.'},
  'ans': 'B',
  'expl': 'The append method inserts the passed object into the list entirely as a single element, '
          'leading to a nested structure in this case ([1, 2, [3, 4]]). Conversely, extend takes '
          'an iterable and appends each of its individual elements to the list sequentially ([1, '
          '2, 3, 4]).'},
 {'q': 'Evaluate the result of negative indexing in the list extraction shown.',
  'code': 'arr = [10, 20, 30, 40, 50]\nprint(arr[-2])',
  'opts': {'A': '20', 'B': '30', 'C': '40', 'D': '50'},
  'ans': 'C',
  'expl': 'In Python sequences, a negative index accesses elements relative to the end of the '
          'structure. The index -1 corresponds to the final element (50), so the index -2 '
          'corresponds to the penultimate element (40).'},
 {'q': 'Identify the output generated by the slicing notation.',
  'code': 'seq = [1, 2, 3, 4]\nprint(seq[::-1])',
  'opts': {'A': '[4, 3, 2, 1]', 'B': '[1, 2, 3, 4]', 'C': '[4]', 'D': 'SyntaxError'},
  'ans': 'A',
  'expl': 'Slicing syntax in Python takes the form [start:stop:step]. When the step argument is '
          'assigned -1 and the start and stop are omitted, Python returns a shallow copy of the '
          'entire list traversed in reverse order.'},
 {'q': 'Analyze the execution of removing items from a list while iterating over it.',
  'code': 'nums = [1, 2, 3, 4]\n'
          'for n in nums:\n'
          '    if n % 2 == 0:\n'
          '        nums.remove(n)\n'
          'print(nums)',
  'opts': {'A': '[1, 3]', 'B': '[1, 2, 3, 4]', 'C': '[1, 3, 4]', 'D': 'ValueError'},
  'ans': 'A',
  'expl': 'Modifying a list during iteration shifts subsequent elements, causing the iterator to '
          'skip items because it relies on sequential index values. When 2 is evaluated at index 1 '
          'and removed, the list shifts left, making 3 the element at index 1. The loop progresses '
          'to index 2, checking 4. 4 is even and is removed. Ultimately, [1, 3] remains.'},
 {'q': 'Evaluate the list comprehension statement provided.',
  'code': 'result = [x for x in range(5) if x % 2 != 0]\nprint(result)',
  'opts': {'A': '[0, 1, 2, 3, 4]', 'B': '[0, 2, 4]', 'C': '[1, 3]', 'D': '[1, 3, 5]'},
  'ans': 'C',
  'expl': 'The range(5) function generates integers 0 through 4. The list comprehension iterates '
          'over these values and filters them using the condition x % 2 != 0, which isolates odd '
          'numbers. Therefore, 1 and 3 are collected into the new list.'}]


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