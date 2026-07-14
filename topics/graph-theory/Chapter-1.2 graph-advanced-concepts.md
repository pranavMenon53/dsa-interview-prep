# Graph — advanced topics

This draft follows the same template as the original document: **Problem → Idea → Complexity → Code → Interview Pattern**. Drop each section in wherever it fits topically (SCC/Articulation Points near cycle detection, Flow/Matching after MST, etc).

---

## Strongly Connected Components (SCC)

**Definition**

* A **Strongly Connected Component** is a maximal subset of vertices in a **directed graph** such that every vertex is reachable from every other vertex in the subset.
* Only meaningful for **directed graphs** (in undirected graphs, connected components already have this property).

**Approaches**

1. **Kosaraju's Algorithm** *(two-pass DFS)*
2. **Tarjan's Algorithm** *(single-pass DFS, low-link values)*

**Time Complexity:** `O(V + E)` (both algorithms)
**Space Complexity:** `O(V)`

### 1. Kosaraju's Algorithm

**Idea**

* Perform a DFS on the original graph and push nodes onto a stack in order of **finishing time** (like topological sort).
* **Reverse** all edges of the graph.
* Pop nodes from the stack and DFS on the reversed graph. Each DFS tree in this pass is exactly one SCC.

**Why it works**

* If `u` finishes after `v` in the first DFS, and there's a path `u → v` in the reversed graph, then `u` and `v` are mutually reachable in the original graph — this is what the two passes exploit.

<details>
<summary>Click to expand code</summary>

```java
class Solution {

    public int kosaraju(int n, List<List<Integer>> adj) {

        boolean[] visited = new boolean[n];
        Stack<Integer> finishOrder = new Stack<>();

        // Step 1: order nodes by finishing time
        for (int i = 0; i < n; i++) {
            if (!visited[i]) dfs1(i, adj, visited, finishOrder);
        }

        // Step 2: reverse the graph
        List<List<Integer>> transpose = new ArrayList<>();
        for (int i = 0; i < n; i++) transpose.add(new ArrayList<>());

        for (int u = 0; u < n; u++) {
            for (int v : adj.get(u)) {
                transpose.get(v).add(u);
            }
        }

        // Step 3: process nodes in reverse finish order on transposed graph
        Arrays.fill(visited, false);
        int sccCount = 0;

        while (!finishOrder.isEmpty()) {
            int node = finishOrder.pop();
            if (!visited[node]) {
                sccCount++;
                dfs2(node, transpose, visited); // marks the whole SCC visited
            }
        }

        return sccCount;
    }

    private void dfs1(int node, List<List<Integer>> adj, boolean[] visited, Stack<Integer> finishOrder) {
        visited[node] = true;
        for (int neighbor : adj.get(node)) {
            if (!visited[neighbor]) dfs1(neighbor, adj, visited, finishOrder);
        }
        finishOrder.push(node);
    }

    private void dfs2(int node, List<List<Integer>> adj, boolean[] visited) {
        visited[node] = true;
        for (int neighbor : adj.get(node)) {
            if (!visited[neighbor]) dfs2(neighbor, adj, visited);
        }
    }
}
```

</details>

### 2. Tarjan's Algorithm

**Idea**

* Do a single DFS while maintaining, for every node:

  * `disc[node]` — the time it was first discovered.
  * `low[node]` — the smallest discovery time reachable from `node` (including through back edges).
* Maintain a stack of nodes currently "in progress" and an `onStack[]` array.
* When `low[node] == disc[node]`, `node` is the **root of an SCC** — pop everything above and including it off the stack; that's one SCC.

<details>
<summary>Click to expand code</summary>

```java
class Solution {

    int timer = 0;
    int[] disc, low;
    boolean[] onStack;
    Deque<Integer> stack;
    int sccCount = 0;

    public int tarjanSCC(int n, List<List<Integer>> adj) {
        disc = new int[n];
        low = new int[n];
        onStack = new boolean[n];
        stack = new ArrayDeque<>();
        Arrays.fill(disc, -1);

        for (int i = 0; i < n; i++) {
            if (disc[i] == -1) dfs(i, adj);
        }
        return sccCount;
    }

    private void dfs(int node, List<List<Integer>> adj) {
        disc[node] = low[node] = timer++;
        stack.push(node);
        onStack[node] = true;

        for (int neighbor : adj.get(node)) {
            if (disc[neighbor] == -1) {
                dfs(neighbor, adj);
                low[node] = Math.min(low[node], low[neighbor]);
            } else if (onStack[neighbor]) {
                // back edge to a node still on the stack -> still same SCC
                low[node] = Math.min(low[node], disc[neighbor]);
            }
        }

        // node is the root of an SCC
        if (low[node] == disc[node]) {
            sccCount++;
            while (stack.peek() != node) {
                onStack[stack.pop()] = false;
            }
            onStack[stack.pop()] = false; // pop node itself
        }
    }
}
```

</details>

### Interview Pattern

* **"Are these nodes mutually reachable?"** → Think **SCC**.
* **Need to collapse cycles into a single node (condensation graph)** → Compute SCCs, then build a **DAG** over them — very common as a first step before further DP/topological reasoning.
* **Kosaraju** is easier to reason about (two clean DFS passes); **Tarjan's** is a single pass and generally preferred in competitive settings for efficiency.
* SCC condensation + DP is the backbone of harder problems like **2-SAT** (see below).

---

## Articulation Points & Bridges

**Definitions**

* **Articulation Point (Cut Vertex):** a vertex whose removal **increases the number of connected components**.
* **Bridge (Cut Edge):** an edge whose removal **increases the number of connected components**.
* Both apply to **undirected graphs**.

**Idea (Tarjan's low-link technique)**

* Same `disc[]` / `low[]` machinery as Tarjan's SCC, but on an **undirected** graph, tracking the DFS **parent** to avoid immediately walking back along the edge you came from.
* For an edge `(node, neighbor)` that's a **tree edge** (i.e., `neighbor` wasn't visited yet):

  * It's a **bridge** if `low[neighbor] > disc[node]` — meaning `neighbor`'s subtree has **no back edge** reaching `node` or higher.
  * `node` is an **articulation point** if `low[neighbor] >= disc[node]` — meaning `neighbor`'s subtree can't reach above `node` without going through `node`.
* **Special case:** the DFS root is an articulation point only if it has **more than one child** in the DFS tree.

**Time Complexity:** `O(V + E)`
**Space Complexity:** `O(V)`

<details>
<summary>Click to expand code</summary>

```java
class Solution {

    int timer = 0;
    int[] disc, low;
    boolean[] visited, isArticulation;
    Set<String> bridges = new HashSet<>(); // store as "min-max" to represent undirected edge

    public void findCutVerticesAndBridges(int n, List<List<Integer>> adj) {
        disc = new int[n];
        low = new int[n];
        visited = new boolean[n];
        isArticulation = new boolean[n];

        for (int i = 0; i < n; i++) {
            if (!visited[i]) dfs(i, -1, adj);
        }
    }

    private void dfs(int node, int parent, List<List<Integer>> adj) {
        visited[node] = true;
        disc[node] = low[node] = timer++;
        int children = 0;

        for (int neighbor : adj.get(node)) {

            if (neighbor == parent) continue; // skip the edge back to immediate parent
                                               // (careful with multi-edges in real input!)

            if (visited[neighbor]) {
                // back edge
                low[node] = Math.min(low[node], disc[neighbor]);
            } else {
                children++;
                dfs(neighbor, node, adj);
                low[node] = Math.min(low[node], low[neighbor]);

                // Bridge condition
                if (low[neighbor] > disc[node]) {
                    bridges.add(Math.min(node, neighbor) + "-" + Math.max(node, neighbor));
                }

                // Articulation point condition (non-root)
                if (parent != -1 && low[neighbor] >= disc[node]) {
                    isArticulation[node] = true;
                }
            }
        }

        // Articulation point condition (root)
        if (parent == -1 && children > 1) {
            isArticulation[node] = true;
        }
    }
}
```

</details>

### Interview Pattern

* **"Critical connections" / "single point of failure" in a network** → **Bridges** and **Articulation Points**.
* **LeetCode "Critical Connections in a Network"** is directly this bridge-finding algorithm.
* Watch out for **parallel edges** (two nodes connected by more than one edge) — the naive `neighbor == parent` skip will incorrectly treat a real back edge as "going back to parent." In practice, skip by **edge id**, not by node, if the graph can have multi-edges.
* Both bridges and articulation points reduce to the same `disc[]`/`low[]` scaffolding as **Tarjan's SCC** — recognizing that shared machinery is a strong signal of graph fluency in interviews.

---

## Network Flow (Max-Flow / Min-Cut)

**Problem**

* Given a **directed graph** with edge **capacities**, and a **source** `s` and **sink** `t`, find the **maximum amount of flow** that can be pushed from `s` to `t` without exceeding any edge's capacity.

**Key Theorem**

* **Max-Flow Min-Cut Theorem:** the maximum flow from `s` to `t` equals the **minimum capacity** among all cuts that separate `s` from `t`.

**Approaches**

1. **Ford-Fulkerson** (generic method, using any augmenting path — e.g. DFS)
2. **Edmonds-Karp** (Ford-Fulkerson using **BFS** to find augmenting paths — guarantees polynomial time)

**Idea**

* Build a **residual graph**: for every edge `u -> v` with capacity `c` and current flow `f`, the residual capacity is `c - f`. Also add a **reverse edge** `v -> u` with residual capacity `f` (this lets flow "undo" itself later, which is essential for correctness).
* Repeatedly find a path from `s` to `t` in the residual graph with **positive residual capacity** (the "augmenting path").
* Push as much flow as the **bottleneck edge** on that path allows.
* Update residual capacities along the path (forward edges decrease, reverse edges increase).
* Repeat until no augmenting path exists.

**Time Complexity:** `O(V × E²)` for Edmonds-Karp (BFS-based); Ford-Fulkerson's complexity depends on capacities and can be much worse with poor path choices.
**Space Complexity:** `O(V + E)`

<details>
<summary>Click to expand code</summary>

```java
class Solution {

    public int edmondsKarp(int n, int[][][] capacity, int source, int sink) {
        // capacity[u][v] represented via a mutable residual matrix
        int[][] residual = new int[n][n];
        for (int u = 0; u < n; u++)
            for (int v = 0; v < n; v++)
                residual[u][v] = capacity[u][v] != null ? capacity[u][v][0] : 0;

        int maxFlow = 0;

        while (true) {
            int[] parent = bfs(n, residual, source, sink);
            if (parent == null) break; // no augmenting path left

            // find bottleneck capacity along the path
            int pathFlow = Integer.MAX_VALUE;
            for (int v = sink; v != source; v = parent[v]) {
                int u = parent[v];
                pathFlow = Math.min(pathFlow, residual[u][v]);
            }

            // update residual capacities
            for (int v = sink; v != source; v = parent[v]) {
                int u = parent[v];
                residual[u][v] -= pathFlow; // forward edge: reduce capacity
                residual[v][u] += pathFlow; // reverse edge: increase capacity (allows undoing flow)
            }

            maxFlow += pathFlow;
        }

        return maxFlow;
    }

    // Returns parent[] describing an augmenting path from source to sink, or null if none exists
    private int[] bfs(int n, int[][] residual, int source, int sink) {
        int[] parent = new int[n];
        Arrays.fill(parent, -1);
        parent[source] = source;

        Queue<Integer> queue = new LinkedList<>();
        queue.offer(source);

        while (!queue.isEmpty()) {
            int u = queue.poll();
            for (int v = 0; v < n; v++) {
                if (parent[v] == -1 && residual[u][v] > 0) {
                    parent[v] = u;
                    if (v == sink) return parent;
                    queue.offer(v);
                }
            }
        }
        return null; // sink unreachable -> no augmenting path
    }
}
```

</details>

**Note:** the `int[][][] capacity` signature above is just illustrative of "capacity may not exist between every pair"; in practice this is usually built directly from an edge list into an `n x n` residual matrix (dense) or an adjacency list of mutable edge objects (sparse, more common in interviews with large `n`).

### Interview Pattern

* **"Maximum concurrent [something] given capacity constraints"** → Think **Max-Flow**.
* **"Minimum number of edges/vertices to remove to disconnect source from sink"** → **Min-Cut**, same value as max-flow.
* **Bipartite matching problems** (see next section) can be solved as a **special case of max-flow** — connect a super-source to all left nodes and all right nodes to a super-sink, all capacities 1.
* **BFS-based augmenting paths (Edmonds-Karp)** give a real complexity guarantee; plain **DFS-based Ford-Fulkerson** can be arbitrarily slow on pathological capacity choices — an important nuance to mention if asked to justify algorithm choice.

---

## Bipartite Matching

**Problem**

* Given a **bipartite graph** (two disjoint sets `L` and `R`), find the **maximum number of edges** such that no two edges share a vertex (a **maximum matching**).

**Approaches**

1. **Kuhn's Algorithm** *(augmenting path via DFS)* — simple, `O(V × E)`.
2. **Hopcroft-Karp** — finds multiple augmenting paths per phase via BFS+DFS, `O(E √V)`, better for large graphs.
3. **Reduction to Max-Flow** — model as a flow network with unit capacities.

**Idea (Kuhn's Algorithm)**

* For each node `u` in `L`, try to find an **augmenting path**: either some neighbor `v` in `R` is unmatched (match them directly), or `v` is matched to some `u'`, and `u'` can be **rematched** to a different neighbor, freeing up `v` for `u`.
* This is a DFS that tries to "kick" the current match of `v` to make room, recursively.

**Time Complexity:** `O(V × E)`
**Space Complexity:** `O(V)`

<details>
<summary>Click to expand code</summary>

```java
class Solution {

    int[] matchR; // matchR[v] = which left-node v is currently matched to, or -1
    boolean[] visited;
    List<List<Integer>> adj; // adjacency list from left nodes to right nodes

    public int maxBipartiteMatching(int leftSize, int rightSize, List<List<Integer>> adj) {
        this.adj = adj;
        matchR = new int[rightSize];
        Arrays.fill(matchR, -1);

        int result = 0;

        for (int u = 0; u < leftSize; u++) {
            visited = new boolean[rightSize]; // reset per augmenting attempt
            if (tryKuhn(u)) result++;
        }

        return result;
    }

    private boolean tryKuhn(int u) {
        for (int v : adj.get(u)) {
            if (visited[v]) continue;
            visited[v] = true;

            // v is free, or its current match can be reassigned elsewhere
            if (matchR[v] == -1 || tryKuhn(matchR[v])) {
                matchR[v] = u;
                return true;
            }
        }
        return false;
    }
}
```

</details>

### Interview Pattern

* **"Assign tasks to workers", "pair up students to projects", job scheduling with 1:1 constraints** → **Bipartite Matching**.
* **Need to verify the graph is bipartite first** → Run the **bipartite-check** (2-coloring) from earlier in this doc before attempting matching.
* **If the problem also has weights** (e.g. "minimum cost assignment") → that's the **Assignment Problem**, solved by the **Hungarian Algorithm** rather than plain augmenting-path matching.
* Recognizing that this is a **special case of max-flow** (unit-capacity source/sink edges) is often a good thing to mention even if you implement Kuhn's directly — it signals you understand *why* the algorithm works, not just the mechanics.

---

## 0-1 BFS

**Problem**

* Shortest path in a graph where every edge weight is **either 0 or 1**.

**Idea**

* A normal Dijkstra with a Priority Queue works, but is overkill — `O(E log V)` when `O(V + E)` is achievable.
* Use a **Deque** instead of a min-heap:

  * Push neighbors reached via a **weight-1 edge** to the **back** of the deque.
  * Push neighbors reached via a **weight-0 edge** to the **front** of the deque.
* This keeps the deque effectively sorted by distance at all times, without needing heap operations.

**Time Complexity:** `O(V + E)`
**Space Complexity:** `O(V)`

<details>
<summary>Click to expand code</summary>

```java
class Solution {
    public int[] zeroOneBFS(int n, List<List<int[]>> adj, int src) {
        // adj.get(u) contains {v, weight} where weight is 0 or 1
        int[] dist = new int[n];
        Arrays.fill(dist, Integer.MAX_VALUE);
        dist[src] = 0;

        Deque<Integer> deque = new ArrayDeque<>();
        deque.offerFirst(src);

        while (!deque.isEmpty()) {
            int node = deque.pollFirst();

            for (int[] edge : adj.get(node)) {
                int neighbor = edge[0], weight = edge[1];

                if (dist[node] + weight < dist[neighbor]) {
                    dist[neighbor] = dist[node] + weight;

                    if (weight == 0) {
                        deque.offerFirst(neighbor); // 0-weight -> process immediately, same "distance level"
                    } else {
                        deque.offerLast(neighbor);  // 1-weight -> process later
                    }
                }
            }
        }
        return dist;
    }
}
```

</details>

**Note:** unlike Dijkstra, the same node may be pushed onto the deque more than once with different distances; you can add a `dist[node] < currentDist` staleness check when popping if you want to skip redundant reprocessing, though it's not strictly required for correctness given the relaxation guard above.

### Interview Pattern

* **Edge weights restricted to `{0, 1}`** → **0-1 BFS**, not Dijkstra — a common "did you know this trick" question meant to test whether you over-apply Dijkstra everywhere.
* Common disguised form: **"some moves are free, others cost 1 step"** (e.g. grid problems with teleporters/free portals).

---

## Multi-Source BFS

**Problem**

* Given **multiple starting nodes simultaneously**, find the shortest distance from *any* of them to every other node (e.g. "time for rot to spread from all rotten oranges", "distance to nearest gate").

**Idea**

* Push **all source nodes** into the queue at the start, each with distance `0`, instead of running BFS from a single source and taking a min over multiple runs (which would be `O(k × (V + E))` for `k` sources).
* Run a single BFS — the queue naturally processes nodes in order of distance from the **nearest** source.

**Time Complexity:** `O(V + E)` (single pass, regardless of number of sources)
**Space Complexity:** `O(V)`

<details>
<summary>Click to expand code</summary>

```java
class Solution {
    public int[] multiSourceBFS(int n, List<List<Integer>> adj, List<Integer> sources) {
        int[] dist = new int[n];
        Arrays.fill(dist, -1);

        Queue<Integer> queue = new LinkedList<>();
        for (int src : sources) {
            dist[src] = 0;
            queue.offer(src);
        }

        while (!queue.isEmpty()) {
            int node = queue.poll();
            for (int neighbor : adj.get(node)) {
                if (dist[neighbor] == -1) {
                    dist[neighbor] = dist[node] + 1;
                    queue.offer(neighbor);
                }
            }
        }
        return dist;
    }
}
```

</details>

### Interview Pattern

* **"Rotting Oranges", "Walls and Gates", "distance to nearest [X] for every cell"** → **Multi-Source BFS**.
* Don't run BFS once per source and take the minimum — seed the queue with **all sources at once**; this is the single most common inefficiency to avoid here.
* Works identically on grids (treat each cell as a node) and explicit graphs.

---

## Topological Sort (Standalone)

**Problem**

* Given a **Directed Acyclic Graph (DAG)**, produce a linear ordering of vertices such that for every directed edge `u -> v`, `u` appears **before** `v`.

**Approaches**

1. **DFS + Stack** (finish-time based)
2. **Kahn's Algorithm** (BFS + indegree)

**Note:** topological sort is only well-defined on a DAG — if the graph has a cycle, no valid ordering exists (see the Cycle Detection sections above, which reuse this exact machinery).

**Time Complexity:** `O(V + E)`
**Space Complexity:** `O(V)`

### 1. DFS-Based

<details>
<summary>Click to expand code</summary>

```java
class Solution {
    public int[] topoSortDFS(int n, List<List<Integer>> adj) {
        boolean[] visited = new boolean[n];
        Stack<Integer> stack = new Stack<>();

        for (int i = 0; i < n; i++) {
            if (!visited[i]) dfs(i, adj, visited, stack);
        }

        int[] result = new int[n];
        int idx = 0;
        while (!stack.isEmpty()) result[idx++] = stack.pop();
        return result;
    }

    private void dfs(int node, List<List<Integer>> adj, boolean[] visited, Stack<Integer> stack) {
        visited[node] = true;
        for (int neighbor : adj.get(node)) {
            if (!visited[neighbor]) dfs(neighbor, adj, visited, stack);
        }
        stack.push(node); // push after all descendants are processed
    }
}
```

</details>

### 2. Kahn's Algorithm (BFS)

<details>
<summary>Click to expand code</summary>

```java
class Solution {
    public int[] topoSortKahn(int n, List<List<Integer>> adj) {
        int[] indegree = new int[n];
        for (int u = 0; u < n; u++)
            for (int v : adj.get(u)) indegree[v]++;

        Queue<Integer> queue = new LinkedList<>();
        for (int i = 0; i < n; i++)
            if (indegree[i] == 0) queue.offer(i);

        int[] result = new int[n];
        int idx = 0;

        while (!queue.isEmpty()) {
            int node = queue.poll();
            result[idx++] = node;

            for (int neighbor : adj.get(node)) {
                if (--indegree[neighbor] == 0) queue.offer(neighbor);
            }
        }

        // if idx != n, the graph has a cycle -> no valid topological order
        return idx == n ? result : new int[0];
    }
}
```

</details>

### Interview Pattern

* **"Order tasks given dependencies"**, **course scheduling**, **build systems** → **Topological Sort**.
* **DFS version** naturally reuses the same pattern as directed cycle detection (Approach 1 earlier in this doc) — if you're already doing DFS cycle detection, you get topo sort almost for free.
* **Kahn's version** is preferred when you also need to **detect a cycle** as a side effect (compare `idx` to `n`), or when an **iterative** (non-recursive) solution is required to avoid stack overflow on deep graphs.

---

## Lowest Common Ancestor (LCA) — Binary Lifting

**Problem**

* Given a **tree** and repeated queries `(u, v)`, find the **lowest common ancestor** of `u` and `v` — the deepest node that is an ancestor of both.

**Idea (Binary Lifting)**

* Precompute `up[node][k]` = the `2^k`-th ancestor of `node`, via `up[node][k] = up[up[node][k-1]][k-1]`.
* To find `LCA(u, v)`:

  1. Bring the deeper node up to the same depth as the shallower one, using binary jumps.
  2. If they're now equal, that's the LCA.
  3. Otherwise, binary-jump **both** nodes up together, in decreasing powers of two, as long as their ancestors differ — the LCA is one step above where they finally meet.

**Time Complexity:** `O((V log V))` preprocessing, `O(log V)` per query
**Space Complexity:** `O(V log V)`

<details>
<summary>Click to expand code</summary>

```java
class LCA {
    int LOG;
    int[][] up;
    int[] depth;

    public void build(int n, List<List<Integer>> adj, int root) {
        LOG = (int) (Math.ceil(Math.log(n) / Math.log(2))) + 1;
        up = new int[n][LOG];
        depth = new int[n];

        boolean[] visited = new boolean[n];
        dfs(root, root, 0, adj, visited);

        // Fill sparse table: up[node][k] = 2^k-th ancestor
        for (int k = 1; k < LOG; k++) {
            for (int node = 0; node < n; node++) {
                up[node][k] = up[up[node][k - 1]][k - 1];
            }
        }
    }

    private void dfs(int node, int parent, int d, List<List<Integer>> adj, boolean[] visited) {
        visited[node] = true;
        depth[node] = d;
        up[node][0] = parent;

        for (int neighbor : adj.get(node)) {
            if (!visited[neighbor]) dfs(neighbor, node, d + 1, adj, visited);
        }
    }

    public int lca(int u, int v) {
        if (depth[u] < depth[v]) { int tmp = u; u = v; v = tmp; }

        int diff = depth[u] - depth[v];
        for (int k = 0; k < LOG; k++) {
            if (((diff >> k) & 1) == 1) u = up[u][k];
        }

        if (u == v) return u;

        for (int k = LOG - 1; k >= 0; k--) {
            if (up[u][k] != up[v][k]) {
                u = up[u][k];
                v = up[v][k];
            }
        }

        return up[u][0]; // one step above where they diverged
    }
}
```

</details>

### Interview Pattern

* **Repeated ancestor/path queries on a fixed tree** → **Binary Lifting LCA** — the `O(log V)` per-query cost matters when there are many queries.
* **Only one or two LCA queries total** → a simpler `O(V)` approach (e.g. storing root-to-node paths and comparing) may be simpler to code under time pressure; mention the trade-off if asked.
* Often combined with computing **distance between two nodes** in a tree: `dist(u, v) = depth[u] + depth[v] - 2 * depth[lca(u, v)]`.

---

## Eulerian Path / Circuit — Hierholzer's Algorithm

**Definitions**

* **Eulerian Path:** a path that uses **every edge exactly once**.
* **Eulerian Circuit:** an Eulerian path that starts and ends at the **same vertex**.

**Existence Conditions (undirected graph)**

* **Eulerian Circuit** exists iff every vertex has **even degree** (and the graph is connected, ignoring isolated vertices).
* **Eulerian Path** (not circuit) exists iff **exactly 0 or 2 vertices** have **odd degree**. If 2, the path must start at one of them and end at the other.

**Idea (Hierholzer's Algorithm)**

* Start at a vertex, greedily follow unused edges until stuck (back at the start, or a dead end for a path).
* This traces out one closed loop (or ends at the "path" endpoint).
* Whenever the current node still has unused edges, that means there's a sub-loop hanging off it — recurse/detour into it, splice it into the route, and continue.
* Implemented efficiently as: DFS while **removing edges as you traverse them**, and add nodes to the answer **on the way back out of the recursion** (post-order) — this naturally handles splicing in the loop-detours in the right order.

**Time Complexity:** `O(V + E)`
**Space Complexity:** `O(V + E)`

<details>
<summary>Click to expand code</summary>

```java
class Solution {

    Map<Integer, LinkedList<Integer>> adj;
    LinkedList<Integer> route = new LinkedList<>();

    public List<Integer> eulerianPath(int n, int[][] edges, int start) {
        adj = new HashMap<>();
        for (int i = 0; i < n; i++) adj.put(i, new LinkedList<>());

        for (int[] e : edges) adj.get(e[0]).add(e[1]);
        // for undirected graphs, also add the reverse edge and remove
        // the specific paired occurrence (not just any edge to that node) when traversing

        dfs(start);
        Collections.reverse(route); // built in post-order, so reverse for the correct traversal order
        return route;
    }

    private void dfs(int node) {
        LinkedList<Integer> neighbors = adj.get(node);
        while (!neighbors.isEmpty()) {
            int next = neighbors.poll(); // consume the edge (removes it so it's not reused)
            dfs(next);
        }
        route.addFirst(node); // post-order add
    }
}
```

</details>

### Interview Pattern

* **"Use every edge/ticket/flight exactly once"** (e.g. **LeetCode "Reconstruct Itinerary"**) → **Eulerian Path** via **Hierholzer's Algorithm**.
* Don't confuse with **Hamiltonian Path** (visit every **vertex** once) — Hamiltonian path is **NP-hard** in general; Eulerian path is `O(V + E)`. Interviewers sometimes phrase problems ambiguously to see if you catch which one actually applies.
* When ties need to be broken (e.g. lexicographically smallest itinerary), traverse neighbors in sorted order (e.g. using a min-heap or sorted structure per node instead of `LinkedList`).

---

## 2-SAT

**Problem**

* Given a boolean formula in **2-CNF** (conjunction of clauses, each with exactly 2 literals, e.g. `(a ∨ ¬b) ∧ (¬a ∨ c) ...`), determine if there's a variable assignment that satisfies all clauses — and if so, construct one.

**Idea**

* For each variable `x`, create two nodes: `x` (true) and `¬x` (false).
* For each clause `(a ∨ b)`, add two **implication edges**: `¬a → b` and `¬b → a` (i.e., "if `a` is false, `b` must be true," and vice versa).
* Compute **SCCs** of this implication graph.
* The formula is **satisfiable** iff, for every variable `x`, `x` and `¬x` are in **different SCCs**.
* If satisfiable, assign each variable based on which of `x` / `¬x` comes **later** in the topological order of the SCC-condensation graph (equivalently: `x = true` if `SCC(x)` comes after `SCC(¬x)` in that ordering).

**Time Complexity:** `O(V + E)` (dominated by the SCC computation)
**Space Complexity:** `O(V + E)`

<details>
<summary>Click to expand code</summary>

```java
class Solution {

    // variables are 0..n-1; node 2*i = variable i is TRUE, node 2*i+1 = variable i is FALSE
    public boolean[] solve2SAT(int n, int[][][] clauses) {
        // clauses[k] = {{varA, valA}, {varB, valB}} representing (litA OR litB)
        // valA/valB: 1 = as-is, 0 = negated
        int numNodes = 2 * n;
        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < numNodes; i++) adj.add(new ArrayList<>());

        for (int[][] clause : clauses) {
            int a = node(clause[0][0], clause[0][1]);
            int b = node(clause[1][0], clause[1][1]);
            // (a OR b)  =>  (NOT a -> b) and (NOT b -> a)
            adj.get(negate(a)).add(b);
            adj.get(negate(b)).add(a);
        }

        int[] sccId = computeSCC(numNodes, adj); // sccId[node] in topological order of condensation

        boolean[] assignment = new boolean[n];
        for (int i = 0; i < n; i++) {
            int trueNode = 2 * i, falseNode = 2 * i + 1;
            if (sccId[trueNode] == sccId[falseNode]) return null; // UNSATISFIABLE

            // whichever literal's SCC comes LATER in topological order is the one that must be true
            assignment[i] = sccId[trueNode] > sccId[falseNode];
        }

        return assignment;
    }

    private int node(int var, int val) { return val == 1 ? 2 * var : 2 * var + 1; }
    private int negate(int node) { return node % 2 == 0 ? node + 1 : node - 1; }

    // returns sccId[] such that a HIGHER id means it comes LATER in topological order
    // (implementation detail: use Kosaraju/Tarjan from earlier sections)
    private int[] computeSCC(int n, List<List<Integer>> adj) {
        // ... reuse Tarjan's or Kosaraju's SCC code from above ...
        throw new UnsupportedOperationException("plug in SCC implementation from earlier section");
    }
}
```

</details>

### Interview Pattern

* **"Assign true/false to variables subject to pairwise constraints", scheduling with mutual-exclusion constraints, "either A or B but figure out consistently"** → **2-SAT**.
* This is a **staff-level favorite** precisely because it chains two earlier concepts together (**implication graph construction** + **SCC**) — a strong signal of depth if you can derive the construction rather than recite it.
* Constraints like "exactly one of A, B" or "A implies B" can all be encoded as 2-CNF clauses — worth practicing the encoding step, since that's usually the harder part relative to the SCC computation itself.

---

## Bidirectional BFS

**Problem**

* Shortest path between a **single source** and a **single target** in an unweighted graph — when you don't need distances to *every* node, just the one path.

**Idea**

* Run **two BFS frontiers simultaneously**: one expanding forward from the source, one expanding backward from the target.
* Alternate expanding whichever frontier is currently **smaller** (this is the key optimization).
* Stop as soon as the two frontiers **meet** — the total path length is the sum of both sides' depths.
* Reduces search space from `O(b^d)` to roughly `O(b^(d/2))` for branching factor `b` and depth `d` — a huge practical speedup on wide graphs.

**Time Complexity:** `O(b^(d/2))` vs. `O(b^d)` for one-directional BFS (same asymptotic worst case of `O(V + E)` but far better in practice)
**Space Complexity:** `O(V)`

<details>
<summary>Click to expand code</summary>

```java
class Solution {
    public int bidirectionalBFS(int n, List<List<Integer>> adj, int source, int target) {
        if (source == target) return 0;

        Map<Integer, Integer> distFromSource = new HashMap<>();
        Map<Integer, Integer> distFromTarget = new HashMap<>();
        distFromSource.put(source, 0);
        distFromTarget.put(target, 0);

        Queue<Integer> frontierSource = new LinkedList<>();
        Queue<Integer> frontierTarget = new LinkedList<>();
        frontierSource.offer(source);
        frontierTarget.offer(target);

        while (!frontierSource.isEmpty() && !frontierTarget.isEmpty()) {

            // always expand the smaller frontier
            if (frontierSource.size() <= frontierTarget.size()) {
                Integer meet = expand(frontierSource, distFromSource, distFromTarget, adj);
                if (meet != null) return distFromSource.get(meet) + distFromTarget.get(meet);
            } else {
                Integer meet = expand(frontierTarget, distFromTarget, distFromSource, adj);
                if (meet != null) return distFromSource.get(meet) + distFromTarget.get(meet);
            }
        }

        return -1; // unreachable
    }

    private Integer expand(Queue<Integer> frontier, Map<Integer, Integer> myDist,
                            Map<Integer, Integer> otherDist, List<List<Integer>> adj) {
        int size = frontier.size();
        for (int i = 0; i < size; i++) {
            int node = frontier.poll();
            for (int neighbor : adj.get(node)) {
                if (!myDist.containsKey(neighbor)) {
                    myDist.put(neighbor, myDist.get(node) + 1);
                    if (otherDist.containsKey(neighbor)) return neighbor; // frontiers met
                    frontier.offer(neighbor);
                }
            }
        }
        return null;
    }
}
```

</details>

### Interview Pattern

* **"Shortest transformation sequence between two words" (Word Ladder), shortest path in a huge implicit graph with one fixed source and one fixed target** → **Bidirectional BFS**.
* Only worth it when you have a **specific target**, not "distance to everything" — for the latter, use plain (multi-source) BFS instead.
* A common follow-up: "why is expanding the smaller frontier important?" — because it keeps the total work proportional to the smaller of the two exponential frontiers rather than always the source side.

---

## Johnson's Algorithm

**Problem**

* All-pairs shortest paths on a **sparse** graph that may have **negative edge weights** (but no negative cycles) — faster than Floyd-Warshall's `O(V³)` when `E` is much smaller than `V²`.

**Idea**

* Add a new virtual node `q` with a **zero-weight edge to every other vertex**.
* Run **Bellman-Ford** from `q` to compute `h[v]` for every vertex (this also detects negative cycles).
* **Reweight** every edge: `w'(u, v) = w(u, v) + h[u] - h[v]`. This reweighting is guaranteed to make all edge weights **non-negative**, while preserving which paths are shortest.
* Run **Dijkstra** from every vertex on the reweighted graph.
* Convert reweighted distances back: `dist(u, v) = dist'(u, v) - h[u] + h[v]`.

**Time Complexity:** `O(V² log V + V × E)` — dominated by running Dijkstra from every node, versus Floyd-Warshall's `O(V³)`.
**Space Complexity:** `O(V²)` (to store all-pairs results) plus `O(V + E)` working space.

<details>
<summary>Click to expand code</summary>

```java
class Solution {
    public int[][] johnsons(int n, int[][] edges) {
        // edges[i] = {u, v, weight}

        // Step 1: add virtual node q (index n) with 0-weight edges to all nodes
        List<int[]> augmentedEdges = new ArrayList<>(Arrays.asList(edges));
        for (int i = 0; i < n; i++) augmentedEdges.add(new int[]{n, i, 0});

        // Step 2: Bellman-Ford from q to get h[] (throws/flags if negative cycle detected)
        int[] h = bellmanFord(n + 1, augmentedEdges.toArray(new int[0][]), n);

        // Step 3: reweight edges so all become non-negative
        List<int[]> reweighted = new ArrayList<>();
        for (int[] e : edges) {
            reweighted.add(new int[]{e[0], e[1], e[2] + h[e[0]] - h[e[1]]});
        }

        List<List<int[]>> adj = new ArrayList<>();
        for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
        for (int[] e : reweighted) adj.get(e[0]).add(new int[]{e[1], e[2]});

        // Step 4: run Dijkstra from every node on the reweighted graph, then un-reweight
        int[][] result = new int[n][n];
        for (int src = 0; src < n; src++) {
            int[] dPrime = dijkstra(n, adj, src);
            for (int v = 0; v < n; v++) {
                result[src][v] = dPrime[v] == Integer.MAX_VALUE
                        ? Integer.MAX_VALUE
                        : dPrime[v] - h[src] + h[v]; // convert back to true distance
            }
        }
        return result;
    }

    // Reuse Bellman-Ford / Dijkstra implementations from earlier in this doc.
    private int[] bellmanFord(int n, int[][] edges, int src) { throw new UnsupportedOperationException(); }
    private int[] dijkstra(int n, List<List<int[]>> adj, int src) { throw new UnsupportedOperationException(); }
}
```

</details>

### Interview Pattern

* **"All-pairs shortest paths, but the graph is sparse and has negative edges"** → **Johnson's Algorithm**, not Floyd-Warshall.
* The **reweighting trick** (`w' = w + h[u] - h[v]`) making all weights non-negative while preserving shortest-path structure is the conceptual core — worth being able to explain *why* it works: any path's total reweighted cost differs from its original cost by exactly `h[source] - h[destination]`, a constant for a fixed pair, so relative path ordering (i.e. which path is shortest) is unchanged.
* Effectively **"Bellman-Ford once + Dijkstra V times"** — a good one-liner if asked to summarize.

---

## Traveling Salesman Problem (Bitmask DP)

**Problem**

* Given `n` cities and pairwise distances, find the shortest possible route that visits **every city exactly once** and returns to the start.
* **NP-hard** in general — the bitmask DP below is an **exact** exponential-time solution, feasible for small `n` (typically `n ≤ ~20`).

**Idea**

* State: `dp[mask][i]` = minimum cost to have visited exactly the set of cities in `mask`, ending at city `i`.
* `mask` is a bitmask where bit `j` set means city `j` has been visited.
* Transition: `dp[mask][i] = min over j in mask, j != i, of dp[mask without i][j] + dist[j][i]`.
* Answer: `min over i of dp[fullMask][i] + dist[i][0]` (returning to the start).

**Time Complexity:** `O(n² × 2ⁿ)`
**Space Complexity:** `O(n × 2ⁿ)`

<details>
<summary>Click to expand code</summary>

```java
class Solution {
    public int tsp(int n, int[][] dist) {
        int fullMask = (1 << n) - 1;
        int[][] dp = new int[1 << n][n];
        for (int[] row : dp) Arrays.fill(row, -1);

        return solve(1, 0, n, fullMask, dist, dp); // start at city 0, mask = {0}
    }

    private int solve(int mask, int pos, int n, int fullMask, int[][] dist, int[][] dp) {
        if (mask == fullMask) return dist[pos][0]; // all visited -> return to start

        if (dp[mask][pos] != -1) return dp[mask][pos];

        int best = Integer.MAX_VALUE;
        for (int next = 0; next < n; next++) {
            if ((mask & (1 << next)) == 0) { // next city not yet visited
                int cost = dist[pos][next] + solve(mask | (1 << next), next, n, fullMask, dist, dp);
                best = Math.min(best, cost);
            }
        }

        return dp[mask][pos] = best;
    }
}
```

</details>

### Interview Pattern

* **"Visit every node exactly once at minimum cost", small `n` (≤ ~20), and the problem explicitly allows exponential time** → **Bitmask DP TSP**. If `n` is large, TSP is intractable exactly — mention that only approximation algorithms (e.g. nearest-neighbor, Christofides) or heuristics are feasible.
* This is a common gateway into recognizing **"visited set as state"** bitmask-DP patterns more broadly (e.g. "assign n tasks to n workers minimizing cost" is a similar shape).
* Contrast explicitly with **Hamiltonian Path/Cycle existence** (yes/no question, still NP-hard) vs. TSP (minimum-cost version) — interviewers sometimes conflate the phrasing.

---

## Disjoint Set Union with Rollback

**Problem**

* Standard DSU with **path compression** doesn't support "undo" cleanly, because path compression permanently changes parent pointers. Some problems (e.g. offline queries, Kruskal-variant problems that need to try-then-revert edges, or DSU-over-time / persistence problems) need to **undo** a union operation.

**Idea**

* Use **union by rank/size only** — **no path compression** (path compression is what makes rollback hard to reverse cleanly).
* Maintain a **history stack** of the changes made by each `union` call (which pointers were changed, and their old values).
* To **rollback**, pop the stack and restore the old values.
* Without path compression, operations are `O(log V)` instead of nearly `O(1)`, but rollback becomes possible.

**Time Complexity:** `O(log V)` per operation (union/find), `O(1)` per rollback
**Space Complexity:** `O(V)`

<details>
<summary>Click to expand code</summary>

```java
class DSURollback {
    int[] parent, rank_;
    Deque<int[]> history = new ArrayDeque<>(); // {childRoot, childOldParent, childOldRank, changedRankFlag}

    public DSURollback(int n) {
        parent = new int[n];
        rank_ = new int[n];
        for (int i = 0; i < n; i++) parent[i] = i;
    }

    // NOTE: no path compression here, intentionally
    public int find(int x) {
        while (parent[x] != x) x = parent[x];
        return x;
    }

    public boolean union(int x, int y) {
        int rx = find(x), ry = find(y);
        if (rx == ry) {
            history.push(new int[]{-1, -1, -1, -1}); // no-op marker, keeps rollback stack aligned
            return false;
        }

        if (rank_[rx] < rank_[ry]) { int tmp = rx; rx = ry; ry = tmp; }

        // record enough info to undo this union
        int rankChanged = (rank_[rx] == rank_[ry]) ? 1 : 0;
        history.push(new int[]{ry, ry, rank_[rx], rankChanged});

        parent[ry] = rx;
        if (rankChanged == 1) rank_[rx]++;

        return true;
    }

    public void rollback() {
        int[] last = history.pop();
        if (last[0] == -1) return; // no-op union, nothing to undo

        int child = last[1];
        int parentRankBeforeMerge = last[2];
        int rankWasIncremented = last[3];

        int root = find(child); // root is now the merged parent (no compression, so this is safe)
        parent[child] = child;
        if (rankWasIncremented == 1) rank_[root] = parentRankBeforeMerge;
    }
}
```

</details>

### Interview Pattern

* **"Process queries offline, some of which add an edge and some of which ask 'is X connected to Y', with the constraint that you need to peel back edges"**, or **divide-and-conquer over time on DSU (CDQ / offline dynamic connectivity)** → **DSU with Rollback**.
* Key trade-off to state explicitly: you give up path compression's near-`O(1)` amortized cost to gain rollback capability — a good example of a **time/functionality trade-off** worth articulating if asked "why not just use standard DSU here?"
* Rarely needed outside of specifically offline / persistence-flavored problems — mention it as a tool you reach for **only** when standard DSU or Kruskal's can't handle "undo."

---

## Karger's Min-Cut Algorithm

**Problem**

* Find the **global minimum cut** of an undirected, weighted (or unweighted) graph — the smallest set of edges whose removal disconnects the graph into two components — **without** a designated source/sink (contrast with max-flow min-cut, which is *s-t* specific).

**Idea (Randomized Contraction)**

* Repeatedly pick a **random edge** and **contract** it — merge its two endpoints into a single "super-node," keeping all edges (including parallel ones), and removing self-loops that result.
* Continue until only **2 super-nodes** remain. The edges remaining between them form a **candidate cut**.
* This is a **randomized algorithm**: a single run finds the true min-cut only with probability `≥ 2 / n²`. Repeating the process `O(n² log n)` times and keeping the smallest cut found boosts the success probability to be very high (this is the standard "**Karger-Stein**" refinement for practical use).

**Time Complexity:** `O(n²)` per trial (naive contraction); repeated `O(n² log n)` times for high-probability correctness, giving `O(n⁴ log n)` total for the naive version (Karger-Stein's recursive variant improves this to `O(n² log³ n)`).
**Space Complexity:** `O(V + E)`

<details>
<summary>Click to expand code</summary>

```java
class Solution {
    public int minCut(int n, int[][] edgeList) {
        int best = Integer.MAX_VALUE;
        int trials = n * n; // roughly O(n^2 log n) for high confidence in practice; simplified here

        for (int t = 0; t < trials; t++) {
            best = Math.min(best, contractOnce(n, edgeList));
        }
        return best;
    }

    private int contractOnce(int n, int[][] edgeList) {
        int[] parent = new int[n];
        for (int i = 0; i < n; i++) parent[i] = i;

        List<int[]> edges = new ArrayList<>(Arrays.asList(edgeList));
        Collections.shuffle(edges);

        int remainingNodes = n;
        int idx = 0;

        while (remainingNodes > 2 && idx < edges.size()) {
            int[] edge = edges.get(idx++);
            int ru = find(parent, edge[0]);
            int rv = find(parent, edge[1]);

            if (ru == rv) continue; // self-loop after contraction, skip

            parent[ru] = rv; // contract u's component into v's
            remainingNodes--;
        }

        // count edges crossing between the two remaining super-nodes
        int cutEdges = 0;
        for (int[] edge : edgeList) {
            if (find(parent, edge[0]) != find(parent, edge[1])) cutEdges++;
        }
        return cutEdges;
    }

    private int find(int[] parent, int x) {
        while (parent[x] != x) x = parent[x];
        return x;
    }
}
```

</details>

### Interview Pattern

* **Mostly theoretical interest** — asked more to test familiarity with **randomized algorithms** than as a "write this from scratch" coding question. Deterministic min-cut via **max-flow min-cut** (fix one node as source, try every other node as sink) is the practical `s-t`-free approach most interviews actually expect: `O(V)` max-flow runs.
* If it does come up, the discussion is usually conceptual: **why repeated random trials boost success probability**, and the contrast with **max-flow-based** deterministic min-cut.
* Good one-liner distinction: **max-flow min-cut** finds the min cut **between two specific nodes**; **Karger's** finds the **global** min cut with no fixed source/sink.

---

## Graph Coloring (Chromatic Number)

**Problem**

* Assign colors to vertices such that **no two adjacent vertices share a color**, using the **minimum number of colors** possible (the **chromatic number**).
* General case is **NP-hard**; interviews usually restrict to a **fixed number of colors `k`** ("can this graph be colored with `k` colors?") rather than asking for the true minimum.

**Idea (Backtracking for fixed `k`)**

* Try coloring vertices one at a time.
* For each vertex, try every color `1..k` that doesn't conflict with already-colored neighbors.
* Recurse; backtrack if no color works for some vertex.

**Time Complexity:** `O(k^V)` worst case (exponential — this is expected, since the decision problem is NP-complete for `k ≥ 3`)
**Space Complexity:** `O(V)`

<details>
<summary>Click to expand code</summary>

```java
class Solution {
    public boolean canColor(int n, List<List<Integer>> adj, int k) {
        int[] color = new int[n];
        Arrays.fill(color, -1);
        return backtrack(0, n, adj, color, k);
    }

    private boolean backtrack(int node, int n, List<List<Integer>> adj, int[] color, int k) {
        if (node == n) return true; // all vertices successfully colored

        for (int c = 0; c < k; c++) {
            if (isSafe(node, c, adj, color)) {
                color[node] = c;
                if (backtrack(node + 1, n, adj, color, k)) return true;
                color[node] = -1; // backtrack
            }
        }
        return false;
    }

    private boolean isSafe(int node, int c, List<List<Integer>> adj, int[] color) {
        for (int neighbor : adj.get(node)) {
            if (color[neighbor] == c) return false;
        }
        return true;
    }
}
```

</details>

### Interview Pattern

* **"Can this be scheduled/assigned with only `k` resources/slots such that conflicting items don't share one?"** (exam scheduling, register allocation, radio-frequency assignment) → **Graph Coloring**.
* Special case worth knowing: a graph is **2-colorable exactly when it's bipartite** — so the bipartite check from the very first section of this doc *is* graph coloring for `k = 2`, solvable in `O(V + E)` instead of exponential time.
* If asked for the **true minimum** number of colors (not a fixed `k`), be upfront that this is NP-hard in general — a reasonable interview answer is to describe the backtracking-for-fixed-`k` approach and mention trying increasing values of `k`.

---

## Widest Path / Maximum Bottleneck Path

**Problem**

* Find the path between two nodes that **maximizes the minimum edge weight** along the path (the "bottleneck" of the path). Common framing: "maximize the minimum bandwidth/capacity along a route."

**Idea**

* Nearly identical structure to Dijkstra, but instead of **summing** weights and minimizing, you track the **bottleneck-so-far** and **maximize** it.
* Use a **max-heap** ordered by bottleneck value.
* Relaxation: `bottleneck[neighbor] = max(bottleneck[neighbor], min(bottleneck[node], edgeWeight))`.

**Time Complexity:** `O(E log V)`
**Space Complexity:** `O(V)`

<details>
<summary>Click to expand code</summary>

```java
class Solution {
    public int[] widestPath(int n, List<List<int[]>> adj, int src) {
        int[] bottleneck = new int[n];
        Arrays.fill(bottleneck, Integer.MIN_VALUE);
        bottleneck[src] = Integer.MAX_VALUE; // no constraint yet at the source

        // max-heap of {bottleneck, node}
        PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> b[0] - a[0]);
        pq.offer(new int[]{Integer.MAX_VALUE, src});

        while (!pq.isEmpty()) {
            int[] curr = pq.poll();
            int currBottleneck = curr[0], node = curr[1];

            if (currBottleneck < bottleneck[node]) continue; // stale entry

            for (int[] edge : adj.get(node)) {
                int neighbor = edge[0], weight = edge[1];
                int candidate = Math.min(currBottleneck, weight);

                if (candidate > bottleneck[neighbor]) {
                    bottleneck[neighbor] = candidate;
                    pq.offer(new int[]{candidate, neighbor});
                }
            }
        }
        return bottleneck;
    }
}
```

</details>

### Interview Pattern

* **"Maximize the minimum edge along a path"** (network bandwidth, "path with maximum possible truck weight limit") → **Widest Path**, a Dijkstra variant with max-heap + min/max instead of sum/min.
* Contrast with **minimax path** (minimize the *maximum* edge weight) — same idea, flipped: min-heap + `max(bottleneck, weight)` relaxation, tracking the smallest possible "worst edge."
* Also solvable via a **modified Kruskal's**: sort edges descending, union-find until source and target connect — the last edge added is the bottleneck. Worth mentioning as an alternative, especially for **all-pairs** widest-path variants.

---

## Summary Table (New Additions)

| Concept | Typical Trigger Phrase | Time Complexity |
|---|---|---|
| SCC (Kosaraju/Tarjan) | "mutually reachable", condensation graph | `O(V + E)` |
| Articulation Points & Bridges | "critical connections", single point of failure | `O(V + E)` |
| Network Flow (Edmonds-Karp) | "max concurrent flow", "min cut between s and t" | `O(V·E²)` |
| Bipartite Matching (Kuhn's) | "assign tasks/workers 1:1" | `O(V·E)` |
| 0-1 BFS | edge weights only 0 or 1 | `O(V + E)` |
| Multi-Source BFS | "distance to nearest X from every cell" | `O(V + E)` |
| Topological Sort (standalone) | task ordering / dependency resolution | `O(V + E)` |
| LCA (Binary Lifting) | repeated ancestor queries on a tree | `O(log V)`/query |
| Eulerian Path (Hierholzer's) | "use every edge exactly once" | `O(V + E)` |
| 2-SAT | boolean constraint satisfaction, pairwise implications | `O(V + E)` |
| Bidirectional BFS | shortest path, single source & single target | `O(b^(d/2))` |
| Johnson's Algorithm | all-pairs shortest path, sparse + negative weights | `O(V² log V + V·E)` |
| TSP (Bitmask DP) | visit every node once, minimum cost, small `n` | `O(n²·2ⁿ)` |
| DSU with Rollback | offline queries needing "undo" on unions | `O(log V)` |
| Karger's Min-Cut | global min-cut, no fixed source/sink | `O(n²)`/trial |
| Graph Coloring | "k resources, no conflicting neighbors" | `O(k^V)` (NP-hard) |
| Widest Path | "maximize the minimum edge along a path" | `O(E log V)` |

---

## Practice Problems by Concept

A few concrete, well-known problems to anchor each concept — useful for building a study plan around this doc.

| Concept | Problem | Notes |
|---|---|---|
| SCC | Number of Provinces (directed variant) / Course Schedule follow-ups | Condensation into a DAG is often the *first step*, not the final answer |
| SCC | Strongly Connected Components (GFG/InterviewBit classic) | Direct application of Kosaraju's or Tarjan's |
| Articulation Points & Bridges | Critical Connections in a Network (LeetCode 1192) | Direct application of the bridge-finding low-link technique |
| Articulation Points & Bridges | Number of Operations to Make Network Connected | Needs bridge/connectivity reasoning, not just raw BFS |
| Network Flow | Maximum Flow (classic textbook problem, e.g. CSES "Download Speed") | Good first flow problem before attempting matching-as-flow |
| Network Flow | Snake and Ladders / project selection style min-cut problems | Practice recognizing when "minimum to remove/select" maps to min-cut |
| Bipartite Matching | Maximum Bipartite Matching (GFG classic) | Direct Kuhn's algorithm application |
| Bipartite Matching | Job Scheduling with 1:1 constraints | Common "disguised" matching problem |
| 0-1 BFS | Shortest Path in Binary Matrix with obstacles that cost 1 to remove | Classic 0-1 BFS setup: 0 to move through open cells, 1 to break a wall |
| Multi-Source BFS | Rotting Oranges (LeetCode 994) | Textbook multi-source BFS |
| Multi-Source BFS | Walls and Gates (LeetCode 286) | Same pattern, distance-to-nearest-gate framing |
| Topological Sort | Course Schedule I & II (LeetCode 207 / 210) | Both Kahn's and DFS versions apply directly |
| LCA | Lowest Common Ancestor of a Binary Tree (generalized to graphs/forests) | Binary lifting shines when there are many repeated queries |
| Eulerian Path | Reconstruct Itinerary (LeetCode 332) | Hierholzer's algorithm, with lexicographic tie-breaking |
| 2-SAT | Boolean assignment / "either-or" constraint problems | Rare in typical interviews, common in competitive programming |
| Bidirectional BFS | Word Ladder (LeetCode 127) | Bidirectional BFS is the standard optimization over plain BFS here |
| Johnson's Algorithm | All-pairs shortest path on sparse graphs with negative weights | Less commonly asked directly; more often a "how would you optimize Floyd-Warshall here" follow-up |
| TSP (Bitmask DP) | Traveling Salesman-style "visit all nodes" DP problems, small `n` | Bitmask DP is the standard exact approach for `n ≤ ~20` |
| DSU with Rollback | Offline dynamic connectivity problems | Niche; usually a follow-up to a "can standard DSU handle undo?" discussion |
| Karger's Min-Cut | Global Min Cut (theoretical/discussion question) | More often discussed conceptually than implemented live |
| Graph Coloring | Bipartite check generalization; "can this be scheduled with k slots" | Emphasize the bipartite = 2-coloring connection |
| Widest Path | "Path with Maximum Minimum Value" (LeetCode 1102) | Direct application of the max-heap Dijkstra variant |