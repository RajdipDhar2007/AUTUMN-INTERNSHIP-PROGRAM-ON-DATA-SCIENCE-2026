#!/usr/bin/env python3
"""
IDEAS TIH Quiz Autumn 26 - Machine Learning 3 - interactive terminal quiz
---------------------------------------------------------------
Run:   python machine_learning_3_quiz.py

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

TITLE = "IDEAS TIH Quiz Autumn 26 - Machine Learning 3"
TIME_LIMIT = 60 * 60          # seconds
OPTION_KEYS = ("A", "B", "C", "D")

QUESTIONS = [{'q': 'What is the main characteristic of unsupervised learning?',
  'code': '',
  'opts': {'A': 'Data has labels',
           'B': 'Data has no labels',
           'C': 'Only images are used',
           'D': 'Predictions are always numbers'},
  'ans': 'B',
  'expl': 'Unsupervised learning algorithms use datasets that do not have labeled outputs or '
          'target variables. The primary goal is to discover hidden patterns, underlying '
          'structures, or groupings within the unlabeled data.'},
 {'q': 'What is clustering?',
  'code': '',
  'opts': {'A': 'Predicting future values',
           'B': 'Grouping similar data points together',
           'C': 'Drawing graphs',
           'D': 'Reducing dataset size'},
  'ans': 'B',
  'expl': 'Clustering is a technique in unsupervised machine learning that involves grouping a set '
          'of objects such that objects in the same group (a cluster) are more similar to each '
          'other than to those in other groups.'},
 {'q': 'With which type of learning is clustering primarily associated?',
  'code': '',
  'opts': {'A': 'Supervised Learning',
           'B': 'Reinforcement Learning',
           'C': 'Unsupervised Learning',
           'D': 'Transfer Learning'},
  'ans': 'C',
  'expl': 'Clustering operates on data without predefined labels or categories, relying on the '
          'inherent structures of the data to find similarities. Therefore, it is associated with '
          'unsupervised learning.'},
 {'q': 'Which clustering algorithm requires specifying the number of clusters beforehand?',
  'code': '',
  'opts': {'A': 'DBSCAN',
           'B': 'Hierarchical Clustering',
           'C': 'K-Means',
           'D': 'Logistic Regression'},
  'ans': 'C',
  'expl': "The K-Means clustering algorithm requires defining 'K' prior to execution. 'K' "
          'represents the target number of clusters the algorithm must identify in the dataset.'},
 {'q': 'What is the primary objective of the K-Means algorithm?',
  'code': '',
  'opts': {'A': 'Separate labeled classes',
           'B': 'Group points into distinct clusters based on similarity',
           'C': 'Predict probabilities',
           'D': 'Detect edges in images'},
  'ans': 'B',
  'expl': 'K-Means attempts to partition the dataset into K distinct, non-overlapping clusters by '
          'grouping data points that are close to one another based on a distance metric.'},
 {'q': 'What do cluster centers (centroids) represent in the K-Means algorithm?',
  'code': '',
  'opts': {'A': 'Random labels',
           'B': 'Average positions of clusters',
           'C': 'Output probabilities',
           'D': 'Activation functions'},
  'ans': 'B',
  'expl': 'In K-Means clustering, the cluster centers (centroids) represent the mean position of '
          'all data points currently assigned to that specific cluster.'},
 {'q': 'Which clustering algorithm can automatically detect outliers/noise?',
  'code': '',
  'opts': {'A': 'Linear Regression', 'B': 'K-Means', 'C': 'DBSCAN', 'D': 'Logistic Regression'},
  'ans': 'C',
  'expl': 'DBSCAN (Density-Based Spatial Clustering of Applications with Noise) groups points '
          'located in high-density areas. Points in low-density regions are marked as noise.'},
 {'q': 'What is an advantage of DBSCAN over K-Means?',
  'code': '',
  'opts': {'A': 'Requires labeled data',
           'B': 'Automatically finds dense regions and outliers',
           'C': 'Only works with images',
           'D': 'Predicts exact numbers'},
  'ans': 'B',
  'expl': 'DBSCAN identifies dense regions of arbitrary shapes and isolates sparse points as '
          'noise. In contrast, K-Means assumes spherical clusters and assigns all points to '
          'clusters, which can lead to outlier misclassification.'},
 {'q': 'Which clustering algorithm builds clusters by recursively merging nearby points or '
       'clusters?',
  'code': '',
  'opts': {'A': 'Linear Regression',
           'B': 'K-Means',
           'C': 'Hierarchical Clustering',
           'D': 'Logistic Regression'},
  'ans': 'C',
  'expl': 'Agglomerative hierarchical clustering builds clusters in a bottom-up approach. It '
          'starts by treating each data point as a separate cluster and recursively merges the '
          'closest pairs of clusters.'},
 {'q': 'Which clustering method is capable of identifying arbitrary cluster shapes and detecting '
       'noise?',
  'code': '',
  'opts': {'A': 'Linear Regression', 'B': 'DBSCAN', 'C': 'Logistic Regression', 'D': 'Perceptron'},
  'ans': 'B',
  'expl': 'DBSCAN forms clusters based on contiguous high-density areas rather than distances to a '
          'central point, making it effective for identifying clusters of arbitrary shapes and '
          'filtering out noise.'},
 {'q': 'Which of the following describes the primary objective of unsupervised learning?',
  'code': '',
  'opts': {'A': 'Mapping input data to specific target labels based on a training set.',
           'B': 'Learning a reward function through trial and error interactions with an '
                'environment.',
           'C': 'Identifying underlying structures, distributions, or patterns in unlabeled data.',
           'D': 'Classifying images into predefined categories with maximum accuracy.'},
  'ans': 'C',
  'expl': 'Unsupervised learning involves algorithms that infer patterns from a dataset without '
          'reference to known or labeled outcomes. The objective is to model the underlying '
          'structure or distribution of the data.'},
 {'q': 'Which of the following problems is generally addressed using unsupervised learning '
       'techniques?',
  'code': '',
  'opts': {'A': 'Spam email detection',
           'B': 'Customer segmentation',
           'C': 'Stock price forecasting',
           'D': 'Medical diagnosis from labeled X-rays'},
  'ans': 'B',
  'expl': 'Customer segmentation aims to group consumers based on similar purchasing behaviors or '
          'demographics without prior labels, which is a standard application of clustering, an '
          'unsupervised learning method.'},
 {'q': 'What differentiates a clustering task from a classification task?',
  'code': '',
  'opts': {'A': 'Clustering requires numerical data, while classification requires categorical '
                'data.',
           'B': 'Classification assigns data to predefined classes, while clustering forms groups '
                'based on data similarity without predefined classes.',
           'C': 'Clustering operates faster than classification models on large datasets.',
           'D': 'Classification is unsupervised, whereas clustering is supervised.'},
  'ans': 'B',
  'expl': 'Classification uses labeled training data to learn how to assign new inputs to known '
          'categories. Clustering discovers natural groupings in data where no target labels are '
          'provided in advance.'},
 {'q': 'In the context of clustering evaluation, what does high intra-cluster similarity indicate?',
  'code': '',
  'opts': {'A': 'Data points within the same cluster are distant from each other.',
           'B': 'Clusters are completely distinct from one another.',
           'C': 'Data points within the same cluster are closely related or geometrically near '
                'each other.',
           'D': 'The algorithm has overfit the data distribution.'},
  'ans': 'C',
  'expl': 'Intra-cluster similarity measures the closeness of objects within the same cluster. '
          'High intra-cluster similarity indicates a cohesive cluster where internal data points '
          'share common attributes.'},
 {'q': "How does the 'curse of dimensionality' generally affect distance-based clustering "
       'algorithms?',
  'code': '',
  'opts': {'A': 'It reduces the computational time required to calculate distances.',
           'B': 'It causes distances between data points to become uniform, making it difficult to '
                'distinguish meaningful clusters.',
           'C': 'It forces all data points into a single cluster.',
           'D': "It improves the algorithm's ability to locate distinct cluster centroids."},
  'ans': 'B',
  'expl': 'In high-dimensional spaces, the difference between the maximum and minimum distances '
          'between pairs of points tends to approach zero. This uniformity degrades the capability '
          'of distance metrics, such as Euclidean distance, to separate clusters effectively.'},
 {'q': 'Which type of clustering algorithm assigns data points to clusters with specific '
       'probability distributions rather than hard boundaries?',
  'code': '',
  'opts': {'A': 'K-Means Clustering',
           'B': 'Gaussian Mixture Models',
           'C': 'Agglomerative Clustering',
           'D': 'DBSCAN'},
  'ans': 'B',
  'expl': 'Gaussian Mixture Models (GMM) use a soft clustering approach where each data point has '
          'a probability of belonging to each cluster, modeled as a combination of Gaussian '
          'distributions.'},
 {'q': 'Based on the provided table, which algorithm assumes spherical cluster geometry and '
       'requires the user to specify the number of clusters?',
  'code': 'Clustering Algorithms Comparison\n'
          '+---------------+-----------------------------+---------------+---------------------+\n'
          '| Algorithm     | Requires Number of Clusters | Handles Noise | Geometry Assumption |\n'
          '+---------------+-----------------------------+---------------+---------------------+\n'
          '| K-Means       | Yes                         | No            | Spherical           |\n'
          '| DBSCAN        | No                          | Yes           | Arbitrary           |\n'
          '| Agglomerative | No                          | No            | Depends on Linkage  |\n'
          '+---------------+-----------------------------+---------------+---------------------+',
  'opts': {'A': 'K-Means', 'B': 'DBSCAN', 'C': 'Agglomerative', 'D': 'Both K-Means and DBSCAN'},
  'ans': 'A',
  'expl': 'According to the table, K-Means requires the number of clusters to be specified, '
          'assumes spherical geometry, and does not handle noise natively.'},
 {'q': 'During the update step of the K-Means algorithm, how are the new cluster centroids '
       'calculated?',
  'code': '',
  'opts': {'A': 'By finding the median of all distances between data points.',
           'B': 'By taking the arithmetic mean of all data points currently assigned to each '
                'cluster.',
           'C': 'By randomly selecting a new point from the dataset.',
           'D': 'By moving the centroid to the data point that is furthest away.'},
  'ans': 'B',
  'expl': "In Lloyd's algorithm for K-Means, the update step involves calculating the mean of the "
          'features for all instances assigned to a given cluster and moving the centroid to this '
          'mean location.'},
 {'q': 'Which metric does the standard K-Means algorithm explicitly attempt to minimize?',
  'code': '',
  'opts': {'A': 'The number of non-core points in the dataset.',
           'B': 'The maximum distance between any two cluster centroids.',
           'C': 'Within-Cluster Sum of Squares (WCSS) or inertia.',
           'D': 'The number of iterations required to reach convergence.'},
  'ans': 'C',
  'expl': 'The objective function of K-Means aims to minimize the Within-Cluster Sum of Squares '
          '(WCSS), also known as inertia. This value is the sum of squared Euclidean distances '
          'between each data point and its assigned cluster centroid.'},
 {'q': 'Why is feature scaling commonly applied before running the K-Means algorithm?',
  'code': '',
  'opts': {'A': 'It determines the optimal number of clusters autonomously.',
           'B': 'K-Means relies on distance metrics like Euclidean distance, which are '
                'disproportionately influenced by features with larger magnitudes.',
           'C': 'Scaling converts categorical data into numerical data.',
           'D': 'Scaling prevents the algorithm from converging to a local minimum.'},
  'ans': 'B',
  'expl': 'Since K-Means computes the distance between data points and centroids, features with '
          'larger scales will dominate the distance calculation. Standardizing or normalizing data '
          'ensures all features contribute equally.'},
 {'q': 'What graphical method is frequently used to estimate the optimal number of clusters K in '
       'K-Means?',
  'code': '',
  'opts': {'A': 'Receiver Operating Characteristic (ROC) curve',
           'B': 'Precision-Recall curve',
           'C': 'Elbow method',
           'D': 'Dendrogram'},
  'ans': 'C',
  'expl': 'The Elbow method involves plotting the objective value (like inertia) against the '
          "number of clusters K. The 'elbow' point, where the rate of decrease drops sharply, is "
          'typically considered a good estimate for the optimal K.'},
 {'q': 'Which problem associated with standard K-Means initialization does the K-Means++ algorithm '
       'attempt to solve?',
  'code': '',
  'opts': {'A': 'The inability to process categorical data.',
           'B': 'The generation of non-convex clusters.',
           'C': 'Convergence to local minima due to random initial centroid placement.',
           'D': 'The necessity to manually input the parameter K.'},
  'ans': 'C',
  'expl': 'Standard random initialization can lead K-Means to converge on a local minimum. '
          'K-Means++ addresses this by selecting initial centroids that are maximally distant from '
          'one another, improving the probability of finding the global minimum.'},
 {'q': 'Let a(i) be the mean distance between data point i and all other points in the same '
       'cluster, and let b(i) be the smallest mean distance from i to all points in any other '
       'cluster. Which equation represents the Silhouette Score s(i) for point i?',
  'code': '',
  'opts': {'A': 's(i) = (a(i) - b(i))/(max(a(i), b(i)))',
           'B': 's(i) = (b(i) - a(i))/(max(a(i), b(i)))',
           'C': 's(i) = (a(i) + b(i))/(b(i) - a(i))',
           'D': 's(i) = max(a(i), b(i)) - min(a(i), b(i))'},
  'ans': 'B',
  'expl': 'The silhouette score measures how similar an object is to its own cluster compared to '
          'other clusters. It is computed as s(i) = (b(i) - a(i))/(max(a(i), b(i))). Values range '
          'from -1 to +1, where a high value indicates the object is well matched to its own '
          'cluster.'},
 {'q': 'How does the presence of extreme outliers affect the K-Means clustering algorithm?',
  'code': '',
  'opts': {'A': 'Outliers are automatically discarded during the initialization phase.',
           'B': 'Outliers have no effect because distances are computed using medians instead of '
                'means.',
           'C': 'Outliers can pull the centroids away from the dense regions of data, skewing the '
                'clusters.',
           'D': 'Outliers force the algorithm to infinitely loop without converging.'},
  'ans': 'C',
  'expl': 'K-Means updates cluster centers using the arithmetic mean of the assigned points. An '
          'extreme outlier distorts the mean computation, shifting the centroid away from the '
          'dense region of the cluster.'},
 {'q': 'Which clustering algorithm is a robust variant of K-Means that chooses actual data points '
       'as cluster centers to reduce sensitivity to outliers?',
  'code': '',
  'opts': {'A': 'DBSCAN',
           'B': 'Agglomerative Clustering',
           'C': 'K-Medoids',
           'D': 'Spectral Clustering'},
  'ans': 'C',
  'expl': 'K-Medoids is an adaptation of K-Means requiring cluster centers (medoids) to be actual '
          'data points from the dataset. It relies on absolute deviations, making it less '
          'sensitive to outliers than K-Means.'},
 {'q': "What is the time complexity of the standard Lloyd's algorithm for K-Means per iteration?",
  'code': '',
  'opts': {'A': 'O(N x K x d)', 'B': 'O(N^2 x K)', 'C': 'O(N log N)', 'D': 'O(d^3)'},
  'ans': 'A',
  'expl': 'For a dataset with N points, d dimensions, and K clusters, the assignment step takes '
          'O(N x K x d) time, as the distance from each point to each centroid must be computed. '
          'The update step takes O(N x d). Therefore, the complexity per iteration is O(N x K x '
          'd).'},
 {'q': 'In the DBSCAN algorithm, what are the two primary parameters that need to be defined by '
       'the user?',
  'code': '',
  'opts': {'A': 'The number of clusters and the number of iterations.',
           'B': 'The maximum distance (epsilon) and the minimum number of points required to form '
                'a dense region (minPts).',
           'C': 'The initial centroid positions and the learning rate.',
           'D': 'The linkage criterion and the distance metric.'},
  'ans': 'B',
  'expl': 'DBSCAN relies on two hyperparameters: epsilon (epsilon), representing the radius of the '
          'neighborhood around a data point, and minPts, representing the minimum number of data '
          'points needed within that radius to classify it as a core point.'},
 {'q': "According to the definitions in DBSCAN, what is a 'core point'?",
  'code': '',
  'opts': {'A': 'A point that lies perfectly in the geometric center of a cluster.',
           'B': 'A point that has at least minPts number of points within its '
                'epsilon-neighborhood, including itself.',
           'C': 'A point that is randomly selected as the initial seed for a cluster.',
           'D': 'A point that has fewer than minPts in its neighborhood but is reachable from '
                'another point.'},
  'ans': 'B',
  'expl': 'A core point in DBSCAN is defined as any data point that contains at least minPts items '
          'within a radius defined by the distance epsilon. Core points form the interior of a '
          'density-based cluster.'},
 {'q': "In DBSCAN, how is a 'border point' differentiated from a 'noise point'?",
  'code': '',
  'opts': {'A': 'A border point has fewer than minPts in its epsilon-neighborhood but is within '
                'the epsilon-neighborhood of a core point. A noise point meets neither condition.',
           'B': 'A border point connects two separate clusters, while a noise point belongs to '
                'only one.',
           'C': 'A border point has exactly minPts in its neighborhood, while a noise point has '
                'zero.',
           'D': 'There is no mathematical difference; the terms are used interchangeably.'},
  'ans': 'A',
  'expl': 'Border points do not possess enough neighbors to be considered core points themselves, '
          'but they fall within the epsilon-radius of at least one core point. Noise points are '
          'isolated, failing to meet the criteria for either core or border points.'},
 {'q': 'Which concept ensures that points connected through a chain of overlapping dense '
       'neighborhoods form a single cluster in DBSCAN?',
  'code': '',
  'opts': {'A': 'Cosine similarity',
           'B': 'Density connectedness',
           'C': "Ward's criterion",
           'D': 'Silhouette maximization'},
  'ans': 'B',
  'expl': 'Density connectedness dictates that if two points are density-reachable from a common '
          'core point (even if they are not directly reachable from each other), they belong to '
          'the same cluster. This allows DBSCAN to identify clusters of arbitrary shapes.'}]


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