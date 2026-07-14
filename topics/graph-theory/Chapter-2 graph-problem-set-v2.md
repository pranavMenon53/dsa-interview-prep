
# Graph

This document aims to take you from zero to hero in graph theory from an interview perspective

# Concepts
Concepts are covered in [Graph concepts](./Chapter-1%20graph-concepts.md)


# Problem list

1. ⭐ [Minimum Genetic Mutation](https://leetcode.com/problems/minimum-genetic-mutation/description/)

    -
      <details>
        <summary>Click to expand code - Approach-1</summary>

        ```java
        class Solution {

          HashMap<String, Integer> nodeIndexMap;
          List<List<Integer>> g;
          int n;

          public int minMutation(String startGene, String endGene, String[] bank) {

              /*
                  Approach-1: Build a graph (n * n) => From each node, build edges
                      - We build an edge if the character count differ by 2
                      - Onces the edges are established, perform a BFS shortest distance run

                  Time Complexity: O(N² × L), which simplifies to O(N²) since L = 8 is constant.
                  Space Complexity: O(N²) due to the adjacency list in the worst case.
              */

              // Mutation, corresponding node number
              nodeIndexMap = new HashMap<>();
              nodeIndexMap.put(startGene, 0);

              for(int i = 0; i < bank.length; i++)
                  nodeIndexMap.put(bank[i], i + 1);

              if(!nodeIndexMap.containsKey(endGene)) return -1;

              List<String> nodes = new ArrayList<>();
              nodes.add(startGene);
              Collections.addAll(nodes, bank);

              g = buildGraph(nodes);
              n = g.size();

              Queue<int[]> q = new ArrayDeque<>();
              q.offer(new int[]{nodeIndexMap.get(startGene), 0});

              boolean[] vis = new boolean[n];
              vis[nodeIndexMap.get(startGene)] = true;

              int targetIndex = nodeIndexMap.get(endGene);

              while(!q.isEmpty())
              {
                  int[] nodePair = q.poll();
                  int nodeIndex = nodePair[0];
                  int dist = nodePair[1];

                  if(nodeIndex == targetIndex) return dist;

                  for(int neighbourIndex : g.get(nodeIndex))
                  {
                      if(!vis[neighbourIndex])
                      {
                          vis[neighbourIndex] = true;
                          q.offer(new int[]{neighbourIndex, dist + 1});
                      }
                  }

              }

              return -1;
          }

          List<List<Integer>> buildGraph(List<String> nodes)
          {
              int size = nodes.size() ;

              List<List<Integer>> graph = new ArrayList<>(size);
              for (int i = 0; i < size; i++)
                  graph.add(new ArrayList<>());

              for(int i = 0; i < size; i++) // takes n * n
              {
                  for(int j = i + 1; j < size; j++)
                  {
                      if(i == j) continue;

                      if(isValidEdge(nodes.get(i), nodes.get(j)))
                      {
                          int u = nodeIndexMap.get(nodes.get(i));
                          int v = nodeIndexMap.get(nodes.get(j));

                          graph.get(u).add(v);
                          graph.get(v).add(u);
                      }
                  }
              }

              return graph;
          }

          boolean isValidEdge(String s1, String s2)
          {
              int diff = 0;

              for (int i = 0; i < 8; i++) {
                  if (s1.charAt(i) != s2.charAt(i))
                      diff++;
              }

              return diff == 1;
          }
      }
        ```
      </details>


    -
      <details>
        <summary>Click to expand code - Approach-2 (better)</summary>

        ```java
        class Solution {

          class Node{
              String word;
              int level;

              Node(String w, int l)
              {
                  word = w;
                  level = l;
              }
          }


          public int minMutation(String startGene, String endGene, String[] bank) {

              Set<String> bankSet = new HashSet<>(Arrays.asList(bank));
              String[] genes = {"A", "C", "G", "T"};

              Queue<Node> q = new LinkedList<>();
              q.add(new Node(startGene, 0));

              while(q.size() > 0)
              {
                  Node node = q.poll();
                  String curGene = node.word;
                  int level = node.level;

                  if(curGene.equals(endGene))
                      return level;

                  // int n = curGene.length();
                  for(int i = 0; i < 8; i++)
                  {
                      String prefix = curGene.substring(0, i);
                      String suffix = curGene.substring(i + 1, 8);
                      for(String gene: genes)
                      {
                          String newMutation = prefix + gene + suffix;
                          if(bankSet.contains(newMutation))
                          {
                              q.offer(new Node(newMutation, level + 1));
                              bankSet.remove(newMutation);
                          }
                      }
                  }
              }

              return -1;
          }
      }
        ```
      </details>

    -
      <details>
        <summary>Click to expand code - Approach-3 (best)</summary>

        ```java
        class Solution {
          // Optimized approach-2

          class Node {
              String gene;
              int level;

              Node(String gene, int level) {
                  this.gene = gene;
                  this.level = level;
              }
          }

          public int minMutation(String startGene, String endGene, String[] bank) {

              Set<String> bankSet = new HashSet<>(Arrays.asList(bank));

              if (!bankSet.contains(endGene))
                  return -1;

              char[] possibleGenes = {'A', 'C', 'G', 'T'};

              Queue<Node> q = new ArrayDeque<>();
              q.offer(new Node(startGene, 0));

              while (!q.isEmpty()) {

                  Node node = q.poll();
                  String currGene = node.gene;

                  if (currGene.equals(endGene))
                      return node.level;

                  char[] chars = currGene.toCharArray();

                  for (int i = 0; i < chars.length; i++) {

                      char original = chars[i];

                      for (char gene : possibleGenes) {

                          if (gene == original)
                              continue;

                          chars[i] = gene;
                          String nextGene = new String(chars);

                          if (bankSet.contains(nextGene)) {
                              bankSet.remove(nextGene);
                              q.offer(new Node(nextGene, node.level + 1));
                          }
                      }

                      chars[i] = original; // Restore original character
                  }
              }

              return -1;
          }
      }
        ```
      </details>

    -
      | Approach                                  | Time                 | Space     |
      | -----------------------------             | -------------------- | --------- |
      | Build graph + BFS   (Approach-1)          | **O(N²)**            | **O(N²)** |
      | Generate neighbors during BFS (Approach-2)| **O(NL)** = **O(N)** | **O(N)**  |



2. ⭐⭐⭐ [Most Stones Removed with Same Row or Column](https://leetcode.com/problems/most-stones-removed-with-same-row-or-column/)

    -
      <details>
        <summary>Click to expand code - Approach-1</summary>

        ```java
        class Solution {
            /*
              Idea:

              1. Treat each stone as a graph node.
              2. Two stones are connected if they share the same row or the same column.
              3. While processing the stones:
                - Maintain a map from row -> first stone seen in that row.
                - Maintain a map from column -> first stone seen in that column.
                - Connect the current stone to the first stone in its row/column.
                  (Connecting to just one representative is sufficient to keep all stones
                    in the same row/column within the same connected component.)
              4. Run DFS to find the size of each connected component.
              5. In a component of size k, exactly one stone must remain, so k - 1 stones
                can be removed.
              6. Sum (componentSize - 1) over all connected components.
            */

          int index;
          int n;
          int m;

          // Node number -> connected nodes
          HashMap<Integer, ArrayList<Integer>> g;

          HashSet<Integer> vis;

          public int removeStones(int[][] stones) {

              n = 0;
              m = 0;

              for(int[] stone : stones)
              {
                  n = Math.max(n, stone[0]);
                  m = Math.max(m, stone[1]);
              }

              // Col number -> some node in this column
              Map<Integer, Integer> colMap = new HashMap<>();

              // row number -> some node in this row
              Map<Integer, Integer> rowMap = new HashMap<>();

              g = new HashMap<>(); // undirected graph

              for(int[] stone : stones)
              {
                  int i = stone[0];
                  int j = stone[1];

                  // convert each coordinate to a node number
                  int nodeNumber = getNodeNumber(i, j);

                  if(rowMap.containsKey(i))
                  {
                      int rowNodeNumber = rowMap.get(i);
                      g.computeIfAbsent(nodeNumber, k -> new ArrayList<>()).add(rowNodeNumber);
                      g.get(rowNodeNumber).add(nodeNumber);
                  }
                  else
                  {
                      rowMap.put(i, nodeNumber);
                      g.computeIfAbsent(nodeNumber, k -> new ArrayList<>());
                  }

                  if(colMap.containsKey(j))
                  {
                      int colNodeNumber = colMap.get(j);
                      g.computeIfAbsent(nodeNumber, k -> new ArrayList<>()).add(colNodeNumber);
                      g.get(colNodeNumber).add(nodeNumber);
                  }
                  else
                  {
                      colMap.put(j, nodeNumber);
                      g.computeIfAbsent(nodeNumber, k -> new ArrayList<>());
                  }

              }

              vis = new HashSet<>();

              int res = 0;

              for(int node : g.keySet())
              {
                  if(!vis.contains(node))
                  {
                      int nodeCountInComponent = dfs(node);
                      res += (nodeCountInComponent - 1);
                  }
              }

              return res;
          }

          int getNodeNumber(int i, int j)
          {
              return i * (m + 1) + j; // each row contains 'n' elements
          }

          int dfs(int node)
          {
              vis.add(node);

              int count = 1;

              for(int e : g.get(node))
              {
                  if(!vis.contains(e)) count += dfs(e);
              }

              return count;
          }
      }
        ```
      </details>

    -
      <details>
        <summary>Click to expand code - Approach-2</summary>

        ```java
        class Solution {

          // Same idea as Approach-1, slightly more optimized

          List<Integer>[] graph;
          boolean[] visited;

          public int removeStones(int[][] stones) {

              int n = stones.length;

              graph = new ArrayList[n];
              visited = new boolean[n];

              for (int i = 0; i < n; i++) {
                  graph[i] = new ArrayList<>();
              }

              // row -> first stone index
              Map<Integer, Integer> rowMap = new HashMap<>();

              // col -> first stone index
              Map<Integer, Integer> colMap = new HashMap<>();

              // Build the graph
              for (int i = 0; i < n; i++) {

                  int row = stones[i][0];
                  int col = stones[i][1];

                  if (rowMap.containsKey(row)) {
                      int other = rowMap.get(row);
                      graph[i].add(other);
                      graph[other].add(i);
                  } else {
                      rowMap.put(row, i);
                  }

                  if (colMap.containsKey(col)) {
                      int other = colMap.get(col);
                      graph[i].add(other);
                      graph[other].add(i);
                  } else {
                      colMap.put(col, i);
                  }
              }

              int answer = 0;

              for (int i = 0; i < n; i++) {
                  if (!visited[i]) {
                      int componentSize = dfs(i);
                      answer += componentSize - 1;
                  }
              }

              return answer;
          }

          private int dfs(int node) {

              visited[node] = true;

              int size = 1;

              for (int neighbor : graph[node]) {
                  if (!visited[neighbor]) {
                      size += dfs(neighbor);
                  }
              }

              return size;
          }
      }
        ```
      </details>

    -
      <details>
        <summary>Click to expand code - Approach-3</summary>

        ```java
        class Solution {

          /*
              Idea:

              - Treat every unique row and every unique column as a DSU node.
              - Each stone (r, c) connects row r with column c.
              - If two stones share a row or a column, they become part of the
                same connected component through these unions.
              - Each connected component must leave exactly one stone behind.
              - Therefore,

                      answer = totalStones - numberOfConnectedComponents

              - But why (totalStones - numberOfConnectedComponents)?

                  Each connected component must leave exactly one stone behind because the last
                  remaining stone has no other stone in its row or column to remove it.

                  Therefore, if there are C connected components and N total stones:

                  Answer = (size1 - 1) + (size2 - 1) + ... + (sizeC - 1)
                        = (size1 + size2 + ... + sizeC) - C
                        = N - C
          */

          class DSU {

              Map<Integer, Integer> parent = new HashMap<>();

              int find(int x) {
                  parent.putIfAbsent(x, x);

                  if (parent.get(x) != x)
                      parent.put(x, find(parent.get(x)));

                  return parent.get(x);
              }

              void union(int a, int b) {

                  int pa = find(a);
                  int pb = find(b);

                  if (pa != pb)
                      parent.put(pa, pb);
              }
          }

          public int removeStones(int[][] stones) {

              DSU dsu = new DSU();

              // Offset columns so that row numbers and column numbers never collide.
              // Constraints:
              // row <= 10000
              // col <= 10000
              final int OFFSET = 10001;

              for (int[] stone : stones) {
                  int row = stone[0];
                  int col = stone[1] + OFFSET;

                  dsu.union(row, col);
              }

              // Count unique connected components.
              HashSet<Integer> components = new HashSet<>();

              for (int[] stone : stones) {
                  components.add(dsu.find(stone[0]));
              }

              return stones.length - components.size();
          }
      }
        ```
      </details>


3. [Nearest Exit from Entrance in Maze](https://leetcode.com/problems/nearest-exit-from-entrance-in-maze/description/)

    -
      <details>
        <summary>Click to expand code</summary>

        ```java
        class Solution {
          public int nearestExit(char[][] maze, int[] entrance) {

              char WALL = '+';
              int[][] delta = {
                  {-1, 0},
                  {1, 0},
                  {0, -1},
                  {0, 1}
              };

              Queue<int[]> q = new ArrayDeque<>();

              int n = maze.length;
              int m = maze[0].length;

              // {i, j, dist from source}
              q.offer(new int[]{entrance[0], entrance[1], 0});

              while(!q.isEmpty())
              {
                  int[] node = q.poll();
                  int i = node[0];
                  int j = node[1];
                  int dist = node[2];

                  if(i < 0 || i >= n || j < 0 || j >= m)
                  {
                      // We do this because (dist - 1 == 0) means the entrance is being treated as the exit
                      if(dist - 1 != 0) return dist - 1;
                      continue;
                  }

                  if(maze[i][j] == WALL) continue;

                  maze[i][j] = WALL;

                  for(int[] d : delta)
                  {
                      q.offer(new int[]{i + d[0], j + d[1], dist + 1});
                  }

              }

              return -1;
          }
      }
        ```
      </details>


4. [Find if Path Exists in Graph](https://leetcode.com/problems/find-if-path-exists-in-graph/description/)

    -
      <details>
        <summary>Click to expand code</summary>

        ```java
        class Solution {
          ArrayList<Integer>[] g;
          boolean[] vis;

          public boolean validPath(int n, int[][] edges, int src, int dest) {
              g = new ArrayList[n];
              vis = new boolean[n];

              for(int i = 0; i < n; i++) g[i] = new ArrayList<>();

              for(int[] e : edges)
              {
                  int u = e[0];
                  int v = e[1];
                  g[u].add(v);
                  g[v].add(u);
              }

              return dfs(src, dest);
          }

          boolean dfs(int src, int dest)
          {
              boolean found = false;
              vis[src] = true;

              if(src == dest) return true;

              for(int e : g[src])
              {
                  if(!vis[e]) found |= dfs(e, dest);
              }

              return found;
          }
      }
        ```
      </details>


5. [Keys and Rooms](https://leetcode.com/problems/keys-and-rooms/description/)

    -
      <details>
        <summary>Click to expand code</summary>

        ```java
        class Solution {
          int n;
          boolean[] vis;
          List<List<Integer>> g;


          public boolean canVisitAllRooms(List<List<Integer>> rooms) {
              n = rooms.size();
              g = rooms;
              vis = new boolean[n];

              dfs(0);

              boolean isValid = true;
              for(boolean isVisited : vis) isValid &= isVisited;

              return isValid;
          }

          void dfs(int src)
          {
              vis[src] = true;

              for(int e : g.get(src))
              {
                  if(!vis[e]) dfs(e);
              }
          }
      }
        ```
      </details>


6. [Possible Bipartition](https://leetcode.com/problems/possible-bipartition/)

    -
      <details>
        <summary>Click to expand code</summary>

        ```java
        class Solution {
          List<List<Integer>> g;
          int n;
          Integer[] colours;

          boolean dfs(int node, int colour, int par)
          {
              colours[node] = colour;
              int newColour = (colour + 1) % 2;

              boolean res = true;
              for(int e : g.get(node))
              {
                  if(e == par) continue;

                  if(colours[e] == null)
                  {
                      res = res && dfs(e, newColour, node);
                  }
                  else if(colour == colours[e]) return false;
              }

              return res;
          }

          public boolean possibleBipartition(int numPeople, int[][] dislikes) {

              n = numPeople;
              colours = new Integer[n + 1];
              g = new ArrayList<>();

              for(int i = 0; i <= n; i++)
              {
                  g.add(new ArrayList<>());
              }

              for(int[] d: dislikes)
              {
                  g.get(d[0]).add(d[1]);
                  g.get(d[1]).add(d[0]);
              }

              boolean res = true;
              for(int i = 1; i <= n; i++)
              {
                  if(colours[i] == null)
                      res = res && dfs(i, 0, -1);
              }

              return res;
          }
      }
        ```
      </details>


7. ⭐⭐⭐ [Sum of Distances in Tree](https://leetcode.com/problems/sum-of-distances-in-tree/description/)

    -
      <details>
        <summary>Click to expand code - Approach-1</summary>

        ```java
        class Solution {

          class Node{
              int nodeCount;
              int dist;

              Node(int nc, int d)
              {
                nodeCount = nc;
                dist = d;
              }
          }

          ArrayList<Integer>[] g;
          int n;
          boolean[] vis;
          Node[] nodes;
          int[] res;

          public int[] sumOfDistancesInTree(int n, int[][] edges) {

              this.n = n;
              g = new ArrayList[n];

              for(int i = 0; i < n; i++) g[i] = new ArrayList<>();
              nodes = new Node[n];

              for(int[] e: edges)
              {
                  g[e[0]].add(e[1]);
                  g[e[1]].add(e[0]);
              }

              vis = new boolean[n];
              populateNodes(0, -1);

              res = new int[n];
              vis = new boolean[n];
              populateRes(0, -1);

              return res;
          }

          /*
          * DFS-1 (populateNodes):
          * ----------------------
          * Computes two values for every subtree:
          *   nodeCount = Number of nodes in the current subtree.
          *   dist      = Sum of distances from the current node to all nodes in its subtree.
          *
          * Formula:
          *   nodeCount = 1 + Σ(child.nodeCount)
          *   dist      = Σ(child.dist + child.nodeCount)
          *
          * Why '+ child.nodeCount'?
          * Every node in the child's subtree is 1 edge farther from the current node than
          * from the child, so we add 1 for each of the child.nodeCount nodes.
          */
          Node populateNodes(int src, int parent)
          {
              vis[src] = true;

              int nodeCount = 1;
              int dist = 0;

              for(int e : g[src])
              {
                  if(e == parent) continue;

                  Node tempNode = new Node(0, 0);

                  if(!vis[e]) tempNode = populateNodes(e, src);

                  nodeCount += tempNode.nodeCount;
                  dist += (tempNode.dist + tempNode.nodeCount);
              }

              return nodes[src] = new Node(nodeCount, dist);
          }

          /*
          * DFS-2 (populateRes):
          * --------------------
          * Uses rerooting DP to compute the answer for every node in O(1) from its parent.
          *
          * Formula:
          *   res[child] = res[parent] - child.nodeCount + (n - child.nodeCount)
          *
          * Derivation:
          *   - res[parent] contains the distance sum to every node in the tree.
          *
          *   - The contribution of the child's subtree to res[parent] is:
          *         child.dist + child.nodeCount
          *
          *     because every node in the child's subtree is exactly 1 edge farther from
          *     the parent than from the child.
          *
          *   - Remove this subtree contribution from the parent's answer:
          *       res[parent] - (child.dist + child.nodeCount)
          *
          *   - Once that is done, we need to add back the current subtree's distance count
          *
          *   - res[i] = res[parent] - (nodes[i].dist + nodes[i].nodeCount) + (nodes[i].dist)
          *
          *   - Now, the parent, and all other nodes connected to the parent are further one step away, therefore, we need to add 1 for each node
          *
          *   - There are (total (n) - nodes[i].nodeCount) remaining in the tree
          *
          *   - Therefore, it becomes -
          *     - res[i] = res[parent] - (nodes[i].dist + nodes[i].nodeCount) + (nodes[i].dist) + (n - nodes[i].nodeCount)
          *     - res[i] = res[parent] - nodes[i].dist - nodes[i].nodeCount + nodes[i].dist + (n - nodes[i].nodeCount)
          *     - res[i] = res[parent] - nodes[i].nodeCount + (n - nodes[i].nodeCount)
          *
          * Reason:
          * - Moving the root from parent -> child:
          *   - All nodes in child's subtree become 1 closer  => -child.nodeCount
          *   - All other nodes become 1 farther             => +(n - child.nodeCount)
          *
          * Overall Complexity: O(n)
          */
          void populateRes(int src, int par)
          {
              vis[src] = true;

              if(par == -1)
                  res[src] = nodes[src].dist;
              else
                  res[src] = (res[par] - nodes[src].nodeCount) + (n - nodes[src].nodeCount);

              for(int e : g[src])
              {
                  if(e == par) continue;

                  if(!vis[e]) populateRes(e, src);
              }
          }
      }
        ```
      </details>

    -
      <details>
        <summary>Click to expand code - Approach-2</summary>

        ```java
        class Solution {

          List<List<Integer>> g;

          int distFromRoot = 0;

          Integer[] count;

          int[] res;

          int n;

          int dfs(int node, int par, int dist)
          {
              distFromRoot += dist;

              int curNodeCount = 1;
              for(int e : g.get(node))
              {
                  if(e == par) continue;

                  curNodeCount += dfs(e, node, dist + 1);
              }

              return count[node] = curNodeCount;
          }

          void fillDistFromNode(int node, int parent)
          {
              if(parent != -1)
                  res[node] = res[parent] - count[node] + n - count[node];

              for(int e : g.get(node))
              {
                  if(e == parent) continue;
                  fillDistFromNode(e, node);
              }
          }

          public int[] sumOfDistancesInTree(int nodeCount, int[][] edges) {
              n = nodeCount;
              distFromRoot = 0;
              g = new ArrayList<>();
              count = new Integer[n];

              for(int i = 0; i < n; i++)
                  g.add(new ArrayList<>());

              for(int[] e: edges)
              {
                  int u = e[0];
                  int v = e[1];

                  g.get(u).add(v);
                  g.get(v).add(u);
              }

              count[0] = dfs(0, -1, 0);

              res = new int[n];
              res[0] = distFromRoot;

              fillDistFromNode(0, -1);

              return res;
          }
      }
        ```
      </details>


8. ⭐ [All Paths From Source to Target](https://leetcode.com/problems/all-paths-from-source-to-target/description/)

    -
      <details>
        <summary>Click to expand  - Approach-1 (Avoid)</summary>

        ```java
        /*
        * DP Memoization:
        * ----------------
        * We memoize all paths from each node to the target, so every node's DFS is
        * executed at most once. This avoids recomputing shared suffixes in the DAG.
        *
        * However, the optimization is limited because the output itself must still be
        * constructed. Every parent must create a new copy of each child path and prepend
        * itself before storing the result.
        *
        * Example:
        *
        *          K
        *          |
        *      10,000 paths
        *
        * If 100 different nodes reach K:
        *   - Backtracking traverses the suffix 100 times.
        *   - DP computes the suffix once.
        *
        * But every one of those 100 parents must still copy all 10,000 paths, so the
        * dominant cost remains constructing the output.
        *
        * Therefore, DP reduces redundant DFS calls, but it does not improve the overall
        * asymptotic complexity (still O(total output size)) and requires significantly
        * more memory than the standard backtracking solution.
        */
        class Solution {

          int[][] g;
          int n;
          List<List<Integer>>[] dp;

          List<List<Integer>> lastNodeInPath;

          public List<List<Integer>> allPathsSourceTarget(int[][] graph) {
              n = graph.length;
              g = graph;


              dp = new ArrayList[n];

              lastNodeInPath = new ArrayList<>();
              lastNodeInPath.add(new ArrayList<>(){{add(n-1);}});

              dp[n - 1] = lastNodeInPath;

              return dfs(0);
          }

          List<List<Integer>> dfs(int node)
          {
              List<List<Integer>> pathFromCurNode = new ArrayList<>();

              if(node == n - 1)
                  return dp[n - 1];

              for(int e : g[node])
              {
                  List<List<Integer>> curNeighbourList = new ArrayList<>();

                  if(dp[e] == null) curNeighbourList = dfs(e);
                  else curNeighbourList = dp[e];

                  addToList(node, pathFromCurNode, curNeighbourList);
              }

              return dp[node] = pathFromCurNode;
          }

          void addToList(int curNode, List<List<Integer>> pathFromCurNode, List<List<Integer>> curNeighbourList)
          {
              for(List<Integer> path : curNeighbourList)
              {
                  List<Integer> curNodePath = new LinkedList<>(path);
                  curNodePath.addFirst(curNode);
                  pathFromCurNode.add(curNodePath);
              }
          }
      }
        ```
      </details>

    -
      <details>
        <summary>Click to expand code - Approach-2 (best)</summary>

        ```java
        /*
          Why Backtracking is Better:
          ---------------------------
          Although DP avoids recomputing DFS for shared subgraphs, it still has to create and copy every path
          for each parent node. Since the output itself is all possible paths, this copying dominates the runtime.

          Backtracking constructs each path exactly once and only copies it when adding it to the final answer,
          achieving the same asymptotic complexity with much lower memory usage and simpler code.
        */
        class Solution {
          List<List<Integer>> res = new ArrayList<>();
          int[][] graph;
          int target;

          public List<List<Integer>> allPathsSourceTarget(int[][] graph) {
              this.graph = graph;
              this.target = graph.length - 1;

              List<Integer> path = new ArrayList<>();
              path.add(0);

              dfs(0, path);

              return res;
          }

          private void dfs(int node, List<Integer> path) {

              if (node == target) {
                  res.add(new ArrayList<>(path));
                  return;
              }

              for (int neighbour : graph[node]) {
                  path.add(neighbour);
                  dfs(neighbour, path);
                  path.remove(path.size() - 1);
              }
          }
      }
      ```
      </details>


9. [Minimum Time to Collect All Apples in a Tree](https://leetcode.com/problems/minimum-time-to-collect-all-apples-in-a-tree/)

    -
      <details>
        <summary>Click to expand code - Approach-1 (best)</summary>

        ```java
        class Solution {

          List<Boolean> hasApple;
          List<Integer>[] g;
          int n;
          boolean[] vis;

          public int minTime(int n, int[][] edges, List<Boolean> hasApple) {
              this.hasApple = hasApple;
              this.n = n;
              vis = new boolean[n];

              g = new ArrayList[n];
              for(int i = 0; i < n; i++)
                  g[i] = new ArrayList<>();

              for(int[] e : edges)
              {
                  g[e[0]].add(e[1]);
                  g[e[1]].add(e[0]);
              }

              int[] res = solve(0);

              return res[1];
          }

          // 0 -> apples collected
          // 1 -> time taken
          int[] solve(int node)
          {
              vis[node] = true;

              int applesCollected = hasApple.get(node) ? 1 : 0;
              int totalTime = 0;

              for(int e : g[node])
              {
                  if(vis[e]) continue;

                  int[] res = solve(e);
                  if(res[0] > 0)
                  {
                      applesCollected += res[0];
                      // We add 2 because it takes 1 unit of time to vist this node,
                      // and 1 unit of time to return
                      totalTime += (2 + res[1]);
                  }
              }

              return new int[]{applesCollected, totalTime};
          }
      }
        ```
      </details>

    -
      <details>
        <summary>Click to expand code - Approach-2</summary>

        ```java
        class Solution {

          // This is still a good solution, and same in TC and SC as approach-1

          class Pair{
              // 'hasApples' indicates whether the current node is an apple
              // or is any child node an apple
              boolean hasApples;
              int time;

              Pair(boolean s, int t)
              {
                  time = t;
                  hasApples = s;
              }
          }

          ArrayList<ArrayList<Integer>> graph;
          List<Boolean> hasApple;

          int MAX = (int)(1e8);

          Pair dfs(int node, int par)
          {
              // time - time at which current node was encountered.

              int curNodeTime = 0;
              boolean childHasApple = false;

              for(int e : graph.get(node))
              {
                  if(e == par) continue;

                  Pair travelToNode = dfs(e, node);

                  if(travelToNode.hasApples)
                  {
                      childHasApple = true;
                      curNodeTime += travelToNode.time;
                  }
              }

              int timeToAdd = (node == 0 ? 0 : 2);

              if(curNodeTime > 0)
                  return new Pair(true, timeToAdd + curNodeTime);

              else if(hasApple.get(node))
                  return new Pair(true, timeToAdd);

              return new Pair(false, 0);
          }

          public int minTime(int n, int[][] edges, List<Boolean> hasApple1) {
              hasApple = hasApple1;
              graph = new ArrayList<>();

              for(int i = 0; i <= n ; i++)
                  graph.add(new ArrayList<Integer>());

              //Build graph(Adjacency List)
              for(int i = 0; i < edges.length; i++)
              {
                  int u = edges[i][0];
                  int v = edges[i][1];

                  graph.get(u).add(v);
                  graph.get(v).add(u);
              }

              return dfs(0, -1).time;
          }
      }
        ```
      </details>


10. [Number of Nodes in the Sub-Tree With the Same Label](https://leetcode.com/problems/number-of-nodes-in-the-sub-tree-with-the-same-label/description/)

    -
      <details>
        <summary>Click to expand  - Approach-1 (Good)</summary>

        ```java
        class Solution {

          int n;
          ArrayList<Integer>[] g;
          char[] labels;
          int[] res;
          boolean[] vis;

          public int[] countSubTrees(int n, int[][] edges, String labels) {
              this.n = n;

              g = new ArrayList[n];
              for(int i = 0; i < n; i++) g[i] = new ArrayList<>();

              for(int[] e : edges)
              {
                  g[e[0]].add(e[1]);
                  g[e[1]].add(e[0]);
              }

              this.labels = labels.toCharArray();

              res = new int[n];
              vis = new boolean[n];

              dfs(0);

              return res;
          }

          int[] dfs(int node)
          {
              /*
                Additional optimization -

                Since the input is a tree, you don't need a visited array. Passing the parent is the standard approach.

                int[] dfs(int node, int parent) {
                    ...
                    for (int child : g[node]) {
                        if (child == parent) continue;
                        ...
                    }
                }

                This saves O(n) space and avoids a boolean read/write for every node.
              */
              vis[node] = true;

              int[] curSubTreeLabels = new int[26];
              curSubTreeLabels[labels[node] - 'a']++;

              for(int e : g[node])
              {
                  if(vis[e]) continue;

                  int[] childSubTreeLabels = dfs(e);

                  for(int i = 0; i < 26; i++)
                      curSubTreeLabels[i] += childSubTreeLabels[i];
              }

              res[node] = curSubTreeLabels[labels[node] - 'a'];

              return curSubTreeLabels;
          }
      }
        ```
      </details>

    -
      <details>
        <summary>Click to expand - Approach-2 (Best)</summary>

        ```java
        class Solution {

          int n;
          ArrayList<Integer>[] g;
          char[] labels;
          int[] res;

          public int[] countSubTrees(int n, int[][] edges, String labels) {
              this.n = n;

              g = new ArrayList[n];
              for(int i = 0; i < n; i++) g[i] = new ArrayList<>();

              for(int[] e : edges)
              {
                  g[e[0]].add(e[1]);
                  g[e[1]].add(e[0]);
              }

              this.labels = labels.toCharArray();

              res = new int[n];

              dfs(0, -1, new int[26]);

              return res;
          }

          void dfs(int node, int par, int[] countSoFar)
          {
              int curNodeVal = labels[node] - 'a';
              int countBefore = countSoFar[curNodeVal];

              countSoFar[curNodeVal]++;

              for(int e : g.get(node))
              {
                  if(e == par) continue;
                  dfs(e, node, countSoFar);
              }

              res[node] = countSoFar[curNodeVal] - countBefore;
          }
      }
      ```
      </details>


11. ⭐ [Longest Path With Different Adjacent Characters](https://leetcode.com/problems/longest-path-with-different-adjacent-characters/description/)

    -
      <details>
        <summary>Click to expand code</summary>

        ```java
        class Solution {
          // DFS returns the longest downward path starting from the current node.
          // At each node, we keep the two longest valid child paths (different adjacent characters).
          // The longest path passing through this node is:
          //      longest + secondLongest + 1
          // because a path can extend into at most two branches through the current node.
          // We update the global answer with this value, but return only:
          //      longest + 1
          // to the parent, since a parent can continue the path through only one child.

          ArrayList<Integer>[] g;
          char[] label;
          int res = 1;

          public int longestPath(int[] parent, String s) {

              int n = parent.length;

              g = new ArrayList[n];
              for (int i = 0; i < n; i++) {
                  g[i] = new ArrayList<>();
              }

              for (int i = 1; i < n; i++) {
                  g[parent[i]].add(i);
              }

              label = s.toCharArray();

              dfs(0);
              return res;
          }

          // Returns the longest downward path starting from 'node'
          private int dfs(int node) {

              int longest = 0;
              int secondLongest = 0;

              for (int child : g[node]) {

                  int childPath = dfs(child);

                  // Adjacent characters must be different
                  if (label[node] == label[child]) {
                      continue;
                  }

                  if (childPath > longest) {
                      secondLongest = longest;
                      longest = childPath;
                  } else if (childPath > secondLongest) {
                      secondLongest = childPath;
                  }
              }

              // Longest path passing through this node
              res = Math.max(res, 1 + longest + secondLongest);

              // Longest downward path to parent
              return 1 + longest;
          }
      }
      ```
      </details>


12. ⭐ [Lexicographically Smallest Equivalent String](https://leetcode.com/problems/lexicographically-smallest-equivalent-string/description/)

    -
      <details>
        <summary>Click to expand code - Approach-1</summary>

        ```java
        class Solution {
          char[] str1, str2;
          int n, componentIndex;
          Integer[] comp;

          Character[] componentToSmallestCharacter;

          ArrayList<Integer>[] g;

          public String smallestEquivalentString(String s1, String s2, String baseStr) {
              str1 = s1.toCharArray();
              str2 = s2.toCharArray();
              n = str1.length;

              g = new ArrayList[26];

              comp = new Integer[26];
              componentToSmallestCharacter = new Character[26];

              for(int i = 0; i < 26; i++) g[i] = new ArrayList<>();

              for(int i = 0; i < n; i++)
              {
                  int u = str1[i] - 'a';
                  int v = str2[i] - 'a';
                  g[u].add(v);
                  g[v].add(u);
              }

              componentIndex = 0;
              for(int i = 0; i < 26; i++)
              {
                  if(comp[i] != null) continue;

                  /*
                    This is important, because the baseStr can contain characters
                    not present in both str1 and str2.
                    In such cases, we want the smallest one to be itself
                  */
                  componentToSmallestCharacter[componentIndex] = (char)('a' + i);
                  dfs(i);
                  componentIndex++;
              }

              StringBuilder sb = new StringBuilder();

              for(char ch : baseStr.toCharArray())
                  sb.append(componentToSmallestCharacter[comp[ch - 'a']]);

              return sb.toString();
          }

          void dfs(int node)
          {
              comp[node] = componentIndex;

              char ch = (char) ('a' + node);

              componentToSmallestCharacter[componentIndex] =
                  (char) Math.min(componentToSmallestCharacter[componentIndex], ch);

              for(int e : g[node])
              {
                  if(comp[e] != null) continue;

                  dfs(e);
              }
          }
      }
        ```
      </details>

    -
      <details>
        <summary>Click to expand code - Approach-2 (better)</summary>

        ```java
        class Solution {

          class DS {
              int[] parent;

              DS() {
                  parent = new int[26];
                  for (int i = 0; i < 26; i++)
                      parent[i] = i;
              }

              int find(int x) {
                  if (parent[x] != x)
                      parent[x] = find(parent[x]);
                  return parent[x];
              }

              void union(int u, int v) {
                  int ru = find(u);
                  int rv = find(v);

                  if (ru == rv) return;

                  /*
                      This is the clever part of the solution
                      Instead of using rank, we use the characters themselves to determine
                      who should be the parent of this union
                      The smallest character becomes the parent
                  */

                  if (ru < rv)
                      parent[rv] = ru;
                  else
                      parent[ru] = rv;
              }
          }

          public String smallestEquivalentString(String s1, String s2, String baseStr) {

              DS ds = new DS();

              for (int i = 0; i < s1.length(); i++)
                  ds.union(s1.charAt(i) - 'a', s2.charAt(i) - 'a');

              StringBuilder ans = new StringBuilder();

              for (char ch : baseStr.toCharArray())
                  ans.append((char) ('a' + ds.find(ch - 'a')));

              return ans.toString();
          }
      }
        ```
      </details>

13. ⭐ [Number of Good Paths](https://leetcode.com/problems/number-of-good-paths/description/)

    - Note on approaches - Idea remains the same across all 3 approaches
      - **Approach-1**: Good algorithm, implementation can be better
      - **Approach-2**: Optimized approach-1, better written code
      - **Approach-3**: Optimized approach-1, better written code
    -
      <details>
        <summary>Click to expand code - Approach-1</summary>

        ```java
        class Solution {

          class DSU{
              int n;
              int[] parent;
              int[] rank;

              DSU(int n){
                  this.n = n;
                  parent = new int[n];
                  rank = new int[n];
                  for(int i = 0; i < n; i++)
                  {
                      parent[i] = i;
                      rank[i] = 1;
                  }
              }

              int find(int x)
              {
                  if(parent[x] == x) return x;

                  return parent[x] = find(parent[x]);
              }

              // return true if nodes have different parents
              // return false if nodes have same parent
              boolean union(int u, int v)
              {
                  u = find(u);
                  v = find(v);

                  if(u == v) return false;

                  if(rank[u] > rank[v]) parent[v] = u;
                  else if(rank[u] < rank[v]) parent[u] = v;
                  else
                  {
                      parent[v] = u;
                      rank[u]++;
                  }

                  return true;
              }
          }

          // nodes[i][0] -> value
          // nodes[i][0] -> node number
          int[][] nodes;
          int n;
          ArrayList<Integer>[] g;
          boolean[] isAlive;

          public int numberOfGoodPaths(int[] vals, int[][] edges) {
              /*
                  Approach-1: For each pair of nodes (i,j) find a path between them
                      - If val[i] == val[j] && max value in path <= val[j] -> count++
                      - TC - N ** 3

                  Approach-2: For each node - I, traverse all other nodes in the graph
                      - If for node - J, vals[J] > vals[I], stop exploring
                      - and if node[J] == node[I] count++;
                      - This can be tricky since (I,J) and (J,I) will be covered in the total count
                      - We might need to use a Set to store unique pairs and check if (i,j) or (j,i) exist before incrementing count
                      - TC - N ** 2

                  Approach-3:
                      1. Build a graph, where g[u] contains all the nodes connected to u
                      2. The core idea is simple
                          - Initailly all nodes are dead and disconnected
                          - We start from the smallest value - k
                          - We mark all nodes with value k as alive
                          - For all alive nodes, we try to connect it's neighbours if they are alive too
                          - We connect them using DSU. and if on connecting they belong to the same componenet, we found a path
              */

              n = vals.length;
              nodes = new int[n][2];

              for(int i = 0; i < n; i++)
                  nodes[i] = new int[]{vals[i], i};

              Arrays.sort(nodes, (a,b) -> a[0] - b[0]);

              buildGraph(edges);

              isAlive = new boolean[n];

              DSU ds = new DSU(n);

              int i = 0;
              int res = n;

              while(i < n)
              {
                  int val = nodes[i][0];

                  // Mark nodes as alive
                  int j = i;
                  while(j < n && nodes[j][0] == val)
                      isAlive[nodes[j++][1]] = true;

                  // Iterate over all the nodes again
                  // Connect edges with nodes that are alive
                  j = i;
                  while(j < n && nodes[j][0] == val)
                  {
                      int node = nodes[j][1];

                      for(int e : g[node])
                      {
                          if(isAlive[e]) ds.union(node, e);
                      }

                      j++;
                  }

                  // Here I need to increment res
                  // The way I'm going to do it is
                  // For each component, I need to find the number of nodes in this componenet with their value == val
                  // Then res += count * (count + 1)/2
                  HashMap<Integer, Integer> freq = new HashMap<>();

                  j = i;

                  while (j < n && nodes[j][0] == val) {
                      int node = nodes[j][1];
                      int root = ds.find(node);

                      freq.put(root, freq.getOrDefault(root, 0) + 1);
                      j++;
                  }

                  for (int cnt : freq.values())
                      res += cnt * (cnt - 1) / 2;

                  i = j;
              }

              return res;
          }

          void buildGraph(int[][] edges){
              g = new ArrayList[n];

              for(int i = 0; i < n; i++) g[i] = new ArrayList<>();

              for(int[] e : edges)
              {
                  g[e[0]].add(e[1]);
                  g[e[1]].add(e[0]);
              }
          }
      }
        ```
      </details>

    -
      <details>
        <summary>Click to expand code - Approach-2</summary>

        ```java
        // Same idea as approach-1
        // Optimized approach-1
        class Solution {

          static class DSU {
              int[] parent;
              int[] size;

              DSU(int n) {
                  parent = new int[n];
                  size = new int[n];

                  for (int i = 0; i < n; i++) {
                      parent[i] = i;
                      size[i] = 1;
                  }
              }

              int find(int x) {
                  if (parent[x] != x)
                      parent[x] = find(parent[x]);
                  return parent[x];
              }

              void union(int u, int v) {
                  u = find(u);
                  v = find(v);

                  if (u == v)
                      return;

                  if (size[u] < size[v]) {
                      int temp = u;
                      u = v;
                      v = temp;
                  }

                  parent[v] = u;
                  size[u] += size[v];
              }
          }

          public int numberOfGoodPaths(int[] vals, int[][] edges) {

              int n = vals.length;

              int[][] sortedNodes = new int[n][2];
              for (int i = 0; i < n; i++) {
                  sortedNodes[i][0] = vals[i];
                  sortedNodes[i][1] = i;
              }

              Arrays.sort(sortedNodes, (a, b) -> Integer.compare(a[0], b[0]));

              List<Integer>[] graph = new ArrayList[n];
              for (int i = 0; i < n; i++)
                  graph[i] = new ArrayList<>();

              for (int[] edge : edges) {
                  graph[edge[0]].add(edge[1]);
                  graph[edge[1]].add(edge[0]);
              }

              DSU dsu = new DSU(n);

              int answer = n;

              int i = 0;

              while (i < n) {

                  int value = sortedNodes[i][0];

                  int j = i;

                  // Union with neighbours whose value is <= current value
                  while (j < n && sortedNodes[j][0] == value) {

                      int node = sortedNodes[j][1];

                      for (int neighbor : graph[node]) {
                          if (vals[neighbor] <= value)
                              dsu.union(node, neighbor);
                      }

                      j++;
                  }

                  HashMap<Integer, Integer> componentCount = new HashMap<>();

                  for (int k = i; k < j; k++) {
                      int root = dsu.find(sortedNodes[k][1]);
                      componentCount.merge(root, 1, Integer::sum);
                  }

                  for (int count : componentCount.values())
                      answer += count * (count - 1) / 2;

                  i = j;
              }

              return answer;
          }
      }
        ```
      </details>

    -
      <details>
        <summary>Click to expand code - Approach-3</summary>

        ```java
        class Solution {

          class DSU {
              int[] parent;
              int[] rank;

              DSU(int n) {
                  parent = new int[n];
                  rank = new int[n];

                  for (int i = 0; i < n; i++) {
                      parent[i] = i;
                      rank[i] = 1;
                  }
              }

              int find(int x) {
                  if (parent[x] == x)
                      return x;

                  return parent[x] = find(parent[x]);
              }

              void union(int u, int v) {
                  u = find(u);
                  v = find(v);

                  if (u == v)
                      return;

                  if (rank[u] > rank[v]) {
                      parent[v] = u;
                  } else if (rank[u] < rank[v]) {
                      parent[u] = v;
                  } else {
                      parent[v] = u;
                      rank[u]++;
                  }
              }
          }

          public int numberOfGoodPaths(int[] vals, int[][] edges) {

              int n = vals.length;

              // value -> nodes having this value
              TreeMap<Integer, List<Integer>> valueToNodes = new TreeMap<>();

              for (int i = 0; i < n; i++) {
                  valueToNodes.computeIfAbsent(vals[i], k -> new ArrayList<>()).add(i);
              }

              List<Integer>[] graph = new ArrayList[n];
              for (int i = 0; i < n; i++)
                  graph[i] = new ArrayList<>();

              for (int[] edge : edges) {
                  graph[edge[0]].add(edge[1]);
                  graph[edge[1]].add(edge[0]);
              }

              DSU dsu = new DSU(n);

              // Every node is a good path by itself.
              int answer = n;

              for (Map.Entry<Integer, List<Integer>> entry : valueToNodes.entrySet()) {

                  int value = entry.getKey();
                  List<Integer> nodes = entry.getValue();

                  // Connect with neighbours whose value is <= current value.
                  for (int node : nodes) {
                      for (int neighbor : graph[node]) {
                          if (vals[neighbor] <= value) {
                              dsu.union(node, neighbor);
                          }
                      }
                  }

                  // Count nodes of the current value in each connected component.
                  HashMap<Integer, Integer> componentCount = new HashMap<>();

                  for (int node : nodes) {
                      int root = dsu.find(node);
                      componentCount.merge(root, 1, Integer::sum);
                  }

                  // Add all pair paths.
                  for (int count : componentCount.values()) {
                      answer += count * (count - 1) / 2;
                  }
              }

              return answer;
          }
      }
        ```
      </details>


14. [Find Closest Node to Given Two Nodes](https://leetcode.com/problems/find-closest-node-to-given-two-nodes/description/)

    -
      <details>
        <summary>Click to expand code - Approach-1</summary>

        ```java
        class Solution {
          int n;
          ArrayList<Integer>[] g;

          public int closestMeetingNode(int[] edges, int node1, int node2) {
              n = edges.length;
              g = new ArrayList[n];
              for(int i = 0; i < n; i++) g[i] = new ArrayList<>();

              for(int i = 0; i < n; i++)
              {
                  int node = edges[i];
                  if(node == -1) continue;
                  g[i].add(node);
              }

              int[] distFromNode1 = bfs(node1);
              int[] distFromNode2 = bfs(node2);

              int MAX = Integer.MAX_VALUE;
              int dist = MAX;
              int res = MAX;

              for(int i = 0; i < n; i++)
              {
                  int curNodeDistanceFromNode1 = distFromNode1[i];
                  int curNodeDistanceFromNode2 = distFromNode2[i];

                  if(curNodeDistanceFromNode1 == -1 || curNodeDistanceFromNode2 == -1) continue;

                  int curRes = Math.max(curNodeDistanceFromNode1, curNodeDistanceFromNode2);

                  if(curRes < dist)
                  {
                      dist = curRes;
                      res = i;
                  }
              }

              return res == MAX ? -1 : res;
          }

          int[] bfs(int node)
          {
              int[] distFromNode = new int[n];
              Arrays.fill(distFromNode, -1);

              Queue<Integer> q = new ArrayDeque<>();
              q.add(node);
              int dist = 0;

              boolean[] vis =  new boolean[n];

              while(!q.isEmpty())
              {
                  int level = q.size();

                  while(level-->0)
                  {
                      int curNode = q.poll();
                      distFromNode[curNode] = dist;
                      vis[curNode] = true;

                      for(int e : g[curNode]){
                          if(!vis[e]) q.add(e);
                      }
                  }

                  dist++;
              }

              return distFromNode;
          }
      }
        ```
      </details>

    -
      <details>
        <summary>Click to expand code - Approach-2 (better)</summary>

        ```java
        class Solution {

          public int closestMeetingNode(int[] edges, int node1, int node2) {

              int[] dist1 = getDistance(edges, node1);
              int[] dist2 = getDistance(edges, node2);

              int ans = -1;
              int minDist = Integer.MAX_VALUE;

              for (int i = 0; i < edges.length; i++) {

                  if (dist1[i] == -1 || dist2[i] == -1)
                      continue;

                  int cur = Math.max(dist1[i], dist2[i]);

                  if (cur < minDist) {
                      minDist = cur;
                      ans = i;
                  }
              }

              return ans;
          }

          private int[] getDistance(int[] edges, int start) {

              int[] dist = new int[edges.length];
              Arrays.fill(dist, -1);

              int d = 0;
              int node = start;

              while (node != -1 && dist[node] == -1) {
                  dist[node] = d++;
                  node = edges[node];
              }

              return dist;
          }
      }
        ```
      </details>



15. ⭐⭐⭐ [Cheapest Flights Within K Stops](https://leetcode.com/problems/cheapest-flights-within-k-stops/)

    -
      <details>
        <summary>Click to expand code - Approach-1 (good)</summary>

        ```java
        class Solution {

          /*
            Idea:
            Treat each BFS level as one additional flight (edge). Since we are allowed
            at most k stops (k+1 edges), process only k+1 levels.

            Unlike normal BFS, edges have different costs, so we cannot use a visited array.
            Instead, maintain the minimum cost to reach each node and relax edges level by level.
            A copy of the cost array is used so that updates from the current level do not affect
            other nodes in the same level (equivalent to Bellman-Ford relaxation).

            Time: O(E * K)
            Space: O(V + E)
          */

          class Pair {
              int node, cost;

              Pair(int node, int cost) {
                  this.node = node;
                  this.cost = cost;
              }
          }

          public int findCheapestPrice(int n, int[][] flights, int src, int dst, int k) {

              ArrayList<Pair>[] graph = new ArrayList[n];
              for (int i = 0; i < n; i++)
                  graph[i] = new ArrayList<>();

              for (int[] f : flights)
                  graph[f[0]].add(new Pair(f[1], f[2]));

              int[] cost = new int[n];
              Arrays.fill(cost, Integer.MAX_VALUE);
              cost[src] = 0;

              Queue<Pair> q = new ArrayDeque<>();
              q.offer(new Pair(src, 0));

              int stops = 0;

              while (!q.isEmpty() && stops <= k) {

                  int size = q.size();

                  while (size-- > 0) {

                      Pair cur = q.poll();

                      for (Pair nei : graph[cur.node]) {

                          int newCost = cur.cost + nei.cost;

                          if (newCost < cost[nei.node]) {
                              cost[nei.node] = newCost;
                              q.offer(new Pair(nei.node, newCost));
                          }
                      }
                  }

                  stops++;
              }

              return cost[dst] == Integer.MAX_VALUE ? -1 : cost[dst];
          }
      }
        ```
      </details>

    -
      <details>
        <summary>Click to expand code - Approach-2 (best)</summary>

        ```java
        class Solution {

          /*
            Idea:
            Bellman-Ford computes the shortest path using at most i edges after the i-th
            relaxation. Since the problem allows at most k stops (k+1 edges), we only
            perform k+1 relaxations.

            A cloned distance array ensures that each iteration only extends paths by one
            additional edge. Without cloning, a single iteration could incorrectly use
            multiple newly relaxed edges.

            Time: O(E * K)
            Space: O(V)
          */

          public int findCheapestPrice(int n, int[][] flights, int src, int dst, int k) {

              int INF = Integer.MAX_VALUE;

              int[] dist = new int[n];
              Arrays.fill(dist, INF);
              dist[src] = 0;

              for (int i = 0; i <= k; i++) {

                  int[] next = dist.clone();

                  for (int[] flight : flights) {

                      int u = flight[0];
                      int v = flight[1];
                      int wt = flight[2];

                      if (dist[u] == INF)
                          continue;

                      next[v] = Math.min(next[v], dist[u] + wt);
                  }

                  dist = next;
              }

              return dist[dst] == INF ? -1 : dist[dst];
          }
      }
        ```
      </details>

    -
      <details>
        <summary>Click to expand code - Approach-3 (too complicated)</summary>

        ```java
        class Solution {

          /*
            Idea:
            The number of stops used is part of the state, so a node may need to be visited
            multiple times with different stop counts. The priority queue stores
            (node, cost, stopsUsed), always expanding the currently cheapest path.

            Maintain best[node][stops] to avoid revisiting worse states. This extends
            Dijkstra by tracking both the destination node and the number of edges used.

            Time: O(E log(V * K))
            Space: O(V * K)
          */

          class State {
              int node;
              int cost;
              int stops;

              State(int node, int cost, int stops) {
                  this.node = node;
                  this.cost = cost;
                  this.stops = stops;
              }
          }

          class Edge {
              int to;
              int wt;

              Edge(int to, int wt) {
                  this.to = to;
                  this.wt = wt;
              }
          }

          public int findCheapestPrice(int n, int[][] flights, int src, int dst, int k) {

              ArrayList<Edge>[] graph = new ArrayList[n];
              for (int i = 0; i < n; i++)
                  graph[i] = new ArrayList<>();

              for (int[] f : flights)
                  graph[f[0]].add(new Edge(f[1], f[2]));

              int[][] best = new int[n][k + 2];

              for (int[] row : best)
                  Arrays.fill(row, Integer.MAX_VALUE);

              best[src][0] = 0;

              PriorityQueue<State> pq =
                      new PriorityQueue<>((a, b) -> a.cost - b.cost);

              pq.offer(new State(src, 0, 0));

              while (!pq.isEmpty()) {

                  State cur = pq.poll();

                  if (cur.node == dst)
                      return cur.cost;

                  if (cur.stops == k + 1)
                      continue;

                  if (cur.cost > best[cur.node][cur.stops])
                      continue;

                  for (Edge edge : graph[cur.node]) {

                      int nextCost = cur.cost + edge.wt;

                      if (nextCost < best[edge.to][cur.stops + 1]) {

                          best[edge.to][cur.stops + 1] = nextCost;

                          pq.offer(new State(
                                  edge.to,
                                  nextCost,
                                  cur.stops + 1));
                      }
                  }
              }

              return -1;
          }
      }
        ```
      </details>


16. [Minimum Score of a Path Between Two Cities](https://leetcode.com/problems/minimum-score-of-a-path-between-two-cities/)

    -
      <details>
        <summary>Click to expand code</summary>

        ```java
        class Solution {
          /*
          * Key Observation:
          * Since the path is allowed to revisit cities and roads, we can always detour
          * to any edge in the connected component containing cities 1 and n, then return
          * and continue to the destination.
          *
          * Therefore, the minimum possible score is simply the minimum edge weight in
          * the connected component containing city 1.
          *
          * Algorithm:
          * 1. Build the undirected graph.
          * 2. Run DFS/BFS starting from city 1.
          * 3. While traversing, keep track of the smallest edge weight encountered.
          * 4. Return the minimum edge weight found.
          *
          * Time: O(V + E)
          * Space: O(V)
          */

          List<List<int[]>> g;
          int n;
          boolean[] vis;

          int res;

          public int minScore(int n, int[][] roads) {
              this.n = n;
              vis = new boolean[n + 1];

              g = new ArrayList<>();

              for(int i = 0; i <= n; i++) g.add(new ArrayList<>());

              for(int[] e : roads)
              {
                  int u = e[0];
                  int v = e[1];
                  int dist = e[2];

                  g.get(u).add(new int[]{v, dist});
                  g.get(v).add(new int[]{u, dist});
              }

              res = Integer.MAX_VALUE;

              dfs(1);

              return res;
          }

          void dfs(int node)
          {
              vis[node] = true;

              for(int[] edge : g.get(node))
              {
                  int next = edge[0];
                  int weight = edge[1];

                  res = Math.min(res, weight);

                  if(!vis[next]) dfs(next);
              }
          }
      }
        ```
      </details>


17. ⭐⭐⭐ [Reorder Routes to Make All Paths Lead to the City Zero](https://leetcode.com/problems/reorder-routes-to-make-all-paths-lead-to-the-city-zero/description/)

    -
      <details>
        <summary>Click to expand code - Approach-1</summary>

        ```java
        class Solution {

          int n;
          boolean[] vis;
          ArrayList<Integer>[] g;
          int flipCount = 0;
          HashSet<String> edges;

          public int minReorder(int n, int[][] connections) {

              /*
                  Approach-1: reverse edges in subsequences, then check if each node can reach 0
                      - (2 ** n) - generating all combinations of reversals
                      - n - time for BFS/DFS
                      - total => (2 ** n) * n

                  Approach-2:
                      - Build an undirected graph from the given directed roads.
                      - Start a DFS from city 0.
                      - During DFS, every edge should effectively point from the current node
                      towards its parent (i.e., towards city 0).
                      - If the original road already points towards the parent, no change is needed.
                      - Otherwise, the road points away from city 0, so it must be reversed.
                      - Count every such reversal while traversing the tree.
              */

              this.n = n;
              g = new ArrayList[n];
              for(int i = 0; i < n; i++) g[i] = new ArrayList<>();

              edges = new HashSet<>();

              for(int[] e : connections)
              {
                  edges.add(e[0] + "|" + e[1]); // stores the original edge directions

                  g[e[0]].add(e[1]);
                  g[e[1]].add(e[0]);
              }

              flipCount = 0;

              vis = new boolean[n];
              dfs(0);

              return flipCount;
          }

          void dfs(int node)
          {
              vis[node] = true;

              for(int next : g[node])
              {
                  if(!vis[next])
                  {
                      if (!edges.contains(next + "|" + node)) flipCount++;
                      dfs(next);
                  }
              }
          }
      }
        ```
      </details>

    -
      <details>
        <summary>Click to expand code - Approach-2 (Don't understand this)</summary>

        ```java
        class Solution {

          // Optimized approach-1

          List<int[]>[] graph;
          boolean[] vis;
          int flips = 0;

          public int minReorder(int n, int[][] connections) {

              /*
              * Key Observation:
              * The underlying graph is a tree, so every node has a unique path to city 0.
              * During a DFS from city 0, every traversed edge should point from the child
              * towards the parent. If an edge points from the parent to the child, it must
              * be reversed.
              *
              * Build an undirected graph while storing whether traversing an edge requires
              * a reversal:
              *      u -> v : cost = 1 (needs reversal)
              *      v -> u : cost = 0 (already correct)
              *
              * During DFS, simply add the cost of each traversed edge.
              *
              * Time : O(n)
              * Space: O(n)
              */

              graph = new ArrayList[n];
              for (int i = 0; i < n; i++)
                  graph[i] = new ArrayList<>();

              for (int[] edge : connections) {
                  int u = edge[0];
                  int v = edge[1];

                  graph[u].add(new int[]{v, 1}); // original direction: u -> v
                  graph[v].add(new int[]{u, 0}); // already points towards parent
              }

              vis = new boolean[n];
              dfs(0);

              return flips;
          }

          private void dfs(int node) {

              vis[node] = true;

              for (int[] edge : graph[node]) {

                  int next = edge[0];
                  int cost = edge[1];

                  if (vis[next])
                      continue;

                  flips += cost;
                  dfs(next);
              }
          }
      }
        ```
      </details>


18. [Count Unreachable Pairs of Nodes in an Undirected Graph](https://leetcode.com/problems/count-unreachable-pairs-of-nodes-in-an-undirected-graph/description/)

    -
      <details>
        <summary>Click to expand code - Approach-1</summary>

        ```java
        class Solution {

          ArrayList<Integer>[] g;
          int n;
          boolean[] vis;
          int nodeCount;

          public long countPairs(int n, int[][] edges) {
              this.n = n;
              vis = new boolean[n];

              g = new ArrayList[n];

              for(int i = 0; i < n; i++) g[i] = new ArrayList<>();

              for(int[] e : edges)
              {
                  g[e[0]].add(e[1]);
                  g[e[1]].add(e[0]);
              }

              List<Integer> componentNodeCount = new ArrayList<>();

              for(int i = 0; i < n; i++)
              {
                  if(vis[i]) continue;

                  nodeCount = 0;
                  dfs(i);
                  componentNodeCount.add(nodeCount);
              }

              long res = 0;
              long sumSoFar = componentNodeCount.get(0);
              n = componentNodeCount.size();

              for(int i = 1; i < n; i++)
              {
                  long curNodeCount = componentNodeCount.get(i);
                  res += curNodeCount * sumSoFar;
                  sumSoFar += curNodeCount;
              }

              return res;
          }

          void dfs(int node)
          {
              vis[node] = true;
              nodeCount++;

              for(int e : g[node])
              {
                  if(vis[e]) continue;

                  dfs(e);
              }
          }
      }
        ```
      </details>

    -
      <details>
        <summary>Click to expand code - Approach-2</summary>

        ```java
        class Solution {

          class DSU {
              int[] parent;
              int[] size;

              DSU(int n) {
                  parent = new int[n];
                  size = new int[n];

                  for (int i = 0; i < n; i++) {
                      parent[i] = i;
                      size[i] = 1;
                  }
              }

              int find(int x) {
                  if (parent[x] == x)
                      return x;

                  return parent[x] = find(parent[x]);
              }

              void union(int u, int v) {
                  u = find(u);
                  v = find(v);

                  if (u == v)
                      return;

                  /*
                      Traditional implementation -

                      if (size[u] >= size[v]) {
                          parent[v] = u;
                          size[u] += size[v];
                      } else {
                          parent[u] = v;
                          size[v] += size[u];
                      }
                  */

                  if (size[u] < size[v]) {
                      int temp = u;
                      u = v;
                      v = temp;
                  }

                  parent[v] = u;
                  size[u] += size[v];
              }
          }

          public long countPairs(int n, int[][] edges) {

              DSU dsu = new DSU(n);

              // Build connected components
              for (int[] edge : edges)
                  dsu.union(edge[0], edge[1]);

              long answer = 0;
              long remaining = n;

              // Count each component exactly once
              for (int i = 0; i < n; i++) {

                  if (dsu.find(i) != i)
                      continue;

                  remaining -= dsu.size[i];
                  answer += (long) dsu.size[i] * remaining;
              }

              return answer;
          }
      }
        ```
      </details>


19. ⭐ [Longest Cycle in a Graph](https://leetcode.com/problems/longest-cycle-in-a-graph/description/)

    -
      <details>
        <summary>Click to expand code</summary>

        ```java
        class Solution {

          int n;
          boolean[] vis;
          int[] dfsVis;
          int[] g;
          int res = -1;
          int nodeIndex;

          public int longestCycle(int[] edges) {
              g = edges;
              n = g.length;
              vis = new boolean[n];
              dfsVis = new int[n];
              Arrays.fill(dfsVis, -1);

              res = -1;
              nodeIndex = 0;

              for(int i = 0; i < n; i++)
              {
                  if(vis[i]) continue;

                  dfs(i);
              }

              return res;
          }

          void dfs(int node)
          {
              vis[node] = true;
              dfsVis[node] = nodeIndex++;

              int next = g[node];

              if(next == -1) {
                  dfsVis[node] = -1;
                  return;
              }

              if(!vis[next]) dfs(next);
              else if(dfsVis[next] != -1)
              {
                  res = Math.max(res, dfsVis[node] - dfsVis[next] + 1);
              }

              dfsVis[node] = -1;
          }
      }
      /*
          ⭐ Note - This solution only works because there is utmost one outgoing edge from each node.

          This means that there can be utmost one cycle in the graph.
      */
      ```
      </details>


20. [Clone Graph](https://leetcode.com/problems/clone-graph/description/)

    -
      <details>
        <summary>Click to expand code - Approach-1</summary>

        ```java
        /*
          // Definition for a Node.
          class Node {
              public int val;
              public List<Node> neighbors;
              public Node() {
                  val = 0;
                  neighbors = new ArrayList<Node>();
              }
              public Node(int _val) {
                  val = _val;
                  neighbors = new ArrayList<Node>();
              }
              public Node(int _val, ArrayList<Node> _neighbors) {
                  val = _val;
                  neighbors = _neighbors;
              }
          }
        */

        class Solution {

            Node[] nodes;

            public Node cloneGraph(Node node) {
                if(node == null) return node;

                nodes = new Node[101];
                solve(node);
                return nodes[node.val];
            }

            void solve(Node node)
            {
                Node newNode = new Node(node.val);
                nodes[node.val] = newNode;

                for(Node n : node.neighbors)
                {
                    if(nodes[n.val] == null) solve(n);
                    newNode.neighbors.add(nodes[n.val]);
                }
            }

        }
      ```
      </details>

    -
      <details>
        <summary>Click to expand code - Approach-2</summary>

        ```java
        class Solution {

            HashMap<Node, Node> map = new HashMap<>();

            public Node cloneGraph(Node node) {
                if (node == null) return null;

                if (map.containsKey(node))
                    return map.get(node);

                Node clone = new Node(node.val);
                map.put(node, clone);

                for (Node neighbor : node.neighbors)
                    clone.neighbors.add(cloneGraph(neighbor));

                return clone;
            }
        }
        ```
      </details>

    -
      <details>
        <summary>Click to expand code - Approach-3</summary>

        ```java
        class Solution {

          public Node cloneGraph(Node node) {
              if (node == null) return null;

              HashMap<Node, Node> map = new HashMap<>();
              Queue<Node> q = new LinkedList<>();

              q.offer(node);
              map.put(node, new Node(node.val));

              while (!q.isEmpty()) {
                  Node cur = q.poll();

                  for (Node nei : cur.neighbors) {

                      if (!map.containsKey(nei)) {
                          map.put(nei, new Node(nei.val));
                          q.offer(nei);
                      }

                      map.get(cur).neighbors.add(map.get(nei));
                  }
              }

              return map.get(node);
          }
      }
      ```
      </details>


21. ⭐⭐⭐❌ [Largest Color Value in a Directed Graph](https://leetcode.com/problems/largest-color-value-in-a-directed-graph/)

    -
      <details>
        <summary>Click to expand code - Approach-1</summary>

        ```java
        /*
            Idea:
            - Perform DFS on the graph while detecting cycles using vis[] + pathVis[].
            - DP State:
                dist[node][c] = maximum count of color 'c' on any path starting from 'node'.
            - After all children are processed, merge their DP arrays by taking the maximum
            count for each color, then include the current node's own color.
            - Since every node is processed once and each DP array has only 26 entries,
            the overall complexity is O((V + E) * 26).

            Cycle Detection:
            - If a back edge is found (pathVis[]), the graph contains a cycle,
            so no valid answer exists and return -1.
        */
        class Solution {

            int res = -1;
            int n;
            char[] colours;
            List<List<Integer>> g;
            boolean[] vis;
            boolean[] pathVis;
            boolean isCyclic;

            int[][] dist;

            void dfs(int node)
            {
                vis[node] = true;
                pathVis[node] = true;
                int key = colours[node] - 'a';

                int[] count = new int[26];
                int[] maxPathCount = new int[26];
                count[key]++;

                res = Math.max(res, count[key]);

                for(int e: g.get(node))
                {
                    if(!vis[e])
                        dfs(e);
                    else if(pathVis[e])
                    {
                        isCyclic = true;
                        break;
                    }

                    for(int i = 0; i < 26; i++)
                    {
                        // count[i] += dist[e][i];
                        int curNodeDist = count[i] + dist[e][i];
                        maxPathCount[i] = Math.max(maxPathCount[i], curNodeDist);
                        res = Math.max(res, maxPathCount[i]);
                    }
                }

                // System.out.println("Processing for node: " + node);
                for(int i = 0; i < 26; i++)
                {
                    count[i] = Math.max(count[i], maxPathCount[i]);
                    if(count[i] == 0) continue;
                    char ch = (char)(i + 'a');

                    // System.out.println("char: " + ch + ", count: " + count[i]);
                }
                    // System.out.println("\n");

                dist[node] = count;
                pathVis[node] = false;
            }

            public int largestPathValue(String colors, int[][] edges) {


                colours = colors.toCharArray();
                n = colours.length;
                g = new ArrayList<>();

                if(edges.length == 0) return 1;

                vis = new boolean[n];
                pathVis = new boolean[n];
                isCyclic = false;

                dist = new int[n][26];

                int[] indegree = new int[n];

                for(int i = 0; i < n; i++)
                    g.add(new ArrayList<>());

                for(int[] e: edges)
                {
                    g.get(e[0]).add(e[1]);
                    indegree[e[1]]++;
                }

                res = -1;
                int dfsCount = 0;
                for(int i = 0; i < n; i++)
                {
                    if(indegree[i] == 0 && g.get(i).size() > 0)
                    {
                        dfs(i);
                        dfsCount++;
                    }
                }

                if(isCyclic || dfsCount == 0) return -1;

                return res;
            }
        }
        ```
      </details>

    -
      <details>
        <summary>Click to expand code - Approach-2</summary>

        ```java
        /*
            Idea:
            - Process the graph in topological order using Kahn's algorithm.
            - DP State:
                dp[node][c] = maximum count of color 'c' on any path ending at 'node'.
            - When processing a node, include its own color, then propagate its DP array
            to all children by taking the maximum for each color.
            - Because a node is processed only after all its parents, its DP already
            contains the best values from every incoming path.
            - Time Complexity: O((V + E) * 26).

            Cycle Detection:
            - If the number of processed nodes is less than n, the graph contains
            a cycle, so return -1.
        */
        class Solution {

            public int largestPathValue(String colors, int[][] edges) {

                int n = colors.length();

                ArrayList<Integer>[] graph = new ArrayList[n];
                for (int i = 0; i < n; i++)
                    graph[i] = new ArrayList<>();

                int[] indegree = new int[n];

                for (int[] e : edges) {
                    graph[e[0]].add(e[1]);
                    indegree[e[1]]++;
                }

                Queue<Integer> q = new LinkedList<>();

                for (int i = 0; i < n; i++)
                    if (indegree[i] == 0)
                        q.offer(i);

                int[][] dp = new int[n][26];

                int visited = 0;
                int ans = 0;

                while (!q.isEmpty()) {

                    int u = q.poll();
                    visited++;

                    // Include the current node's own color.
                    int color = colors.charAt(u) - 'a';
                    dp[u][color]++;

                    ans = Math.max(ans, dp[u][color]);

                    for (int v : graph[u]) {

                        // Propagate the best counts to the child.
                        for (int c = 0; c < 26; c++)
                            dp[v][c] = Math.max(dp[v][c], dp[u][c]);

                        if (--indegree[v] == 0)
                            q.offer(v);
                    }
                }

                return visited == n ? ans : -1;
            }
        }
        ```
      </details>

    -
      <details>
        <summary>Click to expand code - Approach-3</summary>

        ```java
        /*
            Idea:
            - Run DFS while detecting cycles using vis[] and pathVis[].
            - DP State:
                dist[node][c] = maximum count of color 'c' on any path
                starting from 'node'.
            - After processing all children, merge their DP arrays by taking the
            maximum count for each color, then increment the current node's color.
            - The answer is the maximum value across all DP states.
            - Time: O((V + E) * 26)
            - Space: O(V * 26)
        */
        class Solution {

            int n;
            char[] colors;
            ArrayList<Integer>[] graph;

            boolean[] vis;
            boolean[] pathVis;
            boolean hasCycle;

            int[][] dist;
            int ans = 0;

            void dfs(int u) {

                vis[u] = true;
                pathVis[u] = true;

                // Merge DP from all children.
                for (int v : graph[u]) {

                    if (!vis[v]) {
                        dfs(v);
                        if (hasCycle) return;
                    } else if (pathVis[v]) {
                        hasCycle = true;
                        return;
                    }

                    for (int c = 0; c < 26; c++)
                        dist[u][c] = Math.max(dist[u][c], dist[v][c]);
                }

                // Include the current node's own color.
                int color = colors[u] - 'a';
                dist[u][color]++;

                ans = Math.max(ans, dist[u][color]);

                pathVis[u] = false;
            }

            public int largestPathValue(String colors, int[][] edges) {

                this.colors = colors.toCharArray();
                n = colors.length();

                graph = new ArrayList[n];
                for (int i = 0; i < n; i++)
                    graph[i] = new ArrayList<>();

                int[] indegree = new int[n];

                for (int[] e : edges) {
                    graph[e[0]].add(e[1]);
                    indegree[e[1]]++;
                }

                vis = new boolean[n];
                pathVis = new boolean[n];
                dist = new int[n][26];

                // Process all source components first.
                for (int i = 0; i < n; i++) {
                    if (indegree[i] == 0 && !vis[i])
                        dfs(i);
                }

                // Visit any remaining disconnected components.
                for (int i = 0; i < n; i++) {
                    if (!vis[i])
                        dfs(i);
                }

                return hasCycle ? -1 : ans;
            }
        }
        ```
      </details>


22. [Similar String Groups](https://leetcode.com/problems/similar-string-groups/description/)

    -
      <details>
        <summary>Click to expand code</summary>

        ```java
        class Solution {

            class DSU{
                int n;
                int[] parent;
                int[] rank;

                DSU(int n)
                {
                    this.n = n;
                    parent = new int[n];
                    rank = new int[n];

                    for(int i = 0; i < n; i++)
                    {
                        parent[i] = i;
                        rank[i] = 1;
                    }
                }

                int find(int x)
                {
                    if(parent[x] == x) return x;

                    return parent[x] = find(parent[x]);
                }

                void union(int u, int v)
                {
                    u = find(u);
                    v = find(v);

                    if(u == v) return;

                    if(rank[u] >= rank[v])
                    {
                        parent[v] = u;
                        rank[u] += rank[v];
                    }
                    else
                    {
                        parent[u] = v;
                        rank[v] += rank[u];
                    }
                }
            }

            int n;
            int m;

            public int numSimilarGroups(String[] strs) {
                n = strs.length;
                m = strs[0].length();

                DSU ds = new DSU(n);

                for(int i = 0; i < n; i++)
                {
                    for(int j = i + 1; j < n; j++)
                    {
                        if(isValidPair(strs[i], strs[j])) ds.union(i, j);
                    }
                }

                HashSet<Integer> hs = new HashSet<>();
                for(int i = 0; i < n; i++) hs.add(ds.find(i));

                return hs.size();
            }


            // It is given that all strings are anagrams of each other, so we only need
            // to check if they differ by exactly 2 characters or are identical.
            boolean isValidPair(String str1, String str2)
            {
                int count = 0;

                for(int i = 0; i < m; i++)
                {
                    if(str1.charAt(i) != str2.charAt(i)) count++;
                }

                return count == 0 || count == 2;
            }

        }
        ```
      </details>


23. ⭐❌ [Build Array from Permutation](https://leetcode.com/problems/build-array-from-permutation/description/)

    -
      <details>
        <summary>Click to expand code</summary>

        ```java
        class Solution {
            public int[] buildArray(int[] nums) {

                int n = nums.length;

                // Encode old and new value together
                for (int i = 0; i < n; i++) {
                    nums[i] += (nums[nums[i]] % n) * n;
                }

                // Extract new value
                for (int i = 0; i < n; i++) {
                    nums[i] /= n;
                }

                return nums;
            }
        }
        ```
      </details>


24. ⭐⭐⭐ [Checking Existence of Edge Length Limited Paths](https://leetcode.com/problems/checking-existence-of-edge-length-limited-paths/description/)

    - The idea is same as Problem-13: Number of Good Paths.
    -
      <details>
        <summary>Click to expand code</summary>

        ```java
        class Solution {

            class DSU{
                int n;
                int[] parent;
                int[] size;

                DSU(int n)
                {
                    this.n = n;
                    parent = new int[n];
                    size = new int[n];

                    for(int i = 0; i < n; i++)
                    {
                        parent[i] = i;
                        size[i] = 1;
                    }
                }

                int find(int x)
                {
                    if(parent[x] == x) return x;

                    return parent[x] = find(parent[x]);
                }

                void union(int u, int v)
                {
                    u = find(u);
                    v = find(v);

                    if(u == v) return;

                    if(size[u] >= size[v])
                    {
                        parent[v] = u;
                        size[u] += size[v];
                    }
                    else{
                        parent[u] = v;
                        size[v] += size[u];
                    }
                }
            }

            public boolean[] distanceLimitedPathsExist(int n, int[][] edgeList, int[][] queries) {

                Arrays.sort(edgeList, (a,b) -> a[2] - b[2]); // ElogE

                int[][] q = new int[queries.length][4];
                for(int i = 0; i < q.length; i++)
                {
                    q[i] = new int[]{
                        queries[i][0], queries[i][1], queries[i][2], i
                    };
                }

                Arrays.sort(q, (a,b) -> a[2] - b[2]); // QlogQ

                int m = q.length;
                boolean[] res = new boolean[m];

                int j = 0;
                DSU ds = new DSU(n);

                for(int i = 0; i < m; i++)
                {
                    int u = q[i][0];
                    int v = q[i][1];
                    int limit = q[i][2];
                    int ind = q[i][3];

                    while(j < edgeList.length && edgeList[j][2] < limit)
                    {
                        ds.union(edgeList[j][0], edgeList[j][1]);
                        j++;
                    }

                    res[ind] = ds.find(u) == ds.find(v);
                }

                return res;
            }
        }
        ```
      </details>


25. ⭐ [Remove Max Number of Edges to Keep Graph Fully Traversable](https://leetcode.com/problems/remove-max-number-of-edges-to-keep-graph-fully-traversable/description/)

    -
      <details>
        <summary>Click to expand code</summary>

        ```java
        class Solution {

            class DSU{
                int n;
                int[] parent;
                int[] size;
                int components; // ⭐ This is new

                DSU(int n)
                {
                    this.n = n;
                    parent = new int[n + 1];
                    size = new int[n + 1];
                    components = n;  // ⭐ Initially, we have 'n' components

                    for(int i = 1; i <= n; i++)
                    {
                        parent[i] = i;
                        size[i] = 1;
                    }
                }

                int find(int x)
                {
                    if(parent[x] == x) return x;

                    return parent[x] = find(parent[x]);
                }

                boolean union(int u, int v)
                {
                    u = find(u);
                    v = find(v);

                    if(u == v) return false;

                    if(size[u] < size[v])
                    {
                        int temp = u;
                        u = v;
                        v = temp;
                    }

                    parent[v] = u;
                    size[u] += size[v];

                    components--;  // ⭐ After each merge, we decrease the component count
                    return true;
                }
            }

            public int maxNumEdgesToRemove(int n, int[][] edges) {

                Arrays.sort(edges, (a,b) -> b[0] - a[0]);

                DSU alice = new DSU(n);
                DSU bob = new DSU(n);

                int nodesToDelete = 0;

                for(int i = 0; i < edges.length; i++)
                {
                    int type = edges[i][0];
                    int u = edges[i][1];
                    int v = edges[i][2];

                    if(type == 3)
                    {
                        boolean usedByAlice = alice.union(u, v);
                        boolean usedByBob = bob.union(u, v);

                        if (!usedByAlice && !usedByBob)
                            nodesToDelete++;
                    }
                    else if(type == 2)
                    {
                        boolean usedByBob = bob.union(u, v);
                        if(!usedByBob) nodesToDelete++;
                    }
                    else // alice
                    {
                        boolean usedByAlice = alice.union(u, v);
                        if(!usedByAlice) nodesToDelete++;
                    }
                }

                // This is an important check, we need to validate if
                // Alice and Bob can reach every node.
                // If the graph is connected, then the component count will be equal to 1
                if(alice.components != 1 || bob.components != 1)
                    return -1;

                return nodesToDelete;
            }
        }
        ```
      </details>


26. [Minimum Number of Vertices to Reach All Nodes](https://leetcode.com/problems/minimum-number-of-vertices-to-reach-all-nodes/description/)

    -
      <details>
        <summary>Click to expand code</summary>

        ```java
        /*
            Idea:
            - In a DAG, every node with indegree 0 cannot be reached from any other node,
            so it must be included in the answer.
            - Every other node has at least one incoming edge and is therefore reachable
            from some indegree 0 node.
            - Hence, the minimum set of starting vertices is simply all nodes whose
            indegree is 0.
        */
        class Solution {
            public List<Integer> findSmallestSetOfVertices(int n, List<List<Integer>> edges) {

                int[] indegree = new int[n];

                for (List<Integer> edge : edges)
                    indegree[edge.get(1)]++;

                List<Integer> ans = new ArrayList<>();

                for (int i = 0; i < n; i++) {
                    if (indegree[i] == 0)
                        ans.add(i);
                }

                return ans;
            }
        }
        ```
      </details>


27. ⭐ [Evaluate Division](https://leetcode.com/problems/evaluate-division/description/)

    -
      <details>
        <summary>Click to expand code - Approach-1 (Best)</summary>

        ```java
        class Solution {
            /*
                Idea:
                - Treat each variable as a node and each equation as a weighted edge.
                Example: a / b = 2 becomes
                    a -> b (2)
                    b -> a (1/2)
                - For each query, perform a DFS to find any path from the source to the
                destination while multiplying the edge weights along the path.
                - If the destination is reached, the accumulated product is the answer.
                Otherwise, the variables are disconnected and the answer is -1.

                Complexity

                    Suppose:

                        V = number of variables
                        E = number of equations
                        Q = number of queries

                    Building the graph: O(E)

                    Each query performs one DFS: O(V + E)

                    Overall: O(E + Q(V + E))

                    Space: O(V + E)
            */

            class Pair{
                String next;
                double val;

                Pair(String n, double v)
                {
                    next = n;
                    val = v;
                }
            }

            // character -> list of neighbours
            Map<String, List<Pair>> g;

            HashSet<String> vis;

            public double[] calcEquation(List<List<String>> equations, double[] values, List<List<String>> queries) {
                g = new HashMap<>();

                for(int i = 0; i < values.length; i++)
                {
                    String u = equations.get(i).get(0);
                    String v = equations.get(i).get(1);
                    double val = values[i];

                    g.computeIfAbsent(u, k -> new ArrayList<>()).add(new Pair(v, val));
                    g.computeIfAbsent(v, k -> new ArrayList<>()).add(new Pair(u, 1/val));
                }

                int n = queries.size();
                double[] res = new double[n];

                for(int i = 0; i < n; i++)
                {
                    String u = queries.get(i).get(0);
                    String v = queries.get(i).get(1);

                    if(!g.containsKey(u) || !g.containsKey(v))
                    {
                        res[i] = -1;
                        continue;
                    }

                    vis = new HashSet<>();
                    res[i] = dfs(u, v, 1.0);
                }

                return res;
            }

            double dfs(String src, String dest, double curVal)
            {
                vis.add(src);

                if(src.equals(dest)) return curVal;

                for(Pair p : g.get(src))
                {
                    String next = p.next;
                    double val = p.val;

                    if(vis.contains(next)) continue;

                    double cost = dfs(next, dest, curVal * val);
                    if(cost != -1) return cost;
                }

                return -1;
            }
        }
        ```
      </details>

    -
      <details>
        <summary>Click to expand code - Approach-2 (Good)</summary>

        ```java
        class Solution {
            /*
                Idea: use the Floyd-Warshall algorithm
                - Map each variable to an integer and build an adjacency matrix where
                dist[i][j] represents the ratio i / j.
                - Initialize the given equations and their reciprocals in the matrix.
                - Apply Floyd-Warshall:
                    If i / k and k / j are known, then
                        i / j = (i / k) * (k / j)
                allowing us to derive the ratio between every pair of connected variables.
                - Once preprocessing is complete, each query can be answered in O(1)
                by looking up the corresponding entry in the matrix.
            */

            public double[] calcEquation(List<List<String>> equations, double[] values, List<List<String>> queries) {

                // Assign an integer id to every variable
                Map<String, Integer> id = new HashMap<>();

                int idx = 0;

                for (List<String> e : equations) {
                    if (!id.containsKey(e.get(0)))
                        id.put(e.get(0), idx++);

                    if (!id.containsKey(e.get(1)))
                        id.put(e.get(1), idx++);
                }

                int n = idx;

                double[][] dist = new double[n][n];

                for (int i = 0; i < n; i++) {
                    Arrays.fill(dist[i], -1.0);
                    dist[i][i] = 1.0;
                }

                // Build graph
                for (int i = 0; i < equations.size(); i++) {
                    int u = id.get(equations.get(i).get(0));
                    int v = id.get(equations.get(i).get(1));

                    dist[u][v] = values[i];
                    dist[v][u] = 1.0 / values[i];
                }

                // Floyd-Warshall
                for (int k = 0; k < n; k++) {
                    for (int i = 0; i < n; i++) {

                        if (dist[i][k] == -1)
                            continue;

                        for (int j = 0; j < n; j++) {

                            if (dist[k][j] == -1)
                                continue;

                            // Only compute if not already known
                            if (dist[i][j] == -1)
                                dist[i][j] = dist[i][k] * dist[k][j];
                        }
                    }
                }

                double[] ans = new double[queries.size()];

                for (int i = 0; i < queries.size(); i++) {

                    String a = queries.get(i).get(0);
                    String b = queries.get(i).get(1);

                    if (!id.containsKey(a) || !id.containsKey(b)) {
                        ans[i] = -1.0;
                        continue;
                    }

                    ans[i] = dist[id.get(a)][id.get(b)];
                }

                return ans;
            }
        }
        ```
      </details>

    -
      <details>
        <summary>Click to expand code - Approach-3 (Uses new DS - can be complicated)</summary>

        ```java
        class Solution {

            class DSU {
                Map<String, String> parent = new HashMap<>();
                Map<String, Double> weight = new HashMap<>();

                void add(String x) {
                    if (!parent.containsKey(x)) {
                        parent.put(x, x);
                        weight.put(x, 1.0);
                    }
                }

                String find(String x) {
                    if (parent.get(x).equals(x))
                        return x;

                    String p = parent.get(x);
                    String root = find(p);

                    // x/root = (x/p) * (p/root)
                    weight.put(x, weight.get(x) * weight.get(p));
                    parent.put(x, root);

                    return root;
                }

                void union(String a, String b, double value) {

                    add(a);
                    add(b);

                    String ra = find(a);
                    String rb = find(b);

                    if (ra.equals(rb))
                        return;

                    double wa = weight.get(a);
                    double wb = weight.get(b);

                    // Attach ra under rb
                    parent.put(ra, rb);

                    // ra/rb = value * wb / wa
                    weight.put(ra, value * wb / wa);
                }

                double query(String a, String b) {

                    if (!parent.containsKey(a) || !parent.containsKey(b))
                        return -1.0;

                    String ra = find(a);
                    String rb = find(b);

                    if (!ra.equals(rb))
                        return -1.0;

                    return weight.get(a) / weight.get(b);
                }
            }

            public double[] calcEquation(List<List<String>> equations,
                                        double[] values,
                                        List<List<String>> queries) {

                DSU dsu = new DSU();

                for (int i = 0; i < equations.size(); i++) {
                    dsu.union(
                        equations.get(i).get(0),
                        equations.get(i).get(1),
                        values[i]
                    );
                }

                double[] ans = new double[queries.size()];

                for (int i = 0; i < queries.size(); i++) {
                    ans[i] = dsu.query(
                        queries.get(i).get(0),
                        queries.get(i).get(1)
                    );
                }

                return ans;
            }
        }
        ```
      </details>

    - Approach-3 uses [Weighted Union-Find](./Chapter-1.3%20Advanced%20DSU.md)


28. ⭐⭐⭐ [Detonate the Maximum Bombs](https://leetcode.com/problems/detonate-the-maximum-bombs/description/)

    -
      <details>
        <summary>Click to expand code</summary>

        ```java
        class Solution {

            ArrayList<Integer>[] graph;

            public int maximumDetonation(int[][] bombs) {
                int n = bombs.length;

                graph = new ArrayList[n];
                for (int i = 0; i < n; i++) {
                    graph[i] = new ArrayList<>();
                }

                // Build directed graph:
                // i -> j if bomb i can detonate bomb j.
                for (int i = 0; i < n; i++) {
                    for (int j = 0; j < n; j++) {
                        if (i != j && canDetonate(bombs[i], bombs[j])) {
                            graph[i].add(j);
                        }
                    }
                }

                int res = 1;

                // Try detonating every bomb as the starting point.
                for (int i = 0; i < n; i++) {
                    boolean[] vis = new boolean[n];
                    res = Math.max(res, dfs(i, vis));
                }

                return res;
            }

            // Returns the number of bombs detonated starting from 'node'.
            int dfs(int node, boolean[] vis) {
                vis[node] = true;

                int count = 1;

                for (int nei : graph[node]) {
                    if (!vis[nei]) {
                        count += dfs(nei, vis);
                    }
                }

                return count;
            }

            // Returns true if bomb1 can directly detonate bomb2.
            boolean canDetonate(int[] bomb1, int[] bomb2) {
                long x1 = bomb1[0];
                long y1 = bomb1[1];
                long r = bomb1[2];

                long x2 = bomb2[0];
                long y2 = bomb2[1];

                long dx = x1 - x2;
                long dy = y1 - y2;

                return dx * dx + dy * dy <= r * r;
            }
        }
        ```
      </details>


29. [Path with Maximum Probability](https://leetcode.com/problems/path-with-maximum-probability/)

    -
      <details>
        <summary>Click to expand code</summary>

        ```java
        class Solution {

            public double maxProbability(int n, int[][] edges, double[] succProb, int start, int end) {

                // graph[node] = {neighbor, edgeProbability}
                ArrayList<Pair>[] graph = new ArrayList[n];
                for (int i = 0; i < n; i++) {
                    graph[i] = new ArrayList<>();
                }

                for (int i = 0; i < edges.length; i++) {
                    int u = edges[i][0];
                    int v = edges[i][1];
                    double p = succProb[i];

                    graph[u].add(new Pair(v, p));
                    graph[v].add(new Pair(u, p));
                }

                // Maximum probability of reaching each node.
                double[] prob = new double[n];
                prob[start] = 1.0;

                // Max Heap: {node, probability}
                PriorityQueue<State> pq = new PriorityQueue<>(
                    (a, b) -> Double.compare(b.prob, a.prob)
                );

                pq.offer(new State(start, 1.0));

                while (!pq.isEmpty()) {

                    State curr = pq.poll();
                    int node = curr.node;
                    double currProb = curr.prob;

                    // Lazy deletion
                    if (currProb < prob[node])
                        continue;

                    // First time we pop 'end', we've found the maximum probability.
                    if (node == end)
                        return currProb;

                    for (Pair next : graph[node]) {

                        int nei = next.node;
                        double newProb = currProb * next.prob;

                        if (newProb > prob[nei]) {
                            prob[nei] = newProb;
                            pq.offer(new State(nei, newProb));
                        }
                    }
                }

                return 0.0;
            }

            class Pair {
                int node;
                double prob;

                Pair(int node, double prob) {
                    this.node = node;
                    this.prob = prob;
                }
            }

            class State {
                int node;
                double prob;

                State(int node, double prob) {
                    this.node = node;
                    this.prob = prob;
                }
            }
        }
        ```
      </details>


30. [Find Eventual Safe States](https://leetcode.com/problems/find-eventual-safe-states/description/)


    -
      <details>
        <summary>Click to expand code - Approach-1</summary>

        ```java
        class Solution {
            //  TC - O(nlogn)


            List<Integer> res;
            boolean[] vis;
            boolean[] isValidSafeNode;
            int n;
            int[][] g;

            public List<Integer> eventualSafeNodes(int[][] graph) {
                n = graph.length;
                vis = new boolean[n];
                isValidSafeNode = new boolean[n];
                res = new ArrayList<>();
                g = graph;

                for(int i = 0; i < n; i++)
                {
                    if(vis[i]) continue;

                    solve(i);
                }

                Collections.sort(res);

                return res;
            }

            boolean solve(int node)
            {
                vis[node] = true;
                isValidSafeNode[node] = false;

                boolean isValidNode = true;

                for(int e : g[node])
                {
                    if(vis[e]) isValidNode &= isValidSafeNode[e];

                    else isValidNode &= solve(e);
                }

                if(isValidNode) res.add(node);

                return isValidSafeNode[node] = isValidNode;
            }
        }
        ```
      </details>

    -
      <details>
        <summary>Click to expand code - Approach-2</summary>

        ```java
        class Solution {
            /*
                Optimized approach-1.
                This solution gets rid of sorting
                TC - O(n)
            */

            List<Integer> res;
            boolean[] vis;
            boolean[] isValidSafeNode;
            int n;
            int[][] g;

            public List<Integer> eventualSafeNodes(int[][] graph) {
                n = graph.length;
                vis = new boolean[n];
                isValidSafeNode = new boolean[n];
                res = new ArrayList<>();
                g = graph;

                for(int i = 0; i < n; i++)
                {
                    boolean isValidNode = false;

                    if(vis[i]) isValidNode = isValidSafeNode[i];
                    else isValidNode = solve(i);

                    if(isValidNode) res.add(i);
                }

                return res;
            }

            boolean solve(int node)
            {
                vis[node] = true;
                isValidSafeNode[node] = false;

                boolean isValidNode = true;

                for(int e : g[node])
                {
                    if(vis[e]) isValidNode &= isValidSafeNode[e];

                    else isValidNode &= solve(e);
                }

                return isValidSafeNode[node] = isValidNode;
            }
        }
        ```
      </details>

    -
      <details>
        <summary>Click to expand code - Approach-3</summary>

        ```java
        class Solution {

            boolean[] vis;
            boolean[] isSafe;
            boolean[] pathVis;
            int v;

            int[][] g;

            boolean dfs(int i)
            {
                vis[i] = true;
                pathVis[i] = true;

                boolean isCurNodeSafe = true;

                for(int e : g[i])
                {
                    if(!vis[e])
                    {
                        isCurNodeSafe = dfs(e) && isCurNodeSafe;
                    }

                    else if(pathVis[e])
                    {
                        isCurNodeSafe = false;
                    }

                    else{
                        isCurNodeSafe = isCurNodeSafe && isSafe[e];
                    }
                }

                pathVis[i] = false;

                return isSafe[i] = isCurNodeSafe;
            }

            public List<Integer> eventualSafeNodes(int[][] graph) {

                v = graph.length;
                g = graph;

                vis = new boolean[v];
                isSafe = new boolean[v];
                pathVis = new boolean[v];
                for(int i = 0; i < v; i++)
                {
                    if(!vis[i])
                    {
                        dfs(i);
                    }
                }

                List<Integer> res = new ArrayList<>();

                for(int i = 0; i < v; i++)
                {
                    if(isSafe[i])
                    {
                        res.add(i);
                    }
                }

                return res;


            }
        }
        ```
      </details>

<!--
48. []()
    - [YT Solution]()
    -
      <details>
        <summary>Click to expand code</summary>

        ```java
        class Solution {
        }
        ```
      </details>
-->


---

# Legend
```
⭐ - imp problem
❌ - Did not understand/solve
```

---

# Techniques

1.  Reversing the graph

2.  Removing all edges, and building graph again (it could be based on edge weight) – uses DSU.

3.  Adding fake edges in a directed graph (opposite to the real edges)

4.  Topo-sort

5. Connected components
    - example problems - 2

## DP on trees/graphs
it's **very closely related**. In fact, the [Longest Path With Different Adjacent Characters](https://leetcode.com/problems/longest-path-with-different-adjacent-characters/description/) (problem 11 in this sheet) is almost identical to the [Binary Tree Maximum Path Sum](https://leetcode.com/problems/binary-tree-maximum-path-sum/description/) problem. The only differences are **what each DFS returns** and **how you combine child results**.

Here's the comparison:

| Longest Path with Different Adjacent Characters | Binary Tree Maximum Path Sum             |
| ----------------------------------------------- | ---------------------------------------- |
| Return longest downward path (number of nodes)  | Return maximum downward sum              |
| Global answer = best1 + best2 + 1               | Global answer = left + right + node.val  |
| Ignore child if labels are equal                | Ignore child if contribution is negative |

Both problems follow the same template:

```java
int dfs(node) {

    int best1 = ...;   // best contribution from children
    int best2 = ...;   // second best contribution

    // Candidate answer passing through this node
    answer = max(answer, best1 + best2 + selfContribution);

    // Return only one branch to the parent
    return best1 + selfContribution; // or best2 + selfContribution; whichever is greater
}
```

The key observation is:

* A path **passing through** a node can use **two** child branches.
* A path **returned to the parent** can use **only one** child branch.

Once you recognize this pattern, you'll find it appears in many tree DP problems:

* ✅ LeetCode 124 - Binary Tree Maximum Path Sum
* ✅ LeetCode 687 - Longest Univalue Path
* ✅ LeetCode 2246 - Longest Path With Different Adjacent Characters
* ✅ Diameter of Binary Tree / Diameter of N-ary Tree

---

In fact, most Tree DP problems fall into **5-6 common templates**. Once you recognize which template a problem belongs to, the recurrence almost writes itself.

### 1. Return a value to parent + update a global answer (Most Common)

**Idea:** Each node computes some information to return to its parent, while also updating a global answer using its children.

Template:

```java
int dfs(node) {

    // Collect information from children
    ...

    // Update global answer
    answer = ...

    // Return information to parent
    return ...
}
```

Examples:

* Diameter of Tree
* Binary Tree Maximum Path Sum
* Longest Univalue Path
* Longest Path With Different Adjacent Characters

Typical recurrence:

```text
Return:
    Best downward path

Global:
    Best path passing through node
```

### 2. Aggregate information from all children

Here, every child contributes to the answer.

Template:

```java
int dfs(node) {

    int ans = base;

    for(child)
        ans += dfs(child);

    return ans;
}
```

Examples:

* Count nodes in subtree
* Sum of subtree values
* Count nodes with same label (LeetCode 1519)
* Tree size
* Number of descendants

Example:

```text
subtreeSize(node)

=
1 + Σ subtreeSize(child)
```

No global answer is needed.

### 3. DP State per Node

Instead of returning one integer, return multiple states.

Example:

```java
dp[node][0]
dp[node][1]
```

or

```java
class State{
    int include;
    int exclude;
}
```

Examples:

* House Robber III
* Maximum Independent Set
* Vertex Cover
* Tree Matching

Example:

```text
Include node
Exclude node
```

Transition:

```text
include =
node.val +
sum(exclude(child))

exclude =
sum(max(include, exclude))
```

### 4. Re-rooting DP

Compute answer for **every node**.

Instead of

```text
answer(root)
```

compute

```text
answer(0)
answer(1)
answer(2)
...
```

Usually two DFS traversals.

Examples:

* Sum of Distances in Tree
* Tree Distances II (CSES)
* Count nodes at distance K

Typical flow:

```text
DFS1

Compute subtree information

↓

DFS2

Propagate parent information
```

### 5. Merge child DP states (Knapsack on Trees)

Every child has its own DP array.

Merge them.

Template:

```java
for(child){

    dfs(child);

    merge(dp[node], dp[child]);
}
```

Examples:

* Tree Knapsack
* Selecting K nodes
* Tree Coloring
* Connected Subtree DP

Usually complexity

```text
O(NK²)
```

### 6. Bitmask / Frequency DP

Each subtree returns a data structure.

Examples:

Return

```text
HashMap
Frequency array
Bitmask
Trie
```

Merge them.

Examples:

* Small to Large (DSU on Tree)
* Count distinct colors
* Palindrome paths
* Label frequencies

### Recognizing the template

When reading a problem, ask yourself:

#### Is the answer only for the root?

Usually

> Aggregate DP

Example:

```text
Subtree size
Subtree sum
```

### Does the answer pass through any node?

Usually

> Return + Global Answer

Example:

```text
Diameter
Maximum Path Sum
Longest Path
```

#### Does every node need an answer?

Usually

> Re-root DP

Example:

```text
Sum of Distances
```

#### Does the node have multiple choices?

Usually

> DP States

Example:

```text
Take node
Skip node
```

#### Do child DPs need to be combined?

Usually

> Knapsack Merge

### A handy cheat sheet

| Pattern         | Return             | Global Answer | Example                                        |
| --------------- | ------------------ | ------------- | ---------------------------------------------- |
| Aggregate       | Sum/count          | ❌             | Subtree Size, Count Subtrees                   |
| Return + Global | Best downward path | ✅             | Diameter, Max Path Sum, Longest Different Path |
| DP States       | Multiple values    | Sometimes     | House Robber III                               |
| Re-root DP      | Subtree info       | Second DFS    | Sum of Distances                               |
| Knapsack Merge  | DP array           | Sometimes     | Tree Knapsack                                  |
| DSU on Tree     | Map/Bitmask        | No            | Distinct Colors                                |

These six patterns cover the vast majority of tree DP problems you'll encounter in interviews and competitive programming. Once you identify the pattern, deriving the recurrence becomes much more systematic.

---

# Useful links
- [How To Solve ANY Array Problem](https://leetcode.com/discuss/post/8356889/how-to-solve-any-array-problem-prefix-su-dji5/)
- [How To Solve ANY Two Pointers Problem](https://leetcode.com/discuss/post/8358735/how-to-solve-any-two-pointers-problem-op-7o1r/)
- [How To Solve ANY Trie Problem](https://leetcode.com/discuss/post/8354916/how-to-solve-any-trie-problem-step-by-st-cbvu/)
- [How To Solve ANY Stack Problem](https://leetcode.com/discuss/post/8352898/how-to-solve-any-stack-problem-step-by-s-t0a9/)
- [How To Solve ANY Binary Tree / BST Question](https://leetcode.com/discuss/post/8348175/how-to-solve-any-binary-tree-bst-questio-gvl7/)
- [How To Solve ANY Backtracking Problem](https://leetcode.com/discuss/post/8346110/how-to-solve-any-backtracking-problem-st-bel5/)
- [How To Solve ANY Recursion Problem](https://leetcode.com/discuss/post/8343907/how-to-solve-any-recursion-problem-step-zv3xc/)
- [How To Solve ANY Graph Problem](https://leetcode.com/discuss/post/8339106/how-to-solve-any-graph-problem-step-by-s-cwjm/)
- [How To Solve ANY Sliding Window Problem](https://leetcode.com/discuss/post/8336805/how-to-solve-any-sliding-window-problem-srrx7/)
- [How To Solve ANY Binary Search Problem](https://leetcode.com/discuss/post/8334577/how-to-solve-any-binary-search-problem-s-eb6w/)
- [How To Solve ANY DP Problem](https://leetcode.com/discuss/post/8332921/how-to-solve-any-dp-problem-step-by-step-rwxy/)
- [All LeetCode Patterns That You Need To Know](https://leetcode.com/discuss/post/8330844/all-leetcode-patterns-that-you-need-to-k-smrv/)


<!--
Sliding window/2 pointer
Trees
Linked list
DP


Graph
Heap
Stack
Queue
Array
HashSet/HashMap
-->

---

# Bitwise techniques

- a | b will result in a number >= max(a, b)
- a & b will result in a number <= min(a, b)
- a ^ a = 0
