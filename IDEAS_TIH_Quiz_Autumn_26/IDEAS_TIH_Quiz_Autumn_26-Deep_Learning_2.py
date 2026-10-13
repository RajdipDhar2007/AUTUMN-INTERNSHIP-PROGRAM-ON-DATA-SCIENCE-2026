#!/usr/bin/env python3
"""
IDEAS TIH Quiz Autumn 26 - Deep Learning 2 - interactive terminal quiz
---------------------------------------------------------------
Run:   python deep_learning_2_quiz.py

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

TITLE = "IDEAS TIH Quiz Autumn 26 - Deep Learning 2"
TIME_LIMIT = 60 * 60          # seconds
OPTION_KEYS = ("A", "B", "C", "D")

QUESTIONS = [{'q': 'Which of the following functions defines the standard Rectified Linear Unit (ReLU)?',
  'code': '',
  'opts': {'A': 'f(x) = log(1 + e^x)',
           'B': 'f(x) = max(0, x)',
           'C': 'f(x) = |x|',
           'D': 'f(x) = 1/(1 + e^(-x))'},
  'ans': 'B',
  'expl': 'The standard Rectified Linear Unit (ReLU) is defined as f(x) = max(0, x). It outputs '
          'the input value directly if the input is positive; otherwise, it outputs exactly zero. '
          'This piecewise linear property allows it to compute rapidly and helps mitigate the '
          'vanishing gradient problem for positive values.'},
 {'q': "The 'Dying ReLU' problem refers to a situation where neurons permanently output zero "
       'during training. What primarily causes this phenomenon?',
  'code': '',
  'opts': {'A': 'A learning rate that is too small, causing weight updates to freeze entirely',
           'B': 'The input data containing too many positive numerical values',
           'C': "A large gradient causing a weight update that shifts the neuron's pre-activation "
                'value into the negative domain for all training examples',
           'D': 'The absence of bias terms in the fully connected layer'},
  'ans': 'C',
  'expl': 'If a ReLU neuron receives a large weight update (often due to a high learning rate), '
          'its weights may adjust such that the pre-activation output w^Tx + b is negative for '
          'every data point in the dataset. Because the derivative of ReLU for negative inputs is '
          'zero, the neuron will pass a gradient of zero backward. Consequently, its weights will '
          "never update again, rendering the neuron permanently 'dead'."},
 {'q': 'How does the Leaky ReLU activation function differ mathematically from the standard ReLU?',
  'code': '',
  'opts': {'A': 'It bounds the positive output to a maximum value of 1',
           'B': 'It applies a small, non-zero gradient for negative inputs instead of outputting '
                'absolute zero',
           'C': 'It introduces an exponential curve for positive inputs',
           'D': 'It rounds negative inputs to the nearest integer'},
  'ans': 'B',
  'expl': 'Leaky ReLU was designed to address the dying ReLU problem. It is defined as f(x) = '
          'max(alpha x, x), where alpha is a small constant (e.g., 0.01). For negative inputs, it '
          'outputs a small linear value instead of zero. This ensures the derivative is non-zero, '
          'allowing the network to continue updating the corresponding weights.'},
 {'q': 'Which property of the softmax activation function ensures it is suitable for mutually '
       'exclusive multi-class classification tasks?',
  'code': '',
  'opts': {'A': 'It maps all input values strictly to either 0 or 1, removing continuous '
                'probabilities',
           'B': 'It computes the element-wise absolute value of the input vector',
           'C': 'It exponentiates the inputs and normalizes them, ensuring the output vector '
                'components sum exactly to 1.0',
           'D': 'It transforms a sequence of numbers into a single scalar value representing '
                'variance'},
  'ans': 'C',
  'expl': 'The softmax function transforms an arbitrary vector of real numbers (logits) into a '
          'probability distribution. It does this by exponentiating each element (making them '
          'positive) and dividing by the sum of all exponentiated elements. This normalization '
          'guarantees that the resulting values lie in (0, 1) and sum to 1.0, which represents a '
          'categorical probability distribution.'},
 {'q': 'What is the maximum mathematical value of the first derivative of the logistic sigmoid '
       'function, sigma(x)?',
  'code': '',
  'opts': {'A': '1.0', 'B': '0.5', 'C': '0.25', 'D': '0.0'},
  'ans': 'C',
  'expl': 'The derivative of the logistic sigmoid function sigma(x) is sigma(x)(1 - sigma(x)). '
          'Because sigma(x) outputs values strictly between 0 and 1, we can view this as '
          'evaluating y(1 - y) for y in (0, 1). The maximum of the parabola f(y) = y - y^2 occurs '
          'at y = 0.5. Substituting 0.5 yields 0.5(1 - 0.5) = 0.25. This maximum limit is the '
          'reason standard sigmoid networks suffer from vanishing gradients.'},
 {'q': 'Which equation correctly represents the mathematical relationship between the hyperbolic '
       'tangent tanh(x) and the logistic sigmoid sigma(x)?',
  'code': '',
  'opts': {'A': 'tanh(x) = 2 sigma(2x) - 1',
           'B': 'tanh(x) = sigma(x)^2',
           'C': 'tanh(x) = (sigma(x))/(1 - sigma(x))',
           'D': 'tanh(x) = 1 - 2 sigma(-x)'},
  'ans': 'A',
  'expl': 'The hyperbolic tangent is a scaled and shifted version of the logistic sigmoid '
          'function. By writing out the definitions: tanh(x) = (e^x - e^(-x))/(e^x + e^(-x)) and '
          'substituting terms, it simplifies to 2 sigma(2x) - 1. This means tanh(x) has the same '
          'fundamental curve shape as the sigmoid but spans [ - 1, 1] and features a steeper '
          'gradient at the origin.'},
 {'q': 'The Swish activation function, discovered via automated search techniques, is defined as '
       'f(x) = x * sigma(beta x). What unique property distinguishes it from the ReLU function?',
  'code': '',
  'opts': {'A': 'It is perfectly linear for all positive values of x',
           'B': 'It is non-monotonic, meaning the output decreases slightly for small negative '
                'inputs before approaching zero',
           'C': 'Its derivative is exactly zero for all inputs less than zero',
           'D': 'It maps all outputs to the range [ - 1, 1]'},
  'ans': 'B',
  'expl': 'Unlike ReLU, which is strictly zero for x and monotonically increasing for x > 0, Swish '
          'is a smooth, non-monotonic function. For small negative values of x, the multiplication '
          'by the small positive sigmoid output causes the function to dip below zero (creating a '
          '"bump") before asymptoting to zero as x -> - inf. This property aids gradient flow and '
          'generalization in deep networks.'},
 {'q': 'In the architecture of a Convolutional Neural Network, what is the primary computational '
       'objective of a max-pooling layer?',
  'code': '',
  'opts': {'A': 'To apply non-linear activations to the feature map',
           'B': 'To increase the resolution of the image for classification',
           'C': 'To reduce spatial dimensions (downsample), thereby reducing the number of '
                'parameters and computation in subsequent layers',
           'D': 'To convert the image from RGB to grayscale'},
  'ans': 'C',
  'expl': 'Pooling layers summarize the presence of features in patches of the feature map. '
          'Max-pooling outputs the maximum value from a specified window (e.g., 2 x 2). This '
          'effectively downsamples the feature maps, halving their spatial dimensions, which '
          'decreases the number of weights required in later dense layers and provides a degree of '
          'translation invariance.'},
 {'q': "When configuring a convolutional layer, applying 'same' padding to a spatial dimension "
       'indicates what behavior?',
  'code': '',
  'opts': {'A': 'The layer copies the exact pixel values from the input matrix to the output '
                'matrix without convolution',
           'B': 'Sufficient zero-padding is added to the borders of the input so that the output '
                'feature map has the same spatial dimensions as the input (assuming a stride of 1)',
           'C': 'The input is padded with copies of the central pixel',
           'D': 'The filter weights are padded with zeros to match the image size'},
  'ans': 'B',
  'expl': "In CNN terminology, 'valid' padding means no padding is added, which shrinks the "
          "spatial dimensions of the output after convolution. 'Same' padding means the algorithm "
          'dynamically adds zeros around the perimeter of the input matrix so that a convolution '
          'operation using a stride of 1 will yield an output feature map of the same width and '
          'height as the input.'},
 {'q': 'Based on the table below detailing a Convolutional Layer, calculate the total number of '
       'learnable parameters (including biases). Layer properties: - Filter Size: 3 x 3 - Input '
       'Channels: 16 - Output Channels (Filters): 32',
  'code': 'Convolutional Layer Specification\n'
          '+-------------------------------------+-------+\n'
          '| Parameter Type                      | Value |\n'
          '+-------------------------------------+-------+\n'
          '| Filter Spatial Size                 | 3x3   |\n'
          '| Input Channels                      | 16    |\n'
          '| Number of Filters (Output Channels) | 32    |\n'
          '+-------------------------------------+-------+',
  'opts': {'A': '4608', 'B': '4640', 'C': '1536', 'D': '288'},
  'ans': 'B',
  'expl': 'The formula for the number of parameters in a convolutional layer is: (F x F x C_in) x '
          'C_out + C_out, where F is the spatial filter size, C_in is the number of input '
          'channels, and C_out is the number of filters. Substituting the values: (3 x 3 x 16) x '
          '32 + 32 = (144) x 32 + 32 = 4608 + 32 = 4640.'},
 {'q': 'Consider an input image of size 32 x 32. If it is processed by a valid convolutional layer '
       'with a 5 x 5 filter and a stride of 3, what is the spatial size of the output feature map?',
  'code': '',
  'opts': {'A': '10 x 10', 'B': '11 x 11', 'C': '9 x 9', 'D': '8 x 8'},
  'ans': 'A',
  'expl': 'The output size formula is (W - F + 2P)/S + 1, where W is input size (32), F is filter '
          'size (5), P is padding (0 for valid), and S is stride (3). Thus, (32 - 5 + 0)/3 + 1 = '
          '27/3 + 1 = 9 + 1 = 10. The output size is 10 x 10.'},
 {'q': 'In modern CNN architectures like ResNet, what is the primary geometric purpose of applying '
       'a 1 x 1 convolution layer?',
  'code': '',
  'opts': {'A': 'To extract large spatial features like edges and corners',
           'B': 'To increase the resolution of the image dimensions',
           'C': 'To change the depth (number of channels) of the feature map, often used for '
                'dimensionality reduction',
           'D': 'To apply max pooling across the spatial dimensions'},
  'ans': 'C',
  'expl': 'A 1 x 1 convolution operates on a single spatial pixel location at a time but spans '
          'across all input channels. It acts as a fully connected layer applied to each pixel '
          'independently across the depth axis. Its primary purpose is channel-wise pooling or '
          'dimensionality reduction, modifying the number of channels without altering the spatial '
          'dimensions (height and width).'},
 {'q': 'Consider two sequential 3 x 3 convolutional layers (stride 1, no padding) applied to an '
       'input image. What is the effective receptive field on the original image for a single '
       'activation element in the output of the second layer?',
  'code': '',
  'opts': {'A': '3 x 3', 'B': '5 x 5', 'C': '6 x 6', 'D': '7 x 7'},
  'ans': 'B',
  'expl': 'The receptive field is the region of the input space that affects a particular unit. A '
          'single pixel in the output of the first 3 x 3 layer observes a 3 x 3 region of the '
          'original input. A single pixel in the output of the second layer observes a 3 x 3 '
          "region of the first layer's output. Tracing this back, the 3 x 3 grid in layer 1 "
          'requires a 5 x 5 region in the original input to be computed. In general, stacking N '
          'layers of F x F filters yields a receptive field of (F - 1) x N + 1. Here, (3 - 1) x 2 '
          '+ 1 = 5.'},
 {'q': 'Dilated (or atrous) convolutions are sometimes used instead of standard convolutions with '
       'max-pooling. What specific advantage do they provide?',
  'code': '',
  'opts': {'A': 'They exponentially expand the receptive field without decreasing spatial '
                'resolution or adding parameters',
           'B': 'They decrease the receptive field to focus only on micro-textures',
           'C': 'They eliminate the need for activation functions',
           'D': 'They perfectly reconstruct compressed images into high-resolution formats'},
  'ans': 'A',
  'expl': 'Dilated convolutions introduce spaces (holes) between the kernel elements. A 3 x 3 '
          'kernel with a dilation rate of 2 spans a 5 x 5 area while still only having 9 '
          'parameters. This allows the network to capture broader contextual information (a larger '
          'receptive field) without reducing the spatial resolution of the feature maps, which is '
          'useful for tasks like semantic segmentation.'},
 {'q': 'How is a standard RGB color image computationally represented in deep learning libraries '
       'such as PyTorch or TensorFlow?',
  'code': '',
  'opts': {'A': 'As a 2-dimensional tensor of string values',
           'B': 'As a 1-dimensional array of complex numbers',
           'C': 'As a 3-dimensional tensor (e.g., Height x Width x 3 channels)',
           'D': 'As three entirely separate file objects processed independently'},
  'ans': 'C',
  'expl': 'A color image contains three color channels (Red, Green, Blue) for each spatial pixel. '
          'Therefore, it is represented as a 3-dimensional mathematical array (tensor). The '
          'dimensions are typically ordered as (Channels x Height x Width) in PyTorch, or (Height '
          'x Width x Channels) in TensorFlow/Keras.'},
 {'q': 'Before feeding a standard 28 x 28 RGB image into a traditional Multi-Layer Perceptron '
       '(fully connected network), the data must be flattened. What is the size of the resulting '
       '1D input vector?',
  'code': '',
  'opts': {'A': '784', 'B': '2352', 'C': '28', 'D': '3'},
  'ans': 'B',
  'expl': 'An RGB image has three color channels. The total number of pixels in a 28 x 28 image is '
          '784. Since each pixel has 3 values (one for red, green, and blue), the total number of '
          'scalar values is 784 x 3 = 2352. A fully connected network requires a 1D input vector, '
          'so the 3D tensor is unrolled into a flat vector of size 2352.'},
 {'q': 'Consider an MLP with an input layer of 10 neurons, one hidden layer of 20 neurons, and an '
       'output layer of 5 neurons. Assuming every hidden and output neuron has a bias term, what '
       'is the total number of learnable parameters in this network?',
  'code': '',
  'opts': {'A': '325', 'B': '305', 'C': '200', 'D': '35'},
  'ans': 'A',
  'expl': 'The number of parameters between fully connected layers is calculated as (N_in x N_out) '
          '+ N_out to account for the bias terms. From Input to Hidden: (10 x 20) + 20 = 220. From '
          'Hidden to Output: (20 x 5) + 5 = 105. Total parameters: 220 + 105 = 325.'},
 {'q': 'Which loss function is the standard choice for multi-class classification problems where '
       'the output layer utilizes a softmax activation?',
  'code': '',
  'opts': {'A': 'Mean Squared Error',
           'B': 'Categorical Cross-Entropy',
           'C': 'Hinge Loss',
           'D': 'Mean Absolute Percentage Error'},
  'ans': 'B',
  'expl': 'Categorical Cross-Entropy is designed to measure the divergence between two probability '
          'distributions: the true distribution (often a one-hot encoded vector) and the predicted '
          'distribution (the softmax output). It applies a logarithmic penalty to incorrect '
          'predictions, forcing the predicted probability of the correct class toward 1.0.'},
 {'q': 'How does the dropout technique act as a regularization method during the training of '
       'neural networks?',
  'code': '',
  'opts': {'A': 'It adds an L1 penalty to the loss function based on weight magnitudes',
           'B': 'It randomly sets a fraction of the neuron activations to zero at each forward '
                'pass, forcing the network to learn redundant representations',
           'C': 'It removes outliers from the training dataset before calculating the gradient',
           'D': 'It stops the training process early when validation loss begins to rise'},
  'ans': 'B',
  'expl': 'Dropout prevents units from co-adapting too much. By stochastically dropping out '
          '(zeroing) a random subset of neurons during each training step, the network cannot rely '
          'on any single neuron or specific combination of neurons to extract features. This '
          'creates an ensemble effect that mitigates overfitting.'},
 {'q': "In neural network training terminology, what exactly does one 'epoch' represent?",
  'code': '',
  'opts': {'A': 'One forward pass and one backward pass of a single batch of data',
           'B': 'One complete pass through the entire training dataset',
           'C': 'The point at which the validation loss reaches its absolute minimum',
           'D': "A single update to the network's weight matrices"},
  'ans': 'B',
  'expl': 'An epoch is defined as one full cycle through the entire provided training dataset. If '
          'a dataset of 1000 images is divided into batches of 100, the network will perform 10 '
          'batch updates to complete one epoch.'},
 {'q': 'Analyze the accompanying training log table. At which recorded epoch does the model begin '
       'to exhibit clear signs of overfitting?',
  'code': 'Training Log\n'
          '+-------+---------------+-----------------+\n'
          '| Epoch | Training Loss | Validation Loss |\n'
          '+-------+---------------+-----------------+\n'
          '| 10    | 0.45          | 0.50            |\n'
          '| 20    | 0.30          | 0.48            |\n'
          '| 30    | 0.15          | 0.65            |\n'
          '| 40    | 0.05          | 0.85            |\n'
          '+-------+---------------+-----------------+',
  'opts': {'A': 'Epoch 10', 'B': 'Epoch 20', 'C': 'Epoch 30', 'D': 'Epoch 40'},
  'ans': 'C',
  'expl': 'Overfitting occurs when a model learns the training data too well, capturing noise and '
          'losing its ability to generalize to unseen data. This is typically observed when the '
          'training loss continues to decrease while the validation loss begins to increase. In '
          'the table, validation loss reaches its minimum around Epoch 20, but by Epoch 30, it has '
          'increased from 0.48 to 0.65, indicating the onset of overfitting.'},
 {'q': 'Batch Normalization is applied to intermediate layers of deep networks. Mathematically, '
       'what operation does it perform on the mini-batch of activations before applying the '
       'learned scale and shift parameters?',
  'code': '',
  'opts': {'A': 'It calculates the exponential moving average of all previous epochs',
           'B': 'It centers the activations by subtracting the mini-batch mean and scales them by '
                'dividing by the mini-batch standard deviation',
           'C': 'It applies a softmax function across the batch dimension',
           'D': 'It forces all negative activations to zero'},
  'ans': 'B',
  'expl': 'Batch Normalization operates on the activations of a given layer for each mini-batch. '
          'It standardizes the data by computing the mean and variance of that batch. It subtracts '
          'the mean (centering) and divides by the standard deviation (scaling). Finally, it '
          'applies two learnable parameters (gamma and beta) to allow the network to retain '
          'representational power.'},
 {'q': 'When using Xavier (Glorot) initialization for a dense layer with N_in inputs and N_out '
       'outputs, weights are drawn from a distribution with a specific variance. What is the '
       'theoretical mathematical justification for this variance?',
  'code': '',
  'opts': {'A': 'It minimizes the L2 norm of the weight matrix',
           'B': 'It guarantees that the gradients evaluate exactly to zero at the start of '
                'training',
           'C': 'It ensures the variance of the activations and the gradients remains roughly '
                'constant across all layers during forward and backward passes',
           'D': 'It limits the maximum output of any neuron to 1.0'},
  'ans': 'C',
  'expl': 'If weights are initialized too small, activation variance shrinks to zero (vanishing '
          'gradients). If too large, the variance explodes. Xavier initialization calculates the '
          'variance of the weights as Var(W) = 2/(N_in + N_out). Under the assumption of linear '
          'activations, this variance ensures that the signal does not magnify or vanish as it '
          'propagates forward, and the gradient does not explode or vanish as it propagates '
          'backward.'},
 {'q': 'Data augmentation is frequently used when training deep convolutional networks on image '
       'datasets. What is its primary objective?',
  'code': '',
  'opts': {'A': 'To reduce the physical memory size of the dataset on the hard drive',
           'B': 'To artificially increase the diversity and size of the training set by applying '
                'random transformations, thereby reducing overfitting',
           'C': 'To convert the dataset into a format readable by the GPU',
           'D': 'To apply backpropagation before the main training loop starts'},
  'ans': 'B',
  'expl': 'Data augmentation involves applying random, realistic transformations (like rotations, '
          'flips, or color shifts) to training images on the fly. This effectively presents the '
          'network with a larger and more diverse set of examples, preventing it from memorizing '
          'exact pixel layouts and improving its ability to generalize to new data.'},
 {'q': "Which statement accurately describes the 'momentum' technique used alongside gradient "
       'descent algorithms?',
  'code': '',
  'opts': {'A': 'It calculates the second derivative of the loss function to determine the exact '
                'minimum',
           'B': 'It accumulates an exponentially decaying moving average of past gradients to '
                'smooth out oscillations and accelerate convergence along consistent directions',
           'C': 'It randomly drops gradients that fall below a certain threshold',
           'D': 'It scales the learning rate independently for each parameter based on historical '
                'updates'},
  'ans': 'B',
  'expl': 'Standard gradient descent can oscillate in regions of the loss landscape with high '
          'curvature. Momentum addresses this by incorporating a fraction of the previous update '
          'vector into the current update. This moving average acts like physical inertia, damping '
          'oscillations in rapidly changing dimensions while building up speed in dimensions where '
          'the gradient consistently points in the same direction.'},
 {'q': 'Consider the categorical cross-entropy loss function L = - Sum y_i log(y_hat_i) used '
       'alongside a softmax output layer. Why is this specific pairing mathematically advantageous '
       'during backpropagation?',
  'code': '',
  'opts': {'A': 'The loss function is identically equal to zero for all inputs, speeding up '
                'calculation',
           'B': 'The derivative of the loss with respect to the pre-softmax logits simplifies '
                'cleanly to (y_hat_i - y_i), avoiding numerical instability',
           'C': 'The softmax function cancels out the negative sign in the loss formulation',
           'D': 'It enables the network to bypass the chain rule entirely'},
  'ans': 'B',
  'expl': 'The derivative of the softmax function is complex because its output depends on all '
          'inputs (a full Jacobian). However, when paired with categorical cross-entropy, the '
          'derivatives of the logarithm and the exponential terms interact and simplify. The '
          'gradient of the loss with respect to the input logits z_i reduces to the form of '
          '(predicted probability - true label), or y_hat_i - y_i. This numerical stability '
          'prevents gradient explosion or vanishing near the extremes.'},
 {'q': "When processing categorical labels (e.g., 'cat', 'dog', 'bird') for a neural network, what "
       "does 'one-hot encoding' achieve?",
  'code': '',
  'opts': {'A': 'It scales the string data down to a range between 0 and 1',
           'B': 'It transforms the labels into sparse binary vectors where only the index '
                'corresponding to the class is set to 1, and all others are 0',
           'C': 'It removes the least frequent categories from the dataset',
           'D': 'It maps the categories to a continuous scalar progression (1, 2, 3)'},
  'ans': 'B',
  'expl': 'Neural networks require numerical input and cannot output textual classes directly. '
          'Assigning classes integer values (1, 2, 3) suggests an ordinal relationship (e.g., bird '
          '> dog), which is incorrect. One-hot encoding creates a vector of length equal to the '
          'number of classes (e.g., [1, 0, 0] for cat, [0, 1, 0] for dog). This ensures the '
          'network treats all classes neutrally and orthogonally.'},
 {'q': 'Global Average Pooling (GAP) is often used as a replacement for standard fully connected '
       'layers at the end of modern CNN architectures. How does a GAP layer process an input '
       'tensor of dimensions H x W x C (Height, Width, Channels)?',
  'code': '',
  'opts': {'A': 'It averages all elements across the channel dimension, yielding an H x W x 1 '
                'tensor',
           'B': 'It averages all spatial elements for each channel independently, collapsing the '
                'spatial dimensions to 1 x 1 and yielding a 1 x 1 x C tensor',
           'C': 'It flattens the tensor and computes a single global average value for the entire '
                'image',
           'D': 'It computes the arithmetic mean of the weights in the previous layer'},
  'ans': 'B',
  'expl': 'Global Average Pooling computes the average of the feature map for each channel. If the '
          'previous layer outputs 512 distinct feature maps of size 7 x 7, the GAP layer '
          'calculates the mean of each 7 x 7 grid, outputting exactly 512 scalar values. This '
          'reduces parameters (preventing overfitting) and allows the network to process inputs of '
          'varying spatial dimensions.'},
 {'q': 'What is the primary function of a Transposed Convolution layer (often incorrectly referred '
       "to as 'deconvolution') in architectures like Autoencoders or GANs?",
  'code': '',
  'opts': {'A': 'To reverse the mathematical operation of a convolution and recover the exact '
                'original input matrix',
           'B': 'To extract finer spatial features by decreasing the receptive field',
           'C': 'To upsample a low-resolution feature map into a higher-resolution spatial '
                'dimension while learning the optimal interpolation weights',
           'D': 'To convert a 1D sequence into a 2D matrix'},
  'ans': 'C',
  'expl': 'Standard convolutions typically reduce spatial dimensions. In generative models or '
          'segmentation networks, it is necessary to project low-resolution representations back '
          'into high-resolution images. A transposed convolution performs this upsampling. Instead '
          'of using a fixed interpolation algorithm (like bilinear), it uses learnable kernel '
          'weights to project the data, learning how to best reconstruct the spatial dimensions.'},
 {'q': 'How does the Adam (Adaptive Moment Estimation) optimizer differ from basic Stochastic '
       'Gradient Descent (SGD)?',
  'code': '',
  'opts': {'A': 'Adam updates weights randomly without computing gradients',
           'B': 'Adam computes an individual, adaptive learning rate for every parameter using '
                'estimates of first and second moments of the gradients',
           'C': 'Adam computes exact second derivatives (the Hessian) to navigate the loss '
                'landscape',
           'D': 'Adam forces the gradient to zero if it exceeds a predetermined magnitude'},
  'ans': 'B',
  'expl': 'Standard SGD applies the same global learning rate to all parameters. Adam maintains a '
          'moving average of the gradient (first moment, like momentum) and a moving average of '
          'the squared gradient (second moment, like RMSProp). It uses these moving averages to '
          'scale the learning rate on a per-parameter basis, allowing it to navigate complex loss '
          'surfaces more efficiently.'}]


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