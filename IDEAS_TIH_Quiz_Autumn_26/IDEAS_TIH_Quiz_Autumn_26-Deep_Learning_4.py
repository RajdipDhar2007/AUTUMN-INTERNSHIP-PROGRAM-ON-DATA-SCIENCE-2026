#!/usr/bin/env python3
"""
IDEAS TIH Quiz Autumn 26 - Deep Learning 4 - interactive terminal quiz
---------------------------------------------------------------
Run:   python deep_learning_4_quiz.py

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

TITLE = "IDEAS TIH Quiz Autumn 26 - Deep Learning 4"
TIME_LIMIT = 60 * 60          # seconds
OPTION_KEYS = ("A", "B", "C", "D")

QUESTIONS = [{'q': 'How does the inference process (text generation) of a standard Transformer decoder differ '
       'computationally from its training process?',
  'code': '',
  'opts': {'A': 'Inference requires masking, while training does not.',
           'B': 'Inference operates autoregressively generating one token at a time, whereas '
                'training processes the target sequence in parallel.',
           'C': 'Inference removes the cross-attention layers to speed up execution.',
           'D': 'Inference relies on bidirectional processing in the decoder.'},
  'ans': 'B',
  'expl': 'During training, target sequences are fully known, allowing the decoder to process all '
          'tokens in parallel using causal masking. During inference, future tokens are unknown. '
          'The decoder generates tokens one by one (autoregressively), feeding each new predicted '
          'token back into the model to generate the next.'},
 {'q': 'To handle batched sequences of variable lengths, Transformers utilize padding tokens. How '
       'is the attention mechanism modified to ensure these tokens do not influence the '
       'representation?',
  'code': '',
  'opts': {'A': 'By applying a padding mask that sets the pre-softmax attention scores of padding '
                'tokens to -inf.',
           'B': 'By cropping all sequences in the batch to the length of the shortest sequence.',
           'C': 'By setting the value of the padding tokens to 1 in the Value matrix.',
           'D': 'By completely removing the attention layers when padding is detected.'},
  'ans': 'A',
  'expl': 'Padding masks are boolean matrices applied to the raw attention scores prior to the '
          'softmax operation. The positions corresponding to padding tokens are given a large '
          'negative value (-inf), ensuring their resulting softmax probabilities are zero and they '
          'do not contribute to the weighted sum.'},
 {'q': 'Given a sequence length n and model dimension d_model, what is the memory footprint '
       'complexity strictly for storing the attention score matrix in a single self-attention head '
       'during training?',
  'code': '',
  'opts': {'A': 'O(n * d_model)', 'B': 'O(n^2)', 'C': 'O(n + d_model)', 'D': 'O(d_model^2)'},
  'ans': 'B',
  'expl': 'The attention score matrix represents the pairwise compatibility between every query '
          'and every key in the sequence. For a sequence of length n, this requires computing and '
          'storing an n x n matrix of scalars. Thus, the memory complexity for the attention '
          'scores is O(n^2).'},
 {'q': 'Why does self-attention apply learned linear projections to generate the Query, Key, and '
       'Value representations rather than using the raw input embeddings directly?',
  'code': '',
  'opts': {'A': 'To reduce the sequence length dynamically.',
           'B': 'To allow the model to map the input into multiple distinct representation '
                'subspaces, facilitating specific feature extraction.',
           'C': 'To force the resulting matrices to be sparse.',
           'D': 'To convert continuous representations into discrete token IDs.'},
  'ans': 'B',
  'expl': 'Using learned linear projections (W_Q, W_K, W_V) enables the model to transform the raw '
          'input embeddings into distinct representation subspaces. This is required in multi-head '
          'attention, where different heads project the input into different spaces to learn '
          'distinct contextual relationships.'},
 {'q': 'In the cross-attention layer of a Transformer decoder, which tensor is utilized to '
       'generate the Query matrix (Q)?',
  'code': '',
  'opts': {'A': 'The final hidden state of the encoder.',
           'B': "The output tensor from the decoder's preceding masked self-attention layer.",
           'C': 'The raw unencoded target embeddings.',
           'D': 'The input tensor of the encoder.'},
  'ans': 'B',
  'expl': "The Query represents the current decoding context derived from the decoder's internal "
          "state. Thus, the Query matrix is generated using the output of the decoder's preceding "
          'masked self-attention layer.'},
 {'q': 'In dot-product attention, how does the mathematical operation treat a Query vector and a '
       'Key vector that are identical or highly parallel?',
  'code': '',
  'opts': {'A': 'Their dot product will be zero.',
           'B': 'Their dot product will be uniquely negative.',
           'C': 'Their dot product will yield a large positive scalar, resulting in a high '
                'attention weight.',
           'D': 'Their dot product will cause an arithmetic overflow error.'},
  'ans': 'C',
  'expl': 'The dot product measures cosine similarity multiplied by magnitudes. If a Query and a '
          'Key vector point in the same direction, their dot product is maximized. After the '
          'softmax operation, this corresponds to a large attention weight.'},
 {'q': 'Why is the self-attention mechanism more effective for learning long-range dependencies in '
       'sequences compared to standard Recurrent Neural Networks (RNNs)?',
  'code': '',
  'opts': {'A': 'It uses fewer parameters.',
           'B': 'It maps dependencies via a constant O(1) maximum path length, whereas RNNs '
                'require O(n) sequential steps.',
           'C': 'It relies on gradient clipping by default.',
           'D': 'It processes tokens sequentially from right to left.'},
  'ans': 'B',
  'expl': 'In an RNN, information from token A must pass through all intermediate hidden states to '
          'influence token B, resulting in an O(n) path length susceptible to vanishing gradients. '
          'Self-attention calculates direct pairwise interactions between all tokens '
          'simultaneously, creating a constant O(1) path length regardless of distance.'},
 {'q': 'What describes the maximum path length between any two arbitrary positions in a sequence '
       'within a single Transformer encoder block?',
  'code': '',
  'opts': {'A': 'O(1)', 'B': 'O(log n)', 'C': 'O(n)', 'D': 'O(n^2)'},
  'ans': 'A',
  'expl': 'A single self-attention layer computes the interaction of every position with every '
          'other position directly in a single mathematical step. Therefore, the maximum path '
          'length signals must travel to connect any two positions is O(1).'},
 {'q': 'In the general formulation of multi-head attention, is it strictly mathematically required '
       'for the dimensionality of the Value vectors (d_v) to equal the dimensionality of the Key '
       'vectors (d_k)?',
  'code': '',
  'opts': {'A': 'Yes, because they are multiplied together before the softmax operation.',
           'B': 'Yes, otherwise the final concatenation operation will fail due to dimension '
                'mismatch.',
           'C': 'No, d_v can be an independent arbitrary dimension, as the dot product only '
                'involves Queries and Keys.',
           'D': 'No, but d_v must be an integer multiple of d_k.'},
  'ans': 'C',
  'expl': 'The mathematical necessity for equal dimensions applies only to Queries and Keys, as '
          'they must be dot-producted (QK^T). The resulting attention weights are then used to '
          'compute a weighted sum of the Value vectors. Therefore, the Value vectors can '
          'theoretically have any arbitrary dimensionality d_v.'},
 {'q': 'Which type of positional encoding relies on injecting a single fixed embedding vector for '
       'each absolute index directly into the initial input?',
  'code': '',
  'opts': {'A': 'Relative Positional Encoding',
           'B': 'Absolute Positional Encoding',
           'C': 'Autoregressive Positional Encoding',
           'D': 'Convolutional Positional Encoding'},
  'ans': 'B',
  'expl': 'Absolute positional encoding defines a fixed vector for every discrete position index '
          'in the sequence (0, 1, 2, ...). This absolute index vector is added to the token '
          'embedding.'},
 {'q': 'If a Transformer receives a batch of sequences where Sequence A has 10 tokens and Sequence '
       'B has 15 tokens, how is this disparity structurally handled by the attention mechanism?',
  'code': '',
  'opts': {'A': 'The model forces Sequence A to generate 5 extra valid tokens.',
           'B': 'Sequence A is padded with 5 special tokens, and a padding mask ensures their '
                'attention scores evaluate to zero.',
           'C': 'Sequence B is truncated by removing its last 5 tokens.',
           'D': 'The sequences are processed serially rather than in parallel.'},
  'ans': 'B',
  'expl': 'To create a rectangular tensor for efficient batch computation, shorter sequences are '
          'appended with null padding tokens. A padding mask is passed into the attention '
          'mechanism to force the attention weights involving these padding tokens to zero, '
          'preventing them from affecting the calculations.'},
 {'q': 'Prior to concatenating the outputs across h multiple heads, what is the geometric shape of '
       'the output matrix produced by a single attention head for a sequence of length n?',
  'code': '',
  'opts': {'A': 'n x d_model', 'B': 'n x n', 'C': 'n x d_v', 'D': 'd_k x d_v'},
  'ans': 'C',
  'expl': 'A single attention head computes the weighted sum of the Value vectors. Since there are '
          'n tokens, and each Value vector has a dimension of d_v, the output shape for one head '
          'is n x d_v. The attention weight matrix itself is n x n, but the output is the product '
          'of this matrix and the Value matrix.'},
 {'q': 'What primary capability does the Position-wise Feed-Forward Network inject into the '
       'Transformer block that the standard self-attention mechanism lacks?',
  'code': '',
  'opts': {'A': 'Non-linear feature transformation.',
           'B': 'Cross-sequence token alignment.',
           'C': 'Dynamic context weighting.',
           'D': 'Positional encoding mapping.'},
  'ans': 'A',
  'expl': 'The dot-product attention mechanism consists primarily of linear operations (matrix '
          'multiplications) and a softmax scaling. The position-wise FFN contains activation '
          'functions between its linear layers, introducing non-linearity that allows the network '
          'to learn non-linear mappings.'},
 {'q': 'For an input sequence composed of exactly n tokens, what are the dimensions of the raw '
       'attention score matrix (prior to softmax) computed in a standard self-attention layer?',
  'code': '',
  'opts': {'A': '1 x n', 'B': 'n x d_model', 'C': 'n x n', 'D': 'd_k x d_k'},
  'ans': 'C',
  'expl': 'The raw attention score matrix is generated by multiplying the Query matrix (size n x '
          'd_k) by the transposed Key matrix (size d_k x n). The resulting matrix represents the '
          'alignment between every token and every other token, which necessarily has the shape n '
          'x n.'},
 {'q': 'If all non-linear activation functions (e.g., ReLU, Softmax) were removed from a '
       'Transformer, the entire architecture would collapse mathematically into:',
  'code': '',
  'opts': {'A': 'A standard Recurrent Neural Network.',
           'B': 'A Support Vector Machine.',
           'C': 'A single linear transformation.',
           'D': 'A Markov Decision Process.'},
  'ans': 'C',
  'expl': 'Neural networks require non-linear activation functions to compute complex mappings. If '
          'only matrix multiplications and additions are utilized, applying them repeatedly '
          'simplifies mathematically to a single equivalent linear transformation, limiting the '
          "model's capacity."},
 {'q': 'In standard scaled dot-product attention, what is the sum of the attention weights '
       'allocated by a single query token across all available key tokens?',
  'code': '',
  'opts': {'A': '0',
           'B': 'sqrt(d_k)',
           'C': '1.0',
           'D': 'It depends entirely on the sequence length.'},
  'ans': 'C',
  'expl': 'The softmax function is applied across the key dimension for every query. A fundamental '
          'property of the softmax function is that it normalizes an array of numerical values '
          'into a probability distribution where all elements sum to 1.0.'},
 {'q': 'As the input sequence length n becomes vastly larger than the internal representation '
       'dimension d_model, which specific sub-layer dominates the overall computational execution '
       'time in a Transformer?',
  'code': '',
  'opts': {'A': 'The layer normalization operations.',
           'B': 'The position-wise feed-forward networks.',
           'C': 'The self-attention mechanisms.',
           'D': 'The positional encodings.'},
  'ans': 'C',
  'expl': 'The complexity of the self-attention layer scales quadratically with sequence length as '
          'O(n^2 * d). The complexity of the feed-forward network scales linearly with sequence '
          'length as O(n * d^2). When n>>d, the n^2 term dominates, making self-attention the '
          'computational bottleneck.'},
 {'q': 'What primary challenge arises when attempting to process documents containing 100,000 or '
       'more tokens using a standard Transformer architecture?',
  'code': '',
  'opts': {'A': 'The vocabulary size must be increased proportionately.',
           'B': 'The quadratic memory and time complexity of the self-attention mechanism quickly '
                'exhausts available GPU hardware.',
           'C': 'The feed-forward network fails to map linear relations at that scale.',
           'D': 'The residual connections create feedback loops that destabilize the loss.'},
  'ans': 'B',
  'expl': 'Because standard self-attention requires calculating an n x n similarity matrix, both '
          'the computational time and the memory required scale quadratically (O(n^2)) with the '
          'number of tokens. For long documents (e.g., n = 100, 000), this quadratic scaling '
          'demands impractical amounts of hardware memory.'},
 {'q': "In natural language processing, words like 'bank' possess multiple meanings depending on "
       'the surrounding text. Which component of the Transformer enables the generation of '
       'dynamically contextualized embeddings for such words?',
  'code': '',
  'opts': {'A': 'The static word embedding matrix.',
           'B': 'The positional encodings.',
           'C': 'The self-attention mechanism.',
           'D': 'The final softmax layer.'},
  'ans': 'C',
  'expl': 'The self-attention mechanism calculates a new representation for each word by taking a '
          'weighted sum of all other words in the sentence. Therefore, the final embedding for the '
          'token is influenced by surrounding context words, producing a contextualized '
          'representation.'},
 {'q': 'In a sequence-to-sequence translation task, what specific data does the final linear '
       'projection and softmax layer of the Transformer decoder operate upon to make its '
       'predictions?',
  'code': '',
  'opts': {'A': 'The raw input tokens of the source sentence.',
           'B': 'The contextualized output vectors produced by the final block of the decoder.',
           'C': "The encoder's final hidden state.",
           'D': 'The positional encodings alone.'},
  'ans': 'B',
  'expl': 'The decoder consists of a stack of multiple identical blocks. The output of the very '
          'last decoder block contains the contextualized vector representations of the target '
          'sequence. This output is fed into a final linear classifier and a softmax function to '
          'predict the probabilities of the next vocabulary tokens.'},
 {'q': 'During a machine translation inference task, how many times is the complete source '
       "sentence processed by the Transformer's encoder block?",
  'code': '',
  'opts': {'A': 'Exactly once.',
           'B': 'Once for every token generated in the target sentence.',
           'C': 'It is updated dynamically with every decoding step.',
           'D': 'Twice: once for forward context and once for backward context.'},
  'ans': 'A',
  'expl': 'During inference, the source sequence does not change. Therefore, the encoder processes '
          'the entire source sentence exactly once in a parallel step. The resulting encoder '
          "output representations are stored in memory and accessed by the decoder's "
          'cross-attention layers during autoregressive generation.'},
 {'q': 'Assume a Transformer decoder generates a sequence of length L during inference. How many '
       'sequential forward passes through the decoder block are strictly required to produce this '
       'output?',
  'code': '',
  'opts': {'A': '1', 'B': 'L', 'C': 'L^2', 'D': 'log(L)'},
  'ans': 'B',
  'expl': 'Inference in the decoder is autoregressive. To generate the token at position t, the '
          'decoder must process all previously generated tokens from position 1 to t - 1. This '
          'sequential dependency means generating a sequence of length L requires exactly L '
          'distinct forward passes through the decoder.'},
 {'q': 'In modern variations of the Transformer architecture, Layer Normalization is often applied '
       'prior to the self-attention and feed-forward layers (Pre-LN) rather than after them '
       '(Post-LN). What empirical benefit does this provide?',
  'code': '',
  'opts': {'A': 'It eliminates the necessity of the softmax function.',
           'B': 'It guarantees that attention weights equal one.',
           'C': 'It stabilizes gradients early in training and often removes the need for learning '
                'rate warmup.',
           'D': 'It compresses the sequence length by half.'},
  'ans': 'C',
  'expl': 'Pre-Layer Normalization ensures that the input to each sub-layer is well-conditioned. '
          'This arrangement creates a more direct identity path through the residual connections, '
          'which stabilizes gradient flow during backpropagation and usually allows training to '
          'proceed without learning rate warmup schedules.'},
 {'q': 'What is a known limitation of absolute sinusoidal positional encodings when a Transformer '
       'is applied to text significantly longer than any sequence seen during training?',
  'code': '',
  'opts': {'A': 'The sine and cosine waves destructively interfere, resulting in a zero vector.',
           'B': 'The model struggles to generalize to unseen absolute position indices because it '
                'has not learned to interpret the specific high-frequency wave interactions at '
                'those indices.',
           'C': 'The positional encoding matrix dimensions cannot mathematically scale beyond the '
                'pre-defined sequence limit.',
           'D': 'The encoding forces the self-attention matrix to become dense.'},
  'ans': 'B',
  'expl': 'While absolute sinusoidal encodings theoretically map to infinite sequence lengths, '
          'empirical evidence shows models overfit to the position range seen during training. For '
          'length extrapolation, the model fails to interpret unseen absolute positional '
          'embeddings, degrading performance.'},
 {'q': 'How does the context vector in an Attention-enhanced RNN differ structurally from the '
       'context vector in a standard Sequence-to-Sequence RNN?',
  'code': '',
  'opts': {'A': 'The Attention-enhanced context vector is dynamic and recomputed for every '
                'decoding step, whereas the standard context vector is static.',
           'B': 'The Attention-enhanced context vector relies strictly on average pooling.',
           'C': 'The standard context vector is dynamically updated during decoding.',
           'D': 'The standard context vector maintains a higher dimensionality.'},
  'ans': 'A',
  'expl': 'In a standard seq2seq RNN, the context vector is a single, static vector (the final '
          'encoder state). In an Attention-enhanced RNN, a unique context vector is computed '
          'dynamically at every single decoder time step by attending to relevant encoder hidden '
          'states.'},
 {'q': 'In matrix notation, which formula correctly represents the computation of unnormalized '
       'attention scores (prior to scaling) for a set of queries Q and keys K?',
  'code': '',
  'opts': {'A': 'Q * K', 'B': 'Q * K^T', 'C': 'K * Q^T', 'D': 'Q + K^T'},
  'ans': 'B',
  'expl': 'The unnormalized attention scores represent the dot product between every query and '
          'every key. In matrix multiplication, this pairwise dot product is computed by '
          'multiplying the Query matrix Q by the transpose of the Key matrix K^T, resulting in the '
          'formula Q * K^T.'},
 {'q': 'A researcher trains a standard Transformer model with d_model = 256. To increase capacity, '
       'they increase the number of attention heads h from 4 to 8 while keeping d_model constant. '
       'How does this modification alter the mathematical dimension d_k of each individual head?',
  'code': '',
  'opts': {'A': 'd_k increases from 64 to 128.',
           'B': 'd_k remains constant at 64.',
           'C': 'd_k decreases from 64 to 32.',
           'D': 'd_k decreases from 256 to 32.'},
  'ans': 'C',
  'expl': 'In a standard multi-head attention formulation, the dimension of each head is defined '
          'as d_k = d_model/h. When h = 4, d_k = 256/4 = 64. When h is increased to 8, d_k becomes '
          '256/8 = 32. Therefore, the dimension decreases to 32.'},
 {'q': 'Why do very deep Transformers (e.g., architectures possessing 24 or 48 blocks) require '
       'residual (skip) connections for successful optimization?',
  'code': '',
  'opts': {'A': 'To compress the embedding space efficiently.',
           'B': 'To prevent the models from attending to future tokens.',
           'C': 'To force the learning rate to decay exponentially.',
           'D': 'To mitigate the vanishing gradient problem inherent in backpropagating through '
                'many stacked layers.'},
  'ans': 'D',
  'expl': 'During backpropagation, multiplying gradients across many consecutive layers causes '
          'them to diminish towards zero (vanishing gradients), preventing convergence. Residual '
          'connections provide an additive shortcut pathway for gradients to bypass the non-linear '
          'transformations, preserving gradient magnitude.'},
 {'q': 'When a causal mask is applied to the square n x n attention score matrix S (where S_(i, j) '
       'evaluates the attention of query i to key j), what specific topological change is imposed '
       'on the matrix prior to softmax?',
  'code': '',
  'opts': {'A': 'The lower triangular elements are set to -inf.',
           'B': 'The strictly upper triangular elements (where j > i) are set to -inf.',
           'C': 'The diagonal elements (where i = j) are set to zero.',
           'D': 'All elements are multiplied by a scalar of 0.5.'},
  'ans': 'B',
  'expl': 'Causal masking prevents query token i from attending to future key token j (i.e., when '
          'j > i). In the n x n attention score matrix, the elements where j > i correspond to the '
          'strictly upper triangular region above the main diagonal. These specific elements are '
          'assigned -inf.'},
 {'q': 'Which of the following represents the correct mathematical formulation for the output of '
       'scaled dot-product attention, given a Query matrix Q, Key matrix K, Value matrix V, and '
       'key dimension d_k?',
  'code': '',
  'opts': {'A': 'Attention(Q, K, V) = softmax(QK^T/(sqrt(d_k))) V',
           'B': 'Attention(Q, K, V) = softmax(Q^TK/(sqrt(d_k))) V',
           'C': 'Attention(Q, K, V) = softmax(QK^T) V/(sqrt(d_k))',
           'D': 'Attention(Q, K, V) = softmax(QK/(sqrt(d_k))) V^T'},
  'ans': 'A',
  'expl': 'Scaled dot-product attention computes the dot products of queries Q and keys K via '
          'QK^T. This result is scaled by sqrt(d_k) to prevent vanishing gradients during the '
          'softmax operation. The softmax function is then applied across the key dimension to '
          'yield normalized attention weights, which are multiplied by the Value matrix V.'}]


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