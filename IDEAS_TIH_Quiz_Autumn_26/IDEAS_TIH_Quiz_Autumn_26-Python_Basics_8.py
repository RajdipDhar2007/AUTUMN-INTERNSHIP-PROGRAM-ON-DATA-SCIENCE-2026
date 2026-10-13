#!/usr/bin/env python3
"""
IDEAS TIH Quiz Autumn 26 - Python Basics 8 - interactive terminal quiz
---------------------------------------------------------------
Run:   python python_basics_8_quiz.py

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

TITLE = "IDEAS TIH Quiz Autumn 26 - Python Basics 8"
TIME_LIMIT = 60 * 60          # seconds
OPTION_KEYS = ("A", "B", "C", "D")

QUESTIONS = [{'q': 'Which operation correctly filters a DataFrame `df` to include only rows where the value in '
       "column 'Age' is greater than 30?",
  'code': '',
  'opts': {'A': "df.filter('Age' > 30)",
           'B': "df[df['Age'] > 30]",
           'C': 'df.query(Age > 30)',
           'D': 'df.where(Age > 30)'},
  'ans': 'B',
  'expl': "Pandas supports boolean indexing. The expression df['Age'] > 30 creates a boolean "
          'Series of True/False values. Wrapping this inside the DataFrame indexing bracket '
          'df[...] returns only the rows that evaluate to True.'},
 {'q': 'What does the function `np.argmax(arr)` return when applied to a flattened numerical '
       'array?',
  'code': '',
  'opts': {'A': 'The maximum value in the array',
           'B': 'The index of the maximum value in the array',
           'C': 'A boolean array indicating the locations of the maximum value',
           'D': 'The index of the minimum value in the array'},
  'ans': 'B',
  'expl': 'The np.argmax() function computes the maximum value across the specified axis and '
          'returns the index position of that maximum value. If no axis is specified, the array is '
          'implicitly flattened before evaluation.'},
 {'q': 'What does executing `df.dropna(axis=1)` accomplish?',
  'code': '',
  'opts': {'A': 'It removes all rows containing at least one missing value (NaN)',
           'B': 'It removes all columns containing at least one missing value (NaN)',
           'C': 'It drops all columns that contain only numerical data',
           'D': 'It replaces all missing values with a default integer'},
  'ans': 'B',
  'expl': 'The dropna() method is used to remove missing values. Specifying axis=1 (or '
          "axis='columns') instructs Pandas to drop entire columns that contain one or more NaN "
          'values. Default behavior (axis=0) drops rows.'},
 {'q': 'Which function provides a mechanism to apply a custom Python function along a specific '
       'axis of a DataFrame?',
  'code': '',
  'opts': {'A': 'transform()', 'B': 'map()', 'C': 'apply()', 'D': 'evaluate()'},
  'ans': 'C',
  'expl': 'The apply() function in Pandas takes an arbitrary function as an argument and applies '
          'it along an axis of the DataFrame (either rows or columns). While map() is used for '
          'element-wise mapping on a Series, apply() operates on entire rows or columns.'},
 {'q': 'According to NumPy broadcasting rules, if array `A` has shape (3, 1) and array `B` has '
       'shape (1, 4), what will be the shape of the resulting array `C` when performing `C = A + '
       'B`?',
  'code': '',
  'opts': {'A': '(3, 1)',
           'B': '(1, 4)',
           'C': '(3, 4)',
           'D': 'The operation throws a ValueError due to mismatched shapes'},
  'ans': 'C',
  'expl': 'NumPy compares array shapes element-wise, starting from the trailing dimensions. Two '
          'dimensions are compatible if they are equal, or if one of them is 1. Here, the row '
          'dimension is max(3, 1) = 3 and the column dimension is max(1, 4) = 4. Both arrays '
          'broadcast to shape (3, 4) before the addition.'},
 {'q': "Consider a DataFrame `df` with columns 'Category' and 'Values'. What does the operation "
       "`df.groupby('Category')['Values'].sum()` produce?",
  'code': '',
  'opts': {'A': "A DataFrame summarizing the sum of all columns grouped by 'Category'",
           'B': "A scalar value representing the total sum of 'Values'",
           'C': 'A Series where the index is the unique categories and values are the sum of '
                "'Values' for each category",
           'D': "A Series containing the cumulative sum of the 'Values' column"},
  'ans': 'C',
  'expl': "The groupby('Category') method partitions the DataFrame. Selecting ['Values'] isolates "
          'that specific column as a SeriesGroupBy object. Applying .sum() aggregates these '
          'partitions. The final output is a Pandas Series indexed by the unique elements of '
          "'Category'."},
 {'q': 'What is the outcome of the provided boolean indexing operation on the NumPy array?',
  'code': 'import numpy as np\narr = np.array([1, 2, 3, 4, 5])\narr[arr % 2 == 0] = 0\nprint(arr)',
  'opts': {'A': '[0 0 3 0 5]', 'B': '[1 0 3 0 5]', 'C': '[0 2 0 4 0]', 'D': '[1 2 3 4 5]'},
  'ans': 'B',
  'expl': 'The condition arr % 2 == 0 generates a boolean mask [False, True, False, True, False]. '
          'Using this mask to index the array targets the even numbers (2 and 4). The assignment = '
          '0 replaces these targeted values with zero, modifying the array in-place to [1, 0, 3, '
          '0, 5].'},
 {'q': 'Which statement describes the difference between slicing with `.loc` and `.iloc` in '
       'Pandas?',
  'code': '',
  'opts': {'A': 'Both .loc and .iloc slice data by excluding the final index endpoint',
           'B': '.loc slicing is inclusive of the endpoint, while .iloc slicing is exclusive of '
                'the endpoint',
           'C': '.loc uses zero-based indexing, whereas .iloc uses index labels',
           'D': 'There is no distinction in how endpoints are handled during slicing'},
  'ans': 'B',
  'expl': 'In Pandas, label-based slicing using .loc[a:b] includes both label a and label b in the '
          'output. Conversely, integer-position based slicing using .iloc[i:j] follows standard '
          'Python semantics, meaning it includes index i but excludes index j.'},
 {'q': 'Given two 2 x 2 matrices, `A` and `B`, how does the output of `A * B` differ from '
       '`np.dot(A, B)`?',
  'code': '',
  'opts': {'A': 'A * B performs matrix multiplication, while np.dot(A, B) performs element-wise '
                'multiplication',
           'B': 'A * B computes the dot product, while np.dot(A, B) returns a flattened 1D array',
           'C': 'A * B performs element-wise multiplication, while np.dot(A, B) performs matrix '
                'multiplication',
           'D': 'Both operations perform standard matrix multiplication'},
  'ans': 'C',
  'expl': 'In NumPy, the arithmetic * operator performs element-wise multiplication on arrays. To '
          'achieve algebraic matrix multiplication (the dot product of matrices), one must use '
          'np.dot(), np.matmul(), or the @ operator.'},
 {'q': 'Consider the provided table representing a Pandas DataFrame named `df`. What will be the '
       "exact shape of the DataFrame generated by the expression `df[df['Dept'] == 'IT']`?",
  'code': 'Employee Data\n'
          '+----+---------+------+--------+\n'
          '| ID | Name    | Dept | Salary |\n'
          '+----+---------+------+--------+\n'
          '| 1  | Alice   | HR   | 50000  |\n'
          '| 2  | Bob     | IT   | 60000  |\n'
          '| 3  | Charlie | IT   | 70000  |\n'
          '+----+---------+------+--------+',
  'opts': {'A': '(3, 4)', 'B': '(2, 4)', 'C': '(2, 1)', 'D': '(4, 2)'},
  'ans': 'B',
  'expl': "The expression df['Dept'] == 'IT' generates a boolean Series that is True for rows 2 "
          'and 3, and False for row 1. Slicing the DataFrame with this mask yields a new DataFrame '
          'containing only the 2 matching rows. Since the original DataFrame has 4 columns, the '
          'shape of the resulting subset is (2, 4).'},
 {'q': 'What function computes the cumulative sum of elements along a specified axis in a '
       'multidimensional NumPy array?',
  'code': '',
  'opts': {'A': 'np.sum()',
           'B': 'np.add.accumulate()',
           'C': 'np.cumsum()',
           'D': 'Both (B) and (C)'},
  'ans': 'D',
  'expl': 'The np.cumsum() function is the standard method for computing the cumulative sum of '
          'array elements over a given axis. Additionally, the accumulate() method of the np.add '
          'universal function performs the same operation mathematically.'},
 {'q': 'What occurs when two DataFrames are concatenated along `axis=1` (columns) using '
       '`pd.concat()`, but their row indices do not overlap completely?',
  'code': '',
  'opts': {'A': 'Pandas raises a KeyError, requiring the indices to be identical',
           'B': 'Pandas aligns the data based on the indices, filling non-overlapping locations '
                'with NaN',
           'C': 'Pandas ignores the indices and stacks the rows consecutively',
           'D': 'The function drops any rows that do not have matching indices in both DataFrames'},
  'ans': 'B',
  'expl': 'When pd.concat() operates along axis=1, it aligns the disparate DataFrames by their row '
          'indices. If an index exists in one DataFrame but not the other, Pandas creates a union '
          'of the indices and populates the missing column values with NaN.'},
 {'q': 'Which module and function in NumPy is specifically used to compute the multiplicative '
       'inverse of a square matrix?',
  'code': '',
  'opts': {'A': 'np.inv()',
           'B': 'np.linalg.inverse()',
           'C': 'np.linalg.inv()',
           'D': 'np.math.inv()'},
  'ans': 'C',
  'expl': 'Matrix inversion requires linear algebra computations. NumPy provides the numpy.linalg '
          'module for this purpose, and the specific function to invert a square matrix is '
          'np.linalg.inv().'},
 {'q': 'What distinguishes the `pivot_table()` function from a standard `groupby()` operation in '
       'Pandas?',
  'code': '',
  'opts': {'A': 'pivot_table() can only calculate the mean, whereas groupby() supports multiple '
                'aggregations',
           'B': 'pivot_table() automatically reshapes the data to a two-dimensional grid based on '
                'index and columns arguments',
           'C': 'There is no structural distinction; pivot_table is merely an alias for groupby',
           'D': 'groupby() handles missing data, while pivot_table() throws an error when '
                'encountering NaNs'},
  'ans': 'B',
  'expl': 'While both functions perform data aggregation, pivot_table() is designed specifically '
          'to convert tall data into a wide, cross-tabular format. It accepts index and columns '
          'parameters to structure a two-dimensional grid, providing an alternative to chained '
          'groupby().unstack() calls.'},
 {'q': 'How can one perform vectorized string matching to filter a DataFrame where a string column '
       "'City' contains the substring 'York'?",
  'code': '',
  'opts': {'A': "df[df['City'] == '*York*']",
           'B': "df[df['City'].str.contains('York')]",
           'C': "df[df['City'].isin('York')]",
           'D': "df.filter(like='York', axis=0)"},
  'ans': 'B',
  'expl': 'Pandas provides a .str accessor to apply vectorized string methods to Series. The '
          'str.contains() method evaluates each element and returns a boolean Series indicating if '
          'the regex/substring is present, which is then used as a boolean mask.'},
 {'q': "In NumPy, taking a standard slice of an array (e.g., `b = a[1:5]`) creates a 'view' rather "
       "than a distinct 'copy' in memory. What is the consequence of this architecture?",
  'code': '',
  'opts': {'A': 'Modifying values in array b will alter the original array a',
           'B': 'Array b consumes duplicate memory, potentially leading to memory leaks',
           'C': 'Array b is rendered immutable and cannot be modified',
           'D': 'Modifying array a will raise a ValueError if array b is currently in scope'},
  'ans': 'A',
  'expl': 'Because a standard slice creates a view, b acts as a pointer to the same memory buffer '
          'utilized by a, adjusting the strides and offset. Consequently, assigning new values to '
          'elements in the slice b overwrites the data in the original array a.'},
 {'q': 'What structural issue generally triggers the `SettingWithCopyWarning` in Pandas?',
  'code': '',
  'opts': {'A': 'Attempting to cast a string column to an integer type',
           'B': "Performing chained indexing assignment (e.g., df[df['A'] > 5]['B'] = 10)",
           'C': 'Merging two DataFrames that possess conflicting index labels',
           'D': 'Reading a CSV file that contains inconsistent column delimitations'},
  'ans': 'B',
  'expl': 'The SettingWithCopyWarning alerts the user that an assignment operation might be '
          'modifying a temporary copy of a slice rather than the original DataFrame. This '
          'ambiguity occurs during chained indexing (multiple brackets). Pandas recommends using '
          '.loc for assignment to ensure operation on the primary object.'},
 {'q': 'Given an array `X` of shape (4, 3, 2) and an array `Y` of shape (3, 2), what will be the '
       'resulting shape of `X * Y` after broadcasting?',
  'code': '',
  'opts': {'A': '(4, 3, 2)',
           'B': '(12, 6, 2)',
           'C': '(4, 3, 3, 2)',
           'D': 'The arrays cannot broadcast due to mismatched dimensions'},
  'ans': 'A',
  'expl': 'Broadcasting rules align the arrays from the rightmost (trailing) dimension. X ends in '
          '(3, 2), and Y is (3, 2). Since these match, NumPy pads Y with an initial dimension of 1 '
          '(acting as (1, 3, 2)). The operation then iterates the (3, 2) block 4 times, resulting '
          'in a shape of (4, 3, 2).'},
 {'q': "When using `pd.merge()` with `how='outer'`, what is the function of the `indicator=True` "
       'parameter?',
  'code': '',
  'opts': {'A': 'It calculates a statistical significance indicator for the merged columns',
           'B': 'It creates a boolean column identifying duplicated rows across the merge',
           'C': "It appends a categorical column _merge indicating whether each row's keys were "
                "present in 'left_only', 'right_only', or 'both'",
           'D': 'It prints a progress bar to the console indicating merge execution time'},
  'ans': 'C',
  'expl': 'Setting indicator=True during a merge adds a new categorical column (named _merge by '
          'default). This metadata column tracks the source of the data for each resulting row, '
          "mapping values to 'left_only', 'right_only', or 'both', which identifies the source of "
          'the data in full outer joins.'},
 {'q': "What role do 'strides' play in the underlying C architecture of a NumPy array?",
  'code': '',
  'opts': {'A': 'They dictate the number of bytes to step in memory to advance to the next element '
                'in a specific dimension',
           'B': 'They define the maximum contiguous memory block allocated for the array',
           'C': 'They serve as the checksum to maintain data integrity during parallel processing',
           'D': 'They dictate how the elements are formatted when the array is printed to the '
                'console'},
  'ans': 'A',
  'expl': "NumPy arrays are stored in a contiguous 1D block of memory. 'Strides' form a tuple "
          'indicating the byte-steps required to jump to the next element along each dimension. '
          'Manipulating strides allows NumPy to perform operations like transposition or slicing '
          'without copying memory.'},
 {'q': 'If one requires data to be segmented into discrete bins based on sample quantiles '
       '(equal-sized buckets), which Pandas function is used?',
  'code': '',
  'opts': {'A': 'pd.cut()', 'B': 'pd.qcut()', 'C': 'pd.factorize()', 'D': 'pd.get_dummies()'},
  'ans': 'B',
  'expl': 'The pd.qcut() function provides quantile-based discretization. It divides continuous '
          'data into equal-sized bins based on the distribution (quantiles) of the data. '
          'Conversely, pd.cut() bins data based on fixed, explicitly defined numeric intervals.'},
 {'q': "What calculation is executed by the NumPy function `np.einsum('ij,jk->ik', A, B)`?",
  'code': '',
  'opts': {'A': 'Element-wise addition of matrix A and B',
           'B': 'Cross product of vectors A and B',
           'C': 'Standard matrix multiplication of 2D arrays A and B',
           'D': 'Transposition of the combined arrays A and B'},
  'ans': 'C',
  'expl': "The np.einsum function applies Einstein summation convention. The notation 'ij,jk->ik' "
          'describes summing over the repeated subscript j. This operation corresponds to standard '
          'matrix multiplication (the dot product) of a matrix A (rows i, cols j) and matrix B '
          '(rows j, cols k) yielding a matrix of dimensions (i, k).'},
 {'q': 'Consider two tables representing Pandas DataFrames `scores` and `details`. If a left merge '
       "(`how='left'`) is executed calling `scores.merge(details, on='Student_ID')`, how many rows "
       'will the resulting DataFrame contain?',
  'code': 'Student Scores\n'
          '+------------+-------+\n'
          '| Student_ID | Score |\n'
          '+------------+-------+\n'
          '| 101        | 85    |\n'
          '| 102        | 90    |\n'
          '+------------+-------+\n'
          '\n'
          'Student Details\n'
          '+------------+---------+\n'
          '| Student_ID | Name    |\n'
          '+------------+---------+\n'
          '| 102        | Bob     |\n'
          '| 103        | Charlie |\n'
          '+------------+---------+',
  'opts': {'A': '1', 'B': '2', 'C': '3', 'D': '4'},
  'ans': 'B',
  'expl': 'A left merge returns all rows from the left DataFrame (scores), regardless of whether a '
          'matching key exists in the right DataFrame. scores contains 2 rows (IDs 101, 102). ID '
          "101 will have a NaN value for 'Name', and ID 102 will map to 'Bob'. The right-exclusive "
          'row (ID 103) is dropped. The total count remains 2.'},
 {'q': 'In terms of computational performance, which iteration strategy is the most '
       'computationally efficient for processing multi-column logical operations across millions '
       'of rows in Pandas?',
  'code': '',
  'opts': {'A': 'Vectorization utilizing underlying NumPy C arrays',
           'B': 'Iteration using the df.iterrows() generator',
           'C': 'Iteration using the df.itertuples() generator',
           'D': 'Execution through the df.apply() method row-by-row'},
  'ans': 'A',
  'expl': 'Vectorization delegates computation to optimized C libraries, avoiding Python loop '
          'interpreter overhead. itertuples() is faster than iterrows(), and apply() can be faster '
          'than explicit loops, but vectorized operations provide the highest performance.'},
 {'q': 'When working with time series data in Pandas, what is the functional difference between '
       '`tz_localize()` and `tz_convert()`?',
  'code': '',
  'opts': {'A': 'tz_localize() converts an existing timezone to UTC, while tz_convert() removes '
                'the timezone completely',
           'B': 'tz_localize() assigns a timezone to naive timestamps, while tz_convert() '
                'translates an already timezone-aware timestamp to a new timezone',
           'C': 'tz_localize() modifies the system clock format, while tz_convert() translates '
                'string objects into datetime objects',
           'D': 'Both functions apply a timezone to naive data and are functionally identical'},
  'ans': 'B',
  'expl': "A 'naive' timestamp possesses no timezone information. tz_localize() is used to impart "
          "initial timezone metadata to such naive objects. Once a timestamp is 'timezone-aware', "
          'tz_convert() must be used to calculate and shift the data into a different geographic '
          'timezone context.'},
 {'q': 'How does Pandas resolve index alignment when executing mathematical addition (`Series_A + '
       'Series_B`) between two Series that possess partially disjoint indices?',
  'code': '',
  'opts': {'A': 'It calculates the sum for intersection indices and defaults to zero for disjoint '
                'indices',
           'B': 'It raises a standard Python KeyError indicating mismatched axes',
           'C': 'It calculates the sum for intersection indices and inserts NaN for any index '
                'present in only one Series',
           'D': 'It truncates the output Series strictly to the intersection of both indices'},
  'ans': 'C',
  'expl': 'Pandas relies on data alignment by index labels. During arithmetic operations, it forms '
          'the union of the indices. Where labels align, the operation proceeds normally. If a '
          'label exists in one Series but not the other, the absent value is interpreted as '
          'missing, resulting in NaN (since number + NaN = NaN).'},
 {'q': 'What does the `info()` method in Pandas output when executed on a DataFrame?',
  'code': '',
  'opts': {'A': 'A statistical summary of numerical columns',
           'B': 'The first five and last five rows of the data',
           'C': 'A concise summary of the DataFrame, including the column names, non-null counts, '
                'and memory usage',
           'D': 'The correlation matrix for all numerical features'},
  'ans': 'C',
  'expl': 'The info() method prints information about a DataFrame including the index dtype and '
          'columns, non-null values, and memory usage. It is the standard function used for a '
          'rapid assessment of data structure and missing values.'},
 {'q': 'Which operation provides the transpose of a two-dimensional NumPy array `arr`?',
  'code': '',
  'opts': {'A': 'arr.T', 'B': 'np.transpose(arr)', 'C': 'Both (A) and (B)', 'D': 'arr.inverse()'},
  'ans': 'C',
  'expl': 'In NumPy, transposing an array swaps its axes. This can be achieved either by utilizing '
          'the .T attribute property on the array instance or by calling the explicit '
          'np.transpose() function. Both methods yield an identical view of the permuted array.'},
 {'q': 'When modifying a subset of a DataFrame, what is the consequence of Pandas raising a '
       '`KeyError` within the `loc` indexer?',
  'code': '',
  'opts': {'A': 'The data types of the column and row variables do not align',
           'B': "A specified label does not exist within the DataFrame's index or columns",
           'C': 'The indexer bounds exceed the total integer length of the array',
           'D': 'The user attempted to divide by zero'},
  'ans': 'B',
  'expl': 'The .loc indexer queries DataFrames exclusively based on explicit labels. If an exact '
          'label string or index object provided to the .loc expression cannot be found within the '
          'existing axes, Pandas raises a KeyError.'},
 {'q': 'Which function initializes a NumPy array of a designated shape filled exclusively with '
       'ones?',
  'code': '',
  'opts': {'A': 'np.fill(1)', 'B': 'np.ones()', 'C': 'np.array(1)', 'D': 'np.unity()'},
  'ans': 'B',
  'expl': 'The function np.ones() generates a new array of a specified shape and type, '
          'initializing all memory block elements to the scalar value 1. It operates analogously '
          'to np.zeros().'}]


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