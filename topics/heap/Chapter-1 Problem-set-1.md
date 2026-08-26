# Problem list

1. ⭐ [Find Median from Data Stream](https://leetcode.com/problems/find-median-from-data-stream/)
    - [YT Solution](https://www.youtube.com/watch?v=jnj87BSi9Is&list=PLpIkg8OmuX-IkxvvfOeZp-Ot0UWHMGAT-)
    -  <details>
         <summary>Click to expand code - Approach-1</summary>

		```java
		class MedianFinder {

            PriorityQueue<Integer> minHeapRight;
            PriorityQueue<Integer> maxHeapLeft;

            public MedianFinder() {
                minHeapRight = new PriorityQueue<>();
                maxHeapLeft = new PriorityQueue<>((a,b) -> b - a);
            }

            public void addNum(int num) {
                // if it is smaller than the top element of maxHeapLeft
                // It should be put in the left heap
                if(maxHeapLeft.isEmpty() || maxHeapLeft.peek() >= num)
                {
                    maxHeapLeft.offer(num);

                    // The idea is to ensure that the difference in heap size will be <= 1
                    while(maxHeapLeft.size() - minHeapRight.size() > 1)
                        minHeapRight.offer(maxHeapLeft.poll());
                }
                else
                {
                    minHeapRight.offer(num);

                    // The idea is to ensure that the difference in heap size will be <= 1
                    while(minHeapRight.size() - maxHeapLeft.size() > 1)
                        maxHeapLeft.offer(minHeapRight.poll());
                }
            }

            public double findMedian() {
                int size = minHeapRight.size() + maxHeapLeft.size();

                double maxHeapPeak =  (double)maxHeapLeft.peek();

                if(size == 1) return maxHeapPeak;

                double minHeapPeak = (double)minHeapRight.peek();

                if((size & 1) == 1)
                    return minHeapRight.size() > maxHeapLeft.size() ? minHeapPeak : maxHeapPeak;

                return (minHeapPeak + maxHeapPeak)/2;
            }
        }

        /**
        * Your MedianFinder object will be instantiated and called as such:
        * MedianFinder obj = new MedianFinder();
        * obj.addNum(num);
        * double param_2 = obj.findMedian();
        */
		```

       </details>

    -  <details>
         <summary>Click to expand code - Approach-2</summary>

		```java
		class MedianFinder {

            private PriorityQueue<Integer> left;   // Max Heap (smaller half)
            private PriorityQueue<Integer> right;  // Min Heap (larger half)

            public MedianFinder() {
                left = new PriorityQueue<>(Comparator.reverseOrder());
                right = new PriorityQueue<>();
            }

            public void addNum(int num) {

                // Step 1: Insert into the appropriate heap
                if (left.isEmpty() || num <= left.peek())
                    left.offer(num);
                else
                    right.offer(num);

                // Step 2: Rebalance sizes
                if (left.size() > right.size() + 1)
                    right.offer(left.poll());
                else if (right.size() > left.size() + 1)
                    left.offer(right.poll());

                // Step 3: Restore ordering invariant if violated
                if (!left.isEmpty() && !right.isEmpty() && left.peek() > right.peek()) {
                    int leftTop = left.poll();
                    int rightTop = right.poll();

                    left.offer(rightTop);
                    right.offer(leftTop);
                }
            }

            public double findMedian() {

                if (left.size() > right.size())
                    return left.peek();

                if (right.size() > left.size())
                    return right.peek();

                return ((double) left.peek() + right.peek()) / 2;
            }
        }
		```

       </details>

2. [Sort Characters By Frequency](https://leetcode.com/problems/sort-characters-by-frequency/)
    - [YT Solution](https://www.youtube.com/watch?v=HwCYa1_2vkU&list=PLpIkg8OmuX-IkxvvfOeZp-Ot0UWHMGAT-&index=2)
    -  <details>
         <summary>Click to expand code</summary>

		```java
		class Solution {
		}
		```

       </details>

3. []()
    - [YT Solution]()
    -  <details>
         <summary>Click to expand code</summary>

		```java
		class Solution {
		}
		```

       </details>
<!--
4. []()
    - [YT Solution]()
    -  <details>
         <summary>Click to expand code</summary>

		```java
		class Solution {
		}
		```

       </details>

5. []()
    - [YT Solution]()
    -  <details>
         <summary>Click to expand code</summary>

		```java
		class Solution {
		}
		```

       </details>

6. []()
    - [YT Solution]()
    -  <details>
         <summary>Click to expand code</summary>

		```java
		class Solution {
		}
		```

       </details>

7. []()
    - [YT Solution]()
    -  <details>
         <summary>Click to expand code</summary>

		```java
		class Solution {
		}
		```

       </details>

8. []()
    - [YT Solution]()
    -  <details>
         <summary>Click to expand code</summary>

		```java
		class Solution {
		}
		```

       </details>

9. []()
    - [YT Solution]()
    -  <details>
         <summary>Click to expand code</summary>

		```java
		class Solution {
		}
		```

       </details>

10. []()
    - [YT Solution]()
    -  <details>
         <summary>Click to expand code</summary>

		```java
		class Solution {
		}
		```

       </details>

11. []()
    - [YT Solution]()
    -  <details>
         <summary>Click to expand code</summary>

		```java
		class Solution {
		}
		```

       </details>

12. []()
    - [YT Solution]()
    -  <details>
         <summary>Click to expand code</summary>

		```java
		class Solution {
		}
		```

       </details>

13. []()
    - [YT Solution]()
    -  <details>
         <summary>Click to expand code</summary>

		```java
		class Solution {
		}
		```

       </details>

14. []()
    - [YT Solution]()
    -  <details>
         <summary>Click to expand code</summary>

		```java
		class Solution {
		}
		```

       </details>


15. []()
    - [YT Solution]()
    -  <details>
         <summary>Click to expand code</summary>

		```java
		class Solution {
		}
		```

       </details>


16. []()
    - [YT Solution]()
    -  <details>
         <summary>Click to expand code</summary>

		```java
		class Solution {
		}
		```

       </details>


17. []()
    - [YT Solution]()
    -  <details>
         <summary>Click to expand code</summary>

		```java
		class Solution {
		}
		```

       </details>


18. []()
    - [YT Solution]()
    -  <details>
         <summary>Click to expand code</summary>

		```java
		class Solution {
		}
		```

       </details>


19. []()
    - [YT Solution]()
    -  <details>
         <summary>Click to expand code</summary>

		```java
		class Solution {
		}
		```

       </details>


20. []()
    - [YT Solution]()
    -  <details>
         <summary>Click to expand code</summary>

		```java
		class Solution {
		}
		```

       </details>
-->

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
