# Problem list

1. [Bag of Tokens](https://leetcode.com/problems/bag-of-tokens/)
    - [YT Solution](https://www.youtube.com/watch?v=LCx1WzlYgvw&list=PLpIkg8OmuX-J8_n8Vy9P9I3KvyDcPMzRU)
    -  <details>
         <summary>Click to expand code</summary>

		```java
		class Solution {
            public int bagOfTokensScore(int[] tokens, int power) {

                int curPower = power;
                int curScore = 0;
                int maxScore = 0;

                Arrays.sort(tokens);

                int i = 0;
                int j = tokens.length - 1;

                while(i <= j)
                {
                    // Spend the smallest amount of tokens to gain score
                    if(curPower >= tokens[i])
                    {
                        curScore++;
                        curPower -= tokens[i++];
                    }
                    else if(curScore > 0)
                    {
                        // Earn the maximum amount of tokens when spending score
                        curPower += tokens[j--];
                        curScore--;
                    }
                    else break;

                    maxScore = Math.max(maxScore, curScore);
                }

                return maxScore;
            }
        }
		```

       </details>

2. [Boats to Save People](https://leetcode.com/problems/boats-to-save-people/)
    - [YT Solution](https://www.youtube.com/watch?v=UsQzOL6r0HY&list=PLpIkg8OmuX-J8_n8Vy9P9I3KvyDcPMzRU&index=2)
    -  <details>
         <summary>Click to expand code</summary>

		```java
		class Solution {
            public int numRescueBoats(int[] people, int limit) {

                Arrays.sort(people);

                int i = 0;
                int j = people.length - 1;
                int count = 0;

                while(i <= j)
                {
                    if(i == j){
                        count++;
                        break;
                    }

                    if(people[j] + people[i] <= limit)
                    {
                        count++;
                        i++;
                        j--;
                    }
                    else{
                        count++;
                        j--;
                    }
                }

                return count;
            }
        }
		```

       </details>

3. ⭐ [Break a Palindrome](https://leetcode.com/problems/break-a-palindrome/description/)
    - [YT Solution](https://www.youtube.com/watch?v=Pbx0Pvyh7D4&list=PLpIkg8OmuX-J8_n8Vy9P9I3KvyDcPMzRU&index=3)
    -  <details>
         <summary>Click to expand code - Approach-1</summary>

		```java
        /*
            loop runs for = n × 26 × n
            sorting res = n² log n (Sorting n strings of length n costs roughly)
        */
		class Solution {
            int n;

            public String breakPalindrome(String palindrome) {

                n = palindrome.length();
                StringBuilder sb = new StringBuilder(palindrome);

                if(!isPalindrome(sb)) return palindrome;

                List<String> res = new ArrayList<>();

                for(int i = 0; i < n; i++)
                {
                    char orgChar = sb.charAt(i);

                    for(char ch = 'a'; ch <= 'z'; ch++)
                    {
                        if(ch == orgChar) continue;

                        sb.setCharAt(i, ch);

                        if(!isPalindrome(sb))
                        {
                            res.add(sb.toString());
                            break;
                        }
                    }

                    sb.setCharAt(i, orgChar);
                }

                if(res.size() == 0) return "";

                Collections.sort(res);

                return res.get(0);
            }

            boolean isPalindrome(StringBuilder sb)
            {
                int i = 0;
                int j = n - 1;

                while(i < j && sb.charAt(i) == sb.charAt(j))
                {
                    i++;
                    j--;
                }

                return i >= j;
            }
        }
		```

       </details>
    -  <details>
         <summary>Click to expand code - Approach-2 (Best)</summary>

		```java
        /*
            Key observation

            To obtain the lexicographically smallest non-palindrome:

            Change the leftmost non-'a' character in the first half to 'a'.
            If every character in the first half is already 'a', change the last character to 'b'.

            Why only the first half?

            Because changing the second half usually creates a lexicographically larger string than changing its mirrored character in the first half.
        */
		class Solution {
            public String breakPalindrome(String palindrome) {

                int n = palindrome.length();

                if (n == 1)
                    return "";

                char[] s = palindrome.toCharArray();

                for (int i = 0; i < n / 2; i++) {
                    if (s[i] != 'a') {
                        s[i] = 'a';
                        return new String(s);
                    }
                }

                s[n - 1] = 'b';
                return new String(s);
            }
        }
		```

       </details>

4. [Broken Calculator](https://leetcode.com/problems/broken-calculator/description/)
    - [YT Solution](https://www.youtube.com/watch?v=svM2wbyMT4g&list=PLpIkg8OmuX-J8_n8Vy9P9I3KvyDcPMzRU&index=4)
    -  <details>
         <summary>Click to expand code</summary>

		```java
		class Solution {
		}
		```

       </details>

<!--
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
