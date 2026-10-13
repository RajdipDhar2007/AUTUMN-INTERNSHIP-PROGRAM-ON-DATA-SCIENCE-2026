#!/usr/bin/env python3
"""
IDEAS TIH Quiz Autumn 26 - Python Basics 7 - interactive terminal quiz
---------------------------------------------------------------
Run:   python python_basics_7_quiz.py

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

TITLE = "IDEAS TIH Quiz Autumn 26 - Python Basics 7"
TIME_LIMIT = 60 * 60          # seconds
OPTION_KEYS = ("A", "B", "C", "D")

QUESTIONS = [{'q': 'What is one major advantage of NumPy?',
  'code': '',
  'opts': {'A': 'It uses more memory',
           'B': 'It is slower than lists',
           'C': 'It provides efficient storage and faster computation',
           'D': 'It only works with integers'},
  'ans': 'C',
  'expl': 'NumPy arrays are stored at contiguous memory locations, unlike Python lists. This '
          'allows for efficient memory usage and faster computational execution, especially for '
          'vector operations and mathematical processing.'},
 {'q': 'What will be the datatype of the following NumPy array?',
  'code': "np.array([1, 2.87, 'IDEAS-TIH', 4])",
  'opts': {'A': 'int32', 'B': 'float64', 'C': 'object/string type', 'D': 'bool'},
  'ans': 'C',
  'expl': 'NumPy arrays are homogeneous, meaning they can only hold a single data type. When mixed '
          'data types are provided (integer, float, and string), NumPy upcasts all the elements to '
          'the most inclusive data type, which in this case is a string (often represented as an '
          'object or <U string type).'},
 {'q': 'What is the shape of the following array?',
  'code': 'np.array([[3,4,5,6],[3,4,5,6]])',
  'opts': {'A': '(4, 2)', 'B': '(2, 4)', 'C': '(2, 2)', 'D': '(4, )'},
  'ans': 'B',
  'expl': 'The given array is a two-dimensional matrix. It has 2 rows and 4 columns. In NumPy, '
          'shape is represented as a tuple of (rows, columns). Thus, its shape is (2, 4).'},
 {'q': 'What does `np.linspace(1,5,10)` generate?',
  'code': '',
  'opts': {'A': '10 random integers',
           'B': 'Integers from 1 to 5',
           'C': '10 equally spaced values between 1 and 5',
           'D': 'A matrix of size 10 x 10'},
  'ans': 'C',
  'expl': 'The np.linspace(start, stop, num) function in NumPy generates num evenly spaced '
          'numerical values over the interval [start, stop]. Therefore, it will return 10 equally '
          'spaced floating-point values starting from 1 up to 5.'},
 {'q': 'What is the purpose of `flatten()` in NumPy?',
  'code': '',
  'opts': {'A': 'Sorts the array',
           'B': 'Converts multi-dimensional array into 1D array',
           'C': 'Finds determinant',
           'D': 'Removes duplicate elements'},
  'ans': 'B',
  'expl': 'The flatten() method in NumPy is used to collapse a multi-dimensional array into a '
          'single-dimensional (1D) array, laying out all the elements in a contiguous sequence '
          'without changing their data.'},
 {'q': 'Which function is used to compute matrix multiplication in NumPy?',
  'code': '',
  'opts': {'A': 'np.add()', 'B': 'np.matmul()', 'C': 'np.flatten()', 'D': 'np.where()'},
  'ans': 'B',
  'expl': 'The np.matmul() function is used to perform matrix multiplication on two arrays. '
          'Additionally, in modern Python, the @ operator can also be used as a shorthand for this '
          'function.'},
 {'q': 'What does `np.where(ar1 > 5)` return?',
  'code': '',
  'opts': {'A': 'Values greater than 5',
           'B': 'Sum of values greater than 5',
           'C': 'Indices where elements are greater than 5',
           'D': 'Sorted array'},
  'ans': 'C',
  'expl': "When np.where() is called with only a condition (no 'x' and 'y' replacements), it "
          'returns a tuple of arrays detailing the index positions of the elements that satisfy '
          'the given condition.'},
 {'q': 'Which Pandas function is used to read a CSV file?',
  'code': '',
  'opts': {'A': 'pd.open_csv()', 'B': 'pd.read_csv()', 'C': 'pd.load_csv()', 'D': 'pd.csv_read()'},
  'ans': 'B',
  'expl': 'The pd.read_csv() function is the standard Pandas method used to ingest comma-separated '
          'values (CSV) files and convert them into a Pandas DataFrame.'},
 {'q': 'What is the purpose of `reset_index(drop=True)` in a Pandas DataFrame?',
  'code': '',
  'opts': {'A': 'Deletes the dataframe',
           'B': 'Resets index without keeping old index as a column',
           'C': 'Sorts the dataframe',
           'D': 'Removes duplicate rows'},
  'ans': 'B',
  'expl': 'By default, reset_index() moves the old index into a new column in the DataFrame to '
          'save it. When drop=True is provided, Pandas discards the previous index and replaces it '
          'with a default sequential integer index without creating a new column.'},
 {'q': 'Which statement correctly describes `loc` in Pandas?',
  'code': '',
  'opts': {'A': 'It accesses rows and columns using labels',
           'B': 'It performs matrix multiplication',
           'C': 'It converts dataframe into NumPy array',
           'D': 'It removes missing values'},
  'ans': 'A',
  'expl': 'The .loc property is used for label-based indexing in Pandas. It allows for the '
          'selection of specific rows and columns by providing their label names, unlike .iloc '
          'which uses integer positions.'},
 {'q': 'What is the primary difference between `np.zeros()` and `np.empty()` in NumPy?',
  'code': '',
  'opts': {'A': 'np.empty() initializes the array with zeros, while np.zeros() leaves elements '
                'uninitialized',
           'B': 'np.zeros() allocates memory and initializes it to zero, while np.empty() '
                'allocates memory without initializing entries',
           'C': 'Both functions are identical in execution and memory allocation',
           'D': 'np.empty() creates a string array, whereas np.zeros() creates a float array'},
  'ans': 'B',
  'expl': 'The function np.zeros() allocates memory for an array and initializes every element to '
          'zero. In contrast, np.empty() allocates the requested memory but does not initialize '
          'the elements, resulting in the array containing arbitrary values previously stored at '
          'those memory addresses. This makes np.empty() slightly faster when the array will be '
          'overwritten immediately.'},
 {'q': 'What is the primary data structure used by Pandas to represent a one-dimensional labeled '
       'array?',
  'code': '',
  'opts': {'A': 'DataFrame', 'B': 'Array', 'C': 'Series', 'D': 'Matrix'},
  'ans': 'C',
  'expl': 'A Pandas Series is a one-dimensional labeled array capable of holding data of any type '
          '(integer, string, float, python objects, etc.). A DataFrame is a two-dimensional data '
          'structure.'},
 {'q': 'By default, how many rows are returned when executing the `df.head()` function on a Pandas '
       'DataFrame?',
  'code': '',
  'opts': {'A': '1', 'B': '5', 'C': '10', 'D': 'All rows'},
  'ans': 'B',
  'expl': 'The head(n) function in Pandas is used to return the first n rows of a DataFrame or '
          'Series. If the parameter n is not specified, it defaults to returning 5 rows.'},
 {'q': 'What is the expected output type of the `.shape` attribute of a NumPy array?',
  'code': '',
  'opts': {'A': 'List', 'B': 'Integer', 'C': 'Tuple', 'D': 'Dictionary'},
  'ans': 'C',
  'expl': 'The .shape attribute of a NumPy array returns a tuple of integers representing the size '
          'of the array in each dimension.'},
 {'q': 'Which NumPy attribute is used to determine the number of dimensions (axes) of an array?',
  'code': '',
  'opts': {'A': '.size', 'B': '.ndim', 'C': '.shape', 'D': '.itemsize'},
  'ans': 'B',
  'expl': 'The .ndim attribute returns an integer that indicates the number of dimensions, or '
          'axes, of the NumPy array. For example, a 2D matrix will return 2.'},
 {'q': 'What does the `describe()` function in Pandas primarily generate?',
  'code': '',
  'opts': {'A': 'A list of all column names and data types',
           'B': 'Descriptive statistics including count, mean, standard deviation, and percentiles',
           'C': 'The memory usage of the DataFrame',
           'D': 'A visual plot of the DataFrame contents'},
  'ans': 'B',
  'expl': 'The describe() method generates descriptive statistics that summarize the central '
          "tendency, dispersion, and shape of a dataset's distribution, excluding NaN values. By "
          'default, it operates on numeric columns.'},
 {'q': 'Which Pandas function is utilized to replace missing (NaN) values with a specified value?',
  'code': '',
  'opts': {'A': 'dropna()', 'B': 'replace_na()', 'C': 'fillna()', 'D': 'isnull()'},
  'ans': 'C',
  'expl': 'The fillna() function in Pandas is used to replace NULL or NaN values with a specific '
          'constant, or by using a filling strategy like forward fill or backward fill.'},
 {'q': 'How does `np.arange(0, 10, 2)` differ from `np.linspace(0, 10, 2)`?',
  'code': '',
  'opts': {'A': 'arange specifies the step size, while linspace specifies the number of output '
                'samples',
           'B': 'arange generates floating-point numbers, while linspace generates integers',
           'C': 'arange is inclusive of the endpoint, while linspace is exclusive of the endpoint',
           'D': 'There is no difference; both produce the same array'},
  'ans': 'A',
  'expl': 'np.arange(start, stop, step) generates values based on a fixed step size. '
          'np.linspace(start, stop, num) generates num evenly spaced values between the start and '
          'stop boundaries.'},
 {'q': 'Which property of a DataFrame returns an Index object containing the names of the columns?',
  'code': '',
  'opts': {'A': 'df.names', 'B': 'df.columns', 'C': 'df.keys', 'D': 'df.headers'},
  'ans': 'B',
  'expl': 'The .columns attribute of a Pandas DataFrame returns the column labels as an Index '
          'object. It does not require parentheses because it is a property, not a method.'},
 {'q': 'Which function determines the maximum value present within an entire NumPy array?',
  'code': '',
  'opts': {'A': 'np.highest()', 'B': 'np.peak()', 'C': 'np.max()', 'D': 'np.argmax()'},
  'ans': 'C',
  'expl': 'The np.max() function evaluates all elements in an array and returns the largest scalar '
          'value. np.argmax() returns the index of the maximum value, not the value itself.'},
 {'q': "To delete a column named 'Age' from a DataFrame `df`, which parameter configuration is "
       'necessary when using the `drop()` method?',
  'code': '',
  'opts': {'A': "df.drop('Age', axis=0)",
           'B': "df.drop('Age', axis=1)",
           'C': 'df.drop(columns=False)',
           'D': "df.delete('Age')"},
  'ans': 'B',
  'expl': 'The drop() method removes rows or columns by specifying label names and corresponding '
          'axis. axis=1 refers to columns, whereas axis=0 refers to rows. Thus, axis=1 is required '
          'to drop a column.'},
 {'q': 'What does the acronym NaN denote within the Pandas library?',
  'code': '',
  'opts': {'A': 'Not a Noun',
           'B': 'Not a Number',
           'C': 'Null and Null',
           'D': 'Negative and Neutral'},
  'ans': 'B',
  'expl': "NaN stands for 'Not a Number'. It is the standard missing data marker used in pandas, "
          'inherited from the floating-point standard IEEE 754.'},
 {'q': 'When adding a scalar value of 5 to a NumPy array of shape (3, 3), what occurs during the '
       'operation?',
  'code': '',
  'opts': {'A': 'A ValueError is raised due to mismatched shapes',
           'B': 'The scalar is added only to the first element of the array',
           'C': 'The scalar is broadcast across the array, adding 5 to every element',
           'D': 'The scalar is added only to the diagonal elements'},
  'ans': 'C',
  'expl': 'Broadcasting is a mechanism in NumPy that allows arithmetic operations between arrays '
          'of different shapes. When an operation involves a scalar and an array, the scalar is '
          'logically expanded (broadcast) to match the shape of the array, meaning the operation '
          'is applied element-wise.'},
 {'q': 'What will be the output of the code snippet provided?',
  'code': 'import pandas as pd\n'
          "data = {'A': [10, 20, 30], 'B': [40, 50, 60]}\n"
          'df = pd.DataFrame(data)\n'
          'print(df.iloc[1, 0])',
  'opts': {'A': '10', 'B': '20', 'C': '40', 'D': '50'},
  'ans': 'B',
  'expl': 'The .iloc indexer is used for integer-location based indexing. df.iloc[1, 0] requests '
          'the value at row index 1 and column index 0. Row 1 corresponds to the second row '
          "(values 20, 50), and column 0 corresponds to column 'A'. Thus, the value is 20."},
 {'q': 'In the context of the NumPy `reshape()` function, what is the effect of providing `-1` as '
       'one of the dimension sizes?',
  'code': 'arr = np.arange(12)\nnew_arr = arr.reshape(-1, 3)',
  'opts': {'A': 'It reverses the order of the elements in that dimension',
           'B': 'It raises a syntax error because dimensions must be positive integers',
           'C': 'NumPy automatically calculates the size of that dimension based on the array '
                'length and other provided dimensions',
           'D': 'It removes that dimension, effectively flattening the array'},
  'ans': 'C',
  'expl': 'When reshaping an array, providing -1 acts as a placeholder. NumPy infers the correct '
          'dimension size by dividing the total number of elements by the product of the '
          'explicitly specified dimensions. In the provided snippet, an array of length 12 '
          'reshaped to (-1, 3) will result in a shape of (4, 3).'},
 {'q': 'What does the `value_counts()` method return when applied to a Pandas Series?',
  'code': '',
  'opts': {'A': 'The total sum of all numerical values in the Series',
           'B': 'A Series containing counts of unique values, arranged in descending order of '
                'frequency',
           'C': 'A boolean mask identifying duplicated values',
           'D': 'A random sample of values from the Series'},
  'ans': 'B',
  'expl': 'The value_counts() method evaluates a Series and returns an object containing the '
          'frequencies of each unique value. By default, the output is sorted in descending order '
          'so that the most frequent element appears first.'},
 {'q': 'What is the difference between `np.concatenate((a, b), axis=0)` and `np.vstack((a, b))` '
       'when `a` and `b` are 2D arrays of compatible shapes?',
  'code': '',
  'opts': {'A': 'np.concatenate stacks arrays horizontally, while np.vstack stacks them vertically',
           'B': 'np.vstack is faster because it does not allocate memory',
           'C': 'There is no difference; they produce the same result for 2D arrays',
           'D': 'np.vstack only works on 1D arrays, while np.concatenate works on any dimension'},
  'ans': 'C',
  'expl': 'For two-dimensional arrays, np.vstack is a wrapper that performs concatenation along '
          'the first axis (axis=0). Therefore, both function calls yield the same combined array.'},
 {'q': 'Which type of join is executed by default when using the `pd.merge()` function on two '
       'DataFrames?',
  'code': '',
  'opts': {'A': 'Left join', 'B': 'Right join', 'C': 'Outer join', 'D': 'Inner join'},
  'ans': 'D',
  'expl': "By default, pd.merge() performs an inner join (specified by the how='inner' argument). "
          'This means only rows with matching key values in both DataFrames will be included in '
          'the output DataFrame.'},
 {'q': 'What does the syntax `arr[1, :]` denote when operating on a two-dimensional NumPy array?',
  'code': '',
  'opts': {'A': 'It extracts the element at row index 1 and column index 1',
           'B': 'It extracts the entire second row (index 1) across all columns',
           'C': 'It extracts the entire second column (index 1) across all rows',
           'D': 'It deletes the row at index 1'},
  'ans': 'B',
  'expl': 'In NumPy indexing, elements are accessed using a comma-separated tuple of indices. The '
          'first argument specifies the row and the second specifies the column. 1 targets the row '
          "at index 1, and : (colon) acts as a slice representing 'all elements'. Therefore, "
          'arr[1, :] selects all columns for row index 1.'},
 {'q': 'What distribution is used to generate values when calling `np.random.randn(5)`?',
  'code': '',
  'opts': {'A': 'Standard normal distribution (mean 0, variance 1)',
           'B': 'Uniform distribution over the interval [0, 1)',
           'C': 'Uniform distribution over the interval [0, 5)',
           'D': 'Poisson distribution with lambda 5'},
  'ans': 'A',
  'expl': "The function np.random.randn() returns a sample (or samples) from the 'standard normal' "
          'distribution, which is a Gaussian distribution centered at zero with a standard '
          'deviation of 1. Conversely, np.random.rand() generates numbers from a uniform '
          'distribution over [0, 1).'}]


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