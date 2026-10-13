#!/usr/bin/env python3
"""
IDEAS TIH Quiz Autumn 26 - Deep Learning 1 - interactive terminal quiz
---------------------------------------------------------------
Run:   python deep_learning_1_quiz.py

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

TITLE = "IDEAS TIH Quiz Autumn 26 - Deep Learning 1"
TIME_LIMIT = 60 * 60          # seconds
OPTION_KEYS = ("A", "B", "C", "D")

QUESTIONS = [{'q': 'In linear regression, what does the ordinary least squares (OLS) method minimize?',
  'code': '',
  'opts': {'A': 'Sum of absolute residuals',
           'B': 'Sum of squared residuals',
           'C': 'Mean absolute percentage error',
           'D': 'Cross-entropy loss'},
  'ans': 'B',
  'expl': 'The ordinary least squares (OLS) method is a mathematical optimization technique used '
          'in linear regression. It aims to find the line of best fit by minimizing the sum of the '
          'squared differences (squared residuals) between the observed values in the dataset and '
          'the values predicted by the linear model.'},
 {'q': 'Backpropagation computes gradients using which mathematical principle?',
  'code': '',
  'opts': {'A': 'The chain rule of calculus',
           'B': 'Taylor series expansion',
           'C': 'Bayesian inference',
           'D': 'The law of total expectation'},
  'ans': 'A',
  'expl': 'Backpropagation is the core algorithm used to train neural networks. It applies the '
          'chain rule of calculus to compute the gradient of the loss function with respect to '
          'each weight by moving backward from the output layer to the input layer, avoiding '
          'redundant calculations.'},
 {'q': 'Why is a non-linear activation function essential in a multi-layer perceptron?',
  'code': '',
  'opts': {'A': 'It speeds up gradient computation',
           'B': 'Without it, stacking layers collapses to a single linear transformation',
           'C': 'It prevents overfitting by adding noise',
           'D': 'It normalizes inputs to [0, 1]'},
  'ans': 'B',
  'expl': 'The composition of multiple linear functions results in a linear function. If a neural '
          'network used only linear activation functions, it would only solve linear problems '
          'regardless of depth. Non-linear activation functions allow deep networks to model '
          'complex, non-linear relationships.'},
 {'q': 'During backpropagation through a deep MLP using sigmoid activations, what problem commonly '
       'occurs in early layers?',
  'code': '',
  'opts': {'A': 'Exploding gradients only',
           'B': 'Dead neurons',
           'C': 'Vanishing gradients',
           'D': 'Weight symmetry breaking'},
  'ans': 'C',
  'expl': 'The derivative of the sigmoid activation function has a maximum value of 0.25. As '
          'gradients are multiplied backward layer by layer through the chain rule, these small '
          'values cause the gradient to shrink exponentially. Consequently, gradients vanish to '
          'near-zero, and early layers learn slowly.'},
 {'q': 'A grayscale image of size 128 x 128 pixels is represented as a 2D matrix. What does each '
       'element in this matrix encode?',
  'code': '',
  'opts': {'A': 'A complex number encoding frequency and phase',
           'B': 'A 3-element RGB tuple',
           'C': 'A boolean edge indicator',
           'D': 'An integer pixel intensity (commonly 0--255)'},
  'ans': 'D',
  'expl': 'In digital image processing, a grayscale image is stored as a 2D matrix where each '
          'element (pixel) represents the intensity or brightness of light at that location. For a '
          'standard 8-bit image, these intensities are integers ranging from 0 (black) to 255 '
          '(white).'},
 {'q': 'In a convolutional neural network, what are the learnable parameters in a convolutional '
       'layer?',
  'code': '',
  'opts': {'A': 'The pixel values of the input image',
           'B': 'The kernel (filter) weights and biases',
           'C': 'The stride and padding hyperparameters',
           'D': 'The pooling window size'},
  'ans': 'B',
  'expl': 'Learnable parameters are the values the neural network updates during training to '
          'reduce the error. In a CNN, the network learns to detect features by adjusting the '
          'values (weights) within its filters (kernels) and their corresponding biases. Stride, '
          'padding, and pooling sizes are hyperparameters chosen before training begins.'},
 {'q': 'Applying a 3 x 3 filter with stride 1 and no padding to a 6 x 6 feature map gives an '
       'output of what size?',
  'code': '',
  'opts': {'A': '6 x 6', 'B': '5 x 5', 'C': '4 x 4', 'D': '3 x 3'},
  'ans': 'C',
  'expl': 'The mathematical formula to calculate the output dimension of a convolutional layer '
          'along one axis is: (W - F + 2P)/S + 1, where W is input size (6), F is filter size (3), '
          'P is padding (0), and S is stride (1). Substituting the values: (6 - 3 + 0)/1 + 1 = 3/1 '
          '+ 1 = 4. Thus, the output feature map is 4 x 4.'},
 {'q': 'Compared to an MLP trained on MNIST, a CNN achieves better performance primarily because '
       'of which property?',
  'code': '',
  'opts': {'A': 'CNNs use more neurons and thus more parameters',
           'B': 'CNNs exploit translation invariance and local spatial structure via shared kernel '
                'weights',
           'C': 'CNNs apply data augmentation automatically during training',
           'D': 'CNNs replace softmax with sigmoid in the output layer'},
  'ans': 'B',
  'expl': 'Standard Multi-Layer Perceptrons (MLPs) flatten images into 1D arrays, removing the 2D '
          'spatial relationships between adjacent pixels. Convolutional Neural Networks (CNNs) '
          'process images in their natural 2D format using sliding filters, allowing them to '
          'capture local patterns and recognize them regardless of where they appear in the image '
          'using fewer shared parameters.'},
 {'q': 'When training an MLP on MNIST (28 x 28 grayscale images), what is the typical size of the '
       'input layer?',
  'code': '',
  'opts': {'A': '28', 'B': '784', 'C': '256', 'D': '1024'},
  'ans': 'B',
  'expl': 'A Multi-Layer Perceptron (MLP) requires its input to be a flat, one-dimensional vector. '
          'Therefore, a 2-dimensional image of 28 x 28 pixels must be flattened out. Since 28 x 28 '
          '= 784, the input layer must contain exactly 784 neurons to receive every pixel value of '
          'the image.'},
 {'q': "What does the term 'deep' refer to in deep learning?",
  'code': '',
  'opts': {'A': 'The large size of training datasets',
           'B': 'The multiple hidden layers stacked in the network',
           'C': 'The use of high-dimensional input features',
           'D': 'The depth of the mathematical proofs involved'},
  'ans': 'B',
  'expl': 'In artificial neural networks, depth refers to the number of sequential layers the data '
          'passes through. A deep neural network contains multiple hidden layers situated between '
          'the input layer and the output layer, allowing it to learn complex features.'},
 {'q': 'What is the primary objective of gradient descent when applied to a neural network?',
  'code': '',
  'opts': {'A': 'To maximize the activation outputs of the hidden layers',
           'B': 'To minimize the selected loss function by updating network weights',
           'C': 'To increase the dimensionality of the input data',
           'D': 'To compute the second derivative of the error function'},
  'ans': 'B',
  'expl': 'Gradient descent is a first-order iterative optimization algorithm. Its purpose in '
          'neural network training is to find a local minimum of a differentiable function, such '
          'as the loss function, by iteratively moving the parameters (weights and biases) in the '
          'direction of steepest descent, which is the negative of the gradient.'},
 {'q': 'In the context of training deep learning models, what role does the learning rate '
       'hyperparameter serve?',
  'code': '',
  'opts': {'A': 'It determines the size of the step taken towards the minimum of the loss function '
                'during each iteration',
           'B': 'It defines the number of hidden layers in the network architecture',
           'C': 'It specifies the ratio of training data to validation data',
           'D': 'It controls the maximum value an activation function can output'},
  'ans': 'A',
  'expl': 'The learning rate is a scalar multiplier used in optimization algorithms like gradient '
          'descent. It scales the gradient to dictate the magnitude of the update applied to the '
          "model's weights during each iteration. A learning rate that is too high can cause the "
          'model to diverge, while one that is too low results in increased training times.'},
 {'q': 'Which of the following represents the correct mathematical formulation for Mean Squared '
       'Error (MSE) over a dataset of N samples, where y_i is the true value and y_hat_i is the '
       'predicted value?',
  'code': '',
  'opts': {'A': '1/N Sum_(i = 1)^N (y_i - y_hat_i)',
           'B': '1/N Sum_(i = 1)^N|y_i - y_hat_i|',
           'C': '1/N Sum_(i = 1)^N (y_i - y_hat_i)^2',
           'D': 'Sum_(i = 1)^N log(y_i - y_hat_i)^2'},
  'ans': 'C',
  'expl': 'Mean Squared Error (MSE) is calculated by taking the average of the squared differences '
          'between predicted and actual values. The squaring ensures that positive and negative '
          'errors do not cancel each other out and applies a heavier penalty to larger errors. '
          'Option C is the correct standard formula.'},
 {'q': 'Why is the Mean Squared Error (MSE) loss function for linear regression guaranteed to '
       'converge to a global minimum when using gradient descent with an appropriate learning '
       'rate?',
  'code': '',
  'opts': {'A': 'The MSE function is strictly concave',
           'B': 'The MSE function is a convex function with respect to the weights',
           'C': 'The input data is always normalized to a zero mean',
           'D': 'Linear regression models use non-linear activation functions'},
  'ans': 'B',
  'expl': 'The Mean Squared Error surface for a linear regression model forms a multidimensional '
          'parabola (a convex function). A key property of convex functions is that any local '
          'minimum is also the global minimum. Therefore, gradient descent will locate this global '
          'minimum, provided the learning rate is not large.'},
 {'q': 'The closed-form analytical solution for Ordinary Least Squares (OLS) is given by beta = '
       '(X^TX)^(-1) X^Ty. Under what condition does this equation fail to produce a unique '
       'solution?',
  'code': '',
  'opts': {'A': 'When the target vector y contains negative values',
           'B': 'When the design matrix X has more columns (features) than rows (samples), causing '
                'X^TX to be non-invertible',
           'C': 'When the error terms are normally distributed',
           'D': 'When the learning rate hyperparameter is undefined'},
  'ans': 'B',
  'expl': 'The matrix (X^TX) must be invertible (non-singular) to compute the closed-form OLS '
          'solution. If there are more features than observations (p > n), or if perfect '
          'multicollinearity exists among the features, the matrix X^TX will not have full rank '
          'and thus cannot be inverted, requiring regularization techniques like Ridge regression '
          'to resolve.'},
 {'q': 'Ridge regression alters the standard OLS objective by adding a penalty term. Which '
       'mathematical expression represents the Ridge regression cost function?',
  'code': '',
  'opts': {'A': 'MSE + lambda Sum|beta_j|',
           'B': 'MSE + lambda Sum beta_j^2',
           'C': 'MSE + lambda max(|beta_j|)',
           'D': 'MSE x exp(-lambda beta)'},
  'ans': 'B',
  'expl': 'Ridge regression applies L2 regularization to the linear regression model. It modifies '
          'the standard Mean Squared Error loss by adding a penalty term proportional to the sum '
          'of the squared coefficients (Sum beta_j^2). This encourages the model to learn smaller, '
          'more distributed weight values, reducing overfitting.'},
 {'q': 'How does Stochastic Gradient Descent (SGD) differ from Batch Gradient Descent in terms of '
       'computing the gradient?',
  'code': '',
  'opts': {'A': 'SGD computes the gradient using the entire dataset per update, whereas Batch uses '
                'one sample',
           'B': 'SGD computes the gradient using a single, randomly chosen data sample per update, '
                'whereas Batch uses the entire dataset',
           'C': 'SGD does not use gradients; it uses random search',
           'D': 'SGD requires the dataset to be sorted before computing gradients'},
  'ans': 'B',
  'expl': 'Batch Gradient Descent calculates the error for every example in the training dataset '
          'before performing an update to the model weights. Stochastic Gradient Descent (SGD) '
          'estimates the gradient and updates the weights using only one randomly selected data '
          'sample per iteration, resulting in faster but noisier updates.'},
 {'q': 'When evaluating a linear regression model, what does an R-squared (R^2) value of 0.0 '
       'indicate?',
  'code': '',
  'opts': {'A': 'The model predicts the target variable perfectly',
           'B': 'The model explains none of the variance in the target variable around its mean',
           'C': 'The model has encountered a divide-by-zero error',
           'D': 'The target variable contains only negative values'},
  'ans': 'B',
  'expl': 'The R^2 coefficient of determination measures the proportion of variance in the '
          'dependent variable that can be explained by the independent variables. An R^2 of 1.0 '
          'indicates perfect prediction. An R^2 of 0.0 indicates that the model performs no better '
          'than a baseline model that simply predicts the mean of the target variable constantly.'},
 {'q': 'In a neural network trained with gradient descent, why might feature scaling (e.g., '
       'standardizing inputs to zero mean and unit variance) accelerate convergence?',
  'code': '',
  'opts': {'A': 'It forces the neural network to act as a linear classifier',
           'B': 'It reduces the total number of parameters in the network',
           'C': 'It makes the loss surface more spherical, preventing the optimizer from '
                'oscillating inefficiently across elongated contours',
           'D': 'It automatically sets the learning rate to an optimal scalar value'},
  'ans': 'C',
  'expl': 'If input features exist on different scales, the resulting loss function landscape will '
          'be elongated (elliptical). Gradient descent on an elliptical surface tends to oscillate '
          'across the steep axes while making slow progress along the flat axes. Standardizing '
          'features transforms the loss surface to be more spherical, allowing the gradient to '
          'point more directly at the minimum.'},
 {'q': "Newton's method is a second-order optimization algorithm. Why is it rarely used directly "
       'to train deep neural networks?',
  'code': '',
  'opts': {'A': 'It cannot optimize non-convex functions',
           'B': 'It requires the computation and inversion of the Hessian matrix, which is '
                'computationally infeasible for networks with millions of parameters',
           'C': 'It relies exclusively on numerical approximations of gradients rather than '
                'analytical backpropagation',
           'D': 'It is mathematically incapable of utilizing a learning rate'},
  'ans': 'B',
  'expl': "Newton's method involves calculating the inverse of the Hessian matrix (the matrix of "
          'second-order partial derivatives). For a deep neural network with N parameters, the '
          'Hessian is an N x N matrix. Storing and inverting this matrix requires O(N^2) memory '
          'and O(N^3) computational time, which is computationally infeasible for modern networks '
          'featuring millions or billions of parameters.'},
 {'q': "In the training cycle of a neural network, what is the 'forward pass'?",
  'code': '',
  'opts': {'A': 'The process of updating the weights based on the computed gradients',
           'B': 'The calculation of the output predictions from the input data moving sequentially '
                'through the network layers',
           'C': 'The propagation of the error signal from the output layer back to the input layer',
           'D': 'The initialization of the network weights before training begins'},
  'ans': 'B',
  'expl': 'During the forward pass (or forward propagation), the input data is fed into the neural '
          'network and processed layer by layer through linear transformations and activation '
          'functions until it yields an output prediction. This prediction is subsequently used to '
          'compute the loss.'},
 {'q': 'Suppose a network has an intermediate variable z which depends on parameter w, and the '
       'final loss is L. According to the chain rule used in backpropagation, how is dL/dw '
       'calculated?',
  'code': '',
  'opts': {'A': 'dL/dw = dL/dz + dz/dw',
           'B': 'dL/dw = dL/dz x dz/dw',
           'C': 'dL/dw = (dL/dz)/(dz/dw)',
           'D': 'dL/dw = d^2L/dzdw'},
  'ans': 'B',
  'expl': 'The chain rule of calculus states that the derivative of a composite function is the '
          'product of the derivatives of the constituent functions. In backpropagation, to find '
          'the gradient of the loss L with respect to a weight w, one multiplies the gradient of '
          'the loss with respect to the intermediate output z by the gradient of z with respect to '
          'w.'},
 {'q': 'What mechanism physically prevents early layers of a deep Multi-Layer Perceptron from '
       'learning effectively when affected by the vanishing gradient problem?',
  'code': '',
  'opts': {'A': 'The optimizer forces the learning rate to zero',
           'B': 'The magnitude of the partial derivatives with respect to the weights in those '
                'layers approaches zero, resulting in negligible weight updates',
           'C': 'The input data becomes perfectly correlated, causing the Hessian matrix to become '
                'singular',
           'D': 'The activation functions output infinite values, causing numeric overflow'},
  'ans': 'B',
  'expl': 'The weight update in gradient descent is directly proportional to the calculated '
          'gradient (Delta w = - alpha dL/dw). If the gradient signal diminishes exponentially as '
          'it propagates backwards (the vanishing gradient problem), the computed gradients for '
          'the early layers will be close to zero. Consequently, the weights are minimally '
          'adjusted, and the layer stops learning.'},
 {'q': 'Which technique is most commonly employed to directly prevent the exploding gradient '
       'problem during the training of Recurrent Neural Networks (RNNs)?',
  'code': '',
  'opts': {'A': 'Max pooling',
           'B': 'Gradient clipping',
           'C': 'Label smoothing',
           'D': 'Using a larger learning rate'},
  'ans': 'B',
  'expl': 'Exploding gradients occur when large error gradients accumulate, leading to unstable '
          'weight updates. Gradient clipping is a standard intervention technique that sets a '
          'threshold value; if the norm of a computed gradient exceeds this threshold, the '
          'gradient vector is scaled down to match the threshold limit, ensuring numeric '
          'stability.'},
 {'q': 'A computational graph represents the mathematical operations in a neural network. In this '
       'framework, what do the edges typically represent?',
  'code': '',
  'opts': {'A': 'The mathematical functions (e.g., addition, multiplication)',
           'B': 'The flow of data (tensors) between operations',
           'C': 'The specific loss function being optimized',
           'D': 'The learning rate parameters'},
  'ans': 'B',
  'expl': 'In a computational graph used by deep learning frameworks, the nodes represent '
          'mathematical operations (such as matrix multiplication or an activation function), '
          'while the edges represent the tensors (data arrays) flowing from one operation to the '
          'next.'},
 {'q': 'Consider a fully connected layer with an input vector x in R^m, a weight matrix W in R^(n '
       'x m), and an output vector y = Wx. What are the dimensions of the Jacobian matrix dy/dx?',
  'code': '',
  'opts': {'A': 'n x m', 'B': 'm x n', 'C': 'm x m', 'D': 'n x n'},
  'ans': 'A',
  'expl': 'The Jacobian matrix contains the first-order partial derivatives for a vector-valued '
          'function. Since y is an n-dimensional vector and x is an m-dimensional vector, the '
          'Jacobian dy/dx will possess a row for each element of y and a column for each element '
          'of x. Thus, the dimensions are n x m. Specifically, (d(Wx))/dx = W, which is an n x m '
          'matrix.'},
 {'q': 'In high-dimensional non-convex loss landscapes, such as those found in deep neural '
       'networks, what type of critical point is statistically most frequent when the gradient '
       'approaches zero?',
  'code': '',
  'opts': {'A': 'Global minimum', 'B': 'Local minimum', 'C': 'Saddle point', 'D': 'Global maximum'},
  'ans': 'C',
  'expl': 'Mathematical analysis of high-dimensional error surfaces shows that saddle points are '
          'exponentially more common than local minima. A critical point requires the gradient to '
          'be zero. For this point to be a local minimum, the second derivative must be positive '
          'in all orthogonal directions. In a system with millions of dimensions, the probability '
          'of every single dimension curving upwards is low; most often, some curve up and some '
          'curve down, defining a saddle point.'},
 {'q': 'Why does training a deep neural network consume significantly more memory than evaluating '
       '(performing inference on) the same network?',
  'code': '',
  'opts': {'A': 'Inference forces the network to dynamically increase its weight matrix sizes',
           'B': 'Training requires caching the intermediate activation values from the forward '
                'pass to compute gradients during backpropagation',
           'C': 'Inference uses integers while training uses floating-point numbers',
           'D': 'Training requires duplicating the dataset in RAM for every epoch'},
  'ans': 'B',
  'expl': "During inference, once a layer's output is calculated, the previous layer's activations "
          'can be discarded from memory to save space. However, during training, backpropagation '
          'requires the specific activation values computed during the forward pass to evaluate '
          'the derivatives via the chain rule. Storing these intermediate activations for every '
          'layer across the entire batch increases memory consumption.'},
 {'q': 'What is the theoretical output range of the standard logistic sigmoid activation function?',
  'code': '',
  'opts': {'A': '[ - 1, 1]', 'B': '[0, 1]', 'C': '[0, inf)', 'D': '(-inf, inf)'},
  'ans': 'B',
  'expl': 'The logistic sigmoid function is defined mathematically as sigma(x) = 1/(1 + e^(-x)). '
          'As x approaches positive infinity, the denominator approaches 1, making the output '
          'approach 1. As x approaches negative infinity, the denominator grows large, making the '
          'output approach 0. Therefore, its range is strictly between 0 and 1.'},
 {'q': 'What is the theoretical output range of the hyperbolic tangent (tanh) activation function?',
  'code': '',
  'opts': {'A': '[ - 1, 1]', 'B': '[0, 1]', 'C': '[ - 0.5, 0.5]', 'D': '[0, inf)'},
  'ans': 'A',
  'expl': 'The hyperbolic tangent function, commonly denoted as tanh(x), maps any real-valued '
          'number into the range of -1 to 1. Unlike the sigmoid function, its outputs are '
          'zero-centered, which generally makes optimization easier in practice by keeping the '
          'mean of the activations closer to zero.'}]


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