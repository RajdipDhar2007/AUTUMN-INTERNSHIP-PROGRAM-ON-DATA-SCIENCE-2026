#!/usr/bin/env python3
"""
IDEAS TIH Quiz Autumn 26 - Python Basics 9 - interactive terminal quiz
---------------------------------------------------------------
Run:   python python_basics_9_quiz.py

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

TITLE = "IDEAS TIH Quiz Autumn 26 - Python Basics 9"
TIME_LIMIT = 60 * 60          # seconds
OPTION_KEYS = ("A", "B", "C", "D")

QUESTIONS = [{'q': "Which principle describes an interface's ability to process objects of different classes "
       'that implement the same method name?',
  'code': '',
  'opts': {'A': 'Encapsulation', 'B': 'Abstraction', 'C': 'Polymorphism', 'D': 'Instantiation'},
  'ans': 'C',
  'expl': 'Polymorphism allows functions or methods to operate on objects of different types, '
          'provided those objects implement the expected interface or method signatures.'},
 {'q': 'What concept is applied when a child class provides a distinct implementation for a method '
       'already defined in its parent class?',
  'code': '',
  'opts': {'A': 'Method Overloading',
           'B': 'Method Overriding',
           'C': 'Method Casting',
           'D': 'Operator Overloading'},
  'ans': 'B',
  'expl': 'Method overriding occurs when a subclass defines a method with the same name as one in '
          "its superclass, thereby replacing the superclass's behavior with its own specific "
          'implementation.'},
 {'q': "What programming style is best described by the phrase 'If it walks like a duck and quacks "
       "like a duck, it must be a duck'?",
  'code': '',
  'opts': {'A': 'Static Typing', 'B': 'Strong Typing', 'C': 'Duck Typing', 'D': 'Nominal Typing'},
  'ans': 'C',
  'expl': "Duck typing is a dynamic typing concept in Python where an object's suitability is "
          'determined by the presence of certain methods and properties, rather than its exact '
          'class inheritance hierarchy.'},
 {'q': 'Assuming `Parent` is a base class and `Child` inherits from it overriding method '
       '`action()`. How can an instance of `Child` explicitly call the `Parent` version of '
       '`action()` without using `super()`?',
  'code': '',
  'opts': {'A': 'Parent.action()',
           'B': 'self.Parent.action()',
           'C': 'Parent.action(self)',
           'D': 'action(Parent)'},
  'ans': 'C',
  'expl': 'You can explicitly call an unbound method from a class by providing the instance as the '
          "first parameter manually. In this case, Parent.action(self) executes the parent's logic "
          "on the child's instance data."},
 {'q': 'Which Python function determines whether a class is a derived descendant of another class?',
  'code': '',
  'opts': {'A': 'issubclass()', 'B': 'ischild()', 'C': 'hasparent()', 'D': 'inherits()'},
  'ans': 'A',
  'expl': 'The issubclass(class, classinfo) function returns True if the first parameter is a '
          'subclass (direct, indirect, or virtual) of the class information provided in the second '
          'parameter.'},
 {'q': 'What is the standard name for the first parameter of a method decorated with '
       '`@classmethod`?',
  'code': '',
  'opts': {'A': 'self', 'B': 'cls', 'C': 'static', 'D': 'obj'},
  'ans': 'B',
  'expl': 'A class method modifies the class state rather than the instance state. It implicitly '
          'receives the class itself as the first parameter, conventionally named cls.'},
 {'q': 'Which of the following is true regarding a method decorated with `@staticmethod`?',
  'code': '',
  'opts': {'A': "It automatically receives 'self' as the first parameter",
           'B': "It automatically receives 'cls' as the first parameter",
           'C': 'It does not receive an implicit first parameter',
           'D': 'It cannot accept any parameters at all'},
  'ans': 'C',
  'expl': 'A static method acts essentially as a regular function that happens to reside in a '
          "class's namespace. It receives neither self nor cls implicitly, allowing it to process "
          'data independent of class or instance states.'},
 {'q': 'A factory method used to instantiate an object from alternative input formats is typically '
       'implemented as which type of method?',
  'code': '',
  'opts': {'A': 'Instance method', 'B': 'Class method', 'C': 'Static method', 'D': 'Magic method'},
  'ans': 'B',
  'expl': 'Class methods are frequently used as alternative constructors (factory methods) because '
          'they receive the class cls as an argument. This allows them to parse alternative inputs '
          'and return a new instance of the class by calling cls(...).'},
 {'q': "What does the `getattr(obj, 'name', 'default')` function return if the attribute 'name' "
       "does not exist on 'obj'?",
  'code': '',
  'opts': {'A': 'It raises an AttributeError',
           'B': 'It returns None',
           'C': "It returns the string 'default'",
           'D': 'It raises a KeyError'},
  'ans': 'C',
  'expl': 'The built-in function getattr() attempts to retrieve the value of a named attribute '
          'from an object. If the attribute is absent, it returns the provided default value (in '
          "this case, 'default') instead of raising an AttributeError."},
 {'q': 'Which function allows a programmer to verify if an object contains a specific attribute '
       'dynamically at runtime?',
  'code': '',
  'opts': {'A': 'contains()', 'B': 'checkattr()', 'C': 'hasattr()', 'D': 'isattr()'},
  'ans': 'C',
  'expl': "The hasattr(object, name) function evaluates whether the string parameter 'name' "
          'represents an existing attribute of the given object, returning True or False.'},
 {'q': 'In Python, prefixing an attribute name with a single underscore (e.g., `_value`) indicates '
       'what to the programmer?',
  'code': '',
  'opts': {'A': 'The attribute is strictly inaccessible from outside the class',
           'B': 'The attribute is a protected member intended for internal use only',
           'C': 'The attribute undergoes name mangling',
           'D': 'The attribute represents a static variable'},
  'ans': 'B',
  'expl': 'A single underscore prefix is a Python community convention signifying that an '
          "attribute or method is 'protected' and intended for internal operations. It does not "
          'enforce strict access control at the language level.'},
 {'q': 'What mechanism does Python employ when an attribute is prefixed with double underscores '
       '(e.g., `__data`)?',
  'code': '',
  'opts': {'A': 'Data Encryption',
           'B': 'Strict Type Checking',
           'C': 'Name Mangling',
           'D': 'Garbage Collection Lock'},
  'ans': 'C',
  'expl': 'Prefixing an attribute with double underscores triggers name mangling in Python. The '
          'interpreter alters the attribute name to include the class name, reducing the '
          'likelihood of accidental overriding by subclasses.'},
 {'q': 'Given a class named `Vault` with an attribute `__code = 1234`, what is the internally '
       'mangled name of this attribute?',
  'code': 'class Vault:\n    def __init__(self):\n        self.__code = 1234',
  'opts': {'A': '__Vault_code', 'B': '_Vault__code', 'C': 'Vault__code', 'D': '__code_Vault'},
  'ans': 'B',
  'expl': 'During name mangling, Python prepends a single underscore followed by the class name to '
          'the original double-underscored attribute name. Thus, __code inside class Vault becomes '
          '_Vault__code.'},
 {'q': "What is the primary technical rationale for Python's name mangling mechanism?",
  'code': '',
  'opts': {'A': 'To enforce absolute security preventing external access',
           'B': 'To optimize attribute lookup speed at runtime',
           'C': 'To avoid naming collisions between attributes of parent and child classes',
           'D': 'To encrypt sensitive data stored in memory'},
  'ans': 'C',
  'expl': 'Name mangling is not designed as a security measure. Its primary purpose is to ensure '
          'that subclass attributes do not accidentally shadow or overwrite parent class '
          'attributes that share the same name.'},
 {'q': 'How can a developer externally read the value of a mangled attribute `__secret` from an '
       'instance `obj` of class `Box`?',
  'code': '',
  'opts': {'A': 'obj.__secret',
           'B': 'obj._Box__secret',
           'C': 'Box.__secret(obj)',
           'D': "getattr(obj, '__secret')"},
  'ans': 'B',
  'expl': 'Because Python does not enforce strict privacy, a mangled variable can still be '
          'accessed externally by using its mangled name. For an instance of Box, the syntax '
          'obj._Box__secret retrieves the data.'},
 {'q': 'Which module and base class must be imported to properly define an abstract base class in '
       'Python?',
  'code': '',
  'opts': {'A': 'import abstract and inherit from abstract.Base',
           'B': 'from interface import Interface',
           'C': 'from abc import ABC',
           'D': 'import typing and inherit from typing.Abstract'},
  'ans': 'C',
  'expl': 'To create formal abstract classes in Python, a class must inherit from ABC (Abstract '
          'Base Class), which is provided by the built-in abc module.'},
 {'q': 'What error is raised if a program attempts to instantiate a class that inherits from `ABC` '
       'and contains at least one `@abstractmethod`?',
  'code': 'from abc import ABC, abstractmethod\n'
          'class Shape(ABC):\n'
          '    @abstractmethod\n'
          '    def area(self): pass\n'
          '\n'
          's = Shape()',
  'opts': {'A': 'SyntaxError', 'B': 'ValueError', 'C': 'TypeError', 'D': 'NotImplementedError'},
  'ans': 'C',
  'expl': 'Python prevents the instantiation of a class possessing abstract methods. Doing so '
          'triggers a TypeError, stating that abstract methods have not been implemented.'},
 {'q': 'What must a subclass do to be instantiated if it inherits from an abstract base class with '
       'multiple abstract methods?',
  'code': '',
  'opts': {'A': 'Call super().__init__()',
           'B': 'Provide concrete implementations for every inherited abstract method',
           'C': 'Provide a concrete implementation for at least one abstract method',
           'D': 'Define itself as an abstract base class using ABC'},
  'ans': 'B',
  'expl': 'A subclass must override and implement all abstract methods defined in its parent '
          'class. If even a single abstract method is omitted, the subclass remains abstract and '
          'cannot be instantiated.'},
 {'q': 'What is the primary utility of the `@property` decorator in Python class design?',
  'code': '',
  'opts': {'A': 'To declare class-level static attributes',
           'B': 'To evaluate mathematical properties of variables',
           'C': 'To permit method calls without parentheses, simulating attribute access',
           'D': 'To prevent inheritance of specific variables'},
  'ans': 'C',
  'expl': 'The @property decorator converts a class method into a read-only property, enabling '
          'attribute access notation without parentheses while retaining method logic.'},
 {'q': 'To define a setter function for a property previously established as `@property def '
       'temperature(self):`, which decorator must be utilized?',
  'code': '',
  'opts': {'A': '@set_temperature',
           'B': '@temperature.setter',
           'C': '@property.set',
           'D': '@setter(temperature)'},
  'ans': 'B',
  'expl': 'Python syntax requires that the setter decorator matches the name of the established '
          'property method followed by .setter. Therefore, @temperature.setter binds the '
          'assignment operation to the corresponding method.'},
 {'q': 'What distinguishes the `__str__` method from the `__repr__` method concerning object '
       'representation?',
  'code': '',
  'opts': {'A': '__str__ returns memory addresses; __repr__ returns object data',
           'B': '__str__ is intended for end-user readability; __repr__ is intended for '
                'unambiguous debugging',
           'C': '__str__ returns lists; __repr__ returns strings',
           'D': '__str__ cannot be overridden; __repr__ can be overridden'},
  'ans': 'B',
  'expl': 'The __str__ method provides a readable string representation for end-users. The '
          '__repr__ method provides an unambiguous string representation intended for debugging.'},
 {'q': 'Which magic method must be implemented to allow two custom objects to be combined using '
       'the addition operator `+`?',
  'code': '',
  'opts': {'A': '__plus__()', 'B': '__concat__()', 'C': '__sum__()', 'D': '__add__()'},
  'ans': 'D',
  'expl': "Operator overloading in Python relies on specific 'dunder' (double underscore) methods. "
          'The + operator maps directly to the __add__(self, other) method, enabling arithmetic '
          'logic between custom objects.'},
 {'q': 'To define custom logic for testing equality between two instances (using `==`), which '
       'method requires overriding?',
  'code': '',
  'opts': {'A': '__equals__()', 'B': '__eq__()', 'C': '__comp__()', 'D': '__is__()'},
  'ans': 'B',
  'expl': 'The equality operator == invokes the __eq__(self, other) method. Overriding this method '
          'allows instances to be compared based on attribute values rather than distinct memory '
          'addresses.'},
 {'q': 'What constraint applies when overriding the `__len__` method for a custom class?',
  'code': '',
  'opts': {'A': 'It must return a boolean',
           'B': 'It must return a floating-point number',
           'C': 'It must return an integer greater than or equal to zero',
           'D': "It cannot accept the 'self' parameter"},
  'ans': 'C',
  'expl': 'The __len__() method must emulate sequence length. Python strictly mandates that '
          '__len__ return a non-negative integer. Returning a string, float, or negative integer '
          'raises a TypeError or ValueError.'},
 {'q': 'Which magic method enables an instance of a class to be executed as if it were a function '
       '`obj()`?',
  'code': '',
  'opts': {'A': '__func__()', 'B': '__call__()', 'C': '__exec__()', 'D': '__invoke__()'},
  'ans': 'B',
  'expl': 'Defining the __call__(self, *args, **kwargs) method in a class causes its instances to '
          'become callable. This allows the object to maintain state while functioning '
          'syntactically like a standard method.'},
 {'q': "In class design, 'Inheritance' represents an 'is-a' relationship. What type of "
       "relationship does 'Composition' represent?",
  'code': '',
  'opts': {'A': 'is-a-type-of', 'B': 'has-a', 'C': 'inherits-from', 'D': 'acts-as'},
  'ans': 'B',
  'expl': "Composition denotes a 'has-a' relationship, where a class incorporates instances of "
          'other classes as attributes.'},
 {'q': 'What is the principal architectural benefit of defining `__slots__` within a Python class?',
  'code': '',
  'opts': {'A': 'It encrypts variable contents automatically',
           'B': 'It enables dynamic multiple inheritance paths',
           'C': 'It conserves memory by preventing the creation of an instance dictionary',
           'D': 'It grants the class access to standard C libraries'},
  'ans': 'C',
  'expl': 'Declaring __slots__ explicitly restricts the attributes an object can possess. This '
          'eliminates the dynamic __dict__ for instances, reducing memory overhead.'},
 {'q': "When a class establishes `__slots__ = ['name', 'age']`, what happens if a script assigns a "
       "new attribute `obj.address = 'London'`?",
  'code': '',
  'opts': {'A': 'The assignment is ignored silently',
           'B': 'An AttributeError is raised immediately',
           'C': "The attribute 'address' is added to the slots dynamically",
           'D': "A new __dict__ is created to hold the 'address' attribute"},
  'ans': 'B',
  'expl': 'Because __slots__ explicitly restricts the attributes an instance can have and disables '
          'the fallback __dict__, attempting to assign an undeclared attribute results directly in '
          'an AttributeError.'},
 {'q': 'If a parent class utilizes `__slots__`, but its child class does not declare `__slots__`, '
       'how does memory allocation behave for the child class instances?',
  'code': '',
  'opts': {'A': 'The child instances cannot have a __dict__ and rely solely on parent slots',
           'B': 'The child instances automatically generate an instance __dict__, nullifying '
                'memory savings',
           'C': 'A syntax error is raised preventing the inheritance',
           'D': 'The child instances inherit __slots__ strictly and cannot add variables'},
  'ans': 'B',
  'expl': 'A subclass does not automatically inherit the strict memory limits of __slots__ if it '
          'does not explicitly define its own. Consequently, it generates a standard __dict__, '
          "eliminating the memory optimization provided by the parent's __slots__."},
 {'q': 'In standard Python, what built-in class serves as the default metaclass responsible for '
       'defining the behavior of classes themselves?',
  'code': '',
  'opts': {'A': 'object', 'B': 'class', 'C': 'meta', 'D': 'type'},
  'ans': 'D',
  'expl': 'While classes define the behavior of objects, metaclasses define the behavior of '
          'classes. By default, every class in Python is an instance of the built-in metaclass '
          'type.'}]


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