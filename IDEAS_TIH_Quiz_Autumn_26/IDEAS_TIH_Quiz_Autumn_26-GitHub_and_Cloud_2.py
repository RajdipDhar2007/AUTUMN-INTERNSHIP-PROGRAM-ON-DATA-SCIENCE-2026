#!/usr/bin/env python3
"""
IDEAS TIH Quiz Autumn 26 - GitHub and Cloud 2 - interactive terminal quiz
---------------------------------------------------------------
Run:   python github_and_cloud_2_quiz.py

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

TITLE = "IDEAS TIH Quiz Autumn 26 - GitHub and Cloud 2"
TIME_LIMIT = 60 * 60          # seconds
OPTION_KEYS = ("A", "B", "C", "D")

QUESTIONS = [{'q': 'Which cloud computing model provides software applications over the internet, typically on '
       'a subscription basis?',
  'code': '',
  'opts': {'A': 'Infrastructure as a Service (IaaS)',
           'B': 'Platform as a Service (PaaS)',
           'C': 'Software as a Service (SaaS)',
           'D': 'Functions as a Service (FaaS)'},
  'ans': 'C',
  'expl': 'Software as a Service (SaaS) delivers fully functional software applications via the '
          'internet, removing the need for end-users to install or maintain the software locally.'},
 {'q': "What does the term 'elasticity' refer to in cloud computing architecture?",
  'code': '',
  'opts': {'A': 'The ability of a system to route traffic based on geolocation',
           'B': 'The capability to automatically scale computing resources up or down based on '
                'current demand',
           'C': 'The encryption applied to data during transmission',
           'D': 'The process of replicating data across multiple physical data centers'},
  'ans': 'B',
  'expl': 'Elasticity allows cloud environments to dynamically adjust allocated resources to match '
          'workload demands.'},
 {'q': 'A deployment that combines on-premises infrastructure with public cloud services is known '
       'as which of the following?',
  'code': '',
  'opts': {'A': 'Community Cloud',
           'B': 'Private Cloud',
           'C': 'Hybrid Cloud',
           'D': 'Distributed Cloud'},
  'ans': 'C',
  'expl': 'A Hybrid Cloud architecture integrates local, privately maintained hardware resources '
          'with public cloud services, allowing data and applications to be shared between them.'},
 {'q': 'High Availability (HA) in cloud infrastructure ensures which of the following?',
  'code': '',
  'opts': {'A': 'Systems operate continuously with minimal downtime, often through redundancy',
           'B': 'Users are granted maximum administrative access to servers',
           'C': 'Software updates are delayed to avoid disruptions',
           'D': 'Data is compressed to occupy less physical storage space'},
  'ans': 'A',
  'expl': 'High Availability strategies use redundancy and fault tolerance to ensure systems '
          'remain operational and accessible even if individual hardware or software components '
          'fail.'},
 {'q': 'Adding more memory or a faster CPU to an existing virtual server is an example of what '
       'type of scaling?',
  'code': '',
  'opts': {'A': 'Horizontal scaling (Scaling out)',
           'B': 'Vertical scaling (Scaling up)',
           'C': 'Diagonal scaling',
           'D': 'Elastic scaling'},
  'ans': 'B',
  'expl': 'Vertical scaling entails increasing the capacity of a single machine or resource, '
          'whereas horizontal scaling involves adding more individual machines to a cluster.'},
 {'q': 'Which AWS service is responsible for providing scalable domain name system (DNS) routing?',
  'code': '',
  'opts': {'A': 'Amazon CloudFront',
           'B': 'Amazon Route 53',
           'C': 'AWS Direct Connect',
           'D': 'Amazon API Gateway'},
  'ans': 'B',
  'expl': 'Amazon Route 53 is a cloud DNS web service that translates domain names into IP '
          'addresses.'},
 {'q': 'What defines the relationship between AWS Regions and Availability Zones?',
  'code': '',
  'opts': {'A': 'An Availability Zone is a geographic area containing multiple Regions.',
           'B': 'A Region is a physical data center, and Availability Zones are virtual '
                'partitions.',
           'C': 'A Region is a geographical area consisting of two or more isolated and physically '
                'distinct Availability Zones.',
           'D': 'Regions and Availability Zones are identical concepts used interchangeably.'},
  'ans': 'C',
  'expl': 'Regions are broad geographic locations (like US East or Europe), and each Region '
          'contains multiple Availability Zones, which are discrete data centers equipped with '
          'independent power and networking.'},
 {'q': 'Which AWS S3 storage class provides the lowest cost storage for data that is rarely '
       'accessed and allows retrieval times extending to hours?',
  'code': '',
  'opts': {'A': 'S3 Standard',
           'B': 'S3 Intelligent-Tiering',
           'C': 'S3 One Zone-IA',
           'D': 'S3 Glacier Deep Archive'},
  'ans': 'D',
  'expl': 'S3 Glacier Deep Archive is designed for long-term data archiving with retrieval times '
          'of 12 hours or more.'},
 {'q': 'What is the primary function of AWS Identity and Access Management (IAM)?',
  'code': '',
  'opts': {'A': 'Managing billing and cost optimization reports',
           'B': 'Provisioning relational databases securely',
           'C': 'Securely controlling access to AWS resources and APIs for users and roles',
           'D': 'Monitoring application performance and server logs'},
  'ans': 'C',
  'expl': 'AWS IAM enables administrators to control who is authenticated and authorized to use '
          'resources across the AWS cloud environment.'},
 {'q': 'Which AWS service enables users to launch AWS resources into a logically isolated virtual '
       'network defined by the user?',
  'code': '',
  'opts': {'A': 'Amazon Virtual Private Cloud (VPC)',
           'B': 'AWS CloudFormation',
           'C': 'Amazon EC2 Auto Scaling',
           'D': 'AWS Trusted Advisor'},
  'ans': 'A',
  'expl': 'Amazon VPC allows full control over a virtual networking environment, including '
          'resource placement, connectivity, IP addressing, subnets, and routing.'},
 {'q': 'In an Amazon RDS Multi-AZ deployment, how is failover handled in the event of an '
       'infrastructure failure?',
  'code': '',
  'opts': {'A': 'The application must be manually reconfigured to point to a new database '
                'endpoint.',
           'B': 'AWS automatically provisions a new instance from the latest automated backup, '
                'requiring about 1 hour of downtime.',
           'C': 'AWS automatically fails over to a synchronous standby replica in a different '
                'Availability Zone using the same endpoint.',
           'D': 'Traffic is routed to a Read Replica which is immediately promoted to a master '
                'asynchronously.'},
  'ans': 'C',
  'expl': 'Multi-AZ deployments provide high availability and automatic failover. Amazon RDS '
          'automatically switches the database endpoint to point to a synchronous standby instance '
          'located in another AZ without requiring manual application changes.'},
 {'q': 'How does an Elastic Load Balancer (ELB) improve application availability?',
  'code': '',
  'opts': {'A': 'By automatically provisioning larger EC2 instance types when traffic spikes.',
           'B': 'By caching web content at edge locations globally to reduce latency.',
           'C': 'By distributing incoming application traffic across multiple targets, such as EC2 '
                'instances, in multiple Availability Zones.',
           'D': 'By routing database queries to multiple Read Replicas simultaneously.'},
  'ans': 'C',
  'expl': 'ELB distributes incoming application or network traffic across multiple targets to '
          'increase fault tolerance. It ensures that no single instance is overwhelmed, '
          'maintaining application stability.'},
 {'q': 'What is the maximum execution duration limit for a single AWS Lambda function invocation?',
  'code': '',
  'opts': {'A': '1 minute', 'B': '5 minutes', 'C': '15 minutes', 'D': '60 minutes'},
  'ans': 'C',
  'expl': 'AWS Lambda functions have a hard execution timeout limit of 15 minutes (900 seconds) '
          'per invocation. Tasks requiring longer execution times must use alternative services or '
          'architecture patterns.'},
 {'q': 'Which AWS database service provides a fully managed, multi-region, multi-master NoSQL '
       'database?',
  'code': '',
  'opts': {'A': 'Amazon Aurora',
           'B': 'Amazon RDS for PostgreSQL',
           'C': 'Amazon DynamoDB',
           'D': 'Amazon Redshift'},
  'ans': 'C',
  'expl': 'Amazon DynamoDB is a managed NoSQL database service that supports global tables for '
          'multi-master replication.'},
 {'q': 'According to the AWS Shared Responsibility Model, which of the following is the '
       'responsibility of the customer?',
  'code': '',
  'opts': {'A': 'Physical security of data center hardware',
           'B': 'Patching the host operating system of managed services like RDS',
           'C': 'Configuring security groups and encrypting customer data',
           'D': 'Maintenance of physical network infrastructure and cabling'},
  'ans': 'C',
  'expl': "Under the Shared Responsibility Model, AWS handles the 'Security OF the Cloud' "
          "(infrastructure, physical security), while the customer handles 'Security IN the Cloud' "
          '(data encryption, firewall configurations, application security).'},
 {'q': 'Which constraint applies to AWS VPC Peering connections?',
  'code': '',
  'opts': {'A': 'Peering connections can only be established between VPCs in the same region.',
           'B': 'VPC Peering does not support transitive routing; a connection must be established '
                'explicitly between any two VPCs to communicate.',
           'C': 'Data transferred over VPC peering requires establishing IPsec VPN tunnels '
                'manually.',
           'D': 'VPCs must have identical CIDR blocks to successfully establish a peering '
                'connection.'},
  'ans': 'B',
  'expl': 'VPC peering does not support transitive routing. If VPC A peers with VPC B, and VPC B '
          'peers with VPC C, traffic from A cannot route to C through B. A direct connection '
          'between A and C is required.'},
 {'q': 'How can secure, temporary, and direct HTTP access be granted to a private object in an '
       'Amazon S3 bucket?',
  'code': '',
  'opts': {'A': 'By temporarily altering the IAM policy attached to the user account',
           'B': "By changing the object ACL to 'public-read' for a brief period",
           'C': 'By generating an S3 Presigned URL that expires after a defined duration',
           'D': 'By routing the request through a NAT Gateway attached to the S3 bucket'},
  'ans': 'C',
  'expl': 'S3 Presigned URLs provide a mechanism to grant time-limited access to objects without '
          'altering public permissions or requiring AWS credentials.'},
 {'q': 'What distinguishes an Amazon RDS Read Replica from a Multi-AZ standby instance?',
  'code': '',
  'opts': {'A': 'Read Replicas support synchronous replication; Multi-AZ instances rely on '
                'asynchronous replication.',
           'B': 'Read Replicas can handle active read traffic to scale database performance; a '
                'Multi-AZ standby remains idle until failover.',
           'C': 'Read Replicas automatically trigger failover on primary failure; Multi-AZ '
                'instances require manual intervention.',
           'D': 'Read Replicas must reside in the same Availability Zone as the primary database; '
                'Multi-AZ instances must reside in separate regions.'},
  'ans': 'B',
  'expl': 'Read Replicas serve active read queries using asynchronous replication to offload work '
          'from the primary instance. A Multi-AZ standby is strictly for disaster recovery and '
          'cannot accept queries.'},
 {'q': "When integrating Amazon API Gateway with AWS Lambda, what does 'Lambda Proxy Integration' "
       'accomplish?',
  'code': '',
  'opts': {'A': 'It automatically scales the Lambda function based on API Gateway throughput '
                'limits.',
           'B': 'It maps the entire HTTP request directly to the Lambda function event object '
                'without requiring explicit data mapping templates.',
           'C': 'It encrypts the payload transitioning from the gateway to the function.',
           'D': 'It caches responses at the API Gateway layer to reduce Lambda invocations.'},
  'ans': 'B',
  'expl': 'Lambda Proxy Integration passes the raw HTTP request directly to the Lambda handler '
          'function without intermediate data mapping.'},
 {'q': 'Based on the provided EC2 Pricing Models table, which model carries the risk of instance '
       'termination by AWS with short notice?',
  'code': 'EC2 Pricing Models\n'
          '+--------------------+--------------------------------+-------------------------------------+\n'
          '| Model              | Billing Structure              | Optimal Use '
          'Case                    |\n'
          '+--------------------+--------------------------------+-------------------------------------+\n'
          '| On-Demand          | By the second or hour          | Short-term, unpredictable '
          'workloads |\n'
          '| Reserved Instances | 1 or 3 year upfront commitment | Steady-state, continuous '
          'usage      |\n'
          '| Spot Instances     | Variable market price          | Fault-tolerant, flexible '
          'workloads  |\n'
          '+--------------------+--------------------------------+-------------------------------------+',
  'opts': {'A': 'On-Demand',
           'B': 'Reserved Instances',
           'C': 'Spot Instances',
           'D': 'All models carry this risk equally'},
  'ans': 'C',
  'expl': 'Spot Instances utilize unused EC2 capacity, but AWS can terminate them with a '
          'two-minute warning when demand increases.'},
 {'q': "Which command removes a file from both the working directory and Git's tracking index?",
  'code': '',
  'opts': {'A': 'git delete', 'B': 'git rm', 'C': 'git clean', 'D': 'git erase'},
  'ans': 'B',
  'expl': 'The `git rm` command removes files from the filesystem and simultaneously stages the '
          'removal for the next commit.'},
 {'q': 'What does a fast-forward merge imply in Git?',
  'code': '',
  'opts': {'A': 'The merging algorithm bypasses conflict detection for speed.',
           'B': 'The target branch pointer simply advances forward to the merged commit because no '
                'divergent history exists.',
           'C': 'The commits are compressed into a single commit.',
           'D': 'A merge commit is forcibly generated regardless of history.'},
  'ans': 'B',
  'expl': 'A fast-forward merge occurs when there is a linear path from the target branch to the '
          'source branch. Git simply moves the branch pointer forward without creating a distinct '
          'merge commit.'},
 {'q': 'Which service acts as a fully managed data warehouse for large-scale analytics in AWS?',
  'code': '',
  'opts': {'A': 'Amazon S3', 'B': 'Amazon RDS', 'C': 'Amazon Redshift', 'D': 'AWS CloudTrail'},
  'ans': 'C',
  'expl': 'Amazon Redshift is a data warehouse service designed to analyze large datasets using '
          'standard SQL.'},
 {'q': 'What distinguishes AWS CloudTrail from Amazon CloudWatch?',
  'code': '',
  'opts': {'A': 'CloudTrail monitors application performance metrics, while CloudWatch records API '
                'calls for auditing.',
           'B': 'CloudTrail records API interactions and user activity for security and auditing, '
                'while CloudWatch monitors system performance metrics and logs.',
           'C': 'CloudTrail acts as a load balancer, while CloudWatch manages DNS.',
           'D': 'They provide identical functionalities but operate in different AWS regions.'},
  'ans': 'B',
  'expl': 'CloudTrail focuses on tracking user activity and API usage for governance and '
          'compliance. CloudWatch focuses on observing operational health, performance metrics, '
          'and application logs.'},
 {'q': 'Which git command allows the inspection of changes introduced by a specific commit ID '
       'without modifying the current working state?',
  'code': '',
  'opts': {'A': 'git diff', 'B': 'git show', 'C': 'git inspect', 'D': 'git checkout'},
  'ans': 'B',
  'expl': 'The `git show` command accepts a commit hash or reference and outputs the metadata and '
          'content modifications introduced by that specific commit.'},
 {'q': 'When using `git clean`, what is the default behavior?',
  'code': '',
  'opts': {'A': 'It deletes uncommitted changes in tracked files.',
           'B': 'It permanently removes untracked files from the working directory.',
           'C': 'It removes unused branches from the local repository.',
           'D': 'It resolves merge conflicts by accepting incoming changes.'},
  'ans': 'B',
  'expl': 'The `git clean` command deletes untracked files and directories from the local working '
          'directory. It does not affect tracked files.'},
 {'q': 'In a VPC, what is the role of an Internet Gateway (IGW)?',
  'code': '',
  'opts': {'A': 'It translates private IP addresses to public ones for instances without elastic '
                'IP addresses.',
           'B': 'It provides a direct connection between an on-premises data center and the VPC.',
           'C': 'It enables horizontal scaling for backend database clusters.',
           'D': 'It serves as a logically redundant component that allows communication between '
                'instances in a VPC and the internet.'},
  'ans': 'D',
  'expl': 'An Internet Gateway attaches to a VPC and provides a target in the VPC routing tables '
          'for internet-bound traffic, enabling public subnets to communicate externally.'},
 {'q': "Which service automates infrastructure provisioning in AWS by treating 'infrastructure as "
       "code' (IaC)?",
  'code': '',
  'opts': {'A': 'AWS Elastic Beanstalk',
           'B': 'AWS CloudFormation',
           'C': 'AWS CodeDeploy',
           'D': 'Amazon EventBridge'},
  'ans': 'B',
  'expl': 'AWS CloudFormation allows developers to define cloud infrastructure using declarative '
          'templates (JSON or YAML), enabling consistent and repeatable resource provisioning.'},
 {'q': 'When utilizing Amazon CloudFront, what determines how content is cached at edge locations, '
       'and how can stale content be forcibly removed before it expires?',
  'code': '',
  'opts': {'A': 'Cache policies dictate expiration; content is removed using an Invalidation '
                'request.',
           'B': 'Route 53 TTL dictates expiration; content is removed by stopping the CloudFront '
                'distribution.',
           'C': 'Origin access identities control caching; content is removed by deleting the S3 '
                'bucket.',
           'D': 'EC2 instance types determine caching speed; content is removed by rebooting the '
                'instance.'},
  'ans': 'A',
  'expl': 'CloudFront uses cache policies (including headers and TTL values) to manage content '
          'retention. Administrators issue cache invalidations to purge specific objects from edge '
          'nodes before natural expiration.'},
 {'q': 'During an interactive rebase (`git rebase -i`), which command must be selected to combine '
       'multiple commits into one while discarding the intermediate commit messages?',
  'code': '',
  'opts': {'A': 'pick', 'B': 'squash', 'C': 'fixup', 'D': 'reword'},
  'ans': 'C',
  'expl': 'In interactive rebase, `squash` melds the commit into the previous one but preserves '
          'its message in the editor. `fixup` also melds the commit but entirely discards its '
          "commit message in favor of the previous commit's message."}]


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