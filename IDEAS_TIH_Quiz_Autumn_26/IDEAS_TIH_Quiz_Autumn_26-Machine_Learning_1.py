#!/usr/bin/env python3
"""
IDEAS TIH Quiz Autumn 26 - Machine Learning 1 - interactive terminal quiz
---------------------------------------------------------------
Run:   python machine_learning_1_quiz.py

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

TITLE = "IDEAS TIH Quiz Autumn 26 - Machine Learning 1"
TIME_LIMIT = 60 * 60          # seconds
OPTION_KEYS = ("A", "B", "C", "D")

QUESTIONS = [{'q': 'What is the main goal of regression?',
  'code': '',
  'opts': {'A': 'Predict categories',
           'B': 'Predict numbers',
           'C': 'Detect images',
           'D': 'Store data'},
  'ans': 'B',
  'expl': 'The main goal of regression algorithms in machine learning is to predict continuous '
          'numerical values (e.g., predicting house prices, temperature, or stock prices). In '
          'contrast, predicting categories is the goal of classification algorithms.'},
 {'q': 'Which of the following is a classification problem?',
  'code': '',
  'opts': {'A': 'Predicting salary',
           'B': 'Predicting temperature',
           'C': 'Predicting spam or not spam',
           'D': 'Predicting house price'},
  'ans': 'C',
  'expl': 'Classification is the process of predicting a discrete class label or category. '
          "Predicting whether an email is 'spam' or 'not spam' involves assigning the input to one "
          'of two distinct categories, making it a binary classification problem. Predicting '
          'salary, temperature, and house prices involves continuous numerical values, which are '
          'regression problems.'},
 {'q': 'In the equation y = mx + c, what does m represent?',
  'code': '',
  'opts': {'A': 'Input feature', 'B': 'Starting point', 'C': 'Rate of change', 'D': 'Error value'},
  'ans': 'C',
  'expl': 'In the equation of a straight line, y = mx + c, m represents the slope or the rate of '
          'change of the dependent variable y with respect to the independent variable x. It '
          'defines how much y is expected to change when x changes by one unit.'},
 {'q': 'Which algorithm is commonly used for binary classification?',
  'code': '',
  'opts': {'A': 'Linear Regression',
           'B': 'Logistic Regression',
           'C': 'Scatter Plot',
           'D': 'Matplotlib'},
  'ans': 'B',
  'expl': 'Logistic Regression is a statistical algorithm used primarily for binary classification '
          'problems (where there are only two possible outcomes). It calculates the probability '
          'that a given input belongs to a specific class. Linear regression is used for '
          'continuous outputs, while Scatter Plot and Matplotlib are data visualization tools.'},
 {'q': 'What is the output range of the Sigmoid activation function?',
  'code': '',
  'opts': {'A': '-1 to 1', 'B': '0 to 1', 'C': '0 to 100', 'D': 'Any value'},
  'ans': 'B',
  'expl': 'The Sigmoid activation function mathematically maps any real-valued number into a '
          'restricted range between 0 and 1. Because its output resembles a probability, it is '
          'widely used in the output layer of binary classification models.'},
 {'q': 'What is a perceptron?',
  'code': '',
  'opts': {'A': 'A database',
           'B': 'A plotting function',
           'C': 'The simplest neural network',
           'D': 'A loss function'},
  'ans': 'C',
  'expl': 'A perceptron is a basic unit of artificial neural networks. It is often described as '
          'the simplest form of a neural network, consisting of a single neuron or linear '
          'threshold unit that takes inputs, multiplies them by weights, and passes the sum '
          'through an activation function.'},
 {'q': 'What is the role of `optimizer.step()` in PyTorch?',
  'code': '',
  'opts': {'A': 'Draw graphs',
           'B': 'Clear gradients',
           'C': 'Update model weights',
           'D': 'Load data'},
  'ans': 'C',
  'expl': 'In the PyTorch deep learning framework, `optimizer.step()` performs a single '
          "optimization step. It updates the model's parameters (weights and biases) based on the "
          'gradients computed during the backward pass (backpropagation).'},
 {'q': 'What is the purpose of a loss function in machine learning?',
  'code': '',
  'opts': {'A': 'To store the dataset',
           'B': 'To measure prediction error',
           'C': 'To draw graphs',
           'D': 'To create tensors'},
  'ans': 'B',
  'expl': 'A loss function evaluates how well a specific algorithm models the given data. It '
          "measures the prediction error, which is the difference between the model's predicted "
          'outputs and the actual target values. The goal of model training is to minimize this '
          'loss.'},
 {'q': 'In a confusion matrix, what does TP stand for?',
  'code': '',
  'opts': {'A': 'Total Prediction',
           'B': 'True Positive',
           'C': 'Training Parameter',
           'D': 'Tensor Probability'},
  'ans': 'B',
  'expl': 'In a confusion matrix, TP stands for True Positive. It represents the instances where '
          'the model predicted the positive class correctly, and the actual class is indeed '
          'positive.'},
 {'q': 'What is the purpose of `ReLU` in an MLP?',
  'code': '',
  'opts': {'A': 'Convert output to probability',
           'B': 'Store data',
           'C': 'Introduce non-linearity',
           'D': 'Calculate accuracy'},
  'ans': 'C',
  'expl': 'ReLU (Rectified Linear Unit) is an activation function used in Multilayer Perceptrons '
          '(MLPs). Its primary purpose is to introduce non-linearity, enabling the network to '
          'model non-linear relationships in the data.'},
 {'q': 'What distinguishes supervised learning from unsupervised learning?',
  'code': '',
  'opts': {'A': 'The use of labeled training data',
           'B': 'The utilization of neural networks',
           'C': 'The requirement for continuous data',
           'D': 'The absence of an optimization function'},
  'ans': 'A',
  'expl': 'Supervised learning relies on labeled training datasets, where each input is paired '
          'with a known target output. Unsupervised learning operates on unlabeled data to find '
          'hidden structures.'},
 {'q': 'Which type of target variable is associated with a classification task?',
  'code': '',
  'opts': {'A': 'Continuous', 'B': 'Categorical', 'C': 'Infinite', 'D': 'Fractional'},
  'ans': 'B',
  'expl': 'Classification tasks predict a discrete, categorical target variable, assigning inputs '
          'into predefined classes.'},
 {'q': 'Which application represents a regression task?',
  'code': '',
  'opts': {'A': 'Identifying digits in an image',
           'B': 'Determining email sentiment',
           'C': "Forecasting next month's sales revenue",
           'D': 'Grouping customers by purchase behavior'},
  'ans': 'C',
  'expl': 'Forecasting sales revenue requires predicting a continuous numeric value, which defines '
          'a regression task. The other options describe classification or clustering.'},
 {'q': 'What does linear regression attempt to minimize during training?',
  'code': '',
  'opts': {'A': 'The number of input features',
           'B': 'The sum of squared residuals',
           'C': 'The variance of the independent variables',
           'D': 'The correlation between predictors'},
  'ans': 'B',
  'expl': 'Standard Ordinary Least Squares (OLS) linear regression calculates parameters by '
          'minimizing the sum of the squared differences (residuals) between observed and '
          'predicted values.'},
 {'q': 'Why is Mean Squared Error (MSE) often preferred over Mean Absolute Error (MAE) when '
       'training linear models?',
  'code': '',
  'opts': {'A': 'MSE penalizes larger errors more heavily',
           'B': 'MSE ignores outliers completely',
           'C': 'MSE is computationally faster for large datasets',
           'D': 'MSE produces a discrete output space'},
  'ans': 'A',
  'expl': 'MSE squares the difference between predictions and actuals, meaning large deviations '
          'incur a quadratically larger penalty compared to small deviations. MAE scales penalties '
          'linearly.'},
 {'q': 'Which of the following represents the standard formula for Mean Squared Error (MSE) for a '
       'dataset of size n?',
  'code': '',
  'opts': {'A': '1/n Sum_(i = 1)^n (y_i - y_hat_i)',
           'B': '1/n Sum_(i = 1)^n|y_i - y_hat_i|',
           'C': '1/n Sum_(i = 1)^n (y_i - y_hat_i)^2',
           'D': 'Sum_(i = 1)^n sqrt(y_i - y_hat_i)'},
  'ans': 'C',
  'expl': 'The Mean Squared Error is computed by taking the average of the squared differences '
          'between the actual values y_i and the predicted values y_hat_i.'},
 {'q': 'What mathematical operation does Gradient Descent use to find the direction of steepest '
       'descent?',
  'code': '',
  'opts': {'A': 'Integration of the loss function',
           'B': 'Matrix inversion of the dataset',
           'C': 'Calculation of the partial derivatives of the loss function',
           'D': 'Applying a Fourier transform to the weights'},
  'ans': 'C',
  'expl': 'Gradient Descent calculates the gradient, which is a vector of partial derivatives of '
          'the loss function with respect to the model parameters. This vector points in the '
          'direction of steepest ascent, so taking the negative step minimizes the loss.'},
 {'q': 'What is the function of the learning rate in an optimization algorithm?',
  'code': '',
  'opts': {'A': 'It sets the size of the dataset used in each epoch',
           'B': 'It determines the magnitude of parameter updates at each step',
           'C': 'It defines the number of hidden layers in the model',
           'D': 'It specifies the probability threshold for classification'},
  'ans': 'B',
  'expl': 'The learning rate is a hyperparameter that scales the gradient during weight updates. '
          'It dictates the step size taken towards the minimum of the loss function.'},
 {'q': 'What is the primary risk of setting an excessively high learning rate during gradient '
       'descent?',
  'code': '',
  'opts': {'A': 'The model will converge too slowly',
           'B': 'The algorithm will get trapped in a shallow local minimum',
           'C': 'The loss function may oscillate or diverge rather than converge',
           'D': 'The model will perfectly memorize the training data'},
  'ans': 'C',
  'expl': 'A very high learning rate causes the weight updates to be large, meaning the algorithm '
          'can repeatedly overshoot the minimum of the loss function, leading to oscillation or '
          'mathematical divergence.'},
 {'q': 'In multiple linear regression, what is the statistical consequence of severe '
       'multicollinearity among predictor variables?',
  'code': '',
  'opts': {'A': 'It reduces the overall R^2 of the model to near zero',
           'B': 'It inflates the variance of the estimated regression coefficients',
           'C': 'It forces all coefficient estimates to be exactly zero',
           'D': 'It converts the model into a non-linear polynomial formulation'},
  'ans': 'B',
  'expl': 'Multicollinearity occurs when independent variables are highly correlated. This causes '
          'the standard errors (variance) of the coefficient estimates to inflate, making the '
          'estimates unstable and sensitive to minor changes in the model.'},
 {'q': 'Which assumption of Ordinary Least Squares (OLS) regression mandates that the variance of '
       'the error terms is constant across all levels of the independent variables?',
  'code': '',
  'opts': {'A': 'Linearity', 'B': 'No autocorrelation', 'C': 'Homoscedasticity', 'D': 'Exogeneity'},
  'ans': 'C',
  'expl': "Homoscedasticity literally translates to 'same variance.' It is an assumption in OLS "
          'regression requiring that the residuals have constant variance at every level of the '
          'predictor variables.'},
 {'q': 'What does a standard Logistic Regression model output prior to applying a classification '
       'threshold?',
  'code': '',
  'opts': {'A': 'An integer representing the class label',
           'B': 'A continuous probability value between 0 and 1',
           'C': 'A log-odds value ranging from 0 to infinity',
           'D': 'A continuous scalar without bounded limits'},
  'ans': 'B',
  'expl': 'The output of the logistic function (sigmoid) maps any real-valued number into a strict '
          'range between 0 and 1. This output is interpreted as the probability of the input '
          'belonging to the positive class.'},
 {'q': 'How does Logistic Regression fundamentally differ from Linear Regression in its '
       'formulation?',
  'code': '',
  'opts': {'A': 'Logistic regression removes independent variables from the model',
           'B': 'Logistic regression applies a non-linear transformation to a linear combination '
                'of inputs',
           'C': 'Logistic regression only accepts categorical input features',
           'D': 'Logistic regression optimizes for Maximum Squared Error'},
  'ans': 'B',
  'expl': 'While both models compute a linear combination of features and weights (z = mx + c), '
          'logistic regression passes this result through a non-linear sigmoid activation function '
          'to map it to a probability.'},
 {'q': 'In the context of logistic regression, if p is the probability of the positive class, what '
       'does the expression ln(p/(1 - p)) represent?',
  'code': '',
  'opts': {'A': 'The decision boundary',
           'B': 'The binary cross-entropy loss',
           'C': 'The log-odds or logit function',
           'D': 'The inverse gradient'},
  'ans': 'C',
  'expl': 'The term ln(p/(1 - p)) is known as the logit function or log-odds. Logistic regression '
          'models the log-odds of a positive outcome as a linear combination of the predictor '
          'variables.'},
 {'q': 'If a logistic regression model evaluates an input and outputs a probability of 0.72, what '
       'is the standard protocol for binary classification assignment?',
  'code': '',
  'opts': {'A': 'Assign to class 1 because 0.72 > 0.0',
           'B': 'Assign to class 1 because 0.72 >= 0.5',
           'C': 'Assign to class 0 because 0.72 is not 1.0',
           'D': 'Reject the classification due to low confidence'},
  'ans': 'B',
  'expl': 'In binary classification, the default decision threshold is typically set at 0.5. '
          'Because 0.72 >= 0.5, the model assigns the input to the positive class (class 1).'},
 {'q': 'Which loss function is minimized when training a standard Logistic Regression model?',
  'code': '',
  'opts': {'A': 'Hinge Loss',
           'B': 'Mean Squared Error (MSE)',
           'C': 'Binary Cross-Entropy (Log Loss)',
           'D': 'Kullback-Leibler Divergence'},
  'ans': 'C',
  'expl': 'Logistic regression minimizes the Binary Cross-Entropy loss (also called Log Loss), '
          'which calculates the performance of a classification model where the output is a '
          'probability value between 0 and 1.'},
 {'q': 'In Logistic Regression, Maximum Likelihood Estimation (MLE) is used to find optimal '
       'parameters. What is the explicit objective of MLE in this context?',
  'code': '',
  'opts': {'A': 'To maximize the variance of the independent variables',
           'B': 'To maximize the joint probability of observing the given training data',
           'C': 'To minimize the sum of squared distances to the decision boundary',
           'D': 'To maximize the margin between the two distinct classes'},
  'ans': 'B',
  'expl': 'Maximum Likelihood Estimation estimates parameters by maximizing the likelihood '
          'function. In logistic regression, it finds the parameter weights that maximize the '
          'joint probability of the observed class labels given the input features.'},
 {'q': 'Which sequence correctly describes the forward operation of a single perceptron?',
  'code': '',
  'opts': {'A': 'Apply activation, sum inputs, multiply by weights',
           'B': 'Multiply inputs by weights, sum the results and bias, apply activation',
           'C': 'Multiply inputs by bias, sum weights, calculate loss',
           'D': 'Calculate loss, apply activation, multiply inputs by bias'},
  'ans': 'B',
  'expl': 'A perceptron first computes a linear combination of its inputs by multiplying them by '
          'respective weights and adding a bias term. This scalar sum is then passed through an '
          'activation function to generate the output.'},
 {'q': 'What specific activation function did the classic Rosenblatt perceptron employ to generate '
       'its final output?',
  'code': '',
  'opts': {'A': 'Sigmoid function',
           'B': 'ReLU function',
           'C': 'Heaviside step function',
           'D': 'Softmax function'},
  'ans': 'C',
  'expl': 'The original perceptron proposed by Frank Rosenblatt used a Heaviside step function, '
          'which outputs 1 if the weighted sum of inputs exceeds a threshold (or is greater than '
          '0), and 0 otherwise.'},
 {'q': 'Which classic logic problem demonstrated the limitations of a single-layer perceptron?',
  'code': '',
  'opts': {'A': 'The AND problem',
           'B': 'The OR problem',
           'C': 'The NOT problem',
           'D': 'The XOR problem'},
  'ans': 'D',
  'expl': 'Marvin Minsky and Seymour Papert demonstrated that a single-layer perceptron cannot '
          'model the Exclusive-OR (XOR) logic gate because the data points in an XOR problem are '
          'not linearly separable.'}]


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