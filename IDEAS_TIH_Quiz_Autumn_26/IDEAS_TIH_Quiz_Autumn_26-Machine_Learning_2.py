#!/usr/bin/env python3
"""
IDEAS TIH Quiz Autumn 26 - Machine Learning 2 - interactive terminal quiz
---------------------------------------------------------------
Run:   python machine_learning_2_quiz.py

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

TITLE = "IDEAS TIH Quiz Autumn 26 - Machine Learning 2"
TIME_LIMIT = 60 * 60          # seconds
OPTION_KEYS = ("A", "B", "C", "D")

QUESTIONS = [{'q': "What defines a dataset as being 'linearly separable'?",
  'code': '',
  'opts': {'A': 'It can be clustered using exactly two centroids',
           'B': 'A single straight line or hyperplane can completely separate the classes',
           'C': 'The variance of the dataset increases linearly over time',
           'D': 'The inputs can be mapped to continuous probabilistic outputs'},
  'ans': 'B',
  'expl': 'A dataset is linearly separable if there exists a straight line (in 2D space), plane '
          '(in 3D), or hyperplane (in n-dimensions) that can divide the space into two halves, '
          'each containing only one class.'},
 {'q': 'How does a Multilayer Perceptron (MLP) resolve the non-linear separability limitations of '
       'a standard perceptron?',
  'code': '',
  'opts': {'A': 'By processing images using convolutional filters',
           'B': 'By removing bias terms to strictly enforce linear boundaries',
           'C': 'By incorporating one or more hidden layers with non-linear activation functions',
           'D': 'By utilizing random forests instead of gradient descent'},
  'ans': 'C',
  'expl': 'An MLP introduces hidden layers consisting of multiple neurons equipped with non-linear '
          'activation functions (like ReLU or Sigmoid). This depth allows the network to learn '
          'complex, non-linear decision boundaries.'},
 {'q': "What structural role does a 'hidden layer' fulfill in an artificial neural network?",
  'code': '',
  'opts': {'A': 'It directly ingests raw data from the external environment',
           'B': 'It stores backup weights in case of memory failure',
           'C': 'It performs intermediate computations between the input and output layers',
           'D': 'It exclusively evaluates the loss function during backpropagation'},
  'ans': 'C',
  'expl': 'A hidden layer sits between the input and output layers. Its neurons apply weights, '
          'biases, and activations to intermediate representations of data to extract patterns '
          'before reaching the output layer.'},
 {'q': 'Which mathematical equation accurately represents the ReLU (Rectified Linear Unit) '
       'activation function?',
  'code': '',
  'opts': {'A': 'f(x) = 1/(1 + e^(-x))',
           'B': 'f(x) = max(0, x)',
           'C': 'f(x) = ln(1 + e^x)',
           'D': 'f(x) = tanh(x)'},
  'ans': 'B',
  'expl': 'The ReLU function outputs the input x directly if it is positive, and 0 if it is '
          'negative. This is formally defined mathematically as the maximum between 0 and x.'},
 {'q': "What causes the 'Dying ReLU' problem during neural network training?",
  'code': '',
  'opts': {'A': 'The gradient becomes 0 for negative inputs, permanently freezing weight updates',
           'B': "The learning rate is set too low, halting the model's convergence",
           'C': 'Positive inputs create exponentially large gradients, causing overflow',
           'D': 'The weights decay strictly to 0 due to excessive L2 regularization'},
  'ans': 'A',
  'expl': 'Because the derivative of ReLU is exactly zero for all negative inputs, a large weight '
          "update can push a neuron's weights such that it only outputs negative values. When this "
          'happens, gradients can no longer flow through the neuron during backpropagation, '
          "causing it to 'die'."},
 {'q': 'If sigma(x) denotes the standard sigmoid activation function, what is its mathematical '
       "derivative sigma^'(x)?",
  'code': '',
  'opts': {'A': 'sigma(x) + (1 - sigma(x))',
           'B': 'sigma(x)(1 - sigma(x))',
           'C': '(sigma(x))/(sigma(x) - 1)',
           'D': '1 - sigma(x)^2'},
  'ans': 'B',
  'expl': 'A mathematical property of the sigmoid function is that its derivative can be expressed '
          'entirely in terms of its output. The correct derivation is sigma(x)(1 - sigma(x)).'},
 {'q': 'How does the sigmoid activation function contribute to the vanishing gradient problem in '
       'deep neural networks?',
  'code': '',
  'opts': {'A': 'It outputs values exceeding 1, causing gradient explosion',
           'B': 'Its gradient is exactly zero for all positive values',
           'C': 'Its maximum derivative is 0.25, scaling gradients down multiplicatively across '
                'layers',
           'D': 'It removes the bias terms automatically during the backward pass'},
  'ans': 'C',
  'expl': 'The derivative of the sigmoid function peaks at 0.25. During backpropagation in deep '
          'networks, multiplying these small fractional derivatives across multiple layers causes '
          "the gradients to exponentially shrink ('vanish') as they reach early layers."},
 {'q': 'In a multi-class classification neural network, what is the primary function of a Softmax '
       'layer?',
  'code': '',
  'opts': {'A': 'To convert the final neuron outputs into a normalized probability distribution '
                'summing to 1',
           'B': 'To scale inputs into a strict zero-mean range for faster convergence',
           'C': 'To randomly drop neurons to prevent overfitting',
           'D': 'To calculate the distance between features in a high-dimensional space'},
  'ans': 'A',
  'expl': 'The Softmax function takes a vector of arbitrary real-valued scores (logits) and '
          'applies an exponential function normalized by the sum of all exponentials. This ensures '
          'the outputs range from 0 to 1 and sum to 1, representing class probabilities.'},
 {'q': 'What is the continuous output range of the Hyperbolic Tangent (Tanh) activation function?',
  'code': '',
  'opts': {'A': '0 to inf', 'B': '0 to 1', 'C': '-1 to 1', 'D': '-inf to inf'},
  'ans': 'C',
  'expl': 'The Tanh function squashes any real-valued input into a bounded range between -1 and 1. '
          'Unlike the Sigmoid function, its output is zero-centered.'},
 {'q': 'Why is the Tanh function frequently favored over the Sigmoid function in hidden layers of '
       'a neural network?',
  'code': '',
  'opts': {'A': 'Tanh has a derivative that never vanishes',
           'B': 'Tanh is computationally cheaper to compute because it avoids exponential '
                'calculations',
           'C': 'Tanh is zero-centered, which prevents the gradients from shifting consistently in '
                'a single direction',
           'D': 'Tanh strictly outputs discrete binary values'},
  'ans': 'C',
  'expl': 'Because Tanh outputs values between -1 and 1, the mean activation is closer to zero. '
          'Zero-centered activations cause the gradients to distribute more evenly during '
          'backpropagation, leading to faster and more stable weight convergence compared to the '
          'all-positive outputs of Sigmoid.'},
 {'q': 'In standard PyTorch training scripts, what specific task does the command '
       '`loss.backward()` execute?',
  'code': '',
  'opts': {'A': 'It updates the weights inside the neural network',
           'B': 'It computes the gradient of the loss with respect to all tensors possessing '
                '`requires_grad=True`',
           'C': 'It zeroes out the accumulated gradients from the previous batch',
           'D': 'It performs a forward pass inversely through the architecture'},
  'ans': 'B',
  'expl': "The `backward()` method on a loss tensor initiates backpropagation. PyTorch's autograd "
          'engine traverses the computation graph backward, calculating and storing the partial '
          'derivatives (gradients) for every parameter involved in the calculation.'},
 {'q': 'What occurs structurally if `optimizer.zero_grad()` is omitted from a PyTorch training '
       'loop before `loss.backward()`?',
  'code': '',
  'opts': {'A': 'The code will throw an immediate syntax error',
           'B': 'The model will reset to random initial weights',
           'C': 'Gradients from the current batch will be added to the gradients accumulated from '
                'previous batches',
           'D': 'The optimizer will automatically skip the gradient calculation'},
  'ans': 'C',
  'expl': 'By default, PyTorch accumulates gradients in the `.grad` attribute of tensors. If '
          '`zero_grad()` is omitted, the new gradients are added to the existing ones, corrupting '
          'the descent direction for the current batch.'},
 {'q': 'What is the primary data structure utilized by PyTorch to represent variables, inputs, and '
       'parameters?',
  'code': '',
  'opts': {'A': 'DataFrames', 'B': 'Linked Lists', 'C': 'Tensors', 'D': 'Graphs'},
  'ans': 'C',
  'expl': 'Tensors are multi-dimensional arrays serving as the foundational data structure in '
          'PyTorch. They are similar to NumPy arrays but can be accelerated using GPUs and track '
          'computational graphs for automatic differentiation.'},
 {'q': 'In the context of binary classification, what defines a False Positive (FP)?',
  'code': '',
  'opts': {'A': 'The model predicted the negative class, but the actual class is positive',
           'B': 'The model predicted the positive class, but the actual class is negative',
           'C': 'The model predicted the positive class, and the actual class is positive',
           'D': 'The model encountered an error calculating a positive prediction'},
  'ans': 'B',
  'expl': 'A False Positive occurs when the algorithm incorrectly labels an observation as '
          'belonging to the positive class when it actually belongs to the negative class.'},
 {'q': 'Based on the provided Confusion Matrix, calculate the Precision metric for the positive '
       'class.',
  'code': 'Confusion Matrix\n'
          '+-----------------+--------------------+--------------------+\n'
          '|                 | Predicted Positive | Predicted Negative |\n'
          '+-----------------+--------------------+--------------------+\n'
          '| Actual Positive | 40                 | 10                 |\n'
          '| Actual Negative | 20                 | 30                 |\n'
          '+-----------------+--------------------+--------------------+',
  'opts': {'A': '0.80', 'B': '0.66', 'C': '0.57', 'D': '0.40'},
  'ans': 'B',
  'expl': 'Precision is calculated as True Positives divided by total Predicted Positives: TP / '
          '(TP + FP). From the table, TP is 40 and FP is 20. Thus, 40 / (40 + 20) = 40 / 60, which '
          'simplifies to approximately 0.66.'},
 {'q': 'Which formula correctly represents mathematical Recall (Sensitivity) in a binary '
       'classification setting?',
  'code': '',
  'opts': {'A': 'TP/(TP + FP)',
           'B': 'TN/(TN + FP)',
           'C': 'TP/(TP + FN)',
           'D': '(TP + TN)/(TP + TN + FP + FN)'},
  'ans': 'C',
  'expl': 'Recall measures the proportion of actual positives that were correctly identified. It '
          'is defined as True Positives (TP) divided by the sum of True Positives and False '
          'Negatives (FN).'},
 {'q': 'The F1 Score is designed to balance Precision and Recall. Which mathematical mean does it '
       'represent?',
  'code': '',
  'opts': {'A': 'The arithmetic mean of Precision and Recall',
           'B': 'The geometric mean of Precision and Recall',
           'C': 'The harmonic mean of Precision and Recall',
           'D': 'The quadratic mean of Precision and Recall'},
  'ans': 'C',
  'expl': 'The F1 Score calculates the harmonic mean of Precision and Recall. The harmonic mean '
          'penalizes extreme values, meaning a high F1 score requires both Precision and Recall to '
          'be reasonably high.'},
 {'q': 'What does the Specificity metric quantify in a classification model?',
  'code': '',
  'opts': {'A': 'The True Positive Rate',
           'B': 'The True Negative Rate',
           'C': 'The proportion of predicted positives that are actually positive',
           'D': 'The proportion of false positives across all predictions'},
  'ans': 'B',
  'expl': 'Specificity calculates the True Negative Rate (TNR), which is the proportion of actual '
          'negative cases that were correctly identified. The formula is TN / (TN + FP).'},
 {'q': 'An ROC (Receiver Operating Characteristic) curve plots two distinct metrics against one '
       'another across various thresholds. What are the axes of an ROC curve?',
  'code': '',
  'opts': {'A': 'Precision on the Y-axis and Recall on the X-axis',
           'B': 'True Positive Rate on the Y-axis and False Positive Rate on the X-axis',
           'C': 'Specificity on the Y-axis and Sensitivity on the X-axis',
           'D': 'Accuracy on the Y-axis and F1 Score on the X-axis'},
  'ans': 'B',
  'expl': 'The ROC curve is a graphical representation displaying model performance across varying '
          'discrimination thresholds. The Y-axis represents the True Positive Rate (Sensitivity), '
          'while the X-axis represents the False Positive Rate (1 - Specificity).'},
 {'q': 'In statistical hypothesis testing and machine learning evaluation, to which confusion '
       'matrix element does a Type I Error correspond?',
  'code': '',
  'opts': {'A': 'True Positive',
           'B': 'True Negative',
           'C': 'False Positive',
           'D': 'False Negative'},
  'ans': 'C',
  'expl': 'A Type I Error involves rejecting a true null hypothesis. In the nomenclature of a '
          'confusion matrix, this aligns with a False Positive, where a condition is detected '
          'despite being absent.'},
 {'q': 'To which element of a standard confusion matrix does a statistical Type II Error '
       'correspond?',
  'code': '',
  'opts': {'A': 'True Positive',
           'B': 'False Positive',
           'C': 'True Negative',
           'D': 'False Negative'},
  'ans': 'D',
  'expl': 'A Type II Error involves failing to reject a false null hypothesis. In machine learning '
          'classification, this translates to a False Negative, where the model misses a positive '
          'condition that actually exists.'},
 {'q': 'What are the dimensions of a standard confusion matrix used for a binary classification '
       'problem?',
  'code': '',
  'opts': {'A': '1x2', 'B': '2x2', 'C': '3x3', 'D': '4x4'},
  'ans': 'B',
  'expl': 'A binary classification problem distinguishes between exactly two classes (positive and '
          'negative). Therefore, its confusion matrix is a 2x2 grid tracking actual vs. predicted '
          'values for these two states.'},
 {'q': "What condition characterizes 'overfitting' in a machine learning model?",
  'code': '',
  'opts': {'A': 'The model performs poorly on training data and poorly on unseen data',
           'B': 'The model performs well on training data but poorly on unseen test data',
           'C': 'The model performs poorly on training data but well on test data',
           'D': 'The model cannot process data structures properly'},
  'ans': 'B',
  'expl': 'Overfitting occurs when a model captures random noise instead of the underlying '
          'pattern. This causes the model to exhibit high accuracy (low error) on the specific '
          'training set, but fail to generalize to new, unseen test data.'},
 {'q': 'What mathematical penalty does L1 Regularization (Lasso) append to the standard loss '
       'function?',
  'code': '',
  'opts': {'A': 'The sum of the squared magnitudes of the weights',
           'B': 'The sum of the absolute values of the weights',
           'C': 'The square root of the sum of squared weights',
           'D': 'A constant arbitrary bias term'},
  'ans': 'B',
  'expl': 'L1 Regularization penalizes a model by adding the sum of the absolute values of the '
          'coefficient weights to the cost function. This operation pushes some feature weights to '
          'zero, achieving sparse models.'},
 {'q': 'Unlike L1 Regularization, how does L2 Regularization (Ridge) handle coefficient penalties?',
  'code': '',
  'opts': {'A': 'It forces all weights perfectly to zero for feature selection',
           'B': 'It adds a penalty equivalent to the sum of the squared weights, shrinking them '
                'toward zero but rarely exactly to zero',
           'C': 'It increases variance by exponentially raising coefficient weights',
           'D': 'It removes the bias term from the neural network entirely'},
  'ans': 'B',
  'expl': 'L2 regularization minimizes the sum of squared weights. Because the derivative of w^2 '
          'is proportional to w, the penalty decays as weights approach zero. Thus, it shrinks '
          'weights to be small but generally leaves them non-zero.'},
 {'q': 'What is the primary academic objective of k-fold cross-validation?',
  'code': '',
  'opts': {'A': 'To accelerate the calculation speed of the optimizer',
           'B': "To assess the model's ability to generalize by averaging its performance across "
                'multiple mutually exclusive data partitions',
           'C': 'To automatically insert missing data entries into a tabular format',
           'D': 'To increase the volume of training data by synthetically generating points'},
  'ans': 'B',
  'expl': "Cross-validation divides data into 'k' independent subsets (folds). Evaluating the "
          'model systematically on different training/validation splits mitigates variance in '
          'performance metrics and yields a robust estimate of generalization capability.'},
 {'q': 'Which theoretical relationship defines the Bias-Variance tradeoff when assessing expected '
       'model error?',
  'code': '',
  'opts': {'A': 'Total Error = Bias + Variance + Irreducible Error',
           'B': 'Total Error = (Bias x Variance) / 2',
           'C': 'Total Error = Variance - Bias',
           'D': 'Total Error = Bias^2 + Variance^2'},
  'ans': 'A',
  'expl': 'The expected test error of a model decomposes analytically into three components: Bias '
          '(squared), Variance, and Irreducible Error. Decreasing one element often inherently '
          'increases the other.'},
 {'q': 'What behavioral symptom typically indicates a model suffers from high bias?',
  'code': '',
  'opts': {'A': 'It perfectly maps every training point but fails on the test set',
           'B': 'It demands unreasonable amounts of computational memory',
           'C': 'It underfits the data, demonstrating high error on both training and test sets',
           'D': 'It generates probability values exceeding 1.0'},
  'ans': 'C',
  'expl': 'High bias stems from erroneous assumptions in the algorithm, such as trying to fit a '
          'complex non-linear pattern with a simple linear line. This phenomenon is known as '
          'underfitting, yielding high errors across all data splits.'},
 {'q': 'How does increasing the complexity of a model affect its theoretical variance?',
  'code': '',
  'opts': {'A': 'Variance remains statistically constant regardless of complexity',
           'B': 'Variance strictly decreases to absolute zero',
           'C': 'Variance tends to increase as the model becomes highly sensitive to small '
                'fluctuations in training data',
           'D': 'Variance transitions into irreducible error'},
  'ans': 'C',
  'expl': 'Complex models (e.g., highly deep neural networks or deep decision trees) have the '
          'capacity to fit data noise. Consequently, minor changes in the training set cause major '
          'changes in the output weights, defining high variance.'},
 {'q': "By what mechanism does the 'Early Stopping' technique prevent model overfitting during "
       'iterative training?',
  'code': '',
  'opts': {'A': 'It monitors validation loss and halts training epochs when the validation loss '
                'begins to diverge upward',
           'B': "It artificially reduces the size of the dataset midway through the algorithm's "
                'lifecycle',
           'C': 'It zeroes out all gradients to manually simulate convergence',
           'D': 'It converts dense layers into sparse representations randomly'},
  'ans': 'A',
  'expl': 'Early stopping is a procedural regularization method. By calculating error on a '
          'hold-out validation set after each epoch, training is stopped when training error '
          'continues to decrease but validation error begins to rise, signaling overfitting.'}]


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