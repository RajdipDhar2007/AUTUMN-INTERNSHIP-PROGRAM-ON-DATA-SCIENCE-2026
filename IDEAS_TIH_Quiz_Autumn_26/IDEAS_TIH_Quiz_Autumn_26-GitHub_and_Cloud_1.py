#!/usr/bin/env python3
"""
IDEAS TIH Quiz Autumn 26 - GitHub and Cloud 1 - interactive terminal quiz
---------------------------------------------------------------
Run:   python github_and_cloud_1_quiz.py

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

TITLE = "IDEAS TIH Quiz Autumn 26 - GitHub and Cloud 1"
TIME_LIMIT = 60 * 60          # seconds
OPTION_KEYS = ("A", "B", "C", "D")

QUESTIONS = [{'q': 'What is the main purpose of Git?',
  'code': '',
  'opts': {'A': 'To host websites',
           'B': 'To manage versions of files and code',
           'C': 'To run databases',
           'D': 'To create cloud servers'},
  'ans': 'B',
  'expl': 'Git is a version control system that tracks file modifications, enabling concurrent '
          'collaboration and historical version management.'},
 {'q': 'What is the main difference between Git and GitHub?',
  'code': '',
  'opts': {'A': 'Git is online, GitHub is offline',
           'B': 'GitHub stores databases, Git stores code',
           'C': 'Git is a version control tool, GitHub hosts Git repositories online',
           'D': 'There is no difference'},
  'ans': 'C',
  'expl': 'Git is a local version control system. GitHub is a cloud-based hosting service for Git '
          'repositories.'},
 {'q': 'Which Git command saves changes permanently to local history?',
  'code': '',
  'opts': {'A': 'git status', 'B': 'git add', 'C': 'git commit', 'D': 'git clone'},
  'ans': 'C',
  'expl': 'The `git commit` command creates a snapshot of staged changes and stores it in the '
          'repository history.'},
 {'q': 'What does `git add` do?',
  'code': '',
  'opts': {'A': 'Uploads code to GitHub',
           'B': 'Deletes files',
           'C': 'Moves changes to the staging area',
           'D': 'Creates a branch'},
  'ans': 'C',
  'expl': 'The `git add` command prepares modified files for the next commit by placing them in '
          'the staging area.'},
 {'q': 'In Git, what is a branch?',
  'code': '',
  'opts': {'A': 'A cloud server',
           'B': 'A copy of a repository on GitHub',
           'C': 'An independent line of development',
           'D': 'A backup file'},
  'ans': 'C',
  'expl': 'A branch represents an independent line of development, isolating modifications from '
          'the main codebase.'},
 {'q': 'Why do organizations use cloud computing instead of buying physical servers?',
  'code': '',
  'opts': {'A': 'Cloud servers do not require internet',
           'B': 'Cloud services allow flexible scaling and reduce upfront hardware costs',
           'C': 'Cloud servers can only run websites',
           'D': 'Cloud computing stores files only'},
  'ans': 'B',
  'expl': 'Cloud computing provides on-demand computing resources, reducing capital expenditures '
          'and facilitating dynamic scaling.'},
 {'q': 'Which AWS service provides a virtual server in the cloud?',
  'code': '',
  'opts': {'A': 'Amazon S3', 'B': 'Amazon RDS', 'C': 'Amazon EC2', 'D': 'AWS Lambda'},
  'ans': 'C',
  'expl': 'Amazon EC2 lets users launch virtual machines with configurable CPU, memory, and '
          'storage.'},
 {'q': 'Which AWS service is best suited for storing images, videos, and backups?',
  'code': '',
  'opts': {'A': 'Amazon EC2', 'B': 'Amazon S3', 'C': 'Amazon RDS', 'D': 'AWS Lambda'},
  'ans': 'B',
  'expl': 'Amazon S3 is object storage designed for scalable storage of files such as images, '
          'documents, logs, and backups.'},
 {'q': 'Which AWS service manages relational databases like MySQL or PostgreSQL?',
  'code': '',
  'opts': {'A': 'Amazon RDS', 'B': 'Amazon S3', 'C': 'Amazon EC2', 'D': 'AWS Lambda'},
  'ans': 'A',
  'expl': 'Amazon RDS provides managed relational database services, automating backups, '
          'monitoring, and scaling.'},
 {'q': 'Which AWS service runs code only when triggered, without managing servers?',
  'code': '',
  'opts': {'A': 'Amazon EC2', 'B': 'Amazon S3', 'C': 'AWS Lambda', 'D': 'Amazon RDS'},
  'ans': 'C',
  'expl': 'AWS Lambda runs code in response to events such as file uploads, API calls, or '
          'schedules, without provisioning servers.'},
 {'q': 'Which command is used to create a local copy of a remote Git repository?',
  'code': '',
  'opts': {'A': 'git copy', 'B': 'git duplicate', 'C': 'git clone', 'D': 'git mirror'},
  'ans': 'C',
  'expl': 'The `git clone` command duplicates an existing remote repository onto a local '
          'filesystem.'},
 {'q': 'What is the function of the `git status` command?',
  'code': '',
  'opts': {'A': 'To display the state of the working directory and the staging area',
           'B': 'To list all remote repositories',
           'C': 'To show the history of all previous commits',
           'D': 'To commit changes to the local repository'},
  'ans': 'A',
  'expl': 'The `git status` command outputs the current state of the working directory and staging '
          "area, indicating which changes have been staged, which haven't, and which files aren't "
          'being tracked by Git.'},
 {'q': 'Which command transfers committed local changes to a remote repository?',
  'code': '',
  'opts': {'A': 'git pull', 'B': 'git push', 'C': 'git fetch', 'D': 'git remote'},
  'ans': 'B',
  'expl': 'The `git push` command is used to upload local repository content to a remote '
          'repository.'},
 {'q': 'What is the purpose of a `.gitignore` file in a repository?',
  'code': '',
  'opts': {'A': 'To specify files that should be excluded from version control tracking',
           'B': 'To delete files permanently from the repository',
           'C': 'To hide files from other collaborators on GitHub',
           'D': 'To encrypt sensitive data before committing'},
  'ans': 'A',
  'expl': 'A `.gitignore` file contains rules instructing Git which files or directories to ignore '
          'and not track in the version control history.'},
 {'q': 'Which hashing algorithm does Git primarily use to identify and verify the integrity of '
       'commits and objects?',
  'code': '',
  'opts': {'A': 'MD5', 'B': 'SHA-1', 'C': 'SHA-256', 'D': 'RSA'},
  'ans': 'B',
  'expl': 'Git uses the SHA-1 hash function to compute a 40-character checksum for every object, '
          'ensuring data integrity and uniqueness.'},
 {'q': 'What sequence of internal operations is executed when the `git pull` command is run?',
  'code': '',
  'opts': {'A': 'git clone followed by git merge',
           'B': 'git fetch followed by git merge',
           'C': 'git add followed by git commit',
           'D': 'git rebase followed by git push'},
  'ans': 'B',
  'expl': 'The `git pull` command is a combination of two commands: `git fetch`, which downloads '
          'changes from the remote, and `git merge`, which integrates those changes into the '
          'current branch.'},
 {'q': "What occurs when a 'merge conflict' arises in Git?",
  'code': '',
  'opts': {'A': 'Git automatically selects the most recent change and overwrites older data',
           'B': 'The remote repository rejects a push request due to authentication failure',
           'C': 'Two branches have modifications to the same part of a file, requiring manual '
                'resolution',
           'D': 'The repository exceeds its storage limit on GitHub'},
  'ans': 'C',
  'expl': 'A merge conflict happens when Git cannot automatically resolve differences in code '
          'between two commits, typically because the same lines in a file were edited '
          'differently, necessitating manual resolution.'},
 {'q': "In the context of GitHub, what is a 'Pull Request' (PR)?",
  'code': '',
  'opts': {'A': 'A command line tool to enforce code standards',
           'B': 'A proposed change submitted by a developer for review before merging it into the '
                'main branch',
           'C': 'An automated backup process for remote repositories',
           'D': 'A request to increase repository storage quotas'},
  'ans': 'B',
  'expl': 'A Pull Request is a GitHub feature that alerts team members to changes pushed to a '
          'branch, allowing them to review, discuss, and approve the code before it is merged into '
          'the base branch.'},
 {'q': 'Which Git command modifies the most recent commit by combining staged changes with it?',
  'code': '',
  'opts': {'A': 'git commit --replace',
           'B': 'git commit --amend',
           'C': 'git reset --hard',
           'D': 'git rebase -i'},
  'ans': 'B',
  'expl': 'The `git commit --amend` command lets you modify the most recent commit, adding newly '
          'staged changes or altering the commit message.'},
 {'q': 'How does `git stash` function in a local repository?',
  'code': '',
  'opts': {'A': 'It permanently deletes all untracked files',
           'B': 'It pushes untracked changes directly to a new remote branch',
           'C': 'It temporarily shelves modified tracked files, leaving a clean working directory',
           'D': 'It merges all available local branches into the main branch'},
  'ans': 'C',
  'expl': '`git stash` temporarily stores uncommitted changes, returning the working directory to '
          'the state of the HEAD commit.'},
 {'q': "What does a 'detached HEAD' state indicate in Git?",
  'code': '',
  'opts': {'A': 'The repository has lost connection to the remote origin',
           'B': 'The HEAD pointer is referencing a specific commit directly rather than a branch '
                'reference',
           'C': 'The main branch has been deleted, leaving commits inaccessible',
           'D': 'A merge conflict has corrupted the .git directory'},
  'ans': 'B',
  'expl': 'A detached HEAD state occurs when checking out a specific commit rather than a branch '
          'name. Any new commits made in this state will not belong to any branch.'},
 {'q': 'Which statement correctly distinguishes `git reset` from `git revert`?',
  'code': '',
  'opts': {'A': '`git reset` creates a new commit that undoes changes, whereas `git revert` '
                'modifies existing history.',
           'B': '`git reset` only works on branches, whereas `git revert` only works on tags.',
           'C': '`git revert` creates a new commit that undoes changes, preserving history, '
                'whereas `git reset` alters the commit history.',
           'D': 'Both commands perform the exact same function but are used on different operating '
                'systems.'},
  'ans': 'C',
  'expl': '`git revert` generates a new commit containing inverse changes, whereas `git reset` '
          'moves the branch pointer backward, modifying commit history.'},
 {'q': 'Executing `git reset --hard HEAD~1` results in which of the following outcomes?',
  'code': '',
  'opts': {'A': 'The working directory remains unchanged, but the most recent commit is removed '
                'from history.',
           'B': 'The most recent commit is removed, and all changes in the working directory and '
                'staging area are permanently discarded.',
           'C': 'The most recent commit is moved to a new branch, keeping the working directory '
                'clean.',
           'D': 'The staging area is cleared, but modifications in the working directory are '
                'retained.'},
  'ans': 'B',
  'expl': 'The `--hard` flag in `git reset` forces the working directory, staging area, and commit '
          'history to match the specified reference (`HEAD~1`), discarding any uncommitted '
          'modifications.'},
 {'q': 'What distinguishes `git merge` from `git rebase` when integrating feature branches?',
  'code': '',
  'opts': {'A': 'Merging creates a new, linear history, whereas rebasing creates a multi-parent '
                'merge commit.',
           'B': 'Rebasing rewrites project history by placing feature branch commits at the tip of '
                'the base branch, whereas merging preserves chronological commit history.',
           'C': 'Merging deletes the feature branch automatically, whereas rebasing requires '
                'manual deletion.',
           'D': 'Rebasing can only integrate changes from local branches, whereas merging requires '
                'a remote repository.'},
  'ans': 'B',
  'expl': '`git rebase` flattens the commit history by moving the base of a branch to a new '
          'commit, whereas `git merge` combines histories and creates a specific merge commit.'},
 {'q': "In GitHub, what is the architectural difference between 'Forking' a repository and "
       "'Cloning' it?",
  'code': '',
  'opts': {'A': 'Cloning requires administrative permissions on the repository; forking does not.',
           'B': 'Forking creates a distinct, server-side copy on GitHub tied to your account; '
                'cloning creates a local copy on your physical machine.',
           'C': 'Forking downloads the repository to a local machine; cloning copies it to another '
                'cloud provider.',
           'D': 'Forking is only available for private repositories; cloning is for public ones.'},
  'ans': 'B',
  'expl': "A fork is a remote copy of a repository hosted on GitHub under a different user's "
          'account, facilitating external contributions. A clone is a local repository resident on '
          "a user's machine."},
 {'q': 'Which tool provides the most direct method to recover a commit that was accidentally '
       'discarded by a `git reset --hard`?',
  'code': '',
  'opts': {'A': 'git log --all', 'B': 'git reflog', 'C': 'git fsck', 'D': 'git stash pop'},
  'ans': 'B',
  'expl': 'The `git reflog` records updates to the tip of branches and other references, allowing '
          'a user to identify the SHA-1 hash of a lost commit and restore it.'},
 {'q': 'Which three primary internal object types does Git use to represent file systems and '
       'histories?',
  'code': '',
  'opts': {'A': 'File, Directory, Metadata',
           'B': 'Branch, Tag, Reflog',
           'C': 'Blob, Tree, Commit',
           'D': 'Stash, Head, Master'},
  'ans': 'C',
  'expl': 'Git internally represents data using Blobs (file contents), Trees (directory structures '
          'linking blobs), and Commits (metadata pointing to a tree and parent commits).'},
 {'q': 'What does the `git cherry-pick ` command achieve?',
  'code': '',
  'opts': {'A': 'It extracts a single file from an older commit and places it in the working '
                'directory.',
           'B': 'It applies the changes introduced by a specific existing commit onto the current '
                'branch.',
           'C': "It permanently deletes a specified commit from the repository's history.",
           'D': 'It squashes all previous commits into a single base commit.'},
  'ans': 'B',
  'expl': '`git cherry-pick` applies the changes introduced by a specific commit from one branch '
          'onto the current branch.'},
 {'q': 'In a complex repository structure, what is the function of a Git Submodule?',
  'code': '',
  'opts': {'A': 'It automatically executes shell scripts before committing code.',
           'B': 'It enables the inclusion of a secondary repository as a subdirectory within a '
                'primary repository.',
           'C': 'It restricts read/write permissions to specific directories within a project.',
           'D': 'It splits a large repository into multiple independent micro-repositories hosted '
                'on separate servers.'},
  'ans': 'B',
  'expl': 'Git submodules allow a developer to nest one Git repository inside another. This is '
          'typically used to include dependencies while maintaining independent version '
          'histories.'},
 {'q': 'Which Git feature allows automated execution of scripts in response to specific events, '
       'such as preventing a commit if automated tests fail?',
  'code': '',
  'opts': {'A': 'Git Pipelines', 'B': 'Git Triggers', 'C': 'Git Hooks', 'D': 'Git Actions'},
  'ans': 'C',
  'expl': 'Git hooks are executable scripts that run automatically before or after events like '
          '`commit`, `push`, and `receive`. A `pre-commit` hook is often used to enforce code '
          'standards.'}]


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