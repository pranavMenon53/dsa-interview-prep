
# Sliding window

# Templates

## Template-1 (consume, validate, process & increment)
- Most questions can be solved using this pattern.

```java
int func(int[] nums)
{
    int n = nums.length;
    int i = 0, j = 0;
    int res = 0; // res can be initialized with a different value depending on the question

    while(j < n)
    {
       // consume
       intermediateValue += nums[j];

       // validate
       while(intermediateValue is invalid) intermediateValue -= nums[i++];

       //process
       res = min(res, j -i + 1); // it can be min, max, or something else

       // increment
       j++;
    }

    return res;
}
```

## Template-2 (validate, consume, process & increment)
- Most questions can be solved using this pattern.

```java
int func(int[] nums)
{
    int n = nums.length;
    int i = 0, j = 0;
    int res = 0; // res can be initialized with a different value depending on the question

    while(j < n)
    {
       // validate - here we check if the intermediateValue becomes invalid if we consume nums[j]
       // If it does, then we shrink the window
       while((intermediateValue + nums[j]) is invalid) intermediateValue -= nums[i++];

       // consume
       intermediateValue += nums[j];

       //process
       res = min(res, j -i + 1); // it can be min, max, or something else

       // increment
       j++;
    }

    return res;
}
```

# Problem identification

- In sliding window, there are scenarios where the window size is defined in the question.
- The key terms to look at is "subarray" or "substring".
- But, in some cases, we need to define the window size ourselves.
    - Ex - Problem 14
- Useful techniques that are used alongside sliding window
    - Prefix sum
    - Deque - to find min and max element in the window in constant time


# Problem list

1. [Count Occurrences of Anagrams](https://www.geeksforgeeks.org/problems/count-occurences-of-anagrams5839/1)
	- [YT solution](https://www.youtube.com/watch?v=mrUBUWb23hk&list=PLpIkg8OmuX-J2Ivo9YdY7bRDstPPTVGvN)
    -
      <details>
        <summary>Click to expand code</summary>

        ```java
        class Solution {

            char[] pat;
            int n;

            char[] txt;
            int m;

            int search(String p, String t) {

                this.pat = p.toCharArray();
                n = pat.length;

                this.txt = t.toCharArray();
                m = txt.length;

                int[] patCountArr = new int[26];

                for(int i = 0; i < n; i++) patCountArr[pat[i] - 'a']++;


                int i = 0;
                int j = 0;

                // a b c d e
                // a b

                int res = 0;

                while(i <= m - n)
                {
                    patCountArr[txt[j] - 'a']--;

                    if(j - i + 1 == n)
                    {
                        if(isValidAnagram(patCountArr)) res++;

                        patCountArr[txt[i++] - 'a']++;
                    }

                    j++;
                }

                return res;
            }

            boolean isValidAnagram(int[] arr)
            {
                for(int i = 0; i < 26; i++)
                {
                    if(arr[i] != 0) return false;
                }

                return true;
            }
        }
        ```
      </details>


2. [Find All Anagrams in a String](https://leetcode.com/problems/find-all-anagrams-in-a-string/)
	- [YT solution](https://www.youtube.com/watch?v=XxeOHMwBQZU&list=PLpIkg8OmuX-J2Ivo9YdY7bRDstPPTVGvN&index=2)
    -
      <details>
        <summary>Click to expand code</summary>

        ```java
        class Solution {

            char[] str;
            int n;

            char[] pat;
            int m;

            public List<Integer> findAnagrams(String s, String p) {

                str = s.toCharArray();
                n = str.length;

                pat = p.toCharArray();
                m = pat.length;

                int[] patCountArr = new int[26];

                for(int i = 0; i < m; i++) patCountArr[pat[i] - 'a']++;

                int i = 0;
                int j = 0;

                List<Integer> res = new ArrayList<>();

                while(i <= n - m)
                {
                    patCountArr[str[j] - 'a']--;

                    if(j - i + 1 == m)
                    {
                        if(isValidAnagram(patCountArr)) res.add(i);

                        patCountArr[str[i++] - 'a']++;
                    }

                    j++;
                }

                return res;
            }

            boolean isValidAnagram(int[] arr)
            {
                for(int i = 0; i < 26; i++)
                {
                    if(arr[i] != 0) return false;
                }

                return true;
            }
        }
        ```
      </details>


3. [Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/description/)
	- [YT solution](https://www.youtube.com/watch?v=D2MbogiFXWU&list=PLpIkg8OmuX-J2Ivo9YdY7bRDstPPTVGvN&index=3)
    -
      <details>
        <summary>Click to expand code</summary>

        ```java
        class Solution {
            public int minSubArrayLen(int target, int[] nums) {

                int MAX = Integer.MAX_VALUE;
                int sum = 0;
                int i = 0, j = 0;
                int n = nums.length, res = MAX;

                while(j < n)
                {
                    sum += nums[j];

                    while(sum >= target){
                        res = Math.min(res, j - i + 1);
                        sum -= nums[i++];
                    }

                    j++;
                }

                return res == MAX ? 0 : res;
            }
        }
        ```
      </details>


4. ⭐️ [First negative integer in every window of size k](https://www.geeksforgeeks.org/problems/first-negative-integer-in-every-window-of-size-k3345/1)
	- [YT solution](https://www.youtube.com/watch?v=-uc7OCrjp8g&list=PLpIkg8OmuX-J2Ivo9YdY7bRDstPPTVGvN&index=4)
    -
      <details>
        <summary>Click to expand code</summary>

        ```java
        class Solution {
            static List<Integer> firstNegInt(int arr[], int k) {

                Queue<Integer> q = new LinkedList<>();

                int n = arr.length;
                int i = 0, j = 0;

                List<Integer> res = new ArrayList<>();

                while(j < n)
                {
                    if(arr[j] < 0) q.add(j);

                    if(j - i + 1 == k)
                    {
                        if(q.size() == 0) res.add(0);
                        else res.add(arr[q.peek()]);

                        i++;

                        while(!q.isEmpty() && q.peek() < i) q.poll();
                    }

                    j++;
                }

                return res;
            }
        }
        ```
      </details>


5. ⭐️ [Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/description/)
	- [YT solution](https://www.youtube.com/watch?v=3Bp3OVD1EGc&list=PLpIkg8OmuX-J2Ivo9YdY7bRDstPPTVGvN&index=5)
    -
      <details>
        <summary>Click to expand code</summary>

        ```java
        class Solution {
            public String minWindow(String s, String t) {

                char[] str = s.toCharArray();

                int[] srcCountArr = new int[60];
                for(char ch : t.toCharArray()) srcCountArr[ch - 'A']++;

                int i = 0, j = 0, n = str.length;

                int[] destCountArr = new int[60];

                int start = 0, end = 2*n;

                while(j < n)
                {
                    int ind = str[j] - 'A';

                    destCountArr[ind]++;

                    while(isValid(srcCountArr, destCountArr))
                    {
                        if(end - start + 1 > j - i + 1)
                        {
                            start = i;
                            end = j;
                        }

                        ind = str[i] - 'A';
                        destCountArr[ind]--;
                        i++;
                    }

                    j++;
                }

                if(end == 2 * n) return "";

                return s.substring(start, end + 1);
            }

            boolean isValid(int[] src, int[] dest)
            {
                for(int i = 0; i < 60; i++)
                {
                    if(src[i] > dest[i]) return false;
                }

                return true;
            }
        }
        ```
      </details>


6. [Contains Duplicate II](https://leetcode.com/problems/contains-duplicate-ii/)
	- [YT solution](https://www.youtube.com/watch?v=AyiGBwFlMb8&list=PLpIkg8OmuX-J2Ivo9YdY7bRDstPPTVGvN&index=6)
    -
      <details>
        <summary>Click to expand code</summary>

        ```java
        class Solution {
            public boolean containsNearbyDuplicate(int[] nums, int k) {

                Set<Integer> hs = new HashSet<>();

                int i = 0, j = 0;

                while(j < nums.length)
                {
                    while(j - i > k)
                        hs.remove(nums[i++]);

                    if(hs.contains(nums[j])) return true;

                    hs.add(nums[j++]);
                }

                return false;
            }
        }
        ```
      </details>


7. ❌ [Count Subarrays With Fixed Bounds](https://leetcode.com/problems/count-subarrays-with-fixed-bounds/description/)
	- [YT solution](https://www.youtube.com/watch?v=z6LwIkEn9qc&list=PLpIkg8OmuX-J2Ivo9YdY7bRDstPPTVGvN&index=7)
	-
      <details>
        <summary>Click to expand code</summary>

        ```java
        class Solution {
        }
        ```
      </details>


8. [Maximum Number of Vowels in a Substring of Given Length](https://leetcode.com/problems/maximum-number-of-vowels-in-a-substring-of-given-length/description/)
	- [YT solution](https://www.youtube.com/watch?v=CAVnGkDzqAs&list=PLpIkg8OmuX-J2Ivo9YdY7bRDstPPTVGvN&index=8)
    -
      <details>
        <summary>Click to expand code</summary>

        ```java
        class Solution {
            public int maxVowels(String s, int k) {

                char[] str = s.toCharArray();
                int n = str.length;
                int i = 0, j = 0;

                int count = 0;
                int res = 0;

                while(j < n)
                {
                    char ch = str[j];

                    count += (isVowel(ch) ? 1 : 0);

                    if(j - i + 1 == k)
                    {
                        res = Math.max(res, count);

                        ch = str[i++];
                        count += (isVowel(ch) ? -1 : 0);
                    }

                    j++;
                }

                return res;
            }

            boolean isVowel(char ch)
            {
                return ch == 'a' || ch == 'e' || ch == 'i' || ch == 'o' || ch == 'u';
            }
        }
        ```
      </details>


9. [K Radius Subarray Averages](https://leetcode.com/problems/k-radius-subarray-averages/description/)
	- [YT solution](https://www.youtube.com/watch?v=M_YXCATc4ro&list=PLpIkg8OmuX-J2Ivo9YdY7bRDstPPTVGvN&index=9)
    -
      <details>
        <summary>Click to expand code</summary>

        ```java
        class Solution {
            public int[] getAverages(int[] nums, int k) {

                int windowSize = 2 * k + 1;

                int n = nums.length;

                int[] res = new int[n];
                Arrays.fill(res, -1);

                int i = 0, j = 0;

                long sum = 0;

                while(j < n)
                {
                    sum += nums[j];

                    if(j - i + 1 == windowSize)
                    {
                        res[k + i] = (int)(sum / windowSize);

                        sum -= nums[i++];
                    }

                    j++;
                }


                return res;
            }
        }
        ```
      </details>


10. [Longest Subarray of 1's After Deleting One Element](https://leetcode.com/problems/longest-subarray-of-1s-after-deleting-one-element/)
	- [YT solution](https://www.youtube.com/watch?v=SQ8tY9nxeZU&list=PLpIkg8OmuX-J2Ivo9YdY7bRDstPPTVGvN&index=10)
    -
      <details>
        <summary>Click to expand code</summary>

        ```java
        class Solution {
            public int longestSubarray(int[] nums) {

                int res = 0;
                int i = 0, j = 0, zeroCount = 0;
                int n = nums.length;

                while(j < n)
                {
                    zeroCount += (nums[j] == 0 ? 1 : 0);

                    while(zeroCount > 1)
                        zeroCount -= (nums[i++] == 0 ? 1 : 0);

                    res = Math.max(res, j - i );

                    j++;
                }

                return res;
            }
        }
        ```
      </details>


11. [Maximize the Confusion of an Exam](https://leetcode.com/problems/maximize-the-confusion-of-an-exam/description/)
	- [YT solution](https://www.youtube.com/watch?v=vY06L8hZVGI&list=PLpIkg8OmuX-J2Ivo9YdY7bRDstPPTVGvN&index=12)
    -
      <details>
        <summary>Click to expand code</summary>

        ```java
        class Solution {

            char T = 'T';
            char F = 'F';

            public int maxConsecutiveAnswers(String answerKey, int k) {

                char[] arr = answerKey.toCharArray();

                return Math.max(
                    solve(arr, k, T),
                    solve(arr, k, F)
                );
            }

            int solve(char[] arr, int k, char ch) {
                int n = arr.length;

                int i = 0;
                int j = 0;
                int curFlipCount = 0;
                int res = 0;

                while(j < n)
                {
                    if(arr[j] != ch) curFlipCount++;

                    while(curFlipCount > k)
                    {
                        if(arr[i] != ch) curFlipCount--;
                        i++;
                    }

                    res = Math.max(res, j - i + 1);

                    j++;
                }

                return res;
            }


        }
        ```
      </details>
    -
      <details>
        <summary>Click to expand code</summary>

        ```java
        class Solution {
            public int maxConsecutiveAnswers(String answerKey, int k) {
                char[] str = answerKey.toCharArray();
                int n = str.length;
                int falseCount = 0;
                int trueCount = 0;

                int i = 0, j = 0;
                int res = 0;

                while(j < n)
                {
                    if(str[j] == 'T') trueCount++;
                    else falseCount++;

                    while(Math.min(falseCount, trueCount) > k)
                    {
                        if(str[i] == 'T') trueCount--;
                        else falseCount--;
                        i++;
                    }

                    res = Math.max(res, j - i + 1);
                    j++;
                }


                return res;
            }
        }
        ```
      </details>


12. ⭐️ [Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/description/)
	- [YT solution](https://www.youtube.com/watch?v=29OnjVQ-fk4&list=PLpIkg8OmuX-J2Ivo9YdY7bRDstPPTVGvN&index=12)
    -
      <details>
        <summary>Click to expand code</summary>

        ```java
        class Solution {
            /*
                TC - O(NLogN)
                SC - O(N)
            */

            // Number, count
            TreeMap<Integer, Integer> tm;

            public int[] maxSlidingWindow(int[] nums, int k) {

                int n = nums.length;
                int[] res = new int[n - k + 1];

                tm = new TreeMap<>();

                int i = 0;
                int j = 0;

                while(j < n)
                {
                    int count = tm.getOrDefault(nums[j], 0);
                    tm.put(nums[j], count + 1);

                    if(j - i + 1 == k)
                    {
                        res[i] = tm.lastKey();
                        int tempCount = tm.get(nums[i]);

                        if(tempCount == 1) tm.remove(nums[i]);
                        else tm.put(nums[i], tempCount - 1);

                        i++;
                    }


                    j++;
                }

                return res;
            }
        }
        ```
      </details>

    -
      <details>
        <summary>Click to expand code</summary>

        ```java
        class Solution {
            /*
                TC - O(N)
                SC - O(N)
            */
            public int[] maxSlidingWindow(int[] nums, int k) {
                Deque<Integer> dq = new LinkedList<>();
                int n = nums.length;
                int[] res = new int[n - k + 1];
                int i = 0, j = 0;

                while(j < n)
                {
                    int val = nums[j];

                    while(!dq.isEmpty() && val >= nums[dq.peekLast()])
                        dq.pollLast();

                    dq.offerLast(j);

                    if(j - i + 1 == k)
                    {
                        res[i] = nums[dq.peekFirst()];

                        while(!dq.isEmpty() && dq.peekFirst() <= i) dq.pollFirst();

                        i++;
                    }

                    j++;
                }

                return res;
            }
        }
        ```
      </details>

13. ⭐️ [Frequency of the Most Frequent Element](https://leetcode.com/problems/frequency-of-the-most-frequent-element/description/)
	- [YT solution](https://www.youtube.com/watch?v=iOqH_JnXIOQ&list=PLpIkg8OmuX-J2Ivo9YdY7bRDstPPTVGvN&index=13)
    -
      <details>
        <summary>Click to expand code</summary>

        ```java
        class Solution {
            public int maxFrequency(int[] nums, int k) {
                Arrays.sort(nums);

                int n = nums.length;
                int res = 1;
                long sum = 0; // sum of current subarray

                int i = 0, j = 0;

                while(j < n)
                {
                    sum += nums[j];

                    // expectedSum = nums[j] * (j - i + 1);
                    // The idea is to convert all elements to the left 'j' to be equal to nums[j]

                    while((long)(nums[j]) * (j - i + 1) - sum > k)
                        sum -= nums[i++];

                    res = Math.max(res, j - i + 1);
                    j++;
                }

                return res;
            }
        }
        ```
      </details>


14. ⭐⭐⭐ [Count Complete Substrings](https://leetcode.com/problems/count-complete-substrings/description/)
	- [YT solution](https://www.youtube.com/watch?v=ygPMLjxaT2Y&list=PLpIkg8OmuX-J2Ivo9YdY7bRDstPPTVGvN&index=14)
    -
      <details>
        <summary>Click to expand  - Approach-1</summary>

        ```java
        class Solution {
            public int countCompleteSubstrings(String word, int k) {

                // Break the main string into substrings such that no 2 adj characters have a diff > 2
                ArrayList<String> strs = populateStrings(word);

                int res = 0;

                for(String str : strs)
                    res += solve(str, k);

                return res;
            }

            int solve(String str, int k)
            {
                int windowSize = k;
                int n = str.length();

                int res = 0;

                int limit = 26 * k;

                while(windowSize <= n && windowSize <= limit) // runs to a max of 26 * K times
                {
                    int i = 0;
                    int j = 0;
                    int[] countArr = new int[26];

                    while(j < n)
                    {
                        int ind = str.charAt(j) - 'a';
                        countArr[ind]++;

                        if(j - i + 1 == windowSize)
                        {
                            if(validateWindow(countArr, k)) res++;

                            countArr[str.charAt(i++) - 'a']--;
                        }

                        j++;
                    }

                    windowSize += k;
                }

                return res;
            }

            boolean validateWindow(int[] countArr, int k)
            {
                for(int i = 0; i < 26; i++)
                {
                    if(countArr[i] == 0) continue;

                    if(countArr[i] != k) return false;
                }

                return true;
            }

            // Partition the strings such that no adjacent characters have diff > 2
            ArrayList<String> populateStrings(String word)
            {
                ArrayList<String> strs = new ArrayList<>();
                StringBuffer sb = new StringBuffer();
                sb.append(word.charAt(0));

                int n = word.length();
                char prevChar = word.charAt(0);

                for(int i = 1; i < n; i++)
                {
                    char curChar = word.charAt(i);
                    int diff = Math.abs(curChar - prevChar);

                    if(diff > 2)
                    {
                        strs.add(sb.toString());
                        sb = new StringBuffer();
                    }

                    sb.append(curChar);
                    prevChar = curChar;
                }

                if(sb.length() > 0)
                    strs.add(sb.toString());

                return strs;
            }
        }
        ```
      </details>
    -
      <details>
        <summary>Click to expand code - Approach-2</summary>

        ```java
        /*
            Idea is same as apporach-1

            The only optimization here is to identifying if the window has exactly K elements for each distinct characters

            Previously we did it in O(26) - iterating over the count array
            Now, we maintain global variables to do it in O(1)

            Note - although this seems better, the actual runtime differs significantly

            Approach-1 runtime - 147 ms
            Approach-2 runtime - 514 ms
        */
        class Solution {

            int unique;
            int exactlyK;

            public int countCompleteSubstrings(String word, int k) {

                ArrayList<String> strs = populateStrings(word);

                int res = 0;

                for(String str : strs)
                    res += solve(str, k);

                return res;
            }

            int solve(String str, int k)
            {
                int n = str.length();

                int res = 0;

                int distinctCharactersInWindow = 1;

                while(distinctCharactersInWindow <= 26) // we can only have 26 unique characters in the window
                {
                    int windowSize = distinctCharactersInWindow * k;
                    int i = 0;
                    int j = 0;
                    int[] countArr = new int[26];

                    unique = 0; // -> number of unique characters
                    exactlyK = 0; // -> number of unique characters eqaul to K

                    while(j < n)
                    {
                        int ind = str.charAt(j) - 'a';

                        add(countArr, ind, k);

                        if(j - i + 1 == windowSize)
                        {
                            // All unique characters have a count of K
                            if(unique == distinctCharactersInWindow && exactlyK == unique) res++;

                            remove(countArr, str.charAt(i) - 'a', k);

                            i++;
                        }

                        j++;
                    }

                    distinctCharactersInWindow++;
                }

                return res;
            }

            void add(int[] countArr, int ind, int k)
            {
                countArr[ind]++;

                if(countArr[ind] == 1) unique++; // found a unique character

                if(countArr[ind] == k) exactlyK++; // saw this character exactly K times

                // Saw this character more than K times, therefore, need to reduce exactlyK count.
                // Why (k + 1) check? we want to reduce the count only once. If the count increases to K + 2
                // We should not decrease the exactlyK count
                else if (countArr[ind] == k + 1) exactlyK--;
            }

            void remove(int[] countArr, int ind, int k)
            {
                countArr[ind]--;

                if(countArr[ind] == 0) unique--; // Removed a unique character

                if(countArr[ind] == k) exactlyK++; // saw this character exactly K times

                // Saw this character less than K times, therefore, need to reduce exactlyK count.
                // Why (k - 1) check? we want to reduce the count only once.
                // If the count reduces to K - 2 We should not decrease the exactlyK count
                else if (countArr[ind] == k - 1) exactlyK--;
            }

            // Partition the strings such that no adjacent characters have diff > 2
            ArrayList<String> populateStrings(String word)
            {
                ArrayList<String> strs = new ArrayList<>();
                StringBuffer sb = new StringBuffer();
                sb.append(word.charAt(0));

                int n = word.length();
                char prevChar = word.charAt(0);

                for(int i = 1; i < n; i++)
                {
                    char curChar = word.charAt(i);
                    int diff = Math.abs(curChar - prevChar);

                    if(diff > 2)
                    {
                        strs.add(sb.toString());
                        sb = new StringBuffer();
                    }

                    sb.append(curChar);
                    prevChar = curChar;
                }

                if(sb.length() > 0)
                    strs.add(sb.toString());

                return strs;
            }
        }
        ```
      </details>

15. [Binary Subarrays With Sum](https://leetcode.com/problems/binary-subarrays-with-sum/description/)
	- [YT solution](https://www.youtube.com/watch?v=5Quv9nnZs34&list=PLpIkg8OmuX-J2Ivo9YdY7bRDstPPTVGvN&index=15)
    -
      <details>
        <summary>Click to expand code - Approach-1</summary>

        ```java
        class Solution {
            public int numSubarraysWithSum(int[] nums, int goal) {

                // Appraoch-1 - for every (i,j) find sum - n ** 3

                // Approach-2 - built on approach-1, here we calculate the running sum - n ** 2

                // Approach-3 - calculate sum for each window size - k * n -> here, k == n so TC = n ** 2

                // Approach-4 - use prefix sum

                /*
                    nums = [1,0,1,0,1], goal = 2
                    nums arr =.      [1,0,1,0,1]
                    prefix sum arr = [1,1,2,2,3]

                    now, iterate over the prefix sum arr.

                    For each index
                    {
                        if(prefix[ind] == goal) res++;
                        if(prefix[ind] - goal on the left) then res += count of(prefix[ind] - goal)
                    }

                    return res;
                */

                int n = nums.length;
                int[] prefix = new int[n];

                int prev = 0;
                for(int i = 0; i < n; i++)
                {
                    prefix[i] = prev + nums[i];
                    prev = prefix[i];
                }

                int res = 0;

                // sum -> count of sum so far

                HashMap<Integer, Integer> hm = new HashMap<>();
                hm.put(0, 1);

                for(int i = 0; i < n; i++)
                {
                    int findSumOnLeft = prefix[i] - goal;

                    res += hm.getOrDefault(findSumOnLeft, 0);

                    hm.put(prefix[i], hm.getOrDefault(prefix[i], 0) + 1);
                }

                return res;
            }
        }
        ```
      </details>

    -
      <details>
        <summary>Click to expand - Approach-2</summary>

        ```java
        class Solution {
            /*
                Same idea as approach-1, but without using prefix sum array
            */
            public int numSubarraysWithSum(int[] nums, int goal) {

                int n = nums.length;

                // sum, count
                HashMap<Integer, Integer> hm = new HashMap<>();
                int res = 0;
                int runningSum = 0;

                hm.put(0, 1);

                for(int i = 0; i < n; i++)
                {
                    runningSum += nums[i];

                    int sumToFindOnLeft = runningSum - goal;

                    res += hm.getOrDefault(sumToFindOnLeft, 0);

                    int count = hm.getOrDefault(runningSum, 0);

                    hm.put(runningSum, count + 1);
                }

                return res;
            }
        }
        ```
      </details>

16. ⭐ [Subarray Product Less Than K](https://leetcode.com/problems/subarray-product-less-than-k/)
    - [YT Solution](https://www.youtube.com/watch?v=9fmKB1F1pEE&list=PLpIkg8OmuX-J2Ivo9YdY7bRDstPPTVGvN&index=16)
    - What's important here is that the trick to calculate the number of valid subarrays
    - Here, the idea is that the 'j' th index will be the end of the subarray
    - Count of valid subarrays ending at J and starting at `i, i + 1, ... j-1, j` => `(j - i + 1)`
    -
      <details>
        <summary>Click to expand code</summary>

        ```java
        class Solution {
            public int numSubarrayProductLessThanK(int[] nums, int k) {

                if(k <= 1) return 0;

                int i = 0;
                int j = 0;
                int prod = 1;
                int res = 0;
                int n = nums.length;

                while(j < n)
                {
                    prod *= nums[j];

                    while(prod >= k) prod /= nums[i++];

                    // Why (j - 1 + 1)? This gives the number of subarrays
                    // ending at J starting from i, i + 1, i + 2 ... j - 1, j
                    res += (j - i + 1);

                    j++;
                }

                return res;
            }
        }
        ```
      </details>

17. ⭐ [Length of Longest Subarray With at Most K Frequency](https://leetcode.com/problems/length-of-longest-subarray-with-at-most-k-frequency/)
    - [YT Solution](https://www.youtube.com/watch?v=txSMzRMREKA&list=PLpIkg8OmuX-J2Ivo9YdY7bRDstPPTVGvN&index=17)
    -
      <details>
        <summary>Click to expand code</summary>

        ```java
        // Solution-1
        class Solution {
            public int maxSubarrayLength(int[] nums, int k) {

                // Number, freq
                Map<Integer, Integer> hm = new HashMap<>();
                int n = nums.length;
                int i = 0, j = 0, res = 0;

                while(j < n)
                {

                    int count = hm.getOrDefault(nums[j], 0);
                    hm.put(nums[j], count + 1);

                    while(hm.getOrDefault(nums[j], 0) > k)
                    {
                        count = hm.get(nums[i]);
                        if(count == 1) hm.remove(nums[i]);
                        else hm.put(nums[i], count - 1);
                        i++;
                    }

                    res = Math.max(res, j - i + 1);
                    j++;
                }

                return res;
            }
        }
        ```
      </details>


18. ⭐ [Count Subarrays Where Max Element Appears at Least K Times](https://leetcode.com/problems/count-subarrays-where-max-element-appears-at-least-k-times/)
    - [YT Solution](https://www.youtube.com/watch?v=06VaWkj8e-0&list=PLpIkg8OmuX-J2Ivo9YdY7bRDstPPTVGvN&index=18)
    -
      <details>
        <summary>Click to expand code</summary>

        ```java
        class Solution {
            public long countSubarrays(int[] nums, int k) {

                int max = -1;
                for(int e : nums) max = Math.max(max, e);

                int i = 0;
                int j = 0;

                int n = nums.length;
                List<Integer> maxElementIndexes = new ArrayList<>();
                long res = 0;

                while(j < n)
                {
                    if(nums[j] == max) maxElementIndexes.add(j);

                    int curLength = maxElementIndexes.size();

                    // Now, find the number of sub arrays that can end at J
                    if(curLength >= k)
                        res += maxElementIndexes.get(curLength-k) + 1;

                    // Why maxElementIndexes.get(curLength - k) + 1 ?
                    //
                    // Let p = maxElementIndexes.get(curLength - k).
                    //
                    // p is the earliest occurrence among the last k occurrences of the
                    // maximum element seen so far.
                    //
                    // Any subarray ending at j must start at or before p to include
                    // these k occurrences of the maximum.
                    //
                    // Valid starts are: 0, 1, 2, ..., p
                    //
                    // Number of valid starts = p + 1
                    //
                    // Therefore, the number of valid subarrays ending at j is p + 1.

                    j++;
                }

                return res;
            }
        }
        ```
      </details>

    -
      <details>
        <summary>Click to expand code</summary>

        ```java
        class Solution {
            public long countSubarrays(int[] nums, int k) {

                int max = -1;
                for(int e : nums) max = Math.max(max, e);

                int i = 0;
                int j = 0;

                /*
                    How is this Queue based solution better?

                    The space complexity is reduced to O(K) instead of O(n)
                */

                int n = nums.length;
                Queue<Integer> q = new LinkedList<>();
                long res = 0;

                while(j < n)
                {
                    if(nums[j] == max) q.offer(j);

                    while(q.size() > k) q.poll();

                    if(q.size() == k)
                        res += q.peek() + 1;

                    j++;
                }

                return res;
            }
        }
        ```
      </details>

    -
      <details>
        <summary>Click to expand code</summary>

        ```java
        class Solution {
            public long countSubarrays(int[] nums, int k) {

                int n = nums.length;

                int max = -1;
                for(int e : nums) max = Math.max(max, e);

                int i = 0;
                int j = 0;

                int maxElementCount = 0;
                long res = 0;

                while(j < n)
                {
                    if(nums[j] == max) maxElementCount++;

                    while(maxElementCount == k)
                    {
                        // endings j, j + 1... n-1 are now valid
                        res += (n - j);

                        if(nums[i] == max) maxElementCount--;

                        i++;
                    }

                    j++;
                }

                return res;
            }
        }
        ```
      </details>

19. ❌ [Subarrays with K Different Integers]()
    - [YT Solution - 1](https://www.youtube.com/watch?v=uJJSGxfzix8&list=PLpIkg8OmuX-J2Ivo9YdY7bRDstPPTVGvN&index=19)
    - [YT Solution - 2](https://www.youtube.com/watch?v=0Kmbzm5nKqw&list=PLpIkg8OmuX-J2Ivo9YdY7bRDstPPTVGvN&index=20)
    -
      <details>
        <summary>Click to expand code</summary>

        ```java
        class Solution {
        }
        ```
      </details>


20. [Get Equal Substrings Within Budget](https://leetcode.com/problems/get-equal-substrings-within-budget/description/)
    - [YT Solution](https://www.youtube.com/watch?v=MF2MgJQuFhA&list=PLpIkg8OmuX-J2Ivo9YdY7bRDstPPTVGvN&index=21)
    -
      <details>
        <summary>Click to expand code</summary>

        ```java
        class Solution {
            public int equalSubstring(String s, String t, int maxCost) {

                char[] str = s.toCharArray();
                char[] txt = t.toCharArray();

                int i = 0, j = 0, res = 0;

                int costSoFar = 0;
                int n = str.length;

                while(j < n)
                {
                    int cost = Math.abs(str[j] - txt[j]);

                    while(costSoFar + cost > maxCost)
                    {
                        int oldCost = Math.abs(str[i] - txt[i]);
                        costSoFar -= oldCost;
                        i++;
                    }

                    costSoFar += cost;
                    res = Math.max(res, j - i + 1);
                    j++;
                }

                return res;
            }
        }
        ```
      </details>


21. ❌ [Find Subarray With Bitwise AND Closest to K](https://leetcode.com/problems/find-subarray-with-bitwise-or-closest-to-k/description/)
    - [YT Solution](https://www.youtube.com/watch?v=BWBKtU8Euno&list=PLpIkg8OmuX-J2Ivo9YdY7bRDstPPTVGvN&index=22)
    -
      <details>
        <summary>Click to expand code</summary>

        ```java
        class Solution {
        }
        ```
      </details>


22. ⭐ [Grumpy Bookstore Owner](https://leetcode.com/problems/grumpy-bookstore-owner/description/)
    - [YT Solution](https://www.youtube.com/watch?v=kCxCE0_66vM&list=PLpIkg8OmuX-J2Ivo9YdY7bRDstPPTVGvN&index=23)
    - This problem is **not complicated**, however, the optimization from solution-1 to solution-2 is interesting.
        - Solution-1 comes naturally, but on futher observation, it becomes clear on how we can space optimize it to solution-2
    - There are multiple approaches to this problem
    -
      <details>
        <summary>Click to expand code</summary>

        ```java
        // Solution-1
        class Solution {
            public int maxSatisfied(int[] customers, int[] grumpy, int minutes) {

                int n = customers.length;

                int[] prefix = new int[n];
                prefix[0] = grumpy[0] == 1 ? 0 : customers[0];

                for(int i = 1; i < n; i++)
                    prefix[i] = prefix[i - 1] + (grumpy[i] == 1 ? 0 : customers[i]);

                int i = 0;
                int j = 0;
                int k = minutes;
                int res = 0; // max number of satisfied customers

                int curWindowCustomers = 0;

                while(j < n)
                {
                    curWindowCustomers += customers[j];

                    if(j - i + 1 == k)
                    {
                        int leftCount = (i - 1 >= 0) ? prefix[i - 1] : 0;
                        int rightCount = prefix[n - 1] - prefix[j];

                        res = Math.max(res, curWindowCustomers + leftCount + rightCount);

                        curWindowCustomers -= customers[i++];
                    }

                    j++;
                }

                return res;
            }
        }
        ```
      </details>

    -
      <details>
        <summary>Click to expand code</summary>

        ```java
        // Solution-2 (space optimized solution-1)
        class Solution {
            public int maxSatisfied(int[] customers, int[] grumpy, int minutes) {

                int n = customers.length;

                int baseSatisfiedCustomers = 0;

                for(int i = 0; i < n; i++)
                baseSatisfiedCustomers = baseSatisfiedCustomers + (grumpy[i] == 1 ? 0 : customers[i]);

                int i = 0;
                int j = 0;
                int k = minutes;
                int res = baseSatisfiedCustomers; // max number of satisfied customers

                int curWindowCustomers = 0;

                while(j < n)
                {
                    curWindowCustomers += (grumpy[j] == 1 ? customers[j] : 0);

                    if(j - i + 1 == k)
                    {
                        res = Math.max(res, curWindowCustomers + baseSatisfiedCustomers);
                        curWindowCustomers -= (grumpy[i] == 1 ? customers[i] : 0);
                        i++;
                    }

                    j++;
                }

                return res;
            }
        }
        ```
      </details>

23. ❌ [Longest Continuous Subarray With Absolute Diff Less Than or Equal to Limit](https://leetcode.com/problems/longest-continuous-subarray-with-absolute-diff-less-than-or-equal-to-limit/)
    - [YT Solution](https://www.youtube.com/watch?v=xZDbcGB2PQs&list=PLpIkg8OmuX-J2Ivo9YdY7bRDstPPTVGvN&index=24)

24. [Minimum Swaps to Group All 1's Together II]()
    - [YT Solution](https://www.youtube.com/watch?v=t82KJaI1kNQ&list=PLpIkg8OmuX-J2Ivo9YdY7bRDstPPTVGvN&index=25)
    - The key idea here is to find the window size, which would be equal to the number of 1's in the array
    -
      <details>
        <summary>Click to expand code</summary>

        ```java
        class Solution {
            public int minSwaps(int[] nums) {

                int oneCount = 0;

                for(int e : nums) oneCount += e;

                if(oneCount == 0) return 0;

                int n = nums.length;

                int i = 0, j = 0, res = Integer.MAX_VALUE;

                int onesCountInCurWindow = 0;
                int windowSize = oneCount;

                while(i < n)
                {
                    onesCountInCurWindow += nums[j % n];

                    if(j - i + 1 == windowSize)
                    {
                        res = Math.min(res, oneCount - onesCountInCurWindow);
                        onesCountInCurWindow -= nums[i++];
                    }

                    j++;
                }

                return res;
            }
        }
        ```
      </details>

25. [Count Substrings That Satisfy K-Constraint I](https://leetcode.com/problems/count-substrings-that-satisfy-k-constraint-i/)
    - [YT Solution](https://www.youtube.com/watch?v=2d1ALG8wwDc&list=PLpIkg8OmuX-J2Ivo9YdY7bRDstPPTVGvN&index=26)
    -
      <details>
        <summary>Click to expand code</summary>

        ```java
        class Solution {
            public int countKConstraintSubstrings(String s, int k) {

                int res = 0;
                int n = s.length();
                int i = 0, j = 0;
                int oneCount = 0;
                int zeroCount = 0;

                while(j < n)
                {
                    int val = s.charAt(j) - '0';

                    if(val == 0) zeroCount++;
                    else oneCount++;

                    while(oneCount > k && zeroCount > k)
                    {
                        val = s.charAt(i) - '0';

                        if(val == 0) zeroCount--;
                        else oneCount--;

                        i++;
                    }

                    res += (j - i + 1);

                    j++;
                }

                return res;
            }
        }
        ```
      </details>

26. ❌ [Count Substrings That Satisfy K-Constraint II](https://leetcode.com/problems/count-substrings-that-satisfy-k-constraint-ii/description/)
    - [YT Solution](https://youtu.be/2d1ALG8wwDc?si=D_9bmjYzROhZnFij&t=1415)

27. [Permutation in String](https://leetcode.com/problems/permutation-in-string/)
    - [YT Solution](https://www.youtube.com/watch?v=iTwwvsyUsi4&list=PLpIkg8OmuX-J2Ivo9YdY7bRDstPPTVGvN&index=27)
    -
      <details>
        <summary>Click to expand code</summary>

        ```java
        // Solution - 1
        class Solution {
            public boolean checkInclusion(String s1, String s2) {
                // return s2.contains(a permutation of s1)

                int[] sourceCountArray = new int[26];

                for(char ch : s1.toCharArray())
                {
                    int ind = ch - 'a';
                    sourceCountArray[ind]++;
                }

                int[] destCountArray = new int[26];
                int k = s1.length() - 1;
                int n = s2.length();

                for(int i = 0; i < n; i++)
                {
                    int ind = s2.charAt(i) - 'a';
                    destCountArray[ind]++;

                    if(i >= k )
                    {
                        if(checkIfCountIsSame(sourceCountArray, destCountArray))
                            return true;

                        int prevInd = s2.charAt(i - k) - 'a';
                        destCountArray[prevInd]--;
                    }
                }

                return false;
            }

            boolean checkIfCountIsSame(int[] a, int[] b)
            {
                for(int i = 0; i < 26; i++)
                {
                    if(a[i] != b[i]) return false;
                }

                return true;
            }
        }
        ```
      </details>

28. ⭐ [Find the Power of K-Size Subarrays I](https://leetcode.com/problems/find-the-power-of-k-size-subarrays-i/description/)
    - [YT Solution](https://www.youtube.com/watch?v=P1_yXMhqC50&list=PLpIkg8OmuX-J2Ivo9YdY7bRDstPPTVGvN&index=28)
    -
      <details>
        <summary>Click to expand code - Approach-1</summary>

        ```java
        // My Approach-1
        class Solution {
            public int[] resultsArray(int[] nums, int k) {

                /*
                    Approach-1: Sliding window + tree set

                    set prev = -1; // 1 <= nums[i] <= 10 ** 5
                    standard sliding window, consume each element and put it in a tree set.
                    but before consuming, check if prev + 1 == nums[j]
                        - If yes, then the subarray is valid so far, put it inside set
                        - if not, then there can't be any valid sub array from [i..j], increment both and continue (don't forget to initialize prev = -1)
                    if (j - i + 1 == k), then the window is complete, pull the first element from the set

                    TC - nlog(k)
                    SC - k
                */

                int n = nums.length;
                TreeSet<Integer> ts = new TreeSet<>();

                int i = 0, j = 0, prev = -1;

                int[] res = new int[n - k + 1];
                Arrays.fill(res, -1);

                while(j < n)
                {
                    int curElement = nums[j];
                    // check if I can consume this element
                    if(prev == -1 || prev + 1 == curElement)
                    {
                        // cur sub array is valid
                        ts.add(curElement);
                        prev = curElement;

                        if(j - i + 1 == k)
                        {
                            res[i] = ts.getLast();
                            ts.remove(nums[i++]);
                        }

                        if(i > j) prev = -1; // Why i > j? for K = 1,  we need to reset the previous each time

                        j++;
                    }
                    else{
                        // cur sub array [i..j] is invalid
                        // Start again from the current element
                        i = j; // j is the new starting point
                        j++;
                        prev = curElement;
                        ts.clear();
                        ts.add(curElement);
                    }
                }

                return res;
            }
        }
        ```
      </details>

    -
      <details>
        <summary>Click to expand code - Approach-2</summary>

        ```java
        // My Approach-2
        class Solution {
            public int[] resultsArray(int[] nums, int k) {

                /*
                    Approach-2: Optimized approach-1

                    The core idea is still the same, what has changes is the usage of TreeSet
                    We don't need a TreeSet because if a subarray is valid, the the current element will always be the largest

                    TC - n
                    SC - constant
                */

                int n = nums.length;

                int i = 0, j = 0, prev = -1;

                int[] res = new int[n - k + 1];
                Arrays.fill(res, -1);

                while(j < n)
                {
                    int curElement = nums[j];
                    // check if I can consume this element
                    if(prev == -1 || prev + 1 == curElement)
                    {
                        // cur sub array is valid
                        prev = curElement;

                        if(j - i + 1 == k)
                        {
                            res[i] = curElement;
                            i++;
                        }

                        if(i > j) prev = -1; // Why i > j? for K = 1,  we need to reset the previous each time

                        j++;
                    }
                    else{
                        // cur subarray [i..j] is invalid;
                        // Start again from the current element
                        i = j; // j is the new starting point
                        j++;
                        prev = curElement;
                    }
                }

                return res;
            }
        }
        ```
      </details>
    -
      <details>
        <summary>Click to expand code - Approach-3</summary>

        ```java
        // Clearner revision of approach-2
        class Solution {
            public int[] resultsArray(int[] nums, int k) {

                int n = nums.length;
                int[] res = new int[n - k + 1];
                Arrays.fill(res, -1);

                int runLen = 1; // length of consecutive +1 sequence

                for (int j = 0; j < n; j++) {

                    if (j > 0 && nums[j] == nums[j - 1] + 1) {
                        runLen++;
                    } else {
                        runLen = 1;
                    }

                    // when we have a valid window of size k ending at j
                    if (runLen >= k) {
                        res[j - k + 1] = nums[j];
                    }
                }

                return res;
            }
        }
        ```
      </details>
    -
      <details>
        <summary>Click to expand code - Approach-4 (best)</summary>

        ```java
        // Clearner revision of approach-2, 3
        class Solution {
            public int[] resultsArray(int[] nums, int k) {

                int n = nums.length;
                int[] res = new int[n - k + 1];
                int i = 0, j = 0;

                Arrays.fill(res, -1);

                while(j < n)
                {
                    /*
                        Once we know the subarray isn't consecutive, no point in continuing
                        However, the current node 'J' can be part of the answer
                        Therefore, we set the new starting point by doing i = j;
                    */
                    if(j - 1 >= 0 && nums[j] != (nums[j - 1] + 1))
                    {
                        i = j;
                    }

                    if(j - i + 1 == k)
                    {
                        res[i] = nums[j];
                        i++;
                    }

                    j++;
                }

                return res;
            }
        }
        ```
      </details>

    - There could be one more solution using a **monotonic queue**. But since `nums[j]` will always be the largest element, it is not needed. It would result in a similar TC - O(n), SC - O(n)
        - [YT Solution - 2](https://www.youtube.com/watch?v=7xkCA80h5a4&list=PLpIkg8OmuX-J2Ivo9YdY7bRDstPPTVGvN&index=29)

29. ❌ [Shortest Subarray with Sum at Least K](https://leetcode.com/problems/shortest-subarray-with-sum-at-least-k/)
    - [YT Solution](https://www.youtube.com/watch?v=Z4tH40wH6JA&list=PLpIkg8OmuX-J2Ivo9YdY7bRDstPPTVGvN&index=30)
    - Related problem - [Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/)

30. [Maximum Sum of Distinct Subarrays With Length K](https://leetcode.com/problems/maximum-sum-of-distinct-subarrays-with-length-k/description/)
    - [YT Solution](https://www.youtube.com/watch?v=X1LgOR-_pJE&list=PLpIkg8OmuX-J2Ivo9YdY7bRDstPPTVGvN&index=31)

    -
      <details>
        <summary>Click to expand code</summary>

        ```java
        // Approach-1: Using hash map
        class Solution {
            public long maximumSubarraySum(int[] nums, int k) {

                // number, count
                Map<Integer, Integer> hm = new HashMap<>();

                int i = 0, j = 0, n = nums.length;
                long res = 0, curSum = 0;

                while(j < n)
                {
                    curSum += nums[j];
                    int count = 1 + hm.getOrDefault(nums[j], 0);
                    hm.put(nums[j], count);

                    if(j - i + 1 == k)
                    {
                        if(hm.size() == k)
                            res = Math.max(res, curSum);

                        count = hm.get(nums[i]);
                        if(count == 1) hm.remove(nums[i]);
                        else hm.put(nums[i], count - 1);

                        curSum -= nums[i++];
                    }

                    j++;
                }

                return res;
            }
        }
        ```
      </details>
    -
      <details>
        <summary>Click to expand code</summary>

        ```java
        // Approach-2: Using hash set
        class Solution {
            public long maximumSubarraySum(int[] nums, int k) {

                HashSet<Integer> hs = new HashSet<>();

                int i = 0, j = 0, n = nums.length;
                long res = 0, curSum = 0;

                while(j < n)
                {
                    curSum += nums[j];

                    while(hs.contains(nums[j])){
                        curSum -= nums[i];
                        hs.remove(nums[i++]);
                    }

                    hs.add(nums[j]);

                    if(j - i + 1 == k)
                    {
                        res = Math.max(res, curSum);
                        curSum -= nums[i];
                        hs.remove(nums[i++]);
                    }

                    j++;
                }

                return res;
            }
        }
        ```
      </details>

31. ⭐ [Take K of Each Character From Left and Right](https://leetcode.com/problems/take-k-of-each-character-from-left-and-right/description/)
    - [YT Solution](https://www.youtube.com/watch?v=s4nRUC1SDDA&list=PLpIkg8OmuX-J2Ivo9YdY7bRDstPPTVGvN&index=32)

    -
      <details>
        <summary>Click to expand code</summary>

        ```java
        class Solution {

            int MAX = Integer.MAX_VALUE;
            char[] str;
            int[] count;
            int k;
            int n;

            public int takeCharacters(String s, int K) {
                /*

                    We can only remove from the right or left most end
                    Possible combinations for valid answers - (X indicates removal)
                        - [X,X,X,a,b,c] - remove from only left
                        - [a,b,c,X,X,X] - remove from only right
                        - [X,X,X,a,b,c,X,X,X] - remove from both ends
                    Notice a pattern here, if we simply find the larget subarray we can delete while ensuring that on removal,
                    the count od each character is >= k, the n - largestLength will be our answer

                    Approach-1: Using binary search to find the largest window we can delete
                */

                if(K == 0) return 0;

                count = new int[3];
                str = s.toCharArray();
                k = K;
                n = str.length;

                for(char ch : str) count[ch - 'a']++;

                for(int i = 0; i < 3; i++)
                {
                    if(count[i] < k) return -1;
                }

                int largestSubArray = findLargestRemovableSubArray(); // largest sub array we can delete

                return n - largestSubArray;
            }

            int findLargestRemovableSubArray()
            {
                int low = 1; // remove at least one character
                int high = n - 3 * k; // at max, we can remove n - 3 * k characters. Why? because all 3 (a,b,c) characters need a frequency of k or more
                int res = MAX;

                while(low <= high)
                {
                    int mid = low + (high - low)/2;

                    if(isValid(mid))
                    {
                        res = mid;
                        low = mid + 1;
                    }
                    else high = mid - 1;
                }

                return res == MAX ? 0 : res;
            }

            boolean isValid(int windowSize)
            {
                int i = 0, j = 0;
                int[] tempCount = new int[3];
                tempCount[0] = count[0];
                tempCount[1] = count[1];
                tempCount[2] = count[2];

                while(j < n)
                {
                    int ind = str[j] - 'a';
                    tempCount[ind]--;

                    if(j - i + 1 == windowSize)
                    {
                        boolean isValidRemoval = true;
                        for(int p = 0; p < 3; p++)
                            isValidRemoval = isValidRemoval && tempCount[p] >= k;

                        if(isValidRemoval)
                            return true;

                        tempCount[str[i] - 'a']++;
                        i++;
                    }

                    j++;
                }

                return false;
            }
        }
        ```
      </details>

    -
      <details>
        <summary>Click to expand code</summary>

        ```java
        /*
            We can only remove from the right or left most end
            Possible combinations for valid answers - (X indicates removal)
                - [X,X,X,a,b,c] - remove from only left
                - [a,b,c,X,X,X] - remove from only right
                - [X,X,X,a,b,c,X,X,X] - remove from both ends
            Notice a pattern here, if we simply find the larget subarray we can delete while ensuring that on removal,
            the count od each character is >= k, the n - largestLength will be our answer

            Approach-2: Sliding window
        */
        class Solution {
            public int takeCharacters(String s, int k) {

                int[] count = new int[3];

                char[] str = s.toCharArray();

                for(char ch : str) count[ch - 'a']++;

                // If we can't get a count of 'K' (at least) for each character, return -1
                for(int i = 0; i < 3; i++)
                {
                    if(count[i] < k) return -1;
                }

                int largestSubArray = 0; // largest sub array we can delete

                int i = 0, j = 0;

                int n = str.length;

                while(j < n)
                {
                    int ind = str[j] - 'a';
                    count[ind]--;

                    while(count[ind] < k)
                        count[str[i++] - 'a']++;

                    largestSubArray = Math.max(largestSubArray, j - i + 1);

                    j++;
                }

                return n - largestSubArray;
            }
        }
        ```
      </details>

32. ⭐ [Continuous Subarrays](https://leetcode.com/problems/continuous-subarrays/description/)
    - [YT Solution](https://www.youtube.com/watch?v=SWyGD8w_85E&list=PLpIkg8OmuX-J2Ivo9YdY7bRDstPPTVGvN&index=33)

    -
      <details>
        <summary>Click to expand code</summary>

        ```java
        class Solution {
            public long continuousSubarrays(int[] nums) {

                /*
                    Approach-1: Use TreeMap to get the max and the min of the current subarray

                    Time Complexity:
                        - TreeMap contains at most 3 distinct keys because => max(window) - min(window) <= 2.
                        - Therefore each TreeMap operation is O(log 3) = O(1).
                        - Each element is inserted and removed at most once.

                    Overall: O(n)

                    Space Complexity:
                        - TreeMap stores frequencies of at most 3 distinct values.

                    Overall: O(1)
                */

                // Integer, count
                TreeMap<Integer, Integer> tm = new TreeMap<>();

                int i = 0, j = 0, n = nums.length;
                long res = 0;

                while(j < n)
                {
                    int val = nums[j];
                    int count = 1 + tm.getOrDefault(val, 0);
                    tm.put(val, count);

                    while(tm.lastKey() - tm.firstKey() > 2)
                    {
                        count = tm.get(nums[i]);
                        if(count == 1) tm.remove(nums[i]);
                        else tm.put(nums[i], count - 1);
                        i++;
                    }

                    res += (j - i + 1);

                    j++;
                }

                return res;
            }
        }
        ```
      </details>

    -
      <details>
        <summary>Click to expand code</summary>

        ```java
        class Solution {
            public long continuousSubarrays(int[] nums) {

                /*
                    Approach-2: Using monotonic Deque

                    We maintain a sliding window [i, j] such that:
                    max(window) - min(window) <= 2

                    maxQ is a decreasing deque → front gives maximum
                    minQ is an increasing deque → front gives minimum

                    Each element enters and leaves both deques at most once,
                    so all operations are amortized O(1).

                    Time Complexity: O(n)
                    Space Complexity: O(n) (deque stores at most all indices in worst case)
                */

                Deque<Integer> minQ = new LinkedList<>();
                Deque<Integer> maxQ = new LinkedList<>();

                int i = 0, j = 0, n = nums.length;
                long res = 0;

                while(j < n)
                {
                    int val = nums[j];

                    // add val to maxQ
                    // Delete all the elements which are <= val because they can never be the answer for the current window
                    while(maxQ.size() > 0 && nums[maxQ.peekLast()] <= val)
                        maxQ.pollLast();

                    maxQ.offerLast(j);

                    // add val to minQ
                    // Delete all the elements which are >= val because they can never be the answer for the current window
                    while(minQ.size() > 0 && nums[minQ.peekLast()] >= val)
                        minQ.pollLast();

                    minQ.offerLast(j);

                    while(nums[maxQ.peekFirst()] - nums[minQ.peekFirst()] > 2)
                    {
                        i++;
                        while(maxQ.peekFirst() < i) maxQ.pollFirst();
                        while(minQ.peekFirst() < i) minQ.pollFirst();
                    }

                    res += (j - i + 1);
                    j++;
                }

                return res;
            }
        }
        ```
      </details>

    -
      <details>
        <summary>Click to expand code</summary>

        ```java
        /*
            Approach-3: Using Heaps to get min and max elements
        */
        class Solution {
            public long continuousSubarrays(int[] nums) {
                int n = nums.length;

                // Min-heap for smallest elements
                PriorityQueue<int[]> minHeap = new PriorityQueue<>((a, b) -> Integer.compare(a[0], b[0]));
                // Max-heap for largest elements
                PriorityQueue<int[]> maxHeap = new PriorityQueue<>((a, b) -> Integer.compare(b[0], a[0]));

                int i = 0, j = 0;
                long count = 0;

                while (j < n) {
                    // Add the current element to both heaps
                    minHeap.offer(new int[]{nums[j], j});
                    maxHeap.offer(new int[]{nums[j], j});

                    // Maintain the condition that the difference between max and min <= 2
                    while (Math.abs(maxHeap.peek()[0] - minHeap.peek()[0]) > 2) {
                        i++;

                        // Remove elements outside the current window from the maxHeap
                        while (!maxHeap.isEmpty() && maxHeap.peek()[1] < i) {
                            maxHeap.poll();
                        }

                        // Remove elements outside the current window from the minHeap
                        while (!minHeap.isEmpty() && minHeap.peek()[1] < i) {
                            minHeap.poll();
                        }
                    }

                    // Add the number of valid subarrays ending at index j
                    count += j - i + 1;
                    j++;
                }

                return count;
            }
        }
        ```
      </details>

33. [Alternating Groups II](https://leetcode.com/problems/alternating-groups-ii/description/)
    - [YT Solution](https://www.youtube.com/watch?v=EZVLzXvaQ2A&list=PLpIkg8OmuX-J2Ivo9YdY7bRDstPPTVGvN&index=34)

    -
      <details>
        <summary>Click to expand code - Approach-1</summary>

        ```java
        /*
            TC - O(n)
            SC - O(1)
        */

        class Solution {
            public int numberOfAlternatingGroups(int[] colors, int k) {

                int i = 0, j = 0, n = colors.length;

                int prevColor = -1;

                int res = 0;

                while(i < n)
                {
                    int currentColor = colors[j % n];

                    if(prevColor == currentColor)
                    {
                        // [i..j-1] cannot be the starting indexes
                        i = j;
                        j++;
                        prevColor = currentColor;
                        continue;
                    }

                    if(j - i + 1 == k)
                    {
                        res++;
                        i++;
                    }

                    prevColor = currentColor;
                    j++;
                }

                return res;

            }
        }
        ```
      </details>


    -
      <details>
        <summary>Click to expand code - Approach-2 (cleaner rewrite of approach-1)</summary>

        ```java
        /*
            TC - O(n)
            SC - O(1)
        */
        class Solution {
            public int numberOfAlternatingGroups(int[] colors, int k) {

                int n = colors.length;
                int i = 0, j = 0;
                int res = 0;
                int prev = -1;

                while(i < n)
                {
                    int val = colors[j % n];

                    if(val == prev)
                        i = j;

                    if(j - i + 1 == k)
                    {
                        res++;
                        i++;
                    }

                    prev = val;
                    j++;
                }

                return res;
            }
        }
        ```
      </details>

    -
      <details>
        <summary>Click to expand code - Approach-3</summary>

        ```java
        /*
            TC - O(n)
            SC - O(n + k)
        */
        class Solution {
            public int numberOfAlternatingGroups(int[] colors, int k) {

                int n = colors.length;

                // Create a new Array by appending the array twice
                // But if you observe carefully, we just need to append
                // the first K - 1 elements to the end of the array
                int[] arr = new int[n + k - 1];
                for(int i = 0; i < n; i++) arr[i] = colors[i];
                for(int i = n; i < n + k - 1; i++) arr[i] = colors[i % n];

                int i = 0, j = 0, res = 0, prevColor = -1;

                while(j < arr.length)
                {
                    int curColor = arr[j];

                    if(prevColor == curColor)
                    {
                        // [i...j-1] can't be the starting indexes
                        i = j;
                        j++;
                        prevColor = curColor;
                        continue;
                    }

                    if(j - i + 1 == k){ res++; i++; }
                    prevColor = curColor;
                    j++;
                }

                return res;
            }
        }
        ```
      </details>

34. ❌ [Count of Substrings Containing Every Vowel and K Consonants II](https://leetcode.com/problems/count-of-substrings-containing-every-vowel-and-k-consonants-ii/description/)
    - [YT Solution](https://www.youtube.com/watch?v=8FP1kkYf2U4&list=PLpIkg8OmuX-J2Ivo9YdY7bRDstPPTVGvN&index=35)

    -
      <details>
        <summary>Click to expand code</summary>

        ```java
        /*
            Approach-1
            TC: o(nlog(n))
            SC: o(n)
        */
        class Solution {

            int[][] prefix;
            char[] s;
            int n;

            public long countOfSubstrings(String word, int k) {

                s = word.toCharArray();
                n = s.length;

                prefix = new int[n][26];

                for (int i = 0; i < n; i++) {

                    if (i > 0) {
                        System.arraycopy(prefix[i - 1], 0,
                                        prefix[i], 0, 26);
                    }

                    prefix[i][s[i] - 'a']++;
                }

                long ans = 0;

                for (int j = 0; j < n; j++) {

                    int vowelBoundary = findLargestVowelStart(j);

                    if (vowelBoundary == -1)
                        continue;

                    int left = findFirstConsonantStart(j, k);

                    if (left == -1)
                        continue;

                    int right = findLastConsonantStart(j, k);

                    ans += Math.max(
                            0,
                            Math.min(right, vowelBoundary) - left + 1
                    );
                }

                return ans;
            }

            private int getFreq(int c, int l, int r) {

                if (l > r) return 0;

                return prefix[r][c]
                        - (l > 0 ? prefix[l - 1][c] : 0);
            }

            private boolean hasAllVowels(int l, int r) {

                return getFreq('a' - 'a', l, r) > 0
                    && getFreq('e' - 'a', l, r) > 0
                    && getFreq('i' - 'a', l, r) > 0
                    && getFreq('o' - 'a', l, r) > 0
                    && getFreq('u' - 'a', l, r) > 0;
            }

            private int consonants(int l, int r) {

                int len = r - l + 1;

                int vowels =
                    getFreq('a' - 'a', l, r)
                    + getFreq('e' - 'a', l, r)
                    + getFreq('i' - 'a', l, r)
                    + getFreq('o' - 'a', l, r)
                    + getFreq('u' - 'a', l, r);

                return len - vowels;
            }

            private int findLargestVowelStart(int j) {

                int low = 0;
                int high = j;
                int ans = -1;

                while (low <= high) {

                    int mid = low + (high - low) / 2;

                    if (hasAllVowels(mid, j)) {
                        ans = mid;
                        low = mid + 1;
                    } else {
                        high = mid - 1;
                    }
                }

                return ans;
            }

            private int findFirstConsonantStart(int j, int k) {

                int low = 0;
                int high = j;
                int ans = -1;

                while (low <= high) {

                    int mid = low + (high - low) / 2;

                    int cons = consonants(mid, j);

                    if (cons > k) {
                        low = mid + 1;
                    } else {
                        if (cons == k) ans = mid;
                        high = mid - 1;
                    }
                }

                return ans;
            }

            private int findLastConsonantStart(int j, int k) {

                int low = 0;
                int high = j;
                int ans = -1;

                while (low <= high) {

                    int mid = low + (high - low) / 2;

                    int cons = consonants(mid, j);

                    if (cons < k) {
                        high = mid - 1;
                    } else {
                        if (cons == k) ans = mid;
                        low = mid + 1;
                    }
                }

                return ans;
            }
        }
        ```
      </details>
    -
      <details>
        <summary>Click to expand code</summary>

        ```java
        /*
            Approach-2
            TC: o(n)
            SC: o(n)
        */
        class Solution {
            private boolean isVowel(char ch) {
                return ch == 'a' || ch == 'e' || ch == 'i' ||
                    ch == 'o' || ch == 'u';
            }

            private int vowelIndex(char ch) {
                switch (ch) {
                    case 'a': return 0;
                    case 'e': return 1;
                    case 'i': return 2;
                    case 'o': return 3;
                    default:  return 4; // u
                }
            }

            public long countOfSubstrings(String word, int k) {

                int n = word.length();
                char[] arr = word.toCharArray();

                // next consonant position after i
                int[] nextConsonant = new int[n];

                int next = n;

                for (int i = n - 1; i >= 0; i--) {
                    nextConsonant[i] = next;

                    if (!isVowel(arr[i])) {
                        next = i;
                    }
                }

                int[] vowelFreq = new int[5];
                int distinctVowels = 0;
                int consonants = 0;

                long result = 0;

                int left = 0;

                for (int right = 0; right < n; right++) {

                    char ch = arr[right];

                    if (isVowel(ch)) {
                        int idx = vowelIndex(ch);

                        if (vowelFreq[idx]++ == 0) {
                            distinctVowels++;
                        }
                    } else {
                        consonants++;
                    }

                    // Maintain consonants <= k
                    while (consonants > k) {

                        char remove = arr[left++];

                        if (isVowel(remove)) {
                            int idx = vowelIndex(remove);

                            if (--vowelFreq[idx] == 0) {
                                distinctVowels--;
                            }
                        } else {
                            consonants--;
                        }
                    }

                    // Count all valid starts
                    while (distinctVowels == 5 && consonants == k) {

                        result += nextConsonant[right] - right;

                        char remove = arr[left++];

                        if (isVowel(remove)) {
                            int idx = vowelIndex(remove);

                            if (--vowelFreq[idx] == 0) {
                                distinctVowels--;
                            }
                        } else {
                            consonants--;
                        }
                    }
                }

                return result;
            }
        }
        ```
      </details>

35. [Number of Substrings Containing All Three Characters](https://leetcode.com/problems/number-of-substrings-containing-all-three-characters/description/)
    - [YT Solution](https://www.youtube.com/watch?v=wafDgldM9MA&list=PLpIkg8OmuX-J2Ivo9YdY7bRDstPPTVGvN&index=36)
    -
      <details>
        <summary>Click to expand code</summary>

        ```java
        class Solution {
            public int numberOfSubstrings(String s) {

                int[] count = new int[3];
                char[] str = s.toCharArray();
                int n = str.length;
                int i = 0, j = 0, res = 0;

                while(j < n)
                {
                    int ind = str[j] - 'a';
                    count[ind]++;

                    while(isValid(count))
                    {
                        // cur [i..j] is valid
                        // Possible ends for the current stating point i => j, j+1, ... n-1
                        res += (n - j);
                        ind = str[i++] - 'a';
                        count[ind]--;
                    }

                    j++;
                }

                return res;
            }

            boolean isValid(int[] nums)
            {
                for(int e : nums)
                {
                    if(e == 0) return false;
                }

                return true;
            }
        }
        ```
      </details>

36. ⭐⭐⭐ [Longest Nice Subarray](https://leetcode.com/problems/longest-nice-subarray/description/)
    - [YT Solution](https://www.youtube.com/watch?v=t2p4Sn0Qepo&list=PLpIkg8OmuX-J2Ivo9YdY7bRDstPPTVGvN&index=37)
    -
      <details>
        <summary>Click to expand code - Approach-1</summary>

        ```java
        class Solution {
            public int longestNiceSubarray(int[] nums) {

                /**
                    Approach-1: Fix i, j and check if the subarray is nice.
                        The check will result in n ** 2 because you need to check         if all pairs result in 0
                        => n * n (for fixing i and j) * (n * n) (for validating if         it's a nice array)
                        => n ** 4

                    Apporach-2: Optimizing approach-1
                        - We can optimize the validity checking function
                        - Simply maintain a count of set bits - kth bit is set 1,2,        3.. times
                        - If the bit is set more than once, then the subarray         can't be a nice subarray
                        - This brings down the validity check from n ** 2 to (32 *         n)
                        - Why (32 * n)?
                            - 32 * n - For each element in the window, you check         if the kth bit is set
                            - If at any moment kth set bit count > 1 then we         return false - this is because there exists 2 numbers         in this array where they have the same bit set
                        - This brings down the overall complexity to n ** 3

                        - Alternative approach for optimizinf isValid check - this         is better

                            - for every index k (in the range of i,j => i <= k <=         j)
                            - Perform OR operation from i to k-1, and ensure that         OR and AND of nums[k] == 0
                            - ==> OR (nums[i], nums[i + 1], ... nums[k-1]) && nums        [k] == 0
                            - This indicates that [i:k] is a nice subarray
                            - boolean isValid(int[] nums, i, j){
                                for(p = i; p < n; p++)
                                {
                                    int curORRes = nums[p];
                                    for(q = p + 1; q < n; q++)
                                    {
                                        if(curORRes && nums[q] != 0)
                                            return false;
                                        curORRes |= nums[q];
                                    }
                                }
                                return true;
                            }

                    Approach-3: Performing validation in O(1)
                        - Fix i and j, and calculate running mask
                        - for(int i = 0; i < n; i++){
                            int mask = 0;
                            for(int j = i; j < n; j++)
                            {
                                if((mask & nums[j]) != 0) break;

                                mask |= nums[j];
                                res = Math.max(res, j - i + 1);
                            }
                        }
                        - This brings the overall complexity to n ** 2

                    Approach-4
                        - Use sliding windoe for optimization
                */

                int n = nums.length;
                int mask = 0;
                int i = 0, j = 0;
                int res = 1;

                while(j < n)
                {
                    while((mask & nums[j]) != 0)
                    {
                        // We remove the ith element by performing an XOR
                        // For a subarray to be valid, the & of mask and nums[j] should be 0
                        // This is because the mask will contain all the places where it has seen a set bit
                        mask ^= nums[i++];
                    }

                    mask |= nums[j];

                    if(i != j) res = Math.max(res, j - i + 1);

                    j++;
                }

                return res;
            }
        }
        ```
      </details>
    -
      <details>
        <summary>Click to expand code - Approach-2</summary>

        ```java
        class Solution {
            public int longestNiceSubarray(int[] nums) {
                int n = nums.length;
                int mask = 0;
                int i = 0, j = 0;
                int res = 1;

                int[] count = new int[32];

                while(j < n)
                {
                    while((mask & nums[j]) != 0)
                        mask = modify(count, nums[i++], -1);

                    mask = modify(count, nums[j], 1);

                    res = Math.max(res, j - i + 1);

                    j++;
                }

                return res;
            }

            // used for both adding and removing an element's bit count
            int modify(int[] count, int val, int editVal)
            {
                int res = 0;
                for(int i = 0; i < 32; i++)
                {
                    int curBitVal = (1 << i);
                    if((val & curBitVal) == curBitVal)
                    {
                        count[i] += editVal;
                    }

                        if(count[i] > 0) res += curBitVal;
                }

                return res;
            }
        }
        ```
      </details>
    -
      <details>
        <summary>Click to expand code - Approach-3</summary>

        ```java
        class Solution {
            public int longestNiceSubarray(int[] nums) {
                int n = nums.length;
                int mask = 0;
                int i = 0, j = 0;
                int res = 1;

                int[] count = new int[32];

                while(j < n)
                {
                    while(!canAdd(count, nums[j]))
                        modify(count, nums[i++], -1);

                    modify(count, nums[j], 1);

                    res = Math.max(res, j - i + 1);

                    j++;
                }

                return res;
            }

            // used for both adding and removing an element's bit count
            int modify(int[] count, int val, int editVal)
            {
                int res = 0;
                for(int i = 0; i < 32; i++)
                {
                    int curBitVal = (1 << i);
                    if((val & curBitVal) == curBitVal)
                    {
                        count[i] += editVal;
                    }

                        if(count[i] > 0) res += curBitVal;
                }

                return res;
            }

            boolean canAdd(int[] count, int val)
            {
                for(int i = 0; i < 32; i++)
                {
                    int curBit = (1 << i);
                    if(count[i] > 0 && (val & curBit) == curBit) return false;
                }

                return true;
            }
        }
        ```
      </details>


37. [Count the Number of Good Subarrays](https://leetcode.com/problems/count-the-number-of-good-subarrays/)
    - [YT Solution](https://www.youtube.com/watch?v=bO39iLSqvQY&list=PLpIkg8OmuX-J2Ivo9YdY7bRDstPPTVGvN&index=38)
    -
      <details>
        <summary>Click to expand code</summary>

        ```java
        class Solution {
            public long countGood(int[] nums, int k) {
                int n = nums.length;
                int i = 0, j = 0;
                // number, count
                HashMap<Integer, Integer> hm = new HashMap<>();

                long res = 0;

                int pairCountK = 0;

                while(j < n)
                {
                    int val = nums[j];

                    int curValCount = hm.getOrDefault(val, 0);

                    pairCountK += curValCount;

                    hm.put(val, curValCount + 1);

                    while(pairCountK >= k)
                    {
                        // [i..j] is a good subarray
                        // for the starting point 'i', we can have the following endings j, j + 1,.. n-1
                        // Total sub array count = n - j

                        res += (n - j);

                        // Now we need to remove nums[i] and it's count;
                        curValCount = hm.get(nums[i]);

                        // Why are we removing (curValCount - 1) from pairs?
                        // If we have a count of 3 for the ith element,
                        // then it can make a pair with the remaining elements => count[i] - 1 => 3 - 1 = 2
                        pairCountK -= (curValCount - 1);

                        if(curValCount == 1) hm.remove(nums[i]);
                        else hm.put(nums[i], curValCount - 1);

                        i++;
                    }

                    j++;
                }

                return res;
            }
        }
        ```
      </details>


38. [Count Complete Subarrays in an Array](https://leetcode.com/problems/count-complete-subarrays-in-an-array/description/)
    - [YT Solution](https://www.youtube.com/watch?v=t8kDspIQyFQ&list=PLpIkg8OmuX-J2Ivo9YdY7bRDstPPTVGvN&index=39)
    -
      <details>
        <summary>Click to expand code</summary>

        ```java
        class Solution {
            public int countCompleteSubarrays(int[] nums) {

                HashSet<Integer> hs = new HashSet<>();

                for(int e : nums) hs.add(e);

                int k = hs.size();

                int n = nums.length;

                int i = 0, j = 0;

                int res = 0;

                HashMap<Integer, Integer> hm = new HashMap<>();

                while(j < n)
                {
                    int count = hm.getOrDefault(nums[j], 0);
                    hm.put(nums[j], count + 1);

                    while(hm.size() == k)
                    {
                        res += (n - j);

                        count = hm.get(nums[i]);
                        if(count == 1) hm.remove(nums[i]);
                        else hm.put(nums[i], count - 1);

                        i++;
                    }

                    j++;
                }

                return res;
            }
        }
        ```
      </details>


39. [Count Subarrays With Score Less Than K](https://leetcode.com/problems/count-subarrays-with-score-less-than-k/)
    - [YT Solution](https://www.youtube.com/watch?v=wxd3SWgzoKA&list=PLpIkg8OmuX-J2Ivo9YdY7bRDstPPTVGvN&index=40)
    -
      <details>
        <summary>Click to expand code</summary>

        ```java
        class Solution {
            public long countSubarrays(int[] nums, long k) {

                int n = nums.length;

                long res = 0;

                int i = 0, j = 0;
                long sum = 0;

                while(j < n)
                {
                    int len = j - i + 1;
                    sum += nums[j];

                    while(len * sum >= k)
                    {
                        len--;
                        sum -= nums[i++];
                    }

                    res += (j - i + 1);
                    j++;
                }

                return res;
            }
        }
        ```
      </details>


40. ❌ [Maximum Difference Between Even and Odd Frequency II](https://leetcode.com/problems/maximum-difference-between-even-and-odd-frequency-ii/description/)
    - [YT Solution](https://www.youtube.com/watch?v=zNi7uftAYEs&list=PLpIkg8OmuX-J2Ivo9YdY7bRDstPPTVGvN&index=41)
    -
      <details>
        <summary>Click to expand code</summary>

        ```java
        class Solution {
        }
        ```
      </details>


41. ⭐ [Reschedule Meetings for Maximum Free Time](https://leetcode.com/problems/reschedule-meetings-for-maximum-free-time-i/description/)
    - [YT Solution](https://www.youtube.com/watch?v=JPWBTUyGCnM&list=PLpIkg8OmuX-J2Ivo9YdY7bRDstPPTVGvN&index=42)
    -
      <details>
        <summary>Click to expand code</summary>

        ```java
        class Solution {
           // Watch YT video for explanation
            public int maxFreeTime(int eventTime, int k, int[] start, int[] end) {

                // build the array of free times
                ArrayList<Integer> free = new ArrayList<>();
                int n = start.length;

                int prevEnd = 0;
                for(int i = 0; i < n; i++)
                {
                    int curStart = start[i];
                    int curEnd = end[i];

                    free.add(curStart - prevEnd);
                    prevEnd = curEnd;
                }

                // Why "eventTime - prevEnd"?
                // Because the last event can complete before the actual event time
                // Therefore, we will see a gap between the last event end time and eventTime
                free.add(eventTime - prevEnd);

                int windowSize = k + 1; // If we make k shifts, we merge k + 1 free times

                int i = 0, j = 0, res = 0;
                n = free.size();
                int sum = 0;

                while(j < n)
                {
                    sum += free.get(j);

                    if(j - i + 1 == windowSize)
                    {
                        res = Math.max(res, sum);
                        sum -= free.get(i++);
                    }

                    j++;
                }

                return res;
            }
        }
        ```
      </details>


42. [Maximum Erasure Value](https://leetcode.com/problems/maximum-erasure-value/description/)
    - [YT Solution](https://www.youtube.com/watch?v=V7ZmYjVdZSU&list=PLpIkg8OmuX-J2Ivo9YdY7bRDstPPTVGvN&index=43)
    -
      <details>
        <summary>Click to expand code - Approach-1</summary>

        ```java
        class Solution {
            public int maximumUniqueSubarray(int[] nums) {

                int n = nums.length;
                int i = 0, j = 0, sum = 0;
                HashSet<Integer> hs = new HashSet<>();
                int res = 0;

                while(j < n)
                {
                    while(hs.contains(nums[j]))
                    {
                        hs.remove(nums[i]);
                        sum -= nums[i++];
                    }
                    sum += nums[j];
                    hs.add(nums[j]);
                    res = Math.max(res, sum);
                    j++;
                }

                return res;
            }
        }
        ```
      </details>

    -
      <details>
        <summary>Click to expand code - Approach-2</summary>

        ```java
        class Solution {
            public int maximumUniqueSubarray(int[] nums) {
                int n = nums.length;

                // prefix[i] = sum of nums[0...i-1]
                int[] prefix = new int[n + 1];
                for (int i = 0; i < n; i++) {
                    prefix[i + 1] = prefix[i] + nums[i];
                }

                // lastSeen[value] = last index where 'value' appeared
                int[] lastSeen = new int[10001];
                Arrays.fill(lastSeen, -1);

                int left = 0;
                int maxSum = 0;

                for (int right = 0; right < n; right++) {

                    left = Math.max(left, lastSeen[nums[right]] + 1);

                    int windowSum = prefix[right + 1] - prefix[left];
                    maxSum = Math.max(maxSum, windowSum);

                    lastSeen[nums[right]] = right;
                }

                return maxSum;
            }
        }
        ```
      </details>


43. [Fruit Into Baskets](https://leetcode.com/problems/fruit-into-baskets/)
    - [YT Solution](https://www.youtube.com/watch?v=QBi5_btsse4&list=PLpIkg8OmuX-J2Ivo9YdY7bRDstPPTVGvN&index=44)
    -
      <details>
        <summary>Click to expand code - Approach-1</summary>

        ```java
        class Solution {
            public int totalFruit(int[] nums) {
                int n = nums.length;
                int i = 0, j = 0, res = 0;

                // Number, freq
                HashMap<Integer, Integer> hm = new HashMap<>();

                while(j < n)
                {
                    while(hm.size() == 2 && !hm.containsKey(nums[j]))
                    {
                        int curCount = hm.get(nums[i]);
                        if(curCount == 1) hm.remove(nums[i]);
                        else hm.put(nums[i], curCount - 1);

                        i++;
                    }

                    int curCount = hm.getOrDefault(nums[j], 0) + 1;
                    hm.put(nums[j], curCount);

                    res = Math.max(res, j - i + 1);
                    j++;
                }

                return res;
            }
        }
        ```
      </details>
    -
      <details>
        <summary>Click to expand code - Approach-2</summary>

        ```java
        class Solution {
            public int totalFruit(int[] nums) {
                int n = nums.length;
                int i = 0, j = 0, res = 0;

                int[] count = new int[n];
                int uniqueCount = 0;

                while(j < n)
                {
                    // If uniqueCount == 2 and we're seeing this element for the first time
                    while(uniqueCount == 2 && count[nums[j]] == 0)
                    {
                        count[nums[i]]--;
                        if(count[nums[i]] == 0) uniqueCount--;
                        i++;
                    }

                    count[nums[j]]++;

                    // Only increment uniqueCount for the first time
                    if(count[nums[j]] == 1) uniqueCount++;

                    res = Math.max(res, j - i + 1);
                    j++;
                }

                return res;
            }
        }
        ```
      </details>



44. ❌ [Find X-Sum of All K-Long Subarrays II](https://leetcode.com/problems/find-x-sum-of-all-k-long-subarrays-ii/description/)
    - [YT Solution](https://www.youtube.com/watch?v=ZyE1zCe_gSQ&list=PLpIkg8OmuX-J2Ivo9YdY7bRDstPPTVGvN&index=45)
    -
      <details>
        <summary>Click to expand code</summary>

        ```java
        class Solution {
        }
        ```
      </details>


45. ⭐⭐⭐ [Best Time to Buy and Sell Stock using Strategy](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-using-strategy/)
    - [YT Solution](https://www.youtube.com/watch?v=fZl7ymC0uaU&list=PLpIkg8OmuX-J2Ivo9YdY7bRDstPPTVGvN&index=46)
    -
      <details>
        <summary>Click to expand code - Approach-1 (avoid)</summary>

        ```java
        class Solution {

            /*
                The idea is simple, calculate the profit without any modification, then calculate the profit from current window


                Once you have both values, profit = orgPofit - first haf + second half

                TC - O(n)
                SC - O(1)
            */

            public long maxProfit(int[] prices, int[] strategy, int k) {

                int n = prices.length;
                int i = 0, j = 0;

                long profitWithoutModification = 0;

                for(int ind = 0; ind < n; ind++)
                    profitWithoutModification += prices[ind] * strategy[ind];

                long res = profitWithoutModification;

                long firstHalfSum = 0;
                long secondHalfSum = 0;

                int windowHalf = k / 2;

                while(j < n)
                {
                    int midBoundary = i + windowHalf - 1;

                    if (j <= midBoundary) {
                        firstHalfSum += -(1L * prices[j] * strategy[j]);
                    } else {
                        /*
                        Why (1 - strategy[j])?
                        Case-1: strategy[j] = 0;
                            if it was 0, then it wasn't previously included in profitWithoutModification; therefore, add it.

                        Case-2: strategy[j] = 1;
                            if it was 1, then it was previously included in profitWithoutModification; therefore, don't add it

                        Case-3: strategy[j] = -1;
                            if it was -1, then it was previously included in profitWithoutModification; If we were to change it to 1, we need to add it twice.
                            This is because the "profitWithoutModification" would have included the current index as -1 * prices[j];
                            If we change it to one, we need to remove that operation, and also add it again.
                            Therefore, we need to add 2 * prices[j];
                        */
                        secondHalfSum += 1L * prices[j] * (1 - strategy[j]);
                    }

                    if (j - i + 1 == k) {

                        res = Math.max(res, profitWithoutModification + firstHalfSum + secondHalfSum);

                        firstHalfSum += 1L * prices[i] * strategy[i];

                        int mid = i + windowHalf;

                        firstHalfSum -= 1L * prices[mid] * strategy[mid];
                        secondHalfSum -= 1L * prices[mid] * (1 - strategy[mid]);

                        i++;
                    }

                    j++;
                }

                return res;
            }
        }
        ```
      </details>
    -
      <details>
        <summary>Click to expand code - Approach-2 (most intuitive)</summary>

        ```java
        /*
            TC - O(n)
            SC - O(n)
        */
        class Solution {
            public long maxProfit(int[] prices, int[] strategy, int k) {

                int n = prices.length;

                long[] profitPrefix = new long[n];
                profitPrefix[0] = prices[0] * strategy[0];

                for(int ind = 1; ind < n; ind++)
                    profitPrefix[ind] = (profitPrefix[ind-1] + prices[ind] * strategy[ind]);

                int i = 0, j = 0, windowHalf = k / 2;

                long res = profitPrefix[n - 1]; // total profit without any modification
                long secondHalfProfit = 0;

                while(j < n)
                {
                    int windowBoundary = i + windowHalf;

                    if(j >= windowBoundary)
                        secondHalfProfit += prices[j];

                    if(j - i + 1 == k)
                    {
                        long leftToWindowProfit = getProfitInRange(profitPrefix, 0, i-1);
                        long rightToWindowProfit = getProfitInRange(profitPrefix, j + 1, n - 1);

                        long profitInCurrentWindow = secondHalfProfit;

                        res = Math.max(res, leftToWindowProfit + profitInCurrentWindow + rightToWindowProfit);
                        secondHalfProfit -= prices[windowBoundary];

                        i++;
                    }

                    j++;
                }

                return res;
            }

            long getProfitInRange(long[] prefix, int l, int r)
            {
                if(l > r) return 0;
                return prefix[r] - (l - 1 >= 0 ? prefix[l - 1] : 0);
            }
        }
        ```
      </details>

    -
      <details>
        <summary>Click to expand code - Approach-3 (best)</summary>

        ```java
        /*
            TC - O(n)
            SC - O(1)
        */
        class Solution {
            public long maxProfit(int[] prices, int[] strategy, int k) {

                int n = prices.length;
                long originalProfit = 0;

                for(int ind = 0; ind < n; ind++)
                    originalProfit += (prices[ind] * strategy[ind]);

                int i = 0, j = 0, windowHalf = k / 2;

                long res = originalProfit; // total profit without any modification
                long newWindowProfit = 0;
                long originalWindowProfit = 0;

                while(j < n)
                {
                    originalWindowProfit += prices[j] * strategy[j];

                    int windowBoundary = i + windowHalf;

                    if(j >= windowBoundary)
                        newWindowProfit += prices[j];

                    if(j - i + 1 == k)
                    {
                        long newProfit = originalProfit - originalWindowProfit + newWindowProfit;

                        res = Math.max(res, newProfit);

                        newWindowProfit -= prices[windowBoundary];
                        originalWindowProfit -= prices[i] * strategy[i];

                        i++;
                    }

                    j++;
                }

                return res;
            }
        }
        ```
      </details>



46. ❌⭐⭐⭐ [Divide an Array Into Subarrays With Minimum Cost II](https://leetcode.com/problems/divide-an-array-into-subarrays-with-minimum-cost-ii/)
    - [YT Solution](https://www.youtube.com/watch?v=hnj5JrPVqZk&list=PLpIkg8OmuX-J2Ivo9YdY7bRDstPPTVGvN&index=47)
    -
      <details>
        <summary>Click to expand code</summary>

        ```java
        class Solution {
        }
        ```
      </details>


47. ⭐⭐⭐ [Minimum Number of Flips to Make the Binary String Alternating](https://leetcode.com/problems/minimum-number-of-flips-to-make-the-binary-string-alternating/description/)
    - [YT Solution](https://www.youtube.com/watch?v=T3lhIT7hbl4&list=PLpIkg8OmuX-J2Ivo9YdY7bRDstPPTVGvN&index=48)
    -
      <details>
        <summary>Click to expand code</summary>

        ```java
        class Solution {
            public int minFlips(String s) {
                char[] str = s.toCharArray();
                int n = str.length;

                int i = 0, j = 0, res = Integer.MAX_VALUE;

                /*
                    Since we have type-1 operation, we can take the first character
                    and move it to the end.

                    This means that the string can be rotated n times.
                    Ex - 111000
                    1 rotation - 110001
                    2 rotation - 100011
                    3 rotation - 000111
                    and so on.

                    Therefore, we will have N possible strings.

                    Now, each string can be converted into one of the 2 possible sequences
                        - Pattern #1 - 10101010...
                        - Pattern #2 - 01010101...

                    For each string, we can calculate the number of flips required by simply
                    counting the number of mistmatches between  the string, and the patterns

                    We don't need to generate all possible strings, we will simply
                    use sliding window to simulate the rotation
                */

                int patternOneFlipCount = 0;
                int patternTwoFlipCount = 0;

                while(i < n)
                {
                    int val = str[j % n] - '0';

                    // For pattern-1, even indexes have 1, and odd indexes have 0
                    // Even index and has val = 0, we need a flip
                    if((j & 1) == 0 && val == 0) patternOneFlipCount++;
                    // Odd index and we has val = 1, we need a flip
                    else if((j & 1) == 1 && val == 1) patternOneFlipCount++;


                    // For pattern-2, even indexes have 0, and odd indexes have 1
                    // Even index and has val = 0, we need a flip
                    if((j & 1) == 0 && val == 1) patternTwoFlipCount++;
                    // Odd index and we has val = 1, we need a flip
                    else if((j & 1) == 1 && val == 0) patternTwoFlipCount++;

                    if(j - i + 1 == n)
                    {
                        res = Math.min(res, Math.min(patternOneFlipCount, patternTwoFlipCount));

                        val = str[i] - '0';

                        // For pattern-1, even indexes have 1, and odd indexes have 0
                        // Even index and has val = 0, we need a flip
                        if((i & 1) == 0 && val == 0) patternOneFlipCount--;
                        // Odd index and we has val = 1, we need a flip
                        else if((i & 1) == 1 && val == 1) patternOneFlipCount--;

                        // For pattern-2, even indexes have 0, and odd indexes have 1
                        // Even index and has val = 0, we need a flip
                        if((i & 1) == 0 && val == 1) patternTwoFlipCount--;
                        // Odd index and we has val = 1, we need a flip
                        else if((i & 1) == 1 && val == 0) patternTwoFlipCount--;

                        i++;
                    }

                    j++;
                }

                return res;
            }
        }
        ```
      </details>


<!-- 48. []()
    - [YT Solution]()
    -
      <details>
        <summary>Click to expand code</summary>

        ```java
        class Solution {
        }
        ```
      </details> -->


---

> Note: Problems after this aren't covered in the playlist

49. [Longest Repeating Character Replacement](https://leetcode.com/problems/longest-repeating-character-replacement/)
    - [YT Solution]()
    -
      <details>
        <summary>Click to expand code</summary>

        ```java
        class Solution {
            public int characterReplacement(String s, int k) {

                char[] str = s.toCharArray();

                int i = 0, j = 0, res = 0, n = str.length;

                int[] count = new int[26];

                while(j < n)
                {
                    count[str[j] - 'A']++;
                    /*
                        Why (j - i + 1) - getMajorityFreq(count)?

                        The goal is to convert all the strings in the subarray to be of the same character

                        Therefore, it would make sense to keep the character with the majority of frequency the same, while changing others

                        This means that, we can only change K characters and make them equal to the majorit character
                    */
                    while(((j - i + 1) - getMajorityFreq(count)) > k)
                        count[str[i++] - 'A']--;

                    res = Math.max(res, j - i + 1);
                    j++;
                }

                return res;

            }

            int getMajorityFreq(int[] count)
            {
                int max = 0;
                for(int e : count) max = Math.max(max, e);
                return max;
            }
        }
        ```
      </details>

50. [Contiguous Array](https://leetcode.com/problems/contiguous-array/description/)
    - [YT Solution]()
    -
      <details>
        <summary>Click to expand code</summary>

        ```java
        class Solution {
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



# Legend
```
⭐ - imp problem
❌ - Did not understand/solve
```


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

# Bitwise techniques

- a | b will result in a number >= max(a, b)
- a & b will result in a number <= min(a, b)
- a ^ a = 0
