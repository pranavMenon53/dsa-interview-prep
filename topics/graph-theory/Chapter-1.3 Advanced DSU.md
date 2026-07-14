# Weighted Union-Find
Weighted Union-Find (also called **Union-Find with Potentials**, **DSU with Weights**, or **Weighted DSU**) is one of the most useful extensions of the standard DSU.

Unlike normal DSU, which only answers:

> "Are these two nodes in the same component?"

Weighted DSU can also answer:

> "What is the relationship between these two nodes?"

---

# When is it useful?

Suppose you're given equations like

```
a - b = 5
b - c = 3
```

You should be able to answer

```
a - c = 8
```

Or

```
x / y = 2
y / z = 3

=> x / z = 6
```

Or

```
distance(b) - distance(a)
```

Or

```
Relative position
Relative rank
Difference constraints
```

Normal DSU cannot store these relationships.

Weighted DSU can.

---

# Core Idea

Instead of storing only

```
parent[x]
```

we also store

```
weight[x]
```

where

```
weight[x] = relationship between x and parent[x]
```

For additive problems,

```
weight[x] = value(x) - value(parent[x])
```

For multiplicative problems,

```
weight[x] = value(x) / value(parent[x])
```

Everything is stored **relative to the parent**, never globally.

---

# Example

Suppose

```
A - B = 5
```

Choose

```
parent[A] = B
```

Store

```
weight[A] = +5
```

Meaning

```
A = B + 5
```

Now add

```
B - C = 3
```

Store

```
parent[B] = C

weight[B] = 3
```

Graph:

```
A --5--> B --3--> C
```

---

# What does path compression do?

Normally

```
A
 \
  B
   \
    C
```

becomes

```
A
 \
  C
```

But now we must also update the weight.

Originally

```
A -> B = 5
B -> C = 3
```

After compression

```
A -> C = 8
```

So

```
weight[A] += weight[B]
```

This is the key idea.

---

# Find Operation

Normal DSU:

```java
int find(int x) {
    if(parent[x] == x)
        return x;

    parent[x] = find(parent[x]);
    return parent[x];
}
```

Weighted DSU:

```java
int find(int x) {
    if(parent[x] == x)
        return x;

    int p = parent[x];

    parent[x] = find(parent[x]);

    weight[x] += weight[p];

    return parent[x];
}
```

Notice the extra line

```java
weight[x] += weight[p];
```

That accumulates the relationship all the way to the root.

---

# What does weight become?

Suppose

```
A -> B = 5
B -> C = 3
```

Before compression

```
weight[A]=5
weight[B]=3
```

After compression

```
parent[A]=C

weight[A]=8
```

Now every node directly stores

```
value(node)-value(root)
```

---

# Query

Suppose

```
weight[A]=8
weight[D]=2
```

Both have root

```
R
```

Meaning

```
A = R + 8
D = R + 2
```

Then

```
A-D

= (R+8)-(R+2)

=6
```

Formula

```
difference

= weight[A]-weight[D]
```

That's the magic.

---

# Union Operation

Suppose we're told

```
A-B=7
```

Currently

```
A=root1

weight[A]=10

meaning

A=root1+10
```

and

```
B=root2+3
```

Need

```
A-B=7
```

Substitute

```
(root1+10)-(root2+3)=7
```

Simplify

```
root1-root2=0
```

So after attaching one root under the other, we set the connecting edge's weight to preserve this equation.

The exact formula depends on whether your relation is additive, multiplicative, XOR, etc.

---

# Generic Formula (Additive)

Suppose

```
value(u)-value(v)=diff
```

Let

```
ru=find(u)
rv=find(v)

wu=weight[u]
wv=weight[v]
```

where

```
weight[x]

=

value(x)-value(root)
```

Attach

```
ru

under

rv
```

Need

```
value(ru)-value(rv)=?
```

From

```
value(u)=value(ru)+wu
value(v)=value(rv)+wv
```

Given

```
value(u)-value(v)=diff
```

Substitute

```
value(ru)+wu

-

(value(rv)+wv)

=diff
```

Rearrange

```
value(ru)-value(rv)

=

diff-wu+wv
```

Therefore

```java
parent[ru]=rv;

weight[ru]=diff-weight[u]+weight[v];
```

This is the most important union formula for additive constraints.

---

# Complexity

Exactly the same as ordinary DSU.

```
Find

O(α(N))

Union

O(α(N))
```

where

```
α(N)
```

is the inverse Ackermann function, effectively constant for any practical input size.

---

# Common Applications

Weighted DSU appears in problems involving:

* Difference constraints (`a - b = k`)
* Equation evaluation (`a / b = k`)
* Distance between nodes in dynamically merged components
* Relative positions or coordinates
* XOR relationships (`a XOR b = x`)
* Competitive programming problems involving parity or modular differences

---

# Mental Model

Think of every node storing **how far it is from its parent**, not from the root.

```
A --5--> B --3--> C
```

means:

```
A = B + 5
B = C + 3
```

When `find()` compresses the path, those edge weights are accumulated:

```
A --8--> C
```

After compression, every node stores its relationship directly to the root, making future queries and unions efficient while preserving all relative information.

---

# Comparison with Other DSU Variants

| Variant            | Stores                   | Can Answer                                  |
| ------------------ | ------------------------ | ------------------------------------------- |
| Standard DSU       | Parent                   | Are two nodes connected?                    |
| Union by Size/Rank | Parent + size/rank       | Faster unions                               |
| Weighted DSU       | Parent + relative weight | Relative difference/ratio/XOR between nodes |
| Rollback DSU       | Parent history           | Undo unions                                 |
| Persistent DSU     | Versioned parents        | Historical connectivity                     |
| DSU on Tree        | Subtree frequency data   | Offline tree queries                        |

For most "relationship constraint" problems, **Weighted DSU is the standard and most powerful extension** because it augments the classic near-constant-time DSU with the ability to maintain and query relative information within each connected component.
