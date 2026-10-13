#!/usr/bin/env python3
"""
IDEAS TIH Quiz Autumn 26 - Python Basics 5 - interactive terminal quiz
---------------------------------------------------------------
Run:   python python_basics_5_quiz.py

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

TITLE = "IDEAS TIH Quiz Autumn 26 - Python Basics 5"
TIME_LIMIT = 60 * 60          # seconds
OPTION_KEYS = ("A", "B", "C", "D")

QUESTIONS = [{'q': 'What is the primary purpose of a class in Python?',
  'code': '',
  'opts': {'A': 'To execute loops',
           'B': 'To store only numbers',
           'C': 'To act as a blueprint for creating objects',
           'D': 'To perform mathematical operations'},
  'ans': 'C',
  'expl': 'A class acts as a blueprint in Object-Oriented Programming (OOP). It defines the '
          'attributes and methods shared by its instances.'},
 {'q': 'What is automatically executed when an object of a class is created?',
  'code': '',
  'opts': {'A': 'print()', 'B': '__init__()', 'C': 'main()', 'D': 'return()'},
  'ans': 'B',
  'expl': 'The __init__() method is a constructor in Python. It is automatically called upon '
          'object instantiation to initialize attributes.'},
 {'q': 'In a Python class (for example, a `Student` class), what does `self` refer to?',
  'code': '',
  'opts': {'A': 'Parent class',
           'B': 'Global variable',
           'C': 'Current instance of the class',
           'D': 'Constructor only'},
  'ans': 'C',
  'expl': 'The self parameter represents the current instance of the class. It provides access to '
          'instance attributes and methods, distinguishing them from local variables.'},
 {'q': 'Which type of constructor is used in the following code snippet?',
  'code': "Student('Miguel Diaz', 85)",
  'opts': {'A': 'Default constructor',
           'B': 'Copy constructor',
           'C': 'Parameterized constructor',
           'D': 'Destructor'},
  'ans': 'C',
  'expl': "A parameterized constructor accepts arguments alongside self. Here, 'Miguel Diaz' and "
          '85 are passed to initialize the specific Student instance.'},
 {'q': 'Which statement correctly describes a static method?',
  'code': '',
  'opts': {'A': 'It can access instance variables directly',
           'B': 'It requires self parameter',
           'C': 'It belongs to the class rather than an object instance',
           'D': 'It cannot be called'},
  'ans': 'C',
  'expl': 'A static method is bound to the class rather than an instance. It does not require a '
          'self parameter and cannot modify instance state.'},
 {'q': 'What OOP concept is demonstrated by hiding internal implementation details from the user?',
  'code': '',
  'opts': {'A': 'Encapsulation', 'B': 'Abstraction', 'C': 'Inheritance', 'D': 'Recursion'},
  'ans': 'B',
  'expl': 'Abstraction involves hiding implementation details and exposing only essential features '
          'to the user.'},
 {'q': 'If a class `Programmer` inherits from a class `Employee`, what type of inheritance is '
       'this?',
  'code': '',
  'opts': {'A': 'Multiple inheritance',
           'B': 'Multilevel inheritance',
           'C': 'Single inheritance',
           'D': 'Hierarchical inheritance'},
  'ans': 'C',
  'expl': 'Single inheritance occurs when a derived class inherits from exactly one base class.'},
 {'q': 'In the following code, class `C` inherits from `B`, and `B` inherits from `A`. What type '
       'of inheritance is this?',
  'code': 'class B(A):\n    pass\n\nclass C(B):\n    pass',
  'opts': {'A': 'Multiple inheritance',
           'B': 'Hybrid inheritance',
           'C': 'Single inheritance',
           'D': 'Multilevel inheritance'},
  'ans': 'D',
  'expl': 'Multilevel inheritance refers to a class derived from another derived class. Here, C '
          'derives from B, and B derives from A.'},
 {'q': 'What is the primary role of `super()` in Python?',
  'code': '',
  'opts': {'A': 'Deletes parent class',
           'B': 'Accesses methods of the parent class',
           'C': 'Creates loops automatically',
           'D': 'Converts objects into strings'},
  'ans': 'B',
  'expl': 'The super() function returns a proxy object that delegates method calls to a parent or '
          'sibling class, typically used to invoke parent constructors.'},
 {'q': 'Assuming class `B` inherits from class `A` and uses `super()` correctly in its constructor '
       'to initialize the parent class first, what will happen when the following object is '
       'created?',
  'code': 'b = B()',
  'opts': {'A': "Only 'Initializing B' is printed",
           'B': "Only 'Initializing A' is printed",
           'C': "'Initializing A' followed by 'Initializing B' is printed",
           'D': 'Error occurs'},
  'ans': 'C',
  'expl': 'Using super().__init__() in class B invokes the constructor of class A before '
          "proceeding with B's initialization. Thus, 'Initializing A' executes first."},
 {'q': 'What is the technical term for the process of creating a specific object from a defined '
       'class in Python?',
  'code': '',
  'opts': {'A': 'Declaration', 'B': 'Instantiation', 'C': 'Inheritance', 'D': 'Abstraction'},
  'ans': 'B',
  'expl': 'Instantiation is the process of creating an instance, or object, from a class '
          'blueprint. In Python, this is achieved by calling the class name as if it were a '
          'function.'},
 {'q': 'Which syntax is used to access an attribute or method of an object in Python?',
  'code': '',
  'opts': {'A': 'Arrow notation (->)',
           'B': 'Colon notation (:)',
           'C': 'Dot notation (.)',
           'D': 'Bracket notation ([])'},
  'ans': 'C',
  'expl': "Python uses dot notation to access an object's attributes and methods. For example, "
          'object.attribute retrieves the value of the attribute associated with that specific '
          'object.'},
 {'q': 'What keyword is used to define an empty class in Python without causing a syntax error?',
  'code': 'class EmptyClass:\n    ___',
  'opts': {'A': 'continue', 'B': 'break', 'C': 'void', 'D': 'pass'},
  'ans': 'D',
  'expl': 'The pass statement acts as a null operation in Python. It is used as a placeholder when '
          'a statement is syntactically required, such as defining an empty class or function.'},
 {'q': 'Which built-in Python function determines if an object is derived from a specific class?',
  'code': '',
  'opts': {'A': 'istype()', 'B': 'isinstance()', 'C': 'isclass()', 'D': 'type_of()'},
  'ans': 'B',
  'expl': 'The isinstance(object, classinfo) function returns a boolean indicating whether the '
          'specified object is an instance of the provided class or a tuple of classes.'},
 {'q': 'What does the `is` operator evaluate when comparing two object instances in Python?',
  'code': 'class A:\n    pass\n\nobj1 = A()\nobj2 = A()\nprint(obj1 is obj2)',
  'opts': {'A': 'Whether the objects have the same attribute values',
           'B': 'Whether the objects belong to the same class',
           'C': 'Whether the objects occupy the same memory location',
           'D': 'Whether the objects have identical variable names'},
  'ans': 'C',
  'expl': 'The is operator evaluates object identity, meaning it checks if both variables point to '
          'the exact same memory location. Since obj1 and obj2 are instantiated separately, they '
          'occupy different memory locations, resulting in False.'},
 {'q': 'What occurs when an instance method is defined without the `self` parameter, and then '
       'called on an object?',
  'code': "class Test:\n    def display():\n        print('Hello')\n\nt = Test()\nt.display()",
  'opts': {'A': "'Hello' is printed successfully",
           'B': 'A TypeError is raised because an argument is passed implicitly',
           'C': 'A SyntaxError occurs during class definition',
           'D': 'The method executes but returns None implicitly'},
  'ans': 'B',
  'expl': 'When t.display() is called, Python automatically passes the instance t as the first '
          'argument. Since display() was defined to accept zero arguments, a TypeError is raised '
          'indicating that one argument was given but zero were expected.'},
 {'q': "Is it mandatory to use the exact word 'self' to represent the instance in a method "
       'definition?',
  'code': '',
  'opts': {'A': 'Yes, Python will throw a syntax error otherwise',
           'B': 'No, it is merely a strong convention, and any valid identifier can be used',
           'C': "Yes, 'self' is a strictly reserved keyword in Python",
           'D': 'No, the first parameter is always the class itself, not the instance'},
  'ans': 'B',
  'expl': "The identifier 'self' is not a reserved keyword but a strong community convention. Any "
          'valid parameter name in the first position receives the instance reference.'},
 {'q': 'What is the result of executing the following code involving dynamic attribute assignment?',
  'code': 'class Data:\n    pass\n\nd = Data()\nd.value = 42\nprint(d.value)',
  'opts': {'A': 'AttributeError', 'B': '42', 'C': 'None', 'D': 'SyntaxError'},
  'ans': 'B',
  'expl': 'Python allows for dynamic creation of attributes on objects at runtime. Assigning '
          'd.value = 42 successfully creates the value attribute for the specific instance d.'},
 {'q': 'How does Python resolve variable lookup when an object attempts to read an attribute?',
  'code': '',
  'opts': {'A': 'It checks the class namespace first, then the instance namespace',
           'B': 'It checks the global namespace first, then the class namespace',
           'C': 'It checks the instance namespace first, then the class namespace',
           'D': 'It searches only the instance namespace'},
  'ans': 'C',
  'expl': 'When an attribute is accessed via an instance, Python searches the instance namespace '
          'first. If the attribute is not found there, it falls back to the class namespace, and '
          'subsequently follows the method resolution order (MRO).'},
 {'q': 'Which special attribute is used to view the namespace dictionary of a given object in '
       'Python?',
  'code': '',
  'opts': {'A': '__namespace__', 'B': '__dict__', 'C': '__vars__', 'D': '__dir__'},
  'ans': 'B',
  'expl': "The __dict__ attribute contains a dictionary representing the object's local namespace. "
          'It stores all the instance variables and their respective values for that specific '
          'object.'},
 {'q': 'What is the primary difference between the `__new__` and `__init__` methods in Python '
       'class execution?',
  'code': '',
  'opts': {'A': '__new__ deletes an object, while __init__ creates it',
           'B': '__new__ initializes attributes, while __init__ allocates memory',
           'C': '__new__ handles memory allocation and returns the object, while __init__ '
                "initializes the created object's state",
           'D': '__init__ is called before __new__ during instantiation'},
  'ans': 'C',
  'expl': 'In Python, __new__ is a static method responsible for creating and returning a new '
          'instance (memory allocation). __init__ is an instance method called after __new__ to '
          'initialize the attributes of that newly created instance.'},
 {'q': 'What restriction applies to the return value of the `__init__` method?',
  'code': '',
  'opts': {'A': 'It must return the class itself',
           'B': 'It must return an integer',
           'C': 'It must return None',
           'D': "It must return the modified 'self' object"},
  'ans': 'C',
  'expl': "The __init__ method is designed exclusively for initializing an object's state, not for "
          'returning data. Python strictly requires __init__ to return None; returning any other '
          'type results in a TypeError.'},
 {'q': 'What occurs if multiple `__init__` methods are defined within the same Python class?',
  'code': 'class Example:\n'
          '    def __init__(self):\n'
          '        self.a = 1\n'
          '    def __init__(self, val):\n'
          '        self.a = val',
  'opts': {'A': 'Method overloading is achieved, and either can be called based on arguments '
                'passed',
           'B': 'Python throws a SyntaxError during class definition',
           'C': 'The class uses the first defined __init__ and ignores the rest',
           'D': 'The last defined __init__ overrides any previously defined ones'},
  'ans': 'D',
  'expl': 'Python does not support method overloading in the traditional sense. If a method is '
          'defined multiple times, the most recent definition overwrites the previous ones in the '
          'class namespace. Consequently, only the last __init__ is active.'},
 {'q': 'Which special method is invoked when an object is about to be destroyed in Python?',
  'code': '',
  'opts': {'A': '__destroy__()', 'B': '__remove__()', 'C': '__del__()', 'D': '__free__()'},
  'ans': 'C',
  'expl': 'The __del__() method functions as a destructor in Python. It is called by the Python '
          'garbage collector when all references to an object have been deleted, allowing for any '
          'final cleanup tasks.'},
 {'q': 'Analyze the output of the following code involving class and instance variables.',
  'code': 'class Counter:\n'
          '    count = 0\n'
          '\n'
          'c1 = Counter()\n'
          'c2 = Counter()\n'
          'c1.count = 5\n'
          'print(Counter.count, c2.count)',
  'opts': {'A': '5 5', 'B': '0 5', 'C': '0 0', 'D': '5 0'},
  'ans': 'C',
  'expl': 'Assigning c1.count = 5 creates a new instance variable count on the object c1, '
          'shadowing the class variable. The class variable Counter.count remains 0, and since c2 '
          'has no instance variable, c2.count reads the class variable, returning 0.'},
 {'q': 'What is the standard first parameter required in the definition of the `__new__` method?',
  'code': '',
  'opts': {'A': 'self', 'B': 'cls', 'C': 'obj', 'D': 'No parameter is required'},
  'ans': 'B',
  'expl': 'Because __new__ is executed prior to the existence of an instance, it does not receive '
          'self. Instead, it is implicitly a class method and receives the class itself, '
          'conventionally named cls, as its first parameter to allocate memory for that specific '
          'class.'},
 {'q': 'What does the acronym MRO stand for in the context of Python object-oriented programming?',
  'code': '',
  'opts': {'A': 'Memory Randomization Order',
           'B': 'Method Resolution Order',
           'C': 'Module Referencing Object',
           'D': 'Multiple Resolution Output'},
  'ans': 'B',
  'expl': 'MRO stands for Method Resolution Order. It defines the sequence in which Python looks '
          'up methods and attributes in a class hierarchy.'},
 {'q': 'Which algorithm determines the Method Resolution Order (MRO) in Python 3?',
  'code': '',
  'opts': {'A': 'Depth-First Search (DFS)',
           'B': 'Breadth-First Search (BFS)',
           'C': 'C3 Linearization',
           'D': "Dijkstra's Algorithm"},
  'ans': 'C',
  'expl': 'Python 3 uses the C3 Linearization algorithm to establish MRO. This algorithm ensures a '
          'consistent and predictable method lookup order, preserving local precedence ordering '
          'and monotonicity in complex multiple inheritance graphs.'},
 {'q': 'Evaluate the outcome of the following code snippet regarding multiple inheritance.',
  'code': 'class A:\n'
          "    def do(self): return 'A'\n"
          'class B(A):\n'
          "    def do(self): return 'B'\n"
          'class C(A):\n'
          "    def do(self): return 'C'\n"
          'class D(B, C):\n'
          '    pass\n'
          '\n'
          'obj = D()\n'
          'print(obj.do())',
  'opts': {'A': 'A', 'B': 'B', 'C': 'C', 'D': 'Error'},
  'ans': 'B',
  'expl': 'By invoking MRO, Python searches for the do() method starting at D, then to the first '
          'specified parent B, then C, and finally A. The method is found first in B, so it '
          "executes B's version."},
 {'q': 'When using `super()` in a multiple inheritance structure, what class does it delegate '
       'method calls to?',
  'code': '',
  'opts': {'A': 'Always the direct primary parent class',
           'B': 'The root object class',
           'C': 'The next class in the Method Resolution Order (MRO)',
           'D': 'All parent classes simultaneously'},
  'ans': 'C',
  'expl': 'super() does not simply refer to a parent class. It evaluates the MRO of the calling '
          "object's class and delegates the method call to the next class appearing in that linear "
          'sequence.'}]


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