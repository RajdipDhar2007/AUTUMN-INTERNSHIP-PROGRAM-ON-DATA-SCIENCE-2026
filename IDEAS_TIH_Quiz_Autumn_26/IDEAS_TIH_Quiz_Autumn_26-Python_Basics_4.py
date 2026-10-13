#!/usr/bin/env python3
"""
IDEAS TIH Quiz Autumn 26 - Python Basics 4 - interactive terminal quiz
---------------------------------------------------------------
Run:   python python_basics_4_quiz.py

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

TITLE = "IDEAS TIH Quiz Autumn 26 - Python Basics 4"
TIME_LIMIT = 60 * 60          # seconds
OPTION_KEYS = ("A", "B", "C", "D")

QUESTIONS = [{'q': 'Determine the outcome when invoking the pop() method without any arguments.',
  'code': 'data = [10, 20, 30]\nval = data.pop()\nprint(val)',
  'opts': {'A': '10', 'B': '20', 'C': '30', 'D': 'None'},
  'ans': 'C',
  'expl': 'The pop() method, when executed without a designated index argument, defaults to '
          'removing and returning the final element of the list. In the array provided, the last '
          'element is 30.'},
 {'q': 'Analyze the difference between standard list assignment and shallow copying in nested '
       'structures.',
  'code': 'original = [[1, 2], [3, 4]]\n'
          'shallow = list(original)\n'
          'shallow[0][0] = 99\n'
          'print(original[0][0])',
  'opts': {'A': '1', 'B': '99', 'C': '0', 'D': 'TypeError'},
  'ans': 'B',
  'expl': 'Invoking list() generates a shallow copy, meaning a new list object is created, but it '
          'references the same inner lists. Consequently, mutating an inner list through the '
          'shallow copy mutates the inner list accessed via the original variable.'},
 {'q': 'Evaluate the set operation representing a logical union.',
  'code': 's1 = {1, 2, 3}\ns2 = {3, 4, 5}\nprint(s1 | s2)',
  'opts': {'A': '{3}', 'B': '{1, 2, 4, 5}', 'C': '{1, 2, 3, 4, 5}', 'D': '{1, 2, 3, 3, 4, 5}'},
  'ans': 'C',
  'expl': 'The bitwise OR operator | acts as the union operator when applied to set objects. It '
          'merges both sets and eliminates duplicate items, resulting in a single set containing '
          'only unique elements.'},
 {'q': 'Identify the correct syntax for declaring a tuple containing exactly one element.',
  'code': 't1 = (5)\nt2 = (5,)\nprint(type(t1) == type(t2))',
  'opts': {'A': 'True', 'B': 'False', 'C': 'SyntaxError', 'D': 'None'},
  'ans': 'B',
  'expl': 'Parentheses alone encapsulate a mathematical expression in Python. Therefore, t1 '
          'evaluates to an integer (int). To unambiguously declare a one-element tuple, a trailing '
          'comma is required, making t2 a tuple. The comparison thus evaluates to False.'},
 {'q': 'What occurs structurally during tuple unpacking?',
  'code': 'coord = (10, 20)\nx, y = coord\nprint(y)',
  'opts': {'A': '10', 'B': '20', 'C': '(10, 20)', 'D': 'Error'},
  'ans': 'B',
  'expl': 'Tuple unpacking takes the elements inside a tuple structure and assigns them '
          'iteratively to a sequence of variables placed on the left side of the assignment '
          'operator. Here, x is assigned 10 and y is assigned 20.'},
 {'q': 'Why does attempting to utilize a list as a dictionary key result in an exception?',
  'code': "d = {}\nd[[1, 2]] = 'value'",
  'opts': {'A': 'Lists do not possess string representations.',
           'B': 'Lists are unhashable because they are mutable.',
           'C': 'Dictionaries only permit strings as keys.',
           'D': 'Lists exceed memory bounds for key indices.'},
  'ans': 'B',
  'expl': 'Python dictionary implementations rely on hash tables, demanding that all keys yield a '
          'stable hash value throughout their lifecycle. Lists are mutable; their contents can '
          'change, which would alter their hash. Thus, Python enforces unhashability on lists, '
          'yielding a TypeError if used as keys.'},
 {'q': 'Which statement accurately describes the characteristics of a frozenset?',
  'code': '',
  'opts': {'A': 'It is ordered chronologically by insertion.',
           'B': 'It is mutable, allowing elements to be added post-creation.',
           'C': 'It is an immutable set variant, rendering it hashable.',
           'D': 'It cannot participate in mathematical set operations.'},
  'ans': 'C',
  'expl': 'A frozenset in Python contains identical properties to a standard set (unordered, '
          'unique elements) but lacks methods to modify it after initialization. This immutability '
          'ensures a consistent hash value, permitting a frozenset to function as a dictionary key '
          'or as a member of another set.'},
 {'q': 'Analyze the operational difference between the remove() and discard() methods on a set.',
  'code': 's = {1, 2}\ns.discard(3)\ns.remove(3)',
  'opts': {'A': 'discard() raises an error if the element is absent, remove() does not.',
           'B': 'remove() raises a KeyError if the element is absent, discard() ignores it.',
           'C': 'Both methods perform identically in all contexts.',
           'D': 'discard() empties the entire set.'},
  'ans': 'B',
  'expl': 'When attempting to delete an element that does not currently reside in the set object, '
          'discard() simply returns None and allows execution to proceed. Conversely, remove() '
          "strictly enforces the element's existence, raising a KeyError if it is not found."},
 {'q': 'Evaluate the result of the following set comprehension.',
  'code': 'res = {x % 2 for x in [1, 2, 3, 4, 5]}\nprint(res)',
  'opts': {'A': '{1, 0, 1, 0, 1}', 'B': '{0, 1}', 'C': '{1, 2, 3, 4, 5}', 'D': 'SyntaxError'},
  'ans': 'B',
  'expl': 'The generator computes x % 2 for each integer in the list. The sequence of computed '
          'values is 1, 0, 1, 0, 1. Since a set structure prevents duplicate values, only the '
          'unique outcomes 0 and 1 are retained.'},
 {'q': 'Determine the outcome of concatenating two tuple structures using the addition operator.',
  'code': 't1 = (1, 2)\nt2 = (3, 4)\nprint(t1 + t2)',
  'opts': {'A': '(4, 6)', 'B': '((1, 2), (3, 4))', 'C': '(1, 2, 3, 4)', 'D': 'TypeError'},
  'ans': 'C',
  'expl': 'Applying the + operator to two tuples forces tuple concatenation. It creates a new, '
          'independent tuple object containing the ordered sequence of elements from the first '
          'tuple followed consecutively by elements from the second.'},
 {'q': 'Analyze the result of the round() built-in function specifically for standard half-way '
       'floating-point values in Python 3.',
  'code': 'val = round(2.5) + round(3.5)\nprint(val)',
  'opts': {'A': '5', 'B': '6', 'C': '7', 'D': 'Error'},
  'ans': 'B',
  'expl': "Python 3 implements 'Banker's Rounding' (round to even). If a floating-point number is "
          'exactly midway between two integers, it is rounded toward the nearest even integer. '
          'Thus, 2.5 is rounded down to 2, and 3.5 is rounded up to 4. The sum is 2 + 4 = 6.'},
 {'q': 'Examine the output of floor division utilizing a negative dividend.',
  'code': 'print(-7 // 2)',
  'opts': {'A': '-3.5', 'B': '-3', 'C': '-4', 'D': 'Error'},
  'ans': 'C',
  'expl': 'The // operator executes floor division, which mathematically returns the largest '
          'integer less than or equal to the quotient. The precise fractional quotient is -3.5. '
          'The integer lesser than or equal to -3.5 on the number line is -4.'},
 {'q': 'Evaluate the outcome of casting empty container structures to boolean values.',
  'code': 'result = bool([]) or bool({})\nprint(result)',
  'opts': {'A': 'True', 'B': 'False', 'C': 'Error', 'D': 'None'},
  'ans': 'B',
  'expl': "According to Python's internal boolean evaluation rules, empty lists, empty "
          'dictionaries, empty sets, and strings of length zero consistently evaluate to False. '
          'The statement computes False or False, which yields False.'},
 {'q': 'What does passing a floating-point object to the str() built-in construct accomplish?',
  'code': 'print(type(str(3.14)))',
  'opts': {'A': "<class 'float'>", 'B': "<class 'int'>", 'C': "<class 'str'>", 'D': 'TypeError'},
  'ans': 'C',
  'expl': 'The str() function type-casts the numerical value it receives into a character string '
          'literal representation, transforming the mathematical float 3.14 into the string object '
          "'3.14', hence returning the string class type."},
 {'q': 'Examine the identity evaluation mechanism when dealing with small integers inside standard '
       'Python.',
  'code': 'a = 256\nb = 256\nc = 257\nd = 257\nprint(a is b, c is d)',
  'opts': {'A': 'True True', 'B': 'False False', 'C': 'True False', 'D': 'False True'},
  'ans': 'C',
  'expl': 'The standard CPython implementation internally caches (interns) integer objects '
          'residing between -5 and 256 to save memory. Hence, variables assigned 256 reference the '
          'same distinct memory address (True). However, variables assigned 257 point to newly '
          'allocated, non-cached memory addresses, rendering their identity check False (in a '
          'standard REPL environment). (Note: if all five lines are run together as one script or '
          'file, CPython can reuse a single 257 constant and print True True; the answer key '
          'assumes each line is typed separately in the interactive interpreter.)'},
 {'q': 'Determine the output of the modulo operator when operating over floating-point parameters.',
  'code': 'print(5.5 % 2)',
  'opts': {'A': '1', 'B': '1.5', 'C': '2', 'D': 'TypeError'},
  'ans': 'B',
  'expl': 'The modulo operator (%) calculates the remainder. When calculating 5.5/2, 2 fits into '
          '5.5 twice (2 x 2 = 4). The mathematical remainder is therefore 5.5 - 4 = 1.5. Python '
          'safely extends modulo division to float structures.'},
 {'q': 'Evaluate the integer conversion when supplying a custom base parameter.',
  'code': "print(int('101', 2))",
  'opts': {'A': '5', 'B': '101', 'C': '3', 'D': 'ValueError'},
  'ans': 'A',
  'expl': 'The int(string, base) initialization specifies that the string argument should be '
          "parsed interpreting the supplied numerical base. Here, it interprets the string '101' "
          'as a base-2 binary number. Converting binary 101_2 equates mathematically to 1 x 2^2 + '
          '0 x 2^1 + 1 x 2^0 = 5.'},
 {'q': 'Identify the behavior of fetching the real part of a complex numeric literal.',
  'code': 'num = 3 + 4j\nprint(num.real)',
  'opts': {'A': '3.0', 'B': '3', 'C': '4.0', 'D': 'Error'},
  'ans': 'A',
  'expl': 'Complex numeric types possess .real and .imag property attributes. Both values are '
          'returned as floating-point precision numbers. Consequently, extracting .real from 3 + '
          '4j emits the float 3.0.'},
 {'q': 'Evaluate the implicit behavior of chained comparison operators within Python.',
  'code': 'print(1 < 2 < 3)',
  'opts': {'A': 'True', 'B': 'False', 'C': 'Error', 'D': 'None'},
  'ans': 'A',
  'expl': 'Python evaluates chained comparisons identically to logical conjunctions. The '
          'expression 1 < 2 < 3 is directly translated to (1 < 2) and (2 < 3). Since both '
          'conditions evaluate to True, the entire expression yields True.'},
 {'q': 'Trace the execution of bitwise operations acting on integers.',
  'code': 'print(4 | 1)',
  'opts': {'A': '4', 'B': '1', 'C': '5', 'D': '3'},
  'ans': 'C',
  'expl': 'The operator | performs a bitwise logical OR. The binary layout for 4 is 100_2 and for '
          '1 is 001_2. Combining these bits yields 101_2, which equates back to the decimal '
          'integer 5.'},
 {'q': 'The attached table illustrates a two-dimensional matrix. If this mathematical matrix is '
       'implemented identically as a nested list object matrix = [[1, 2, 3], [4, 5, 6]], what does '
       'the evaluation of matrix[1][2] yield?',
  'code': 'Matrix Representation\n'
          '+---------+---------+---------+\n'
          '| Index 0 | Index 1 | Index 2 |\n'
          '+---------+---------+---------+\n'
          '| 1       | 2       | 3       |\n'
          '| 4       | 5       | 6       |\n'
          '+---------+---------+---------+',
  'opts': {'A': '3', 'B': '4', 'C': '5', 'D': '6'},
  'ans': 'D',
  'expl': 'Double indexing traverses multi-dimensional structures. The expression matrix[1] points '
          'to the second inner list [4, 5, 6]. From this nested list, the index [2] accesses the '
          'third element, returning the value 6.'},
 {'q': 'Observe the variable scopes utilized inside this functional routine.',
  'code': 'x = 10\ndef modify():\n    global x\n    x = 20\nmodify()\nprint(x)',
  'opts': {'A': '10', 'B': '20', 'C': 'Error', 'D': 'None'},
  'ans': 'B',
  'expl': 'The global reserved keyword notifies the interpreter that the assignment must occur at '
          'the module level rather than initiating a new local variable. The internal assignment '
          'updates the global x to 20.'},
 {'q': 'Identify the data format returned by iterating via the enumerate() function.',
  'code': "for data in enumerate(['A']):\n    print(type(data))",
  'opts': {'A': "<class 'list'>",
           'B': "<class 'tuple'>",
           'C': "<class 'str'>",
           'D': "<class 'dict'>"},
  'ans': 'B',
  'expl': 'The enumerate() construct yields an iterator tracking numerical count alongside '
          'sequential elements. It packages these two discrete components as standard tuples, '
          "e.g., (0, 'A')."},
 {'q': 'Evaluate the list length generated when applying zip() to iterables of unequal length.',
  'code': "l1 = [1, 2, 3]\nl2 = ['a', 'b']\nprint(len(list(zip(l1, l2))))",
  'opts': {'A': '2', 'B': '3', 'C': '5', 'D': 'ValueError'},
  'ans': 'A',
  'expl': 'By definition, zip() aggregates iterables but ceases iteration immediately when the '
          'shortest provided iterator is completely exhausted. Since l2 holds a length of 2, the '
          'combined list also yields length 2.'},
 {'q': 'Trace the logic implemented by combining boolean list evaluations.',
  'code': "b1 = all([True, 1, 'Hello'])\nb2 = any([False, 0, []])\nprint(b1 == b2)",
  'opts': {'A': 'True', 'B': 'False', 'C': 'TypeError', 'D': 'None'},
  'ans': 'B',
  'expl': 'The all() functional call requires every item to be truthy. Because True, 1, and '
          "'Hello' are truthy, b1 evaluates to True. Conversely, any() mandates at least a single "
          'truthy item. False, 0, and [] are falsy, making b2 False. Thus b1 == b2 computes as '
          'False.'},
 {'q': 'Observe the execution pathway of an exception handling architecture comprising an else '
       'directive.',
  'code': 'def fetch():\n'
          '    try:\n'
          '        x = 5 / 1\n'
          '    except ZeroDivisionError:\n'
          "        return 'Error'\n"
          '    else:\n'
          "        return 'Success'\n"
          'print(fetch())',
  'opts': {'A': 'Error', 'B': 'Success', 'C': 'None', 'D': 'SyntaxError'},
  'ans': 'B',
  'expl': 'Within a try...except...else block, the else clause executes only if no exception is '
          'raised inside the try block. Dividing 5 by 1 succeeds without exception. Therefore, the '
          "except block is bypassed, and the else clause executes, returning 'Success'."},
 {'q': 'Evaluate the precise difference between the type() and isinstance() diagnostic checks when '
       'evaluating subclasses.',
  'code': 'class A: pass\nclass B(A): pass\nobj = B()\nprint(type(obj) == A, isinstance(obj, A))',
  'opts': {'A': 'True True', 'B': 'False True', 'C': 'True False', 'D': 'False False'},
  'ans': 'B',
  'expl': 'The type() comparison checks for the exact type, returning False because obj is '
          'exclusively class B, not A. In direct contrast, isinstance() checks for inheritance, '
          "returning True because obj's class B inherits successfully from parent class A."},
 {'q': 'Determine the outcome when directly modifying a string character by assignment.',
  'code': "s = 'Data'\ns[0] = 'd'\nprint(s)",
  'opts': {'A': 'data', 'B': 'Data', 'C': 'TypeError', 'D': 'SyntaxError'},
  'ans': 'C',
  'expl': 'Strings are immutable collections in Python. Attempting to overwrite or mutate an '
          'existing character via index assignment raises a TypeError.'},
 {'q': 'How does python resolve undefined parameter counts using the *args identifier?',
  'code': 'def sum_all(*args):\n    return type(args)\nprint(sum_all(1, 2, 3))',
  'opts': {'A': "<class 'list'>",
           'B': "<class 'tuple'>",
           'C': "<class 'set'>",
           'D': "<class 'dict'>"},
  'ans': 'B',
  'expl': 'The *args packing syntax instructs Python to aggregate all positional arguments into a '
          'tuple during function invocation.'},
 {'q': 'Observe the functional result of dictionary retrieval via the get() mechanism.',
  'code': "info = {'id': 1}\nval = info.get('name', 'Unknown')\nprint(val)",
  'opts': {'A': '1', 'B': 'Unknown', 'C': 'KeyError', 'D': 'None'},
  'ans': 'B',
  'expl': 'The get(key, default) method retrieves the value for a designated key. Because the key '
          "'name' does not exist in the dictionary, it returns the provided default parameter, "
          "'Unknown'."}]


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