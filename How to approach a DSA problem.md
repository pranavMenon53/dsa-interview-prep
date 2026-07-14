
// Use stack when the flow is linear - left to right or right to left
// Use recursion when the flow is hierarchical - moving up or down - in trees for example
// A recursion problem can most likely be solved using recursion
// But a stack problem may not be solvable using recursion -  why is this?
// Also, recursion shines when there is a need for backtracking.


When to use recursion -

1. When a big problem can be broken down into several smaller problems of the same type
2. Dept is low - languages have a recursion stack dept limitation
3. Recursion shines when backtracking is needed

when to use stack
1. Most recursion solutions can be written in an interative fashion using stack - this will introduce more code by also give you more control - additionally, you will be responsible for storing state
2.

---


Recursion
- Break a bigger problem into smaller sub-problem of the same type
- Backtracking
-

Limitation
- Recursion stack size - depends on the programming language but a depth of 10 ^ 3 is the limit in most cases

---

🔥 This Leads to the Real Insight

🧩 Recursion = Stack + Automatic State Management (All the inputs to the function)

🧩 Explicit Stack = Stack + Manual State Management (you manually descide what to store)

---

🔥 Why You Didn’t Think of Stack

Because your brain optimized for:

“Can I solve this recursively?” → YES → stop searching

🧠 Upgrade This Habit

Force yourself to ask:

“Is there a linear + nested + boundary-driven structure?”

If yes → consider stack EVEN IF recursion works


---

I’m going to give you a compact mental trigger system — not theory, not vague cues — but if-this-then-that rules your brain can actually execute under pressure.

🧠 THE CORE IDEA

When you see a problem, your brain should run this:

INPUT → STRUCTURE → CONSTRAINT → ACTION → PATTERN
🔥 MASTER TRIGGER TREE (Memorize this)
Step 1: What is the input?
🧩 1. Linear (array / string)

→ go to FLOW problems

🌳 2. Hierarchical (tree / graph)

→ go to RECURSION / DFS / BFS

🧠 PATTERN TRIGGERS
1️⃣ STACK
🚨 Trigger:
IF:
- Nested structure exists
- AND input is linear (string/array)
- AND you act on closing boundary (like ')')

THEN → STACK
💡 Keywords:
parentheses
nested expression
“evaluate inside first”
“valid brackets”
“decode string”
🧠 Mental Image:
Push until boundary → collapse → push result back
2️⃣ RECURSION / DFS
🚨 Trigger:
IF:
- Problem can be broken into SAME smaller problems
- AND structure is hierarchical OR branching

THEN → RECURSION
💡 Keywords:
tree
combinations
subsets
paths
divide and conquer
🧠 Mental Image:
Solve(subproblem) → combine results
3️⃣ TWO POINTERS
🚨 Trigger:
IF:
- Array is sorted OR can be sorted
- AND you need pairs/triplets/optimal range

THEN → TWO POINTERS
💡 Keywords:
pair sum
triplet sum
palindrome
container with most water
🧠 Mental Image:
Left ↔ Right → shrink search space
4️⃣ SLIDING WINDOW
🚨 Trigger:
IF:
- Subarray / substring
- AND condition depends on window
- AND you need max/min/longest/shortest

THEN → SLIDING WINDOW
💡 Keywords:
longest substring
max sum subarray
at most K
exactly K
🧠 Mental Image:
Expand → violate → shrink
5️⃣ BINARY SEARCH
🚨 Trigger:
IF:
- Answer lies in a RANGE
- AND condition is monotonic (T → T → F or F → F → T)

THEN → BINARY SEARCH ON ANSWER
💡 Keywords:
minimum / maximum possible
capacity / speed / days
“find smallest X such that…”
🧠 Mental Image:
mid → check → eliminate half
6️⃣ GREEDY
🚨 Trigger:
IF:
- Local optimal choice seems safe
- AND no future dependency breaks it

THEN → GREEDY
💡 Keywords:
intervals
scheduling
minimum steps
maximum profit (simple)
🧠 Mental Image:
Take best now → move on
7️⃣ DYNAMIC PROGRAMMING (DP)
🚨 Trigger:
IF:
- Overlapping subproblems
- AND optimal substructure
- AND brute force is exponential

THEN → DP
💡 Keywords:
count ways
min cost
max profit (complex)
subsequence
🧠 Mental Image:
Store → reuse → avoid recomputation
8️⃣ GRAPH (BFS / DFS)
🚨 Trigger:
IF:
- Nodes + edges OR implicit graph
- AND traversal / connectivity / shortest path

THEN → GRAPH
💡 Keywords:
islands
shortest path
dependencies
cycles
🧠 Mental Image:
Explore neighbors
🔥 APPLY THIS TO YOUR PROBLEM

👉 Parsing A Boolean Expression

Run the system:
Input → string (linear)
Structure → nested
Constraint → evaluate when ')' appears

👉 Matches:

Nested + linear + boundary-driven

✅ → STACK

🧠 FINAL ULTRA-SHORT CHEAT SHEET

Memorize this:

Nested + linear → STACK
Tree/branching → RECURSION
Sorted + pairs → TWO POINTERS
Subarray + condition → SLIDING WINDOW
Range + monotonic → BINARY SEARCH
Local best works → GREEDY
Reuse subproblems → DP
Nodes + edges → GRAPH
🚀 The Real Upgrade

Right now you think:

“What pattern should I use?”

You need to think:

“What constraints FORCE a pattern?”

⚡ If You Want to Master This Fast

Next step (highly recommended):

I give you 10 mixed problems
You:

identify pattern using this system
explain WHY

I’ll correct your thinking → this builds instinct in ~2–3 sessions.

This is exactly how candidates reach Google/Uber level intuition.


START
  |
  v
Q1: What is the input type?
  |
  ├── Tree / Graph / Hierarchical?
  |       |
  |       ├── Need full traversal? → DFS / BFS
  |       |
  |       ├── Shortest path? → BFS (unweighted) / Dijkstra
  |       |
  |       └── All combinations / paths? → RECURSION (Backtracking)
  |
  └── Array / String (Linear)?
          |
          v
Q2: Is there NESTING (like brackets / expressions)?
          |
          ├── YES →
          |       Q: Do I process when I see closing symbol ')'?
          |              ├── YES → STACK
          |              └── NO → RECURSION (rare cases)
          |
          └── NO →
                |
                v
Q3: Are we dealing with SUBARRAY / SUBSTRING?
                |
                ├── YES →
                |       Q: Is it about longest/shortest/max/min?
                |              ├── YES → SLIDING WINDOW
                |              └── NO → Prefix Sum / Hashing
                |
                └── NO →
                      |
                      v
Q4: Is the array SORTED (or can be sorted)?
                      |
                      ├── YES →
                      |       Q: Pair / triplet / range problem?
                      |              ├── YES → TWO POINTERS
                      |              └── NO → Binary Search candidate
                      |
                      └── NO →
                            |
                            v
Q5: Is the answer in a RANGE?
                            |
                            ├── YES →
                            |       Q: Can I check validity (T/F)?
                            |              ├── YES → BINARY SEARCH ON ANSWER
                            |
                            └── NO →
                                  |
                                  v
Q6: Is it asking for OPTIMAL (min/max/count ways)?
                                  |
                                  ├── YES →
                                  |       Q: Overlapping subproblems?
                                  |              ├── YES → DP
                                  |              └── NO → GREEDY
                                  |
                                  └── NO →
                                        |
                                        v
Q7: Need ordering / frequency / fast lookup?
                                        |
                                        ├── YES → HASHMAP / HEAP
                                        |
                                        └── Default → BRUTE → OPTIMIZE



🔥 HOW TO USE THIS IN INTERVIEW (IMPORTANT)

You don’t say the whole flowchart. You think it.

What you say out loud is:

“This is a linear input without nesting, and we’re looking for a longest substring under constraints — this suggests a sliding window approach.”

🧠 ULTRA-COMPACT VERSION (MEMORY HOOK)

If the full flowchart feels heavy, memorize this:

Tree → DFS/BFS
Nested + linear → STACK
Subarray + condition → SLIDING WINDOW
Sorted + pairs → TWO POINTERS
Range + monotonic → BINARY SEARCH
Reuse subproblems → DP
Local optimal works → GREEDY