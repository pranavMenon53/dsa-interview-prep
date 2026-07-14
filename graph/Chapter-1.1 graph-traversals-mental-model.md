# Graph Traversal Deep Dive

Graph traversal patterns can be easy to mix up because the required state changes depending on whether the graph is **directed** or **undirected**, and whether the goal is **traversal**, **cycle detection**, or **topological sorting**.

This document serves as a mental model for remembering *which traversal to use, why it works, and what additional state (visited array, recursion stack, parent, indegree, etc.) is required for each scenario.*

With graphs, it is easy to mix up **graph traversal** with **cycle detection** and **topological sorting**.

They're related, but not the same algorithm.

Here's a cleaner mental model.

---

# Directed Graphs

## 1. Plain DFS Traversal

```java
dfs(node) {
    vis[node] = true;

    for (int nei : g[node]) {
        if (!vis[nei])
            dfs(nei);
    }
}
```

Purpose:

* Traverse all reachable nodes
* Count connected components (weakly, if you ignore direction)
* DFS ordering
* Foundation for many DP problems

Only needs

* `visited[]`

Practice problem - [DFS of Graph](https://www.geeksforgeeks.org/problems/depth-first-traversal-for-a-graph/1)

---

## 2. DFS Cycle Detection

Here we need to know whether an edge goes **back into the current recursion stack**.

```java
visited[]
dfsVisited[]
```

```text
A → B → C
     ↑   ↓
     └───┘
```

Algorithm:

* first visit → `visited = true`
* currently in recursion → `dfsVisited = true`
* while exploring,

  * if `visited == false`
    recurse
  * else if `dfsVisited == true`
    cycle

On returning

```java
dfsVisited[node] = false;
```

Purpose:

* Detect cycle
* Also traverses the graph

---

## 3. Kahn's Algorithm (BFS Toposort)

Uses

* indegree[]
* queue

```text
Put all indegree = 0 nodes into queue.
```

Then

```
pop node

for every neighbor
    indegree--
    if indegree==0
         push
```

If

```
processedNodes < n
```

→ cycle exists.

Purpose:

* Topological ordering
* Cycle detection

No visited array required.

---

## 4. DFS Topological Sort

This is different from DFS cycle detection.

Uses

```java
visited[]
stack
```

Algorithm

```text
visit children first

then push current node
```

Finally reverse stack.

Example

```
1 → 2 → 3
```

Output

```
3
2
1
```

Reverse

```
1 2 3
```

If graph may contain cycles, combine with `dfsVisited[]`; otherwise, on a DAG, `visited[]` alone is sufficient.

---

# Undirected Graphs

The big difference:

In an undirected graph

```
A ----- B
```

every edge exists twice.

So from B you'll naturally go back to A.

That's **not** a cycle.

Hence we ignore the parent.

---

## 1. DFS Traversal

Plain traversal:

```java
dfs(node,parent){

    vis[node]=true;

    for(nei){

        if(!vis[nei])
            dfs(nei,node);
    }
}
```

Notice:

You don't even need `parent` if you're **only traversing**.

Parent is only needed for **cycle detection**.

---

## 2. DFS Cycle Detection

```java
dfs(node,parent){

    vis[node]=true;

    for(nei){

        if(!vis[nei])
            dfs(nei,node);

        else if(nei!=parent)
            cycle
    }
}
```

Need

* visited[]
* parent

---

## 3. BFS Traversal

Normal BFS

```java
queue

visited[]
```

Again, parent isn't needed if you're simply traversing.

---

## 4. BFS Cycle Detection

Store

```java
(node,parent)
```

inside queue.

When visiting neighbors

```
visited && neighbor != parent
```

⇒ cycle.

---

# A Simple Rule to Remember

| Graph      | Traversal   | Cycle Detection                                         | Topological Sort                      |
| ---------- | ----------- | ------------------------------------------------------- | ------------------------------------- |
| Directed   | `visited[]` | `visited[] + dfsVisited[]` (DFS) or `indegree[]` (Kahn) | DFS (`visited + stack`) or BFS (Kahn) |
| Undirected | `visited[]` | `visited[] + parent`                                    | ❌ Not defined                         |

## The key intuition

The only reason **undirected** graphs need a `parent` is because every edge appears twice.

The only reason **directed** graphs need `dfsVisited` is because the notion of a **back edge into the current recursion stack** is what characterizes a cycle.

Once you remember those two ideas, almost every graph traversal pattern becomes much easier to reconstruct from first principles.
