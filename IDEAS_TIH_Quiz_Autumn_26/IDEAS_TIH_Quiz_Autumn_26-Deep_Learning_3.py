#!/usr/bin/env python3
"""
IDEAS TIH Quiz Autumn 26 - Deep Learning 3 - interactive terminal quiz
---------------------------------------------------------------
Run:   python deep_learning_3_quiz.py

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

TITLE = "IDEAS TIH Quiz Autumn 26 - Deep Learning 3"
TIME_LIMIT = 60 * 60          # seconds
OPTION_KEYS = ("A", "B", "C", "D")

QUESTIONS = [{'q': 'Which of the following best describes the role of the Query (Q), Key (K), and Value (V) '
       'matrices in scaled dot-product attention?',
  'code': '',
  'opts': {'A': 'Q and K compute compatibility scores; V provides the weighted output content',
           'B': 'Q stores the input tokens; K stores the output tokens; V is a bias term',
           'C': 'Q is used only in the encoder; K and V are used only in the decoder',
           'D': 'All three matrices are identical projections of the same input'},
  'ans': 'A',
  'expl': 'In the attention mechanism, the Query (Q) and Key (K) matrices are multiplied to '
          'calculate a compatibility score. This score determines the relative weight assigned to '
          'each token. The Value (V) matrix contains the content, which is multiplied by these '
          'normalized weights to produce the final context-aware output.'},
 {'q': 'What is the key advantage of multi-head attention over single-head attention?',
  'code': '',
  'opts': {'A': 'It reduces the total number of parameters in the model',
           'B': 'It allows the model to jointly attend to information from different '
                'representation subspaces at different positions',
           'C': 'It eliminates the need for positional encodings',
           'D': 'It replaces the feed-forward layers entirely'},
  'ans': 'B',
  'expl': 'Multi-head attention splits the attention mechanism into multiple independent heads. '
          'This allows the model to extract different types of relationships and representation '
          'subspaces simultaneously, avoiding the loss of information that can occur through '
          'simple averaging in a single attention head.'},
 {'q': 'Self-attention in a transformer differs from cross-attention in that:',
  'code': '',
  'opts': {'A': 'Self-attention uses queries from one sequence and keys/values from another '
                'sequence',
           'B': 'Self-attention is only used in the decoder; cross-attention is only used in the '
                'encoder',
           'C': 'Self-attention derives Q, K, and V all from the same sequence; cross-attention '
                'draws Q from one sequence and K, V from another',
           'D': 'There is no functional difference; the terms are interchangeable'},
  'ans': 'C',
  'expl': 'In self-attention, all three matrices (Query, Key, and Value) are derived from the same '
          'input sequence, allowing the sequence to model internal dependencies. In '
          'cross-attention, the Query is derived from the current sequence, while the Keys and '
          'Values are derived from a separate sequence.'},
 {'q': 'In the transformer encoder-decoder architecture, which component does the decoder use to '
       "attend to the encoder's output at each decoder layer?",
  'code': '',
  'opts': {'A': 'Masked self-attention',
           'B': 'Position-wise feed-forward network',
           'C': 'Cross-attention (encoder-decoder attention)',
           'D': 'Layer normalization'},
  'ans': 'C',
  'expl': 'In a standard Transformer, the decoder contains a specific sub-layer for '
          'cross-attention. This mechanism allows the decoder to attend to relevant parts of the '
          "encoder's output representations while generating subsequent tokens."},
 {'q': 'What is the computational complexity of standard (dense) self-attention with respect to '
       'sequence length n?',
  'code': '',
  'opts': {'A': 'O(n^2)', 'B': 'O(n)', 'C': 'O(n log n)', 'D': 'O(n^3)'},
  'ans': 'A',
  'expl': 'Standard self-attention computes a compatibility score for every token in the sequence '
          'against every other token. For a sequence length of n, this requires an n x n matrix '
          'multiplication, yielding a computational complexity of O(n^2).'},
 {'q': 'After computing multi-head attention with h heads, the outputs of all heads are:',
  'code': '',
  'opts': {'A': 'Averaged element-wise and passed to the next layer',
           'B': 'Concatenated along the head dimension and projected through a learned output '
                'matrix W_O',
           'C': 'Stacked as separate feature maps like in a CNN',
           'D': 'Fed independently into separate feed-forward layers, one per head'},
  'ans': 'B',
  'expl': 'After the individual attention heads compute their outputs, the separate output vectors '
          'are concatenated into a single continuous vector. This combined vector is multiplied by '
          'a learned weight matrix (W_O) to project it back to the expected hidden dimension of '
          'the model.'},
 {'q': 'What is the primary function of the self-attention mechanism in a Transformer?',
  'code': '',
  'opts': {'A': 'To reduce the dimensionality of the input',
           'B': 'To perform image augmentation during training',
           'C': 'To replace gradient descent optimization',
           'D': 'To allow each token to attend to other relevant tokens in the sequence'},
  'ans': 'D',
  'expl': 'Self-attention models context by allowing each token in a sequence to attend to other '
          'tokens within that same sequence. This operation captures long-range dependencies and '
          'relational contexts between elements.'},
 {'q': 'In scaled dot-product attention, why are the dot products divided by sqrt(d) before '
       'applying softmax?',
  'code': '',
  'opts': {'A': 'To normalize the output to sum to 1',
           'B': 'To prevent extremely large dot products that push softmax into near-zero gradient '
                'regions',
           'C': 'To reduce memory usage of the attention matrix',
           'D': 'To enforce causality in the decoder'},
  'ans': 'B',
  'expl': 'When the dimension d is large, the dot products of queries and keys yield values of '
          'high magnitude. Applying the softmax function to these values pushes the output toward '
          '0 or 1, resulting in vanishing gradients. Scaling down by sqrt(d) maintains gradient '
          'magnitude during backpropagation.'},
 {'q': "In a sequence-to-sequence encoder-decoder model, what role does the encoder's final hidden "
       'state play?',
  'code': '',
  'opts': {'A': 'It is the predicted output token',
           'B': 'It computes positional embeddings for the decoder',
           'C': 'It initializes the decoder and encodes the full input context',
           'D': 'It serves as the key matrix in cross-attention'},
  'ans': 'C',
  'expl': 'In traditional sequence-to-sequence models, the encoder processes the input sequence '
          'and outputs a final hidden state. This state functions as a fixed-length vector '
          'representation of the input context, which initializes the decoder for sequence '
          'generation.'},
 {'q': 'What is the purpose of positional encodings added to token embeddings at the start of a '
       'transformer?',
  'code': '',
  'opts': {'A': 'To reduce the embedding dimension for efficiency',
           'B': 'To apply dropout regularization to the input',
           'C': 'To separate encoder embeddings from decoder embeddings',
           'D': "To inject information about each token's position"},
  'ans': 'D',
  'expl': 'Unlike Recurrent Neural Networks, Transformers process tokens in parallel without '
          'sequence constraints. Because they lack an implicit sequence representation, positional '
          'encodings are explicitly added to input embeddings to model token order.'},
 {'q': 'Which mathematical operation is applied to the scaled dot products of the queries and keys '
       'to convert them into valid attention weights?',
  'code': '',
  'opts': {'A': 'Rectified Linear Unit (ReLU)',
           'B': 'Sigmoid',
           'C': 'Softmax',
           'D': 'Hyperbolic Tangent (Tanh)'},
  'ans': 'C',
  'expl': 'The softmax function is applied to the scaled dot products of the queries and keys. '
          'This operation normalizes the raw similarity scores into a probability distribution, '
          'ensuring that the attention weights for each query sum to 1.'},
 {'q': 'Why is the standard self-attention mechanism considered permutation equivariant rather '
       'than strictly dependent on sequence order?',
  'code': '',
  'opts': {'A': 'Because it processes tokens sequentially from left to right.',
           'B': 'Because the operations are simple matrix multiplications that do not inherently '
                'encode positional data.',
           'C': 'Because the scaling factor eliminates positional variance.',
           'D': 'Because the multi-head structure randomizes the input order.'},
  'ans': 'B',
  'expl': 'Self-attention treats the input as an unordered set of tokens. The matrix '
          "multiplications compute similarities regardless of the tokens' positions in the "
          'sequence. Without explicit positional encodings, changing the order of input tokens '
          'permutes the output tokens identically.'},
 {'q': 'In a Transformer decoder, what is the specific function of the masked self-attention '
       'layer?',
  'code': '',
  'opts': {'A': 'To prevent the model from attending to future tokens during training.',
           'B': 'To drop out randomly selected attention weights for regularization.',
           'C': 'To mask padded tokens in the encoder input.',
           'D': 'To hide the encoder representations from the decoder.'},
  'ans': 'A',
  'expl': 'The masked self-attention layer in the decoder restricts tokens from attending to '
          'subsequent (future) tokens in the sequence. This preserves the autoregressive property, '
          'ensuring that predictions for position i can depend only on the known outputs at '
          'positions less than i.'},
 {'q': 'How is masking mathematically implemented in the scaled dot-product attention mechanism of '
       'a Transformer decoder?',
  'code': '',
  'opts': {'A': 'By multiplying future token embeddings by zero before the dot product.',
           'B': 'By setting the attention scores of future tokens to -inf prior to the softmax '
                'operation.',
           'C': 'By setting the attention scores of future tokens to zero after the softmax '
                'operation.',
           'D': 'By removing future tokens from the Key and Value matrices completely.'},
  'ans': 'B',
  'expl': 'To prevent attendance to future tokens, their corresponding unnormalized attention '
          'scores are set to negative infinity (-inf). When the softmax function is applied, '
          'e^(-inf) evaluates to 0, resulting in an attention weight of zero for future tokens.'},
 {'q': 'In the standard Transformer architecture, how does the Position-wise Feed-Forward Network '
       '(FFN) process the sequence of vectors output by the attention mechanism?',
  'code': '',
  'opts': {'A': 'It processes the entire sequence collectively using a recurrent layer.',
           'B': 'It flattens the sequence into a single vector and applies a dense layer.',
           'C': 'It applies the same linear transformations independently to each position in the '
                'sequence.',
           'D': 'It computes dot products between adjacent positions in the sequence.'},
  'ans': 'C',
  'expl': 'The Position-wise Feed-Forward Network applies two linear transformations with a ReLU '
          "activation in between. It is 'position-wise' because these identical transformations "
          'are applied independently to the vector representation at each individual position in '
          'the sequence.'},
 {'q': 'If a Transformer model has a hidden dimension d_model = 512 and uses h = 8 attention '
       'heads, what is the standard dimensionality of the Query (d_k) and Value (d_v) vectors for '
       'each individual head?',
  'code': '',
  'opts': {'A': 'd_k = 512, d_v = 512',
           'B': 'd_k = 64, d_v = 64',
           'C': 'd_k = 8, d_v = 8',
           'D': 'd_k = 4096, d_v = 4096'},
  'ans': 'B',
  'expl': 'In standard multi-head attention, the model dimension is divided equally among the '
          'attention heads. Therefore, d_k = d_v = d_model/h = 512/8 = 64. This keeps the total '
          'computational cost comparable to single-head attention with full dimensionality.'},
 {'q': 'When the outputs of multiple attention heads are concatenated in a standard Transformer, '
       'what is the dimensionality of the resulting concatenated vector before the final linear '
       'projection?',
  'code': '',
  'opts': {'A': 'h x d_v', 'B': 'd_model/h', 'C': 'h x d_model', 'D': 'd_v/h'},
  'ans': 'A',
  'expl': 'Each of the h attention heads produces an output vector of dimension d_v. When these '
          'are concatenated along the feature dimension, the resulting vector has a dimensionality '
          'of h x d_v. In standard configurations where d_v = d_model/h, this evaluates back to '
          'd_model.'},
 {'q': 'The original Transformer utilizes a specific formulation for positional encodings '
       'involving sine and cosine functions of different frequencies. What mathematical property '
       'does this design explicitly enable?',
  'code': '',
  'opts': {'A': 'It ensures the positional embeddings sum to exactly zero.',
           'B': 'It enables the model to learn relative position dependencies, as any positional '
                'offset can be represented as a linear function of the position.',
           'C': 'It prevents the need for adding the encodings, allowing them to be multiplied '
                'instead.',
           'D': 'It maps all positional representations to binary values.'},
  'ans': 'B',
  'expl': 'The sine and cosine functions with varying frequencies allow the model to learn '
          'relative positions. For any fixed offset k, the positional encoding at position p + k '
          'can be represented as a linear transformation of the positional encoding at position '
          'p.'},
 {'q': 'How are positional encodings combined with token embeddings at the input layer of a '
       'standard Transformer?',
  'code': '',
  'opts': {'A': 'By concatenating them along the sequence dimension.',
           'B': 'By concatenating them along the feature dimension.',
           'C': 'By computing the dot product between them.',
           'D': 'By performing element-wise addition.'},
  'ans': 'D',
  'expl': 'In the standard Transformer architecture, the positional encoding vectors possess the '
          'same dimension (d_model) as the token embeddings. They are combined via element-wise '
          'addition, injecting positional information directly into the initial token '
          'representations.'},
 {'q': 'In a standard Transformer block, what is the computational complexity of the Position-wise '
       'Feed-Forward Network relative to the sequence length n and model dimension d_model?',
  'code': '',
  'opts': {'A': 'O(n^2 * d_model)',
           'B': 'O(n * d_model^2)',
           'C': 'O(n^2 * d_model^2)',
           'D': 'O(n log n * d_model)'},
  'ans': 'B',
  'expl': 'The FFN is applied independently to each of the n positions. The network consists of '
          'two linear layers. The matrix multiplications involve dimensions d_model and typically '
          '4 * d_model. For each token, the cost is proportional to d_model^2. Across n tokens, '
          'the complexity is O(n * d_model^2).'},
 {'q': 'What primary limitation of traditional RNN-based Sequence-to-Sequence models did the '
       'introduction of the attention mechanism aim to resolve?',
  'code': '',
  'opts': {'A': 'The inability to output discrete categorical tokens.',
           'B': 'The strict requirement for input and output sequences to be of equal length.',
           'C': 'The information bottleneck caused by compressing the entire input sequence into a '
                'single fixed-length context vector.',
           'D': 'The high memory usage associated with processing short sentences.'},
  'ans': 'C',
  'expl': 'Prior to attention, seq2seq models compressed all input information into a single '
          'fixed-length context vector (the final encoder hidden state). This created an '
          'information bottleneck, degrading performance on long sequences. Attention resolves '
          'this by allowing the decoder to selectively look at all encoder states.'},
 {'q': 'What role does Layer Normalization play within the sub-layers of a Transformer block?',
  'code': '',
  'opts': {'A': 'It normalizes the attention scores to sum to one across the sequence.',
           'B': 'It standardizes the activations across the features for each individual token '
                'independently, stabilizing the training dynamics.',
           'C': 'It regularizes the model by randomly zeroing out elements in the input batch.',
           'D': 'It maps the output representation into the final vocabulary distribution.'},
  'ans': 'B',
  'expl': 'Layer Normalization is applied over the feature dimension for each token independently. '
          'It centers and scales the activations, which prevents internal covariate shift, '
          'stabilizes gradients, and allows for faster and more stable training of deep '
          'architectures.'},
 {'q': 'In the structural diagram of a standard Transformer block, what is the function of the '
       'residual (skip) connections?',
  'code': '',
  'opts': {'A': 'To connect the encoder directly to the final softmax output.',
           'B': 'To bypass sub-layers and add the original input to the sub-layer output, aiding '
                'gradient flow.',
           'C': 'To feed the loss value backward through the network.',
           'D': 'To convert multi-head attention back into single-head attention.'},
  'ans': 'B',
  'expl': 'Residual connections add the input of a sub-layer (like self-attention or the FFN) '
          'directly to its output. This creates a shortcut path for gradients during '
          'backpropagation, mitigating the vanishing gradient problem in deep networks.'},
 {'q': 'Ignoring bias terms, how many learned parameters are associated with computing the Query, '
       'Key, and Value projections for a single self-attention layer processing inputs of '
       'dimension d_model?',
  'code': '',
  'opts': {'A': '3 x d_model', 'B': 'd_model^2', 'C': '3 x d_model^2', 'D': '4 x d_model^2'},
  'ans': 'C',
  'expl': 'To compute Q, K, and V, the input (dimension d_model) is multiplied by three separate '
          'weight matrices: W_Q, W_K, W_V. Each of these matrices has dimensions d_model x '
          'd_model. Thus, each contains d_model^2 parameters, yielding a total of 3 x d_model^2 '
          'parameters.'},
 {'q': 'The scaling factor 1/(sqrt(d_k)) in scaled dot-product attention serves a mathematical '
       'purpose analogous to adjusting which parameter in a standard softmax function?',
  'code': '',
  'opts': {'A': 'The bias offset',
           'B': 'The temperature',
           'C': 'The learning rate',
           'D': 'The dropout probability'},
  'ans': 'B',
  'expl': 'In a temperature-scaled softmax, dividing the logits by a temperature term controls the '
          'sharpness of the resulting distribution. The scaling factor sqrt(d_k) acts as a '
          'temperature parameter; increasing d_k softens the distribution, mitigating vanishing '
          'gradients.'},
 {'q': 'In a standard RNN-based sequence-to-sequence model without attention, how is the source '
       'sentence representation transferred to the decoder?',
  'code': '',
  'opts': {'A': 'Through multiple context vectors passed at every time step.',
           'B': 'Exclusively via the initial hidden state of the decoder.',
           'C': 'By directly adding the source embeddings to the target embeddings.',
           'D': 'Through an intermediate multi-head attention layer.'},
  'ans': 'B',
  'expl': 'In the foundational seq2seq architecture without attention, the final hidden state of '
          'the encoder RNN encapsulates the entire source sentence. This single vector is provided '
          'as the initial hidden state to the decoder RNN, serving as the primary conduit of '
          'information.'},
 {'q': 'If the attention scores computed via softmax result in a perfectly uniform distribution '
       'for a specific query token across a sequence of n keys, what is the output vector for that '
       'query?',
  'code': '',
  'opts': {'A': 'A vector of pure zeros.',
           'B': 'The arithmetic mean of all n Value vectors in the sequence.',
           'C': 'The Value vector corresponding to the same position as the query.',
           'D': 'The sum of all Key vectors in the sequence.'},
  'ans': 'B',
  'expl': 'The output of the attention mechanism is a weighted sum of the Value vectors. If the '
          'softmax distribution is perfectly uniform, the weight assigned to each of the n Value '
          'vectors is 1/n. The resulting output vector is the arithmetic mean of all the Value '
          'vectors.'},
 {'q': 'In a Transformer decoder block, the architecture typically contains two distinct attention '
       'sub-layers. What distinguishes the inputs to the second attention sub-layer from the '
       'first?',
  'code': '',
  'opts': {'A': 'The second sub-layer generates its own Keys and Values from the decoder input, '
                'while the first uses encoder outputs.',
           'B': "The second sub-layer uses the decoder's intermediate state for Queries, but draws "
                "Keys and Values from the encoder's final output.",
           'C': "Both layers draw exclusively from the encoder's final output.",
           'D': 'The second sub-layer applies masking, whereas the first does not.'},
  'ans': 'B',
  'expl': 'The first sub-layer is masked self-attention, generating Q, K, and V internally from '
          "the decoder's sequence. The second sub-layer is cross-attention (encoder-decoder "
          'attention). It derives its Queries from the output of the first sub-layer (decoder '
          'state) and its Keys and Values from the final output of the encoder block.'},
 {'q': 'Without the scaling factor sqrt(d_k) in scaled dot-product attention, what issue '
       'frequently arises during training when the dimensionality d_k is large?',
  'code': '',
  'opts': {'A': 'The attention weights converge to a uniform distribution.',
           'B': 'The softmax function encounters vanishing gradients due to large magnitude dot '
                'products.',
           'C': 'The matrix multiplications exceed memory limits.',
           'D': 'The model attends to future tokens, breaking causality.'},
  'ans': 'B',
  'expl': 'As d_k grows, the variance of the dot product between random vectors increases, '
          'resulting in scalar values with large magnitudes. When passed through a softmax '
          'function, these values push the output into regions with extremely small gradients, '
          'inhibiting weight updates.'},
 {'q': "During the training of autoregressive Sequence-to-Sequence Transformer models, 'Teacher "
       "Forcing' is commonly employed. How does the Transformer apply this technique efficiently?",
  'code': '',
  'opts': {'A': "By using a separate neural network to evaluate the model's predictions.",
           'B': 'By processing the entire ground-truth target sequence through the decoder in a '
                'single forward pass, enabled by causal masking.',
           'C': 'By updating the gradients only after the entire output sequence is generated '
                'sequentially.',
           'D': 'By replacing the cross-entropy loss function with an adversarial loss.'},
  'ans': 'B',
  'expl': 'Teacher forcing involves providing the true previous target tokens as input to the '
          'decoder to predict the next token. Because Transformers lack recurrence and use causal '
          'masking to hide future tokens, the entire ground-truth sequence can be passed into the '
          'decoder in a single parallel forward step during training.'}]


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