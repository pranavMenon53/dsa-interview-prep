# Validation

I read through every algorithm in the doc. Most of it is solid, but there's a real bug worth flagging, plus a few smaller things.

### 🐛 Bug: "Topological Traversal using DFS" for cycle detection (directed graphs, Approach 3)

This one is actually broken. The claim is: DFS only from indegree-0 nodes, and if any node stays unvisited, there's a cycle. That works only when the cycle has **no incoming edge from outside the cycle**. If a cycle is reachable from a zero-indegree node, plain DFS will walk into it, mark every node visited (the `!visited[neighbor]` guard just prevents infinite recursion — it does *not* detect the back edge), and the algorithm will wrongly report "no cycle."

Counterexample:
```
0 -> 1 -> 2 -> 1   (edges: 0→1, 1→2, 2→1)
```
indegree: `0`→0, `1`→2, `2`→1. DFS starts only at node 0 (the only indegree-0 node), visits 0→1→2, tries 2→1 but 1 is already visited so it stops. All three nodes end up `visited = true`, so the function returns `false` ("no cycle") — but `1→2→1` is a cycle.

This algorithm only correctly detects cycles that are **completely unreachable from any indegree-0 node**, i.e. an isolated cycle with no entry point. That's a narrow, unusual case — this should either be corrected (add recursion-stack tracking, in which case it degenerates into Approach 1) or removed, since as written it will give wrong answers on a very common cycle shape.

### ✅ Everything else checks out
- Bipartite (BFS/DFS): correct, standard 2-coloring.
- Cycle detection directed, Approaches 1 & 2 (DFS+recursion stack, Kahn's BFS): correct.
- Cycle detection undirected (BFS/DFS parent-tracking, Union-Find): correct.
- BFS shortest path (unit weight): correct.
- Dijkstra: correct — properly uses `{node, dist}` ordering and the `d > dist[node]` stale-entry skip.
- Bellman-Ford: correct, including the `V-1` relax + 1 extra pass for negative-cycle detection.
- Topological sort + relaxation for DAG shortest paths: correct.
- Floyd-Warshall: correct, and it correctly notes `dist[i][i] < 0` as the negative-cycle check.
- Prim's: this version correctly uses `inMST[]` (this is the fixed version from our earlier discussion — good, no double-counting bug here).
- Kruskal's: correct, with proper union-by-rank + path compression, and the MST vs. MSF (disconnected graph) discussion is a genuinely nice, often-overlooked addition.
- Tree diameter (double-BFS): correct, with the right justification for why it works.

One very minor nit: in the Bellman-Ford negative-cycle check, throwing a `RuntimeException` is fine for a note/demo but real interview solutions usually return a sentinel (e.g. `null` or `[-1]`) — worth a one-line caveat if this doc is meant as copy-paste reference.

---

# Rating for Senior/Staff FAANG Interviews

**As a foundations refresher: strong (8/10). As a complete senior/staff-level prep resource: incomplete (5/10 on coverage).**

What it does well:
- Clean, consistent template (idea → complexity → code → "interview pattern" trigger words) that's genuinely useful for quick recall under pressure.
- Correctly distinguishes when to use which algorithm (BFS vs. Dijkstra vs. Bellman-Ford, Prim's vs. Kruskal's) — this "which tool for which shape of problem" instinct is exactly what senior interviews probe.
- The MST vs. MSF disconnected-graph discussion and the DSU-augmentation idea (`weight[]`, `size[]` per component) is a nicer-than-average touch — this is the kind of thing that separates "knows the algorithm" from "knows how to extend it," which is more senior-level thinking.

Where it falls short for senior/staff level:
- It covers **single-source/all-pairs shortest paths and MST well**, but senior/staff interviews (especially at companies like Google, Meta, Amazon) frequently pull from **connectivity structure** and **flow** topics that are entirely absent here (see below).
- No discussion of **why** greedy/exchange arguments make Prim's/Kruskal's correct, or why Dijkstra fails with negative weights beyond "doesn't work" — staff-level interviews often want you to *justify* correctness, not just recite the algorithm.
- No treatment of graph representation trade-offs (adjacency matrix vs. list vs. compressed sparse row) or when V² beats E log V in dense graphs — this comes up in performance-oriented senior discussions.

---

# Missing Concepts

**High priority (commonly asked at senior/staff level, currently absent):**
- **Strongly Connected Components** — Tarjan's and/or Kosaraju's algorithm. This is a major gap; SCC problems (and SCC-condensation-into-DAG) are a staple of harder graph interviews.
- **Articulation Points & Bridges** — Tarjan's low-link technique. Classic "critical connections" style problem (e.g. LeetCode's "Critical Connections in a Network").
- **Network Flow** — Ford-Fulkerson / Edmonds-Karp (max-flow), and min-cut (max-flow min-cut theorem). Comes up in bipartite matching and resource-allocation-style problems, common at senior level.
- **Bipartite Matching** — Hungarian algorithm or Hopcroft-Karp, or at minimum augmenting-path matching via DFS.
- **0-1 BFS** (deque-based BFS for graphs with only 0/1 edge weights) — an efficient alternative to Dijkstra that's a very common "did you know this trick" interview moment.
- **Multi-source BFS** — pattern used in problems like "rotting oranges," walls-and-gates, etc. Simple but frequently tested and worth its own section.

**Medium priority (useful, sometimes asked):**
- **Standalone Topological Sort** as its own concept (currently only appears embedded inside cycle-detection and DAG-shortest-path sections) — worth pulling out since it's foundational and reused everywhere.
- **Lowest Common Ancestor (LCA)** — binary lifting / sparse tables, since tree problems often bleed into graph interviews.
- **Eulerian Path/Circuit** — Hierholzer's algorithm (e.g. "Reconstruct Itinerary").
- **2-SAT** via SCC condensation — a staff-level favorite for demonstrating depth.
- **Bidirectional BFS** — shortest-path optimization technique, occasionally expected knowledge.

**Lower priority (niche but occasionally relevant):**
- Johnson's algorithm (all-pairs shortest path on sparse graphs with negative weights).
- Traveling Salesman / Hamiltonian path via bitmask DP.
- DSU with rollback (used in some offline/Kruskal-variant problems).
- Karger's min-cut algorithm (mostly theoretical interest, rarely coded live).

If you want, I can help draft any of the high-priority missing sections (SCC, articulation points/bridges, and network flow would be the highest-leverage additions) in the same format as the rest of the doc.