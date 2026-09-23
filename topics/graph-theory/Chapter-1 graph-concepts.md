
# Graph

This document aims to take you from zero to hero in graph theory from an interview perspective

# Concepts

## Bipartite Graph

**Definition**

* A graph is **bipartite** if its vertices can be divided into **2 sets (2 colours)** such that **no two adjacent vertices belong to the same set**.

**Approach**

* Traverse every connected component (graph may be disconnected).
* Maintain a `color[]` array.

  * `-1` → Not visited
  * `0` → Color 1
  * `1` → Color 2
* Assign the starting node any colour.
* Every neighbour gets the **opposite colour**.
* If you ever encounter an edge connecting two nodes with the **same colour**, the graph is **not bipartite**.

**Time Complexity:** `O(V + E)`
**Space Complexity:** `O(V)`

### BFS

<details>
<summary>Click to expand code</summary>

```java
class Solution {
    public boolean isBipartite(int[][] graph) {
        int n = graph.length;
        int[] color = new int[n];
        Arrays.fill(color, -1);

        for (int i = 0; i < n; i++) { // look for all the components in the graph
            if (color[i] != -1) continue; // already coloured, part of a processed component

            Queue<Integer> queue = new LinkedList<>();
            queue.offer(i);
            color[i] = 0;

            while (!queue.isEmpty()) {
                int node = queue.poll();
                for (int neighbor : graph[node]) {
                    if (color[neighbor] == -1) {
                        color[neighbor] = 1 - color[node]; // opposite colour
                        queue.offer(neighbor);
                    } else if (color[neighbor] == color[node]) {
                        return false; // same colour as parent -> not bipartite
                    }
                }
            }
        }
        return true;
    }
}
```

</details>


### DFS

<details>
<summary>Click to expand code</summary>

```java
class Solution {
    public boolean isBipartite(int[][] graph) {
        int n = graph.length;
        int[] color = new int[n];
        Arrays.fill(color, -1);

        for (int i = 0; i < n; i++) {
            if (color[i] == -1 && !dfs(i, 0, graph, color))
                return false;
        }

        return true;
    }

    private boolean dfs(int node, int c, int[][] graph, int[] color) {
        color[node] = c;

        for (int neighbor : graph[node]) {
            if (color[neighbor] == -1) {
                if (!dfs(neighbor, 1 - c, graph, color))
                    return false;
            } else if (color[neighbor] == c) {
                return false;
            }
        }

        return true;
    }
}
```

</details>

### Interview Pattern

* **Graph colouring problem** → Think **Bipartite**.
* **Need to divide nodes into 2 groups with no conflicts** → Use **2-colouring**.
* **Can be solved using either BFS or DFS.**
* **Remember to iterate through all vertices** because the graph may be **disconnected**.

---

## Cycle Detection in Directed Graph

**Problem**

* Detect whether a **directed graph contains a cycle**.

**Approaches**

1. **DFS + Recursion Stack** *(Most common)*
2. **Topological Sort (Kahn's Algorithm - BFS)**
3. **Topological Traversal using DFS** *(Less common)*

**Time Complexity:** `O(V + E)`
**Space Complexity:** `O(V)`


### 1. DFS + Recursion Stack

**Idea**

* Maintain two arrays:

  * `vis[]` → Node has been visited.
  * `dfsVis[]` → Node is part of the current DFS path (recursion stack).
* If DFS reaches a node already present in the current recursion stack, a **back edge** exists → **Cycle found**.
* Remove the node from `dfsVis` while backtracking.

<details>
<summary>Click to expand code</summary>

```java
class Solution {

    int[] vis;
    int[] dfsVis;

    public boolean isCyclic(int n, List<List<Integer>> adj) {

        vis = new int[n];
        dfsVis = new int[n];

        for (int i = 0; i < n; i++) {
            if (vis[i] == 0 && dfs(i, adj))
                return true;
        }

        return false;
    }

    private boolean dfs(int node, List<List<Integer>> adj) {

        vis[node] = 1;
        dfsVis[node] = 1;

        for (int neighbor : adj.get(node)) {

            if (vis[neighbor] == 0) {
                if (dfs(neighbor, adj)) return true;
            }
            else if (dfsVis[neighbor] == 1) {
                return true;
            }
        }

        dfsVis[node] = 0;
        return false;
    }
}
```

</details>


### 2. Topological Sort (BFS - Kahn's Algorithm)

**Idea**

* Compute the **indegree** of every node.
* Push all nodes with **indegree = 0** into the queue.
* Remove nodes one by one while decreasing the indegree of their neighbours.
* Count how many nodes are processed.
* If **processed nodes < total nodes**, the remaining nodes must belong to a **cycle**.

<details>
<summary>Click to expand code</summary>

```java
class Solution {
    public boolean isCyclic(int n, List<List<Integer>> adj) {

        int[] indegree = new int[n];

        for (int u = 0; u < n; u++) {
            for (int v : adj.get(u))
                indegree[v]++;
        }

        Queue<Integer> queue = new LinkedList<>();

        for (int i = 0; i < n; i++) {
            if (indegree[i] == 0)
                queue.offer(i);
        }

        int processed = 0;

        while (!queue.isEmpty()) {

            int node = queue.poll();
            processed++;

            for (int neighbor : adj.get(node)) {
                indegree[neighbor]--;

                if (indegree[neighbor] == 0)
                    queue.offer(neighbor);
            }
        }

        return processed != n;
    }
}
```

</details>


### 3. Topological Traversal using DFS

**Idea**

* Compute the **indegree** of every node.
* Start DFS **only from nodes with indegree = 0** — these are the only valid starting points for a topological traversal.
* During DFS, don't recurse into a neighbor just because it's unvisited. Instead, **decrement its indegree** as you traverse the edge, and recurse into it **only once its indegree drops to 0** — i.e., only once every one of its prerequisites has actually been consumed by the traversal.
* This is the crucial invariant: a node is "ready" to visit exactly when all its incoming edges have been walked, which is the same condition Kahn's algorithm enforces with an explicit queue — here it's enforced implicitly through the recursion.
* After DFS completes:

  * If every node was visited → **No cycle**.
  * If some nodes remain unvisited, their indegree never reached 0 → they're trapped inside a **cycle** (or depend on one).


<details>
<summary>Click to expand code</summary>

```java
class Solution {
    public boolean isCyclic(int n, List<List<Integer>> adj) {

        int[] indegree = new int[n];
        for (int u = 0; u < n; u++)
            for (int v : adj.get(u))
                indegree[v]++;

        boolean[] visited = new boolean[n];

        for (int i = 0; i < n; i++) {
            if (indegree[i] == 0 && !visited[i]) {
                dfs(i, adj, indegree, visited);
            }
        }

        for (boolean v : visited) {
            if (!v) return true; // some node never had its indegree fully cleared -> cycle
        }
        return false;
    }

    private void dfs(int node, List<List<Integer>> adj, int[] indegree, boolean[] visited) {
        visited[node] = true;

        for (int neighbor : adj.get(node)) {
            indegree[neighbor]--;                 // "remove" this incoming edge
            if (indegree[neighbor] == 0) {         // only enter once ALL its edges are gone
                dfs(neighbor, adj, indegree, visited);
            }
        }
    }

    /*
        ⭐ Optimization: If all you care about is detecting a cycle, then you can get rid of the visted array.
        Maintain a global counter, and instead of making a node as visted, increment the counter.
        In the main function, return counter == n;
    */
}
```

</details>

#### Is it really Kahn?

Yes.

The invariant is identical.

Kahn says:

> Process a node when its indegree becomes 0.

Your recursive version says exactly the same thing.

The queue has simply been replaced by recursive calls.

#### One caveat

There is one practical difference from the queue version.

Consider a very deep DAG:

```text
0 → 1 → 2 → 3 → ... → 100000
```

Your recursive implementation may cause a **stack overflow** in Java.

The queue version doesn't have that issue.

So:

* **Recursive version:** elegant, same asymptotic complexity, but recursion depth = longest path.
* **Queue version:** iterative, safer for very deep graphs.



### Interview Pattern

* **Directed graph + cycle detection** → Think **DFS + Recursion Stack**.
* **Topological sorting possible?** → Graph is **acyclic (DAG)**.
* **Kahn's algorithm processes fewer than `V` nodes** → **Cycle exists**.
* **Recursion stack (`dfsVis`) detects back edges**, which only indicate cycles in directed graphs.

---

### Practice problem

- [Topological Sort - GFG](https://www.geeksforgeeks.org/problems/topological-sort/1)

- Here, we collect the toposort sequence

-
    <details>
        <summary>BFS - Click to expand code</summary>

    ```java
    class Solution {

        int v;
        ArrayList<ArrayList<Integer>> g;
        int[] indegree;

        public ArrayList<Integer> topoSort(int V, int[][] edges) {
            v = V;
            g = new ArrayList<>();

            indegree = new int[v];

            for(int i = 0; i < v; i++) g.add(new ArrayList<>());

            for(int[] e: edges)
            {
                g.get(e[0]).add(e[1]);
                indegree[e[1]]++;
            }

            Queue<Integer> q = new ArrayDeque<Integer>();

            for(int i = 0; i < v; i++)
            {
                if(indegree[i] == 0) q.offer(i);
            }

            ArrayList<Integer> res = new ArrayList<Integer>();

            while(q.size() > 0)
            {
                int node = q.poll();

                for(int e : g.get(node))
                {
                    indegree[e]--;
                    if(indegree[e] == 0) q.offer(e);
                }

                res.add(node);
            }

            return res;
        }
    }
    ```

    </details>


-
    <details>
        <summary>DFS - Click to expand code</summary>

    ```java
    class Solution {

        int v;
        ArrayList<ArrayList<Integer>> g;
        int[] indegree;
        ArrayList<Integer> res;
        boolean[] vis;

        public ArrayList<Integer> topoSort(int V, int[][] edges) {
            v = V;
            g = new ArrayList<>();
            res = new ArrayList<Integer>();
            vis = new boolean[v];
            indegree = new int[v];

            for(int i = 0; i < v; i++) g.add(new ArrayList<>());

            for(int[] e: edges)
            {
                g.get(e[0]).add(e[1]);
                indegree[e[1]]++;
            }

            for(int i = 0; i < v; i++)
            {
                if(indegree[i] == 0 && !vis[i]) dfs(i);
            }

            return res;
        }

        void dfs(int node)
        {
            vis[node] = true;
            res.add(node);
            for(int e : g.get(node))
            {
                indegree[e]--;
                if(indegree[e] == 0)
                    dfs(e);
            }
        }
    }
    ```

    </details>

---

## Cycle Detection in Undirected Graph

**Problem**

* Detect whether an **undirected graph contains a cycle**.

**Approaches**

1. **BFS + Parent Tracking**
2. **DFS + Parent Tracking**
3. **Union-Find (Disjoint Set)** *(Edge List)*

**Time Complexity:** `O(V + E)` *(BFS / DFS)*
**Space Complexity:** `O(V)`



### 1. BFS + Parent Tracking

**Idea**

* Traverse every connected component.
* Store both the **current node** and its **parent** in the queue.
* If a visited neighbour is encountered **and it is not the parent**, a **cycle exists**.

<details>
<summary>Click to expand code</summary>

```java id="5xv2mn"
class Solution {
    public boolean isCyclic(int n, List<List<Integer>> adj) {

        boolean[] visited = new boolean[n];

        for (int i = 0; i < n; i++) {
            if (!visited[i] && bfs(i, adj, visited))
                return true;
        }

        return false;
    }

    private boolean bfs(int start, List<List<Integer>> adj, boolean[] visited) {

        Queue<int[]> queue = new LinkedList<>();
        queue.offer(new int[]{start, -1});
        visited[start] = true;

        while (!queue.isEmpty()) {

            int[] curr = queue.poll();
            int node = curr[0];
            int parent = curr[1];

            for (int neighbor : adj.get(node)) {

                if (neighbor == parent) continue;

                if (!visited[neighbor]) {
                    visited[neighbor] = true;
                    queue.offer(new int[]{neighbor, node});
                }
                else
                    return true;
            }
        }

        return false;
    }
}
```

</details>



### 2. DFS + Parent Tracking

**Idea**

* Traverse every connected component.
* Pass the **parent node** during DFS.
* If a visited neighbour is encountered **and it isn't the parent**, a **cycle exists**.

<details>
<summary>Click to expand code</summary>

```java id="l2z1ck"
class Solution {
    public boolean isCyclic(int n, List<List<Integer>> adj) {

        boolean[] visited = new boolean[n];

        for (int i = 0; i < n; i++) {
            if (!visited[i] && dfs(i, -1, adj, visited))
                return true;
        }

        return false;
    }

    private boolean dfs(int node,
                        int parent,
                        List<List<Integer>> adj,
                        boolean[] visited) {

        visited[node] = true;

        for (int neighbor : adj.get(node)) {

            if (neighbor == parent) continue;

            if (!visited[neighbor]) {
                if (dfs(neighbor, node, adj, visited))
                    return true;
            }
            else
                return true;
        }

        return false;
    }

/*
    // Alternative DFS solution

    boolean dfs(int node, int par)
    {
        vis[node] = true;
        boolean isCyclic = false;

        for(int e : g[node])
        {
            if(e == par) continue;

            if(!vis[e])
                isCyclic |= dfs(e, node);
            else
                return true;
        }

        return isCyclic;
    }
*/
}
```

</details>



### 3. Union-Find (Disjoint Set)

**When to use**

* Input is given as an **edge list** instead of an adjacency list.
* Very common in interview problems like **Redundant Connection**.

**Idea**

* Initially every node belongs to its own set.
* For every edge `(u, v)`:

  * If `find(u) == find(v)` → both nodes are already connected → **Cycle found**.
  * Otherwise, merge the two sets.

<details>
<summary>Click to expand code</summary>

```java id="e84mvy"
class Solution {

    int[] parent;
    int[] rank;

    public boolean isCyclic(int n, int[][] edges) {

        parent = new int[n];
        rank = new int[n];

        for (int i = 0; i < n; i++)
            parent[i] = i;

        for (int[] edge : edges) {

            int u = find(edge[0]);
            int v = find(edge[1]);

            if (u == v)
                return true;

            union(u, v);
        }

        return false;
    }

    private int find(int x) {
        if (parent[x] != x)
            parent[x] = find(parent[x]);

        return parent[x];
    }

    private void union(int x, int y) {

        if (rank[x] < rank[y])
            parent[x] = y;
        else if (rank[x] > rank[y])
            parent[y] = x;
        else {
            parent[y] = x;
            rank[x]++;
        }
    }
}
```

</details>

### Interview Pattern

* **Undirected graph + cycle detection** → Think **Parent Tracking**.
* **Visited neighbour ≠ parent** → **Cycle exists**.
* **Need recursion stack?** → **No** (only required for directed graphs).
* **Edge list input** → **Union-Find** is often the cleanest solution.
* **Remember to process every connected component**, as the graph may be disconnected.

---

### Practice Problem
- [Undirected Graph Cycle](https://www.geeksforgeeks.org/problems/detect-cycle-in-an-undirected-graph/1)

---

## Graph Traversal Deep Dive

Graph traversal patterns can be easy to mix up because the required state changes depending on whether the graph is **directed** or **undirected**, and whether the goal is **traversal**, **cycle detection**, or **topological sorting**.

This document serves as a mental model for remembering *which traversal to use, why it works, and what additional state (visited array, recursion stack, parent, indegree, etc.) is required for each scenario.*

For a detailed explanation, see: [Graph Traversals - Mental Model](./Chapter-1.1%20graph-traversals-mental-model.md)

---

## Shortest Path in Graphs

**Problem**

* Find the **shortest distance from a source node to every other node**.

### 1. BFS (Unit Weight Graph)

**When to use**

* Every edge has **weight = 1** (or equal weight).

**Idea**

* Maintain a `dist[]` array initialized to `∞`.
* Start from the source with distance `0`.
* Whenever a shorter distance to a neighbour is found:

  * Update its distance.
  * Push it into the queue.

**Time Complexity:** `O(V + E)`
**Space Complexity:** `O(V)`

<details>
<summary>Click to expand code</summary>

```java id="c73nm1"
class Solution {
    public int[] shortestPath(int n, List<List<Integer>> adj, int src) {

        int[] dist = new int[n];
        Arrays.fill(dist, Integer.MAX_VALUE);

        dist[src] = 0;

        Queue<Integer> queue = new LinkedList<>();
        queue.offer(src);

        while (!queue.isEmpty()) {

            int node = queue.poll();

            for (int neighbor : adj.get(node)) {

                if (dist[node] + 1 < dist[neighbor]) {
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

---

#### Practice Problem

- [Shortest Path in Unweighted Graph](https://www.geeksforgeeks.org/problems/shortest-path-in-undirected-graph-having-unit-distance/1)
-
    <details>
    <summary>Click to expand code</summary>

    ```java id="c73nm1"
    class Solution {

        int n;
        ArrayList<Integer>[] g;

        public int shortestPath(int V, int[][] edges, int src, int dest) {

            n = V;
            g = new ArrayList[n];

            for(int i = 0; i < n; i++)
                g[i] = new ArrayList<>();

            for(int[] e : edges)
            {
                g[e[0]].add(e[1]);
                g[e[1]].add(e[0]);
            }

            int MAX = Integer.MAX_VALUE;

            // node, dist from source
            Queue<int[]> q = new ArrayDeque<>();

            q.offer(new int[]{src, 0});

            int[] dist = new int[n];

            Arrays.fill(dist, MAX);
            dist[src] = 0;


            while(!q.isEmpty())
            {
                int[] pair = q.poll();
                int node = pair[0];
                int distFromSrc = pair[1];

                if(node == dest)
                    return distFromSrc;

                if(dist[node] != distFromSrc) continue;

                for(int e : g[node])
                {
                    int newDist = distFromSrc + 1;
                    if(newDist < dist[e])
                    {
                        q.offer(new int[]{e, newDist});
                        dist[e] = newDist;
                    }
                }
            }

            return -1;
        }
    }
    ```

    </details>


---

### 2. Dijkstra's Algorithm

**When to use**

* All edge weights are **non-negative**.

**Idea**

* Maintain the shortest distance found so far for every node.
* Use a **min-heap (Priority Queue)** ordered by distance.
* Always process the node with the **smallest current distance**.
* Ignore stale heap entries.

**Does NOT work for**

* Negative edge weights.

**Time Complexity:** `O(E log V)`
**Space Complexity:** `O(V)`

<details>
<summary>Click to expand code</summary>

```java id="j5vm9t"
class Solution {
    public int[] dijkstra(int n, List<List<int[]>> adj, int src) {
        // adj.get(u) contains int[]{v, weight} pairs
        int[] dist = new int[n];
        Arrays.fill(dist, Integer.MAX_VALUE);
        dist[src] = 0;

        // min-heap of {node, distance}, ordered by distance
        PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> a[1] - b[1]);
        pq.offer(new int[]{src, 0});

        while (!pq.isEmpty()) {
            int[] curr = pq.poll();
            int node = curr[0], d = curr[1];

            if (d > dist[node]) continue; // stale/outdated entry, skip

            for (int[] edge : adj.get(node)) {
                int neighbor = edge[0], weight = edge[1];
                if (dist[node] + weight < dist[neighbor]) {
                    dist[neighbor] = dist[node] + weight;
                    pq.offer(new int[]{neighbor, dist[neighbor]});
                }
            }
        }
        return dist;
    }
}
```

</details>


---

#### Practice Problem

- [Dijkstra's algo](https://www.geeksforgeeks.org/problems/implementing-dijkstra-set-1-adjacency-matrix/1)
-
    <details>
    <summary>Click to expand code</summary>

    ```java id="c73nm1"
    class Solution {

        int n;
        ArrayList<Edge>[] g;

        class Edge {

            int node;
            int dist;

            Edge(int d, int w) {
            node = d;
            dist = w;
            }
        }

        public ArrayList<Integer> dijkstra(int V, int[][] edges, int src) {
            int MAX = Integer.MAX_VALUE;
            n = V;
            g = new ArrayList[n];
            ArrayList<Integer> res = new ArrayList<>();

            for (int i = 0; i < n; i++) {
            g[i] = new ArrayList<>();
            res.add(MAX);
            }

            for (int[] e : edges) {
            g[e[0]].add(new Edge(e[1], e[2]));
            g[e[1]].add(new Edge(e[0], e[2]));
            }

            PriorityQueue<Edge> pq = new PriorityQueue<>((a, b) -> a.dist - b.dist);
            pq.offer(new Edge(src, 0));
            res.set(src, 0);

            while (!pq.isEmpty()) {
            Edge e = pq.poll();
            int node = e.node;
            int distFromSrc = e.dist;

            if (distFromSrc != res.get(node)) continue;

            for (Edge neighbour : g[node]) {
                int newDist = neighbour.dist + distFromSrc;
                if (newDist < res.get(neighbour.node)) {
                res.set(neighbour.node, newDist);
                pq.offer(new Edge(neighbour.node, newDist));
                }
            }
            }

            return res;
        }
        }

    ```

    </details>

---

### 3. Bellman-Ford Algorithm

**When to use**

* Graph contains **negative edge weights**.
* Need to **detect negative weight cycles**.
* Works even with negative edge weights (unlike Dijkstra), and can detect negative weight cycles.
    - Relax all edges (n - 1) times; if any edge can still be relaxed on the n-th pass, a negative cycle exists.
    - Slower than Dijkstra: O(V * E) instead of O(E log V).

**Idea**

* Relax every edge exactly **`V - 1`** times.
* Perform one additional iteration.
* If any edge can still be relaxed, a **negative weight cycle** exists.

**Time Complexity:** `O(V × E)`
**Space Complexity:** `O(V)`

<details>
<summary>Click to expand code</summary>

```java id="pw7n8a"
class Solution {
    public int[] bellmanFord(int n, int[][] edges, int src) {
        // edges[i] = {u, v, weight}
        int[] dist = new int[n];
        Arrays.fill(dist, Integer.MAX_VALUE);
        dist[src] = 0;

        // relax all edges n - 1 times
        for (int i = 0; i < n - 1; i++) {
            for (int[] edge : edges) {
                int u = edge[0], v = edge[1], w = edge[2];
                if (dist[u] != Integer.MAX_VALUE && dist[u] + w < dist[v]) {
                    dist[v] = dist[u] + w;
                }
            }
        }

        // one more pass to detect a negative weight cycle
        for (int[] edge : edges) {
            int u = edge[0], v = edge[1], w = edge[2];
            if (dist[u] != Integer.MAX_VALUE && dist[u] + w < dist[v]) {
                throw new RuntimeException("Graph contains a negative weight cycle");
            }
        }

        return dist;
    }
}
```

</details>

---

### 4. Topological Sort + Relaxation (DAG only)

**Idea**

1. Compute the **topological order**.
2. Initialize `dist[src] = 0`, all others to `∞`.
3. Process nodes in topological order.
4. If the current node is unreachable (`dist[node] == ∞`), skip it.
5. Otherwise, relax all outgoing edges.

<details>
<summary>Click to expand code</summary>

```java id="r2j7qv"
class Solution {
    public int[] shortestPath(int n, List<List<int[]>> adj, int src) {
        // Step 1: get topological order via DFS
        boolean[] visited = new boolean[n];
        Stack<Integer> topoStack = new Stack<>();

        for (int i = 0; i < n; i++) {
            if (!visited[i]) {
                topoDfs(i, adj, visited, topoStack);
            }
        }

        // Step 2: initialize distances
        int[] dist = new int[n];
        Arrays.fill(dist, Integer.MAX_VALUE);
        dist[src] = 0;

        // Step 3: process nodes in topological order
        while (!topoStack.isEmpty()) {
            int node = topoStack.pop();

            if (dist[node] != Integer.MAX_VALUE) {
                for (int[] edge : adj.get(node)) {
                    int neighbor = edge[0], weight = edge[1];
                    if (dist[node] + weight < dist[neighbor]) {
                        dist[neighbor] = dist[node] + weight;
                    }
                }
            }
        }
        return dist;
    }

    private void topoDfs(int node, List<List<int[]>> adj, boolean[] visited, Stack<Integer> topoStack) {
        visited[node] = true;
        for (int[] edge : adj.get(node)) {
            int neighbor = edge[0];
            if (!visited[neighbor]) {
                topoDfs(neighbor, adj, visited, topoStack);
            }
        }
        topoStack.push(node);
    }
}
```

</details>

---

#### 4.1. Why does this approach work?

When you pop vertices from the DFS stack, they appear in topological order. Therefore, every predecessor of a vertex is processed before that vertex.

As a result, by the time you process a vertex, all possible incoming paths from its predecessors have already had a chance to update its distance.

That is why a single relaxation pass is sufficient.

#### 4.2. Does it work with negative Edges?
Yes, absolutely! You can use this approach for a Directed Acyclic Graph (DAG), even when edge weights are negative.

The key conditions are:

* The graph must be directed and acyclic.

* You must process vertices in a valid topological order.

* You must relax outgoing edges only from reachable vertices.

Unlike Dijkstra's algorithm, this approach does not require non-negative edge weights.

#### 4.3. Interview-ready summary

> This approach works because a topological ordering guarantees that every predecessor of a vertex is processed before that vertex. Consequently, when we process a vertex, all possible incoming paths from its predecessors have already been considered, allowing us to compute shortest-path distances with a single relaxation pass. Since a DAG cannot contain cycles, negative-weight edges are supported without any negative-cycle issues.

**Complexity**: O(V+E) time.

---

### 5. Floyd-Warshall Algorithm (All-Pairs Shortest Path)

**When to use**

* Need the shortest distance between **every pair of vertices**.
* Works for **directed and undirected graphs**.
* Supports **negative edge weights**, but **not negative weight cycles**.

**Idea**

* Consider every node `k` as an intermediate node.
* Update the shortest distance between every pair `(i, j)` by checking whether passing through `k` produces a shorter path.

**Time Complexity:** `O(V³)`
**Space Complexity:** `O(V²)`

<details>
<summary>Click to expand code</summary>

```java id="f9kp4m"
class Solution {

    public int[][] floydWarshall(int n, int[][] matrix) {

        // matrix[i][j] = weight of edge i -> j, or INF if no edge, 0 if i == j
        int[][] dist = new int[n][n];

        for (int i = 0; i < n; i++)
            dist[i] = matrix[i].clone();

        final int INF = (int) 1e9;

        for (int k = 0; k < n; k++) {

            for (int i = 0; i < n; i++) {

                for (int j = 0; j < n; j++) {

                    if (dist[i][k] < INF &&
                        dist[k][j] < INF &&
                        dist[i][k] + dist[k][j] < dist[i][j]) {

                        dist[i][j] = dist[i][k] + dist[k][j];
                    }
                }
            }
        }

        // If dist[i][i] < 0, a negative weight cycle exists.
        return dist;
    }
}
```

</details>

---

### Dijkstra vs Bellman Ford

Both Dijkstra and Bellman–Ford **can be used** on graphs that contain cycles. The presence of a cycle alone does not prevent either algorithm from working.

What matters is the edge weights and, for Bellman–Ford, whether a reachable negative-weight cycle exists.


#### 1. Dijkstra

Dijkstra works on directed or undirected graphs with non-negative edge weights, even if the graph contains cycles.

* Positive-weight cycles: allowed.

* Zero-weight cycles: allowed.

* Negative-weight edges: Dijkstra is not guaranteed to produce correct shortest paths.

For example, a graph with `A → B → C → A` is perfectly fine for Dijkstra if all its edge weights are non-negative.

#### 2. Bellman–Ford

Bellman–Ford works on directed or undirected graphs with positive, zero, or negative edge weights, provided there is no reachable negative-weight cycle that makes the shortest-path distance undefined.

* Positive-weight cycles: allowed.

* Zero-weight cycles: allowed.

* Negative-weight edges: allowed.

* Reachable negative-weight cycles: detected by Bellman–Ford; shortest-path distances for vertices affected by such cycles are unbounded below.

A negative-weight cycle is a cycle whose total edge weight is less than zero.

#### Quick interview cheat sheet

|Graph|Dijkstra|Bellman–Ford|
| --- | --- | --- |
|Directed, cyclic, non-negative weights|Yes|Yes|
|Undirected, cyclic, non-negative weights|Yes|Yes|
|Directed, negative edges, no reachable negative cycle|Not guaranteed|Yes|
|Undirected, negative edge|Not guaranteed|Negative cycle exists under standard walk semantics|
|Reachable negative-weight cycle|Not guaranteed|Detects it|

**Remember**: Cycles are not the problem. Negative edge weights are the problem for Dijkstra, and reachable negative-weight cycles are the problem for finite shortest-path distances in Bellman–Ford.


---

### Interview Pattern

* **Unweighted graph / Every edge = 1** → **BFS**.
* **Positive edge weights** → **Dijkstra**.
* **Negative edge weights** → **Bellman-Ford**.
* **Need to detect negative cycles** → **Bellman-Ford**.
* **Never use Dijkstra if negative edges are present.**
* **Shortest path in a DAG** → **Topological Sort + Relaxation** (`O(V + E)`).
* **Need shortest paths between every pair of nodes** → **Floyd-Warshall**.
* **Graph contains cycles?** → Use **Dijkstra** (positive weights) or **Bellman-Ford** (negative weights) instead of Topological Sort.
* **Need to detect negative cycles** → **Bellman-Ford** (single-source) or check `dist[i][i] < 0` after **Floyd-Warshall**.

---

### Choosing the Algorithm

| Graph Type                     | Algorithm        | Time Complexity |
| ------------------------------ | ---------------- | --------------- |
| Unweighted / Unit Weight (`1`) | **BFS**          | `O(V + E)`      |
| DAG                              | Topological Sort + Relaxation | **O(V + E)** |
| Positive Edge Weights          | **Dijkstra**     | `O(E log V)`    |
| Negative Edge Weights          | **Bellman-Ford** | `O(V × E)`      |

---

## Minimum Spanning Tree (MST)

**Problem**

* Given a **connected, undirected, weighted graph**, find a subset of edges that:

  * Connects **all vertices**.
  * Has **no cycles**.
  * Has the **minimum possible total edge weight**.

**Approaches**

1. **Prim's Algorithm**
2. **Kruskal's Algorithm**

---

### Choosing the Algorithm

| Algorithm     | Idea                                                                             | Time Complexity |
| ------------- | -------------------------------------------------------------------------------- | --------------- |
| **Prim's**    | Grow a single tree by repeatedly adding the minimum-weight edge leaving the tree | `O(E log V)`    |
| **Kruskal's** | Sort all edges and greedily add the smallest edge that doesn't form a cycle      | `O(E log E)`    |

---

### 1. Prim's Algorithm

**Idea**

* Start from any vertex.
* Maintain a **Min Heap (Priority Queue)** of candidate edges.
* Repeatedly pick the **minimum-weight edge** that connects a new vertex to the MST.
* Ignore vertices already included in the MST.

**Time Complexity:** `O(E log V)`
**Space Complexity:** `O(V)`

<details>
<summary>Click to expand code</summary>

```java id="pw3nhx"
class Solution {
    public int spanningTree(int n, List<List<int[]>> adj) {
        boolean[] inMST = new boolean[n];
        // min-heap of {weight, node}
        PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> a[0] - b[0]);
        pq.offer(new int[]{0, 0}); // start from node 0

        int totalWeight = 0;

        while (!pq.isEmpty()) {
            int[] curr = pq.poll();
            int weight = curr[0], node = curr[1];

            if (inMST[node]) continue; // already added, skip

            inMST[node] = true;
            totalWeight += weight;

            for (int[] edge : adj.get(node)) {
                int neighbor = edge[0], edgeWeight = edge[1];
                if (!inMST[neighbor]) {
                    pq.offer(new int[]{edgeWeight, neighbor});
                }
            }
        }
        return totalWeight;
    }
}
```

</details>

---

### 2. Kruskal's Algorithm

**Idea**

* Sort all edges by **weight**.
* Process edges from smallest to largest.
* Add an edge only if it **does not create a cycle**.
* Use **Union-Find (Disjoint Set)** to efficiently detect cycles.

**Time Complexity:** `O(E log E)`
**Space Complexity:** `O(V)`

<details>
<summary>Click to expand code</summary>

```java id="g4zr2k"
class Solution {
    int[] parent, rank_;

    public int spanningTree(int n, int[][] edges) {
        // edges[i] = {u, v, weight}
        parent = new int[n];
        rank_ = new int[n];
        for (int i = 0; i < n; i++) parent[i] = i;

        Arrays.sort(edges, (a, b) -> a[2] - b[2]); // sort by weight ascending

        int totalWeight = 0;
        for (int[] edge : edges) {
            if (union(edge[0], edge[1])) { // adding this edge won't form a cycle
                totalWeight += edge[2];
            }
        }
        return totalWeight;
    }

    private int find(int x) {
        if (parent[x] == x)
            return x;

        return parent[x] = find(parent[x]);
    }

    private boolean union(int x, int y) {

        x = find(x);
        y = find(y);

        if(x == y) return false; // they share the same parent, no need to perform union

        if (rank_[x] < rank_[y])
            parent[x] = y;
        else if (rank_[x] > rank_[y])
            parent[y] = x;
        else {
            parent[y] = x;
            rank_[x]++;
        }

        return true;
    }
}
```

</details>

---

#### What if the graph is disconnected?
If the graph is disconnected, your code returns the total weight of the Minimum Spanning Forest (MSF), not an MST.


Suppose the graph is

```
Component 1:
0 --1-- 1
 \      |
  3     2
   \    |
      2

Component 2:
3 --5-- 4
```

Kruskal processes every edge.

* Builds MST of Component 1
* Builds MST of Component 2

Result:

```
0 --1-- 1
|
2

3 --5-- 4
```

The total weight is simply

```
MST(Component1) + MST(Component2)
```

This is called a **Minimum Spanning Forest (MSF)**.

For problems involving **per-component statistics**, it's common to augment the DSU:

```java
parent[]
rank[]
weight[]   // MST weight of this component
size[]     // Number of vertices
```

Whenever you merge two components:

```
weight[newRoot] =
    weight[root1] +
    weight[root2] +
    edgeWeight;
```

Now every DSU root stores the MST weight of its component, making queries like min/max/sum trivial after Kruskal completes.

---

### Practice problem

- [Minimum Spanning Tree - GFG](https://www.geeksforgeeks.org/problems/minimum-spanning-tree/1)

- Here, we collect the toposort sequence

-
    <details>
        <summary>Prims - Click to expand code</summary>

    ```java
    class Solution {

        class Edge{
            int node;
            int weight;

            Edge(int n, int w)
            {
                node = n;
                weight = w;
            }
        }

        public int spanningTree(int V, int[][] edges) {
            // code here
            int n = V;
            ArrayList<Edge>[] g = new ArrayList[n];

            for(int i = 0; i < n; i++) g[i] = new ArrayList<>();

            for(int[] e : edges)
            {
                int u = e[0];
                int v = e[1];
                int w = e[2];

                g[u].add(new Edge(v, w));
                g[v].add(new Edge(u, w));
            }

            int totalWeight = 0;

            boolean[] inMST = new boolean[n];

            PriorityQueue<Edge> pq = new PriorityQueue<>((a,b) -> a.weight - b.weight);

            // node, weight
            pq.offer(new Edge(0, 0));

            while(!pq.isEmpty())
            {
                Edge edge = pq.poll();
                int node = edge.node;
                int weight = edge.weight;

                if(inMST[node]) continue;

                inMST[node] = true;
                totalWeight += weight;

                for(Edge e : g[node])
                {
                    int neighbourNode = e.node;
                    int neighbourWeight = e.weight;

                    if(!inMST[neighbourNode])
                        pq.offer(new Edge(neighbourNode, neighbourWeight));
                }
            }


            return totalWeight;
        }
    }

    ```

    </details>


-
    <details>
        <summary>Kruskals - Click to expand code</summary>

    ```java
    class Solution {

        int[] rank;
        int[] par;

        public int spanningTree(int V, int[][] edges) {
            // code here
            int n = V;

            rank = new int[n];
            par = new int[n];

            for(int i = 0; i < n;  i++) par[i] = i;

            Arrays.sort(edges, (a,b) -> a[2] - b[2]);

            int totalWeight = 0;

            for(int[] edge : edges)
            {
                int u = edge[0];
                int v = edge[1];
                int w = edge[2];

                if(union(u,v))
                {
                    totalWeight += w;
                }
            }

            return totalWeight;
        }

        int find(int x)
        {
            if(par[x] == x) return x;

            return par[x] = find(par[x]);
        }

        boolean union(int x, int y)
        {
            x = find(x);
            y = find(y);

            if(x == y) return false;

            if(rank[x] > rank[y])
                par[y] = x;
            else if(rank[y] > rank[x])
                par[x] = y;
            else{
                par[y] = x;
                rank[x]++;
            }

            return true;

        }
    }

    ```

    </details>

---

### Interview Pattern

* **Connect all vertices with minimum cost** → **Minimum Spanning Tree**.
* **Need to grow one tree from a starting node** → **Prim's Algorithm**.
* **Input is an edge list** → **Kruskal's Algorithm**.
* **Need efficient cycle detection** → **Union-Find (Disjoint Set)**.
* **MST is defined only for connected, undirected graphs.**
* **An MST always contains exactly `V - 1` edges.**
* **Shortest Path ≠ Minimum Spanning Tree**. Shortest path minimizes the distance from a source, whereas MST minimizes the **total weight** required to connect all vertices.

---

## Diameter of a Tree

**Problem**

* Find the **diameter of a tree**, i.e., the **longest path between any two vertices**.
* The diameter can be measured in terms of **edges** or **vertices**, depending on the problem statement.

### Approach - Two BFS / DFS Traversals

**Key Observation**

1. Start from **any node `A`**.
2. Find the **farthest node `D`** from `A`.
3. Start another traversal from `D`.
4. The **farthest node `B`** from `D` is the **other endpoint of the diameter**.
5. The distance between `D` and `B` is the **diameter of the tree**.

**Why does this work?**

* In a tree, there is exactly **one unique path** between any two vertices.
* The farthest node from any arbitrary node is guaranteed to be **one endpoint of the diameter**.

**Time Complexity:** `O(V)`
**Space Complexity:** `O(V)`

<details>
<summary>Click to expand code</summary>

```java id="r8mq2v"
class Solution {

    public int treeDiameter(int n, List<List<Integer>> adj) {

        // First traversal
        int[] first = bfs(0, adj);

        int diameterEnd1 = first[0];

        // Second traversal
        int[] second = bfs(diameterEnd1, adj);

        int diameter = second[1];

        return diameter;
    }

    // Returns {farthestNode, distance}
    private int[] bfs(int start, List<List<Integer>> adj) {

        boolean[] visited = new boolean[adj.size()];
        Queue<int[]> queue = new LinkedList<>();

        queue.offer(new int[]{start, 0});
        visited[start] = true;

        int farthestNode = start;
        int distance = 0;

        while (!queue.isEmpty()) {

            int[] currNodePair = queue.poll();
            int node = currNodePair[0];
            int nodeDistance = currNodePair[1];

            farthestNode = node;
            distance = nodeDistance;

            for (int neighbor : adj.get(node)) {
                if (!visited[neighbor]) {
                    visited[neighbor] = true;
                    queue.offer(new int[]{neighbor, nodeDistance + 1});
                }
            }

        }

        return new int[]{farthestNode, distance};
    }
}
```

</details>

### Alternative Approach - Tree DP (Single DFS)

**Idea**

* Perform a single DFS.
* For every node, compute the **two longest downward paths** through its children.
* The sum of these two paths gives the longest path passing through that node.
* The maximum value over all nodes is the tree diameter.

**Time Complexity:** `O(V)`
**Space Complexity:** `O(V)`

### Interview Pattern

* **Need the diameter of a tree** → **Two BFS/DFS traversals**.
* **First traversal** → Find one endpoint of the diameter.
* **Second traversal** → Find the opposite endpoint and the diameter length.
* **Works only for trees** because there is exactly **one unique path** between every pair of vertices.
* **Both BFS and DFS** can be used for the two traversals with the same `O(V)` complexity.

---

# Problem list

Problems are covered in [Graph problems](./Chapter-2%20graph-problem-set-v2.md)
