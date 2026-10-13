#!/usr/bin/env python3
"""
IDEAS TIH Quiz Autumn 26 - Machine Learning 4 - interactive terminal quiz
---------------------------------------------------------------
Run:   python machine_learning_4_quiz.py

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

TITLE = "IDEAS TIH Quiz Autumn 26 - Machine Learning 4"
TIME_LIMIT = 60 * 60          # seconds
OPTION_KEYS = ("A", "B", "C", "D")

QUESTIONS = [{'q': 'What is a recognized weakness of the standard DBSCAN algorithm?',
  'code': '',
  'opts': {'A': 'It requires the manual input of the number of clusters K.',
           'B': 'It only identifies spherical clusters.',
           'C': 'It struggles to identify clusters accurately when the density varies '
                'significantly across the dataset.',
           'D': 'It classifies all outliers as separate individual clusters.'},
  'ans': 'C',
  'expl': 'DBSCAN utilizes a global density threshold (fixed epsilon and minPts). If a dataset '
          'contains clusters of different densities, parameters calibrated for a high-density '
          'cluster will classify less dense clusters as noise.'},
 {'q': "Which algorithm was developed to address DBSCAN's limitation regarding clusters of varying "
       'densities?',
  'code': '',
  'opts': {'A': 'K-Means++',
           'B': 'Agglomerative Clustering',
           'C': 'OPTICS (Ordering Points To Identify the Clustering Structure)',
           'D': 'Mean-Shift Clustering'},
  'ans': 'C',
  'expl': 'OPTICS is an extension of DBSCAN that creates an augmented ordering of the database '
          'representing its density-based clustering structure. It functions similarly to DBSCAN '
          'but allows for the identification of clusters at variable density thresholds.'},
 {'q': 'What graphical heuristic is used to determine a suitable value for epsilon in DBSCAN?',
  'code': '',
  'opts': {'A': 'The k-distance graph',
           'B': 'The Silhouette plot',
           'C': 'The Dendrogram',
           'D': 'The ROC curve'},
  'ans': 'A',
  'expl': 'The k-distance graph plots the distance to the k-th nearest neighbor for all data '
          "points sorted in descending order. The point of maximum curvature (the 'knee') "
          'indicates a threshold where noise points transition to points belonging to clusters, '
          'serving as a good estimate for epsilon.'},
 {'q': 'Assuming the implementation of a spatial index (like an R-tree or k-d tree), what is the '
       'average case time complexity of the DBSCAN algorithm for N points?',
  'code': '',
  'opts': {'A': 'O(N)', 'B': 'O(N log N)', 'C': 'O(N^2)', 'D': 'O(N^3)'},
  'ans': 'B',
  'expl': 'By utilizing a spatial indexing structure, neighborhood queries in DBSCAN can be '
          'executed in O(log N) time on average. Since a query is made for each of the N points, '
          'the overall average time complexity reduces to O(N log N). Without spatial indexing, it '
          'scales to O(N^2).'},
 {'q': 'Which type of hierarchical clustering starts with all data points in a single large '
       'cluster and recursively splits them?',
  'code': '',
  'opts': {'A': 'Agglomerative', 'B': 'Divisive', 'C': 'Partitional', 'D': 'Density-based'},
  'ans': 'B',
  'expl': "Divisive hierarchical clustering uses a 'top-down' approach. It initializes with all "
          'points in one single cluster and systematically splits them until each point forms its '
          'own cluster or a stopping criterion is met.'},
 {'q': 'What does the y-axis of a standard dendrogram represent in hierarchical clustering?',
  'code': '',
  'opts': {'A': 'The sequence of clusters formed.',
           'B': 'The number of data points inside a cluster.',
           'C': 'The distance or dissimilarity metric at which clusters are merged or split.',
           'D': 'The variance of the raw features.'},
  'ans': 'C',
  'expl': 'In a dendrogram, the y-axis specifies the distance or dissimilarity measure. Horizontal '
          'lines connect clusters, and the height at which the connection occurs indicates the '
          'distance between the merged clusters.'},
 {'q': 'Which linkage criterion in agglomerative clustering calculates the distance between two '
       'clusters as the shortest distance between any single point in the first cluster and any '
       'single point in the second?',
  'code': '',
  'opts': {'A': 'Complete linkage',
           'B': 'Average linkage',
           'C': 'Single linkage',
           'D': "Ward's linkage"},
  'ans': 'C',
  'expl': 'Single linkage (or nearest-neighbor linkage) defines cluster distance based on the '
          'minimum distance between elements of different clusters. This can lead to a phenomenon '
          "known as 'chaining'."},
 {'q': 'What does the complete linkage method use to measure the distance between two clusters?',
  'code': '',
  'opts': {'A': 'The distance between the centroids of the two clusters.',
           'B': 'The maximum distance between any point in the first cluster and any point in the '
                'second cluster.',
           'C': 'The sum of all squared distances between the two clusters.',
           'D': 'The average distance between all pairs of points across the two clusters.'},
  'ans': 'B',
  'expl': 'Complete linkage determines the distance between clusters based on the maximum distance '
          'between a point in one cluster and a point in the other. It tends to produce more '
          'compact, spherical clusters than single linkage.'},
 {'q': 'Which linkage method in hierarchical clustering merges pairs of clusters in a way that '
       'minimizes the increase in total within-cluster variance?',
  'code': '',
  'opts': {'A': 'Single linkage',
           'B': 'Complete linkage',
           'C': 'Centroid linkage',
           'D': "Ward's method"},
  'ans': 'D',
  'expl': "Ward's method uses an objective function similar to K-Means. At each step, it "
          'calculates the within-cluster sum of squares for all possible cluster merges and '
          'selects the merge that causes the smallest increase in this total variance.'},
 {'q': 'What is the standard worst-case space complexity for agglomerative hierarchical clustering '
       'on a dataset with N items?',
  'code': '',
  'opts': {'A': 'O(N)', 'B': 'O(N log N)', 'C': 'O(N^2)', 'D': 'O(N^3)'},
  'ans': 'C',
  'expl': 'Agglomerative clustering typically requires the computation and storage of an N x N '
          'distance or similarity matrix, mapping distances between all possible pairs of items. '
          'This leads to an O(N^2) space complexity constraint.'},
 {'q': 'How is a specific number of clusters extracted from a computed hierarchical agglomerative '
       'dendrogram?',
  'code': '',
  'opts': {'A': 'By summing the distances of all nodes.',
           'B': "By defining a horizontal cut threshold across the dendrogram's y-axis.",
           'C': 'By taking the square root of the number of terminal leaves.',
           'D': 'By recalculating the distance matrix.'},
  'ans': 'B',
  'expl': 'Flat clusters are generated by cutting the dendrogram horizontally at a chosen distance '
          'threshold. Each distinct vertical line intersected by this horizontal cut represents '
          'one cluster.'},
 {'q': 'The chaining effect, where clusters grow as elongated, non-compact structures, is most '
       'commonly a vulnerability of which linkage metric?',
  'code': '',
  'opts': {'A': 'Complete Linkage',
           'B': "Ward's Method",
           'C': 'Single Linkage',
           'D': 'Average Linkage'},
  'ans': 'C',
  'expl': 'Single linkage merges clusters based on the shortest distance between any two '
          'constituent elements. Consequently, an isolated sequence of points separated by short '
          'distances can cause two distant dense regions to merge, creating an elongated chain.'},
 {'q': 'When evaluating clustering models against external ground truth labels, what does the Rand '
       'Index calculate?',
  'code': '',
  'opts': {'A': 'The sum of squared distances to the cluster centers.',
           'B': 'The ratio of true positives and true negatives over all possible pairs of data '
                'points.',
           'C': 'The variance between external label dimensions.',
           'D': 'The expected value of cluster sizes under random assignment.'},
  'ans': 'B',
  'expl': 'The Rand Index evaluates external clustering performance. It considers all pairs of '
          'samples and counts pairs that are correctly assigned to the same or different clusters '
          '(True Positives and True Negatives) divided by the total number of pairs.'},
 {'q': 'Why is the Adjusted Rand Index (ARI) generally preferred over the standard Rand Index for '
       'evaluating clustering performance?',
  'code': '',
  'opts': {'A': 'It operates without requiring ground truth labels.',
           'B': 'It has a lower computational time complexity.',
           'C': 'It corrects for chance groupings, ensuring that random cluster assignments yield '
                'an expected score near zero.',
           'D': 'It maps all values to a strict binary output of 0 or 1.'},
  'ans': 'C',
  'expl': 'The standard Rand Index can yield high scores due to random chance, especially if the '
          'number of clusters is large. The Adjusted Rand Index subtracts the expected index given '
          'a random model, scaling the metric such that random clustering yields an ARI close to '
          '0, and perfect clustering yields 1.'},
 {'q': 'Which distance metric calculates the length of the shortest path between two points across '
       'axes at right angles, equivalent to the sum of absolute differences?',
  'code': '',
  'opts': {'A': 'Euclidean distance',
           'B': 'Manhattan distance',
           'C': 'Chebyshev distance',
           'D': 'Cosine distance'},
  'ans': 'B',
  'expl': 'Manhattan distance (also known as L1 norm or taxicab geometry) computes the distance '
          'between two points by summing the absolute differences of their Cartesian coordinates.'},
 {'q': 'In document clustering based on text data, why is Cosine similarity favored over Euclidean '
       'distance?',
  'code': '',
  'opts': {'A': 'Cosine similarity evaluates the angle between document vectors rather than '
                'magnitude, mitigating the effect of differing document lengths.',
           'B': 'Euclidean distance is computationally impossible for text data.',
           'C': 'Cosine similarity inherently performs stop-word removal and lemmatization.',
           'D': 'Cosine similarity scales vectors linearly up to O(N^3).'},
  'ans': 'A',
  'expl': 'Text documents are represented as sparse frequency vectors. Two documents might share '
          'proportional word usage but have different lengths, causing a large Euclidean distance. '
          'Cosine similarity measures the angle between vectors, identifying proportional '
          'similarity irrespective of vector magnitude.'},
 {'q': 'Which iterative algorithm is used to estimate the parameters of a Gaussian Mixture Model '
       '(GMM) by alternating between estimating latent probabilities and maximizing expected '
       'log-likelihood?',
  'code': '',
  'opts': {'A': 'Backpropagation',
           'B': 'Expectation-Maximization (EM) algorithm',
           'C': 'Gradient Descent',
           'D': 'Principal Component Analysis'},
  'ans': 'B',
  'expl': 'The Expectation-Maximization (EM) algorithm is the standard method for finding maximum '
          'likelihood estimates of parameters in statistical models with latent variables, such as '
          'calculating the component weights, means, and covariances in a Gaussian Mixture Model.'},
 {'q': 'How does Bisecting K-Means differ from standard K-Means?',
  'code': '',
  'opts': {'A': 'It operates using median values instead of arithmetic means.',
           'B': 'It executes a top-down hierarchical approach where a cluster is split using '
                'standard K-Means (K = 2) at each step until the desired number of clusters is '
                'reached.',
           'C': 'It computes clusters from both the top-down and bottom-up simultaneously.',
           'D': 'It inherently discovers the parameter K by removing the farthest outliers at each '
                'iteration.'},
  'ans': 'B',
  'expl': 'Bisecting K-Means merges the concepts of hierarchical clustering and K-Means. It '
          'initializes with all points in one cluster, and iteratively applies basic K-Means with '
          'K = 2 to bisect the existing cluster with the highest variance until the target number '
          'of clusters is achieved.'},
 {'q': 'In a Gaussian Mixture Model, what is the effect of forcing the covariance matrices of all '
       "cluster components to be 'spherical'?",
  'code': '',
  'opts': {'A': 'The model behaves identically to DBSCAN.',
           'B': 'The model allows clusters to form distinct elliptical shapes.',
           'C': 'The model essentially approximates the behavior of standard K-Means clustering, '
                'generating uniformly spherical clusters.',
           'D': 'The model diverges and fails to converge to any local optimum.'},
  'ans': 'C',
  'expl': 'Standard K-Means implicitly assumes that all clusters are spherical and have equal '
          'variance. By restricting the covariance matrices in a GMM to be spherical (a scalar '
          'multiple of the identity matrix) and uniform, the GMM approximates K-Means.'},
 {'q': 'Which unsupervised learning technique is used to transform a high-dimensional dataset into '
       'fewer dimensions while retaining as much variance as possible?',
  'code': '',
  'opts': {'A': 'Linear Discriminant Analysis',
           'B': 'K-Means Clustering',
           'C': 'Principal Component Analysis (PCA)',
           'D': 'Logistic Regression'},
  'ans': 'C',
  'expl': 'Principal Component Analysis (PCA) is an unsupervised dimensionality reduction method '
          'that maps data onto a lower-dimensional space using orthogonal transformations, '
          'maximizing the variance captured by each principal component.'},
 {'q': 'What does the parameter K explicitly define in the K-Means algorithm?',
  'code': '',
  'opts': {'A': 'The number of features in the dataset.',
           'B': 'The number of non-overlapping clusters to segment the data into.',
           'C': 'The maximum number of iterations the algorithm will execute.',
           'D': 'The distance radius used to locate neighbors.'},
  'ans': 'B',
  'expl': 'In K-Means clustering, the parameter K represents the user-defined target number of '
          'clusters that the algorithm is expected to partition the input data into.'},
 {'q': 'When using DBSCAN, what outcome is expected for points that are located in low-density '
       'areas and are not reachable from any core point?',
  'code': '',
  'opts': {'A': 'They are forced into the nearest cluster.',
           'B': 'They form their own cluster.',
           'C': 'They are classified as noise or outliers.',
           'D': 'They serve as new initial centroids.'},
  'ans': 'C',
  'expl': 'DBSCAN algorithm categorizes any point that is neither a core point nor '
          'density-reachable from a core point as noise. This designation is used for outlier '
          'detection.'},
 {'q': 'Which statement correctly describes the initialization phase of an agglomerative '
       'hierarchical clustering process?',
  'code': '',
  'opts': {'A': 'All data points are randomly assigned to two major clusters.',
           'B': 'Every single data point acts as an independent cluster.',
           'C': 'Data points are aggregated into exactly K clusters based on an initial guess.',
           'D': 'The algorithm selects random core points to construct density regions.'},
  'ans': 'B',
  'expl': 'Agglomerative clustering is a bottom-up approach. It starts by treating each individual '
          'data point as a single-point cluster. It then merges pairs of clusters progressively.'},
 {'q': 'What condition acts as the stopping criterion for the standard K-Means algorithm?',
  'code': '',
  'opts': {'A': 'When the silhouette score reaches exactly 1.0.',
           'B': 'When all points become core points.',
           'C': 'When the cluster assignments no longer change between iterations.',
           'D': 'When the total number of clusters K decreases to 1.'},
  'ans': 'C',
  'expl': 'K-Means operates iteratively. It terminates when the assignment of data points to '
          'centroids does not change between iterations, indicating a local minimum for the '
          'objective function has been reached.'},
 {'q': 'In terms of cluster shapes, how does average linkage perform compared to single linkage '
       'and complete linkage?',
  'code': '',
  'opts': {'A': 'It enforces strict spherical shapes exactly like K-Means.',
           'B': 'It creates arbitrary shaped clusters that are more severely chained than single '
                'linkage.',
           'C': 'It yields a compromise between single and complete linkage, creating relatively '
                'compact clusters without high sensitivity to outliers.',
           'D': 'It only works on 1-dimensional data arrays.'},
  'ans': 'C',
  'expl': 'Average linkage considers the mean distance between all pairs of points in two '
          'different clusters. This mitigates the chaining seen in single linkage and the '
          'sensitivity to outliers seen in complete linkage, offering a balanced structural '
          'output.'},
 {'q': 'Which distance metric is combined with the epsilon parameter in most implementations of '
       'DBSCAN?',
  'code': '',
  'opts': {'A': 'Jaccard index',
           'B': 'Mahalanobis distance',
           'C': 'Euclidean distance',
           'D': 'Hamming distance'},
  'ans': 'C',
  'expl': 'While DBSCAN can employ any distance metric, implementations on continuous numerical '
          'variables often default to Euclidean distance to determine if neighbors fall within the '
          'epsilon-radius.'},
 {'q': 'How does Spectral Clustering construct groupings differently from conventional K-Means?',
  'code': '',
  'opts': {'A': 'It relies exclusively on external labels to assign centroids.',
           'B': 'It transforms the data using the eigenvectors of a similarity matrix before '
                'applying a standard clustering algorithm like K-Means.',
           'C': 'It computes the absolute median distance rather than squared distances.',
           'D': 'It generates random density regions until an optimal silhouette score is found.'},
  'ans': 'B',
  'expl': 'Spectral clustering computes an affinity (similarity) matrix of the data, derives a '
          'Graph Laplacian, and uses the top eigenvectors of this Laplacian to map the data to a '
          'lower-dimensional space. Standard K-Means is then applied in this transformed space, '
          'allowing it to identify non-convex clusters.'},
 {'q': 'If a dataset consists of two non-overlapping concentric circles, how will standard K-Means '
       'perform with K = 2?',
  'code': '',
  'opts': {'A': 'It will successfully identify the inner and outer circles as separate clusters.',
           'B': 'It will fail to separate the circles and will divide the dataset linearly (e.g., '
                'separating left from right half).',
           'C': 'It will classify the outer circle as noise.',
           'D': 'It will classify the inner circle as noise.'},
  'ans': 'B',
  'expl': 'Standard K-Means uses Euclidean distance from centroids and creates linear boundaries '
          '(Voronoi partitions). It cannot model non-convex shapes like concentric circles. It '
          'will split the concentric circles geometrically (e.g., down the middle), failing to '
          'separate the rings.'},
 {'q': 'Which algorithm represents an application of unsupervised learning focused on finding '
       'relationships between variables in large transaction databases?',
  'code': '',
  'opts': {'A': 'Apriori algorithm (Association Rules)',
           'B': 'Random Forest',
           'C': 'Support Vector Machines',
           'D': 'Multi-Layer Perceptron'},
  'ans': 'A',
  'expl': 'Association rule learning, exemplified by the Apriori algorithm, is an unsupervised '
          'approach used to discover relations between variables in large databases, commonly used '
          'in market basket analysis to see which products are bought together.'},
 {'q': 'If two separate core points P_1 and P_2 in DBSCAN each have epsilon-neighborhoods that '
       "intersect, but neither core point falls within the other's epsilon-radius, do they belong "
       'to the same cluster?',
  'code': '',
  'opts': {'A': 'Yes, because they share density-reachable points in their intersection, '
                'establishing density-connectedness.',
           'B': 'No, core points must directly contain each other in their radii to merge '
                'clusters.',
           'C': 'Yes, but only if they have identical minPts values.',
           'D': 'No, because the overlapping points will be designated as noise.'},
  'ans': 'A',
  'expl': 'According to the property of density-connectedness in DBSCAN, if a common point q '
          'exists that is reachable from both P_1 and P_2, the core points (and their '
          'neighborhoods) form a continuous dense region and are assigned to the same cluster.'}]


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