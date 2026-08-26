# Problem list

1. ⭐ [Insert Delete GetRandom O(1)](https://leetcode.com/problems/insert-delete-getrandom-o1/description/)
   - [YT Solution](https://www.youtube.com/watch?v=3yTnLrNdJGo&list=PLpIkg8OmuX-JW5294URE-iwVhl_tdWEP5)
   -  <details>
        <summary>Click to expand code</summary>

		```java
		class RandomizedSet {

			HashMap<Integer, Integer> hm;
			List<Integer> list;

			public RandomizedSet() {
				hm = new HashMap<>();
				list = new ArrayList<>();
			}

			public boolean insert(int val) {
				if(hm.containsKey(val)) return false;

				hm.put(val, list.size());
				list.add(val);

				return true;
			}

			public boolean remove(int val) {

				if (!hm.containsKey(val))
					return false;

				int ind = hm.get(val);
				int last = list.get(list.size() - 1);

				list.set(ind, last);
				hm.put(last, ind);

				list.remove(list.size() - 1);
				hm.remove(val);

				return true;
			}

			public int getRandom() {
				Random rand = new Random();

				return list.get(rand.nextInt(list.size()));

				// Or we can use this
				// Math.random() returns a double between - 0.0 <= x < 1.0
				// return list.get((int)(Math.random() * list.size()));
			}
		}

		/**
		 * Your RandomizedSet object will be instantiated and called as such:
		* RandomizedSet obj = new RandomizedSet();
		* boolean param_1 = obj.insert(val);
		* boolean param_2 = obj.remove(val);
		* int param_3 = obj.getRandom();
		*/
		```

      </details>

2. ⭐ [LRU Cache](https://leetcode.com/problems/lru-cache/)
   - [YT Solution]()
   -  <details>
        <summary>Click to expand code - Approach-1 (okayish approach)</summary>

		```java
		class LRUCache {
			class Node{
				int key, val;
				Node prev;
				Node next;

				Node(int k, int v)
				{
					key = k;
					val = v;
				}
			}

			HashMap<Integer, Node> hm;
			Node curNode;
			Node head;

			int capacity;

			public LRUCache(int capacity) {
				this.capacity = capacity;
				hm = new HashMap<>();
			}

			public int get(int key) {

				if(!hm.containsKey(key)) return -1;

				bringNodeToLast(key);

				return hm.get(key).val;

			}

			public void put(int key, int value) {
				if(hm.containsKey(key)){
					Node node = hm.get(key);
					node.val = value;
					bringNodeToLast(key);
					return;
				}

				Node node = new Node(key, value);
				hm.put(key, node);

				if(head == null) head = node;

				if(curNode == null) curNode = node;
				else{
					curNode.next = node;
					node.prev = curNode;
					curNode = node;
				}

				if(hm.size() > capacity){
					Node next = head.next;
					next.prev = null;
					hm.remove(head.key);
					head = next;
				}
			}

			void bringNodeToLast(int key)
			{
				Node node = hm.get(key);

				if(node == curNode) return;

				if(node.prev != null) node.prev.next = node.next;
				if(node.next != null) node.next.prev = node.prev;

				if(node == head){
					head = head.next;
					head.prev = null;
				}

				node.next = null;

				curNode.next = node;
				node.prev = curNode;
				curNode = node;
				node.next = null;
			}
		}

		/**
		* Your LRUCache object will be instantiated and called as such:
		* LRUCache obj = new LRUCache(capacity);
		* int param_1 = obj.get(key);
		* obj.put(key,value);
		*/
		```

      </details>

   -  <details>
        <summary>Click to expand code - Approach-2 (good, but not intuitive)</summary>

		```java
		class LRUCache {
			class Node {
				int key, val;
				Node prev, next;
				Node(int k, int v) { key = k; val = v; }
			}

			private final int capacity;
			private final Map<Integer, Node> map;
			private final Node head, tail; // dummies: head <-> ... <-> tail

			public LRUCache(int capacity) {
				this.capacity = capacity;
				map = new HashMap<>();
				head = new Node(-1, -1);
				tail = new Node(-1, -1);
				head.next = tail;
				tail.prev = head;
			}

			public int get(int key) {
				if (!map.containsKey(key)) return -1;
				Node node = map.get(key);
				remove(node);
				insertAtTail(node);
				return node.val;
			}

			public void put(int key, int value) {
				if (map.containsKey(key)) {
					Node node = map.get(key);
					node.val = value;
					remove(node);
					insertAtTail(node);
					return;
				}

				if (map.size() == capacity) {
					Node lru = head.next;      // least recently used
					remove(lru);
					map.remove(lru.key);
				}

				Node node = new Node(key, value);
				map.put(key, node);
				insertAtTail(node);
			}

			private void remove(Node node) {
				node.prev.next = node.next;
				node.next.prev = node.prev;
			}

			private void insertAtTail(Node node) {
				node.prev = tail.prev;
				node.next = tail;
				tail.prev.next = node;
				tail.prev = node;
			}
		}
		```

      </details>

   -  <details>
        <summary>Click to expand code - Approach-3 (⭐ personal fav)</summary>

		```java
		class LRUCache {
			class Node {
				int key, value;
				Node prev, next;
				Node(int k, int v) { key = k; value = v; }
			}

			private final int capacity;
			private final Map<Integer, Node> hm;
			private Node head, tail;

			public LRUCache(int capacity) {
				this.capacity = capacity;
				hm = new HashMap<>();
			}

			public int get(int key) {
				if(!hm.containsKey(key)) return -1;

				int value = hm.get(key).value;
				put(key, value);

				return value;
			}

			public void put(int key, int value) {

				if(hm.containsKey(key))
					remove(key);

				Node node = new Node(key, value);
				hm.put(key, node);

				if(tail == null)
				{
					head = node;
					tail = node;
				}
				else
				{
					tail.next = node;
					node.prev = tail;
					tail = node;
				}

				if(hm.size() > capacity)
				{
					remove(head.key);
				}
			}

			void remove(int key){

				Node node = hm.get(key);

				if(node == head)
				{
					if(head.next != null)
						head.next.prev = null;

					head = head.next;
					node.next = null;
				}

				if(node == tail)
				{
					if(tail.prev != null) tail.prev.next = null;

					tail = tail.prev;
					node.prev = null;
				}

				if(node.next != null && node.prev != null) // middle of the list
				{
					node.prev.next = node.next;
					node.next.prev = node.prev;
					node.next = null;
					node.prev = null;
				}

				hm.remove(key);
			}

		}
		```

      </details>

3. ⭐⭐⭐ [LFU Cache](https://leetcode.com/problems/lfu-cache/)
   - [YT Solution](https://www.youtube.com/watch?v=-Vch0tHAsOM&list=PLpIkg8OmuX-JW5294URE-iwVhl_tdWEP5&index=3)
   -  <details>
        <summary>Click to expand code - Approach-1</summary>

		```java
		/*
			There is a problem with this approach, it runs in O(nlogn) time complexity

			for n queries (get or put), it takes logn time
		*/
		class LFUCache {
			class LRU{
				class LRU_Node
				{
					int key;
					LRU_Node prev, next;
					LRU_Node(int k){ key = k; }
				}

				Map<Integer, LRU_Node> hm;
				LRU_Node head;
				LRU_Node tail;

				LRU(){
					hm = new HashMap<>();
					head = null;
					tail = null;
				}

				void put(int key)
				{
					LRU_Node node = new LRU_Node(key);
					hm.put(key, node);

					if(tail == null)
					{
						head = node;
						tail = node;
					}
					else
					{
						tail.next = node;
						node.prev = tail;
						tail = node;
					}
				}

				int remove(){
					int key = head.key;
					remove(key);
					return key;
				}

				void remove(int key){
					if(!hm.containsKey(key)) return;

					LRU_Node node = hm.get(key);

					if(node == head)
					{
						if(head.next != null)
							head.next.prev = null;

						head = head.next;
						node.next = null;
					}

					if(node == tail)
					{
						if(tail.prev != null) tail.prev.next = null;

						tail = tail.prev;
						node.prev = null;
					}

					if(node.next != null && node.prev != null) // middle of the list
					{
						node.prev.next = node.next;
						node.next.prev = node.prev;
						node.next = null;
						node.prev = null;
					}

					hm.remove(key);
				}

				int size(){
					return hm.size();
				}

			}

			int capacity;

			int curCapacity;

			// Key -> value, freq
			// int[0] -> value
			// int[1] -> freq
			Map<Integer, int[]> keyMap;

			TreeMap<Integer, LRU> freqMap;

			public LFUCache(int capacity) {
				this.capacity = capacity;
				keyMap = new HashMap<>();
				freqMap = new TreeMap<>();
			}

			public int get(int key) {
				if(!keyMap.containsKey(key)) return -1;

				return updateFreq(key, -1, false);
			}

			public void put(int key, int value) {
				if(keyMap.containsKey(key))
				{
					updateFreq(key, value, true);
					return;
				}

				if(curCapacity == capacity)
				{
					Map.Entry<Integer, LRU> entry = freqMap.firstEntry();

					int removedKey = entry.getValue().remove();
					if(entry.getValue().size() == 0) freqMap.remove(entry.getKey());

					keyMap.remove(removedKey);
					curCapacity--;
				}

				if(freqMap.get(1) == null)
					freqMap.put(1, new LRU());

				freqMap.get(1).put(key);

				keyMap.put(key, new int[]{value, 1});

				curCapacity++;
			}

			int updateFreq(int key, int value, boolean updateValue)
			{
				int[] node = keyMap.get(key);

				if(updateValue) node[0] = value;

				int previousFreq = node[1]++;
				int newFreq = node[1];

				freqMap.get(previousFreq).remove(key);
				if(freqMap.get(previousFreq).size() == 0)
					freqMap.remove(previousFreq);

				if(freqMap.get(newFreq) == null)
					freqMap.put(newFreq, new LRU());

				freqMap.get(newFreq).put(key);

				return node[0];
			}
		}

		/**
		* Your LFUCache object will be instantiated and called as such:
		* LFUCache obj = new LFUCache(capacity);
		* int param_1 = obj.get(key);
		* obj.put(key,value);
		*/
		```

      </details>

   -  <details>
        <summary>Click to expand code - Approach-2</summary>

		```java
		/*
			Optimized solution-1: Runs in O(1) for each operation
			for 'n' operations, it takes O(n) time
		*/
		class LFUCache {

			class LRU{
				class LRU_Node
				{
					int key;
					LRU_Node prev, next;
					LRU_Node(int k){ key = k; }
				}

				Map<Integer, LRU_Node> hm;
				LRU_Node head;
				LRU_Node tail;

				LRU(){
					hm = new HashMap<>();
					head = null;
					tail = null;
				}

				void put(int key)
				{
					LRU_Node node = new LRU_Node(key);
					hm.put(key, node);

					if(tail == null)
					{
						head = node;
						tail = node;
					}
					else
					{
						tail.next = node;
						node.prev = tail;
						tail = node;
					}
				}

				int remove(){
					int key = head.key;
					remove(key);
					return key;
				}

				void remove(int key){
					if(!hm.containsKey(key)) return;

					LRU_Node node = hm.get(key);

					if(node == head)
					{
						if(head.next != null)
							head.next.prev = null;

						head = head.next;
						node.next = null;
					}

					if(node == tail)
					{
						if(tail.prev != null) tail.prev.next = null;

						tail = tail.prev;
						node.prev = null;
					}

					if(node.next != null && node.prev != null) // middle of the list
					{
						node.prev.next = node.next;
						node.next.prev = node.prev;
						node.next = null;
						node.prev = null;
					}

					hm.remove(key);
				}

				int size(){
					return hm.size();
				}

			}

			int capacity;

			int curCapacity;

			// Key -> value, freq
			// int[0] -> value
			// int[1] -> freq
			Map<Integer, int[]> keyMap;

			Map<Integer, LRU> freqMap;

			int minFreq;

			public LFUCache(int capacity) {
				this.capacity = capacity;
				keyMap = new HashMap<>();
				freqMap = new HashMap<>(); // Change: changed this to HashMap
				minFreq = 1;
			}

			public int get(int key) {
				if(!keyMap.containsKey(key)) return -1;

				return updateFreq(key, -1, false);
			}

			public void put(int key, int value) {
				if(keyMap.containsKey(key))
				{
					updateFreq(key, value, true);
					return;
				}

				if(curCapacity == capacity)  // Change: Instead of using TreeMap, we maintain a variable called minFreq
				{
					int removedKey = freqMap.get(minFreq).remove();

					if(freqMap.get(minFreq).size() == 0)
						freqMap.remove(minFreq);

					keyMap.remove(removedKey);
					curCapacity--;
				}

				minFreq = 1;

				if(freqMap.get(minFreq) == null)
					freqMap.put(minFreq, new LRU());

				freqMap.get(minFreq).put(key);

				keyMap.put(key, new int[]{value, 1});

				curCapacity++;
			}

			int updateFreq(int key, int value, boolean updateValue)
			{
				int[] node = keyMap.get(key);

				if(updateValue) node[0] = value;

				int previousFreq = node[1]++;
				int newFreq = node[1];

				freqMap.get(previousFreq).remove(key);
				if(freqMap.get(previousFreq).size() == 0) {
					freqMap.remove(previousFreq);
					if(minFreq == previousFreq) minFreq++; // Change: Update min freq if the previousFreq does not exist anymore
				}

				if(freqMap.get(newFreq) == null)
					freqMap.put(newFreq, new LRU());

				freqMap.get(newFreq).put(key);

				return node[0];
			}
		}

		/**
		* Your LFUCache object will be instantiated and called as such:
		* LFUCache obj = new LFUCache(capacity);
		* int param_1 = obj.get(key);
		* obj.put(key,value);
		*/
		```

      </details>


   -  <details>
        <summary>Click to expand code - Approach-3 (best)</summary>

		```java
		/*
			Same TC as approach-2, but better written code
		*/
		class LFUCache {

			class Node {
				int key;
				int value;
				int freq;

				Node prev;
				Node next;

				Node(int key, int value) {
					this.key = key;
					this.value = value;
					this.freq = 1;
				}
			}

			class DoublyLinkedList { // LRU style DLL

				Node head;
				Node tail;

				int size;

				void addLast(Node node) {

					node.prev = tail;
					node.next = null;

					if(tail == null)
					{
						head = node;
					}
					else
					{
						tail.next = node;
						node.prev = tail;
					}

					tail = node;
					size++;
				}

				void remove(Node node) {

					if(node == head)
					{
						if(head.next != null)
							head.next.prev = null;

						head = head.next;
						node.next = null;
					}

					if(node == tail)
					{
						if(tail.prev != null) tail.prev.next = null;

						tail = tail.prev;
						node.prev = null;
					}

					if(node.next != null && node.prev != null) // middle of the list
					{
						node.prev.next = node.next;
						node.next.prev = node.prev;
						node.next = null;
						node.prev = null;
					}

					size--;
				}

				Node removeFirst() {
					Node node = head;

					if (node != null) remove(node);

					return node;
				}

				boolean isEmpty() {
					return size == 0;
				}
			}

			private final Map<Integer, Node> keyNodeMap;
			private final Map<Integer, DoublyLinkedList> frequencyMap;

			private final int capacity;
			private int minFreq;

			public LFUCache(int capacity) {

				this.capacity = capacity;

				keyNodeMap = new HashMap<>();
				frequencyMap = new HashMap<>();

				minFreq = 1;
			}

			public int get(int key) {

				Node node = keyNodeMap.get(key);

				if (node == null)
					return -1;

				increaseFrequency(node);

				return node.value;
			}

			public void put(int key, int value) {

				// if (capacity == 0) return; // This is not needed since - 1 <= capacity <= 10 ^ 4

				if (keyNodeMap.containsKey(key)) {

					Node node = keyNodeMap.get(key);

					node.value = value;

					increaseFrequency(node);

					return;
				}

				if (keyNodeMap.size() == capacity) {

					DoublyLinkedList list = frequencyMap.get(minFreq);

					Node victim = list.removeFirst();

					keyNodeMap.remove(victim.key);

					if (list.isEmpty()) frequencyMap.remove(minFreq);
				}

				Node node = new Node(key, value);

				keyNodeMap.put(key, node);

				frequencyMap
					.computeIfAbsent(1, f -> new DoublyLinkedList())
					.addLast(node);

				minFreq = 1;
			}

			private void increaseFrequency(Node node) {

				int oldFreq = node.freq;

				DoublyLinkedList oldList = frequencyMap.get(oldFreq);

				oldList.remove(node);

				if (oldList.isEmpty()) {

					frequencyMap.remove(oldFreq);

					if (minFreq == oldFreq)
						minFreq++;
				}

				node.freq++;

				frequencyMap
					.computeIfAbsent(node.freq, f -> new DoublyLinkedList())
					.addLast(node);
			}
		}

		/**
		* Your LFUCache object will be instantiated and called as such:
		* LFUCache obj = new LFUCache(capacity);
		* int param_1 = obj.get(key);
		* obj.put(key,value);
		*/
		```

      </details>

4. ⭐ [Design Browser History](https://leetcode.com/problems/design-browser-history/description/)
   - [YT Solution](https://www.youtube.com/watch?v=FNcanLK6aZs&list=PLpIkg8OmuX-JW5294URE-iwVhl_tdWEP5&index=4)
   -  <details>
        <summary>Click to expand code - Approach-1</summary>

		```java
		class BrowserHistory {
			String[] path;
			int curIndex;
			int lastIndex;

			public BrowserHistory(String homepage) {
				path = new String[5000];
				curIndex = -1;
				lastIndex = -1;
				visit(homepage);
			}

			public void visit(String url) {
				if(curIndex == lastIndex)
				{
					curIndex++;
					lastIndex++;
					path[curIndex] = url;
				}
				else{
					curIndex++;
					lastIndex = curIndex;
					path[curIndex] = url;
				}
			}

			public String back(int steps) {
				curIndex = Math.max(0, curIndex - steps);
				return path[curIndex];
			}

			public String forward(int steps) {
				curIndex = Math.min(lastIndex, curIndex + steps);
				return path[curIndex];
			}
		}

		/**
		* Your BrowserHistory object will be instantiated and called as such:
		* BrowserHistory obj = new BrowserHistory(homepage);
		* obj.visit(url);
		* String param_2 = obj.back(steps);
		* String param_3 = obj.forward(steps);
		*/
		```

      </details>

   -  <details>
        <summary>Click to expand code - Approach-2</summary>

		```java
		class BrowserHistory {

			List<String> path;
			int curIndex;

			public BrowserHistory(String homepage) {
				path = new ArrayList<>();
				path.add(homepage);
				curIndex = 0;
			}

			// This takes O(K) where K is the number of elements present after
			/*
			public void visit(String url) {
				path.subList(curIndex + 1, path.size()).clear();
				path.add(url);
				curIndex++;
			}
			*/

			// Runs in O(1)
			public void visit(String url) {

				curIndex++;

				if (curIndex < path.size())
					path.set(curIndex, url);
				else
					path.add(url);

				lastIndex = curIndex;
			}

			public String back(int steps) {
				curIndex = Math.max(0, curIndex - steps);
				return path.get(curIndex);
			}

			public String forward(int steps) {
				curIndex = Math.min(path.size() - 1, curIndex + steps);
				return path.get(curIndex);
			}
		}
		```

      </details>


5. [Design Add and Search Words Data Structure](https://leetcode.com/problems/design-add-and-search-words-data-structure/description/)
   - [YT Solution](https://www.youtube.com/watch?v=wyUO7Oq9uS4&list=PLpIkg8OmuX-JW5294URE-iwVhl_tdWEP5&index=5)
   -  <details>
        <summary>Click to expand code - Approach-1 (too complicated)</summary>

		```java
		class WordDictionary {

			int TRIE_NODE_ARRAY_LENGTH = 26;

			class Node{
				boolean isEnd;
				Node[] next;

				Node(boolean isEnd){
					this.isEnd = isEnd;
					next = new Node[TRIE_NODE_ARRAY_LENGTH];
				}
			}

			class Trie{
				Node root;

				Trie(){
					root = new Node(false);
				}

				void add(String word, Node curNode, int index)
				{
					int n = word.length();

					if(index == n) return;

					int charInd = word.charAt(index)  - 'a';

					if (curNode.next[charInd] == null)
						curNode.next[charInd] = new Node(false);

					if (index == n - 1)
						curNode.next[charInd].isEnd = true;

					add(word, curNode.next[charInd], index + 1);
				}

				boolean find(String word, Node curNode, int index)
				{
					int n = word.length();

					if(index == n) return curNode.isEnd;

					char ch = word.charAt(index);

					if(ch == '.')
					{
						boolean found = false;

						for(int i = 0; i < 26 && !found; i++)
						{
							if(curNode.next[i] == null) continue;
							found |= find(word, curNode.next[i], index + 1);
						}

						return found;
					}

					int charInd = ch - 'a';

					if(curNode.next[charInd] == null) return false;

					return find(word, curNode.next[charInd], index + 1);
				}

			}

			Trie trie;

			public WordDictionary() {
				trie = new Trie();
			}

			public void addWord(String word) {
				trie.add(word, trie.root, 0);
			}

			public boolean search(String word) {
				return trie.find(word, trie.root, 0);
			}
		}

		/**
		* Your WordDictionary object will be instantiated and called as such:
		* WordDictionary obj = new WordDictionary();
		* obj.addWord(word);
		* boolean param_2 = obj.search(word);
		*/
		```

      </details>

   -  <details>
        <summary>Click to expand code - Approach-2 (best)</summary>

		```java
		class WordDictionary {

			int TRIE_NODE_ARRAY_LENGTH = 26;

			class Node{
				boolean isEnd;
				Node[] next;

				Node(){
					isEnd = false;
					next = new Node[TRIE_NODE_ARRAY_LENGTH];
				}
			}

			class Trie{
				Node root;

				Trie(){
					root = new Node();
				}

				void add(String word, int index)
				{
					Node cur = root;

					for (char ch : word.toCharArray()) {

						int idx = ch - 'a';

						if (cur.next[idx] == null)
							cur.next[idx] = new Node();

						cur = cur.next[idx];
					}

					cur.isEnd = true;
				}

				boolean find(String word, Node curNode, int index)
				{
					int n = word.length();

					if(index == n) return curNode.isEnd;

					char ch = word.charAt(index);

					if(ch == '.')
					{
						for (Node child : curNode.next) {
							if (child != null && find(word, child, index + 1))
								return true;
						}

						return false;
					}

					int charInd = ch - 'a';

					if(curNode.next[charInd] == null) return false;

					return find(word, curNode.next[charInd], index + 1);
				}

			}

			Trie trie;

			public WordDictionary() {
				trie = new Trie();
			}

			public void addWord(String word) {
				trie.add(word, 0);
			}

			public boolean search(String word) {
				return trie.find(word, trie.root, 0);
			}
		}

		/**
		* Your WordDictionary object will be instantiated and called as such:
		* WordDictionary obj = new WordDictionary();
		* obj.addWord(word);
		* boolean param_2 = obj.search(word);
		*/
		```

      </details>

   -  <details>
        <summary>Click to expand code - Approach-3 (good)</summary>

		```java
		class WordDictionary {

			class TrieNode {
				boolean isEnd;
				TrieNode[] children = new TrieNode[26];
			}

			private final TrieNode root;

			public WordDictionary() {
				root = new TrieNode();
			}

			public void addWord(String word) {

				TrieNode cur = root;

				for (char ch : word.toCharArray()) {

					int idx = ch - 'a';

					if (cur.children[idx] == null)
						cur.children[idx] = new TrieNode();

					cur = cur.children[idx];
				}

				cur.isEnd = true;
			}

			public boolean search(String word) {
				return search(word, 0, root);
			}

			private boolean search(String word, int index, TrieNode node) {

				if (index == word.length())
					return node.isEnd;

				char ch = word.charAt(index);

				if (ch == '.') {

					for (TrieNode child : node.children) {
						if (child != null && search(word, index + 1, child))
							return true;
					}

					return false;
				}

				TrieNode child = node.children[ch - 'a'];

				return child != null && search(word, index + 1, child);
			}
		}
		```

      </details>

6. [Design Parking System](https://leetcode.com/problems/design-parking-system/)
   - [YT Solution](https://www.youtube.com/watch?v=ysZ7Rla4w7Y&list=PLpIkg8OmuX-JW5294URE-iwVhl_tdWEP5&index=6)
   -  <details>
        <summary>Click to expand code</summary>

		```java
		class ParkingSystem {

			int bigLimit, curBigCount;
			int mediumLimit, curMediumCount;
			int smallLimit, curSmallCount;

			public ParkingSystem(int big, int medium, int small) {
				bigLimit = big;
				mediumLimit = medium;
				smallLimit = small;

				curBigCount = 0;
				curMediumCount = 0;
				curSmallCount = 0;
			}

			public boolean addCar(int carType) {

				if(carType == 1)
				{
					if(curBigCount == bigLimit) return false;
					curBigCount++;
					return true;
				}

				if(carType == 2)
				{
					if(curMediumCount == mediumLimit) return false;
					curMediumCount++;
					return true;
				}

				if(curSmallCount == smallLimit) return false;
				curSmallCount++;
				return true;
			}
		}

		/**
		* Your ParkingSystem object will be instantiated and called as such:
		* ParkingSystem obj = new ParkingSystem(big, medium, small);
		* boolean param_1 = obj.addCar(carType);
		*/
		```

      </details>

7. [Design Underground System](https://leetcode.com/problems/design-underground-system/description/)
   - [YT Solution](https://www.youtube.com/watch?v=AdRVFQo0l7w&list=PLpIkg8OmuX-JW5294URE-iwVhl_tdWEP5&index=8)
   -  <details>
        <summary>Click to expand code</summary>

		```java
		class UndergroundSystem {
			class Pair{
				String stationName;
				int time;

				Pair(String stName, int t)
				{
					stationName = stName;
					time = t;
				}
			}

			Map<Integer, Pair> checkInMap;
			Map<String, int[]> avgTimeMap; // start|end => {timeSum, timesTravelled}

			public UndergroundSystem() {
				checkInMap = new HashMap<>();
				avgTimeMap = new HashMap<>();
			}

			public void checkIn(int id, String stationName, int t) {
				checkInMap.put(id, new Pair(stationName, t));
			}

			public void checkOut(int id, String stationName, int t) {

				Pair p = checkInMap.get(id);

				String key = p.stationName + "|" + stationName;

				if(!avgTimeMap.containsKey(key))
					avgTimeMap.put(key, new int[2]);

				int[] keyPair = avgTimeMap.get(key);

				keyPair[0] += (t - p.time);
				keyPair[1]++;

				checkInMap.remove(id);
			}

			public double getAverageTime(String startStation, String endStation) {
				String key = startStation + "|" + endStation;

				if(!avgTimeMap.containsKey(key)) return 0;

				int[] keyPair = avgTimeMap.get(key);

				return ((double)keyPair[0])/keyPair[1];
			}
		}

		/**
		* Your UndergroundSystem object will be instantiated and called as such:
		* UndergroundSystem obj = new UndergroundSystem();
		* obj.checkIn(id,stationName,t);
		* obj.checkOut(id,stationName,t);
		* double param_3 = obj.getAverageTime(startStation,endStation);
		*/
		```

      </details>

8. ⭐ [Snapshot Array](https://leetcode.com/problems/snapshot-array/)
   - [YT Solution](https://www.youtube.com/watch?v=yEYoNCom72Q&list=PLpIkg8OmuX-JW5294URE-iwVhl_tdWEP5&index=9)
   -  <details>
        <summary>Click to expand code - Approach-1 (good)</summary>

		```java
		class SnapshotArray {
			// Index -> snapshot ID -> value at that snapshot
			Map<Integer, TreeMap<Integer, Integer>> data;
			int snapId;

			public SnapshotArray(int length) {
				data = new HashMap<>();

				for(int i = 0; i < length; i++) data.put(i, new TreeMap<>(){{
					put(0, 0);
				}});

				snapId = 0;
			}

			public void set(int index, int val) {
				data.get(index).put(snapId, val);
			}

			public int snap() {
				return snapId++;
			}

			public int get(int index, int snap_id) {
				// Version, value
				TreeMap<Integer, Integer> mp = data.get(index);
				int version = mp.floorKey(snap_id);
				return mp.get(version);
			}
		}

		/**
		* Your SnapshotArray object will be instantiated and called as such:
		* SnapshotArray obj = new SnapshotArray(length);
		* obj.set(index,val);
		* int param_2 = obj.snap();
		* int param_3 = obj.get(index,snap_id);
		*/
		```

      </details>

   -  <details>
        <summary>Click to expand code - Approach-2 (good)</summary>

		```java
		class SnapshotArray {

			private final TreeMap<Integer, Integer>[] data;
			private int snapId;

			@SuppressWarnings("unchecked")
			public SnapshotArray(int length) {
				data = new TreeMap[length];
			}

			public void set(int index, int val) {
				if (data[index] == null) {
					data[index] = new TreeMap<>();
					data[index].put(0, 0);
				}

				data[index].put(snapId, val);
			}

			public int snap() {
				return snapId++;
			}

			public int get(int index, int snapId) {
				if (data[index] == null) {
					return 0;
				}

				return data[index].floorEntry(snapId).getValue();
			}
		}
		```

      </details>

9. [Implement Stack using Queues](https://leetcode.com/problems/implement-stack-using-queues/)
   - [YT Solution](https://www.youtube.com/watch?v=LaBE0gNYCaM&list=PLpIkg8OmuX-JW5294URE-iwVhl_tdWEP5&index=10)
   -  <details>
        <summary>Click to expand code - Approach-1</summary>

		```java
		class MyStack {

			Queue<Integer> q1;
			Queue<Integer> q2;

			public MyStack() {
				q1 = new LinkedList<>();
				q2 = new LinkedList<>();
			}

			public void push(int x) {
				while(q1.size() > 0) q2.offer(q1.poll());
				q1.offer(x);
				while(q2.size() > 0) q1.offer(q2.poll());
			}

			public int pop() {
				return q1.poll();
			}

			public int top() {
				return q1.peek();
			}

			public boolean empty() {
				return q1.isEmpty();
			}
		}

		/**
		* Your MyStack object will be instantiated and called as such:
		* MyStack obj = new MyStack();
		* obj.push(x);
		* int param_2 = obj.pop();
		* int param_3 = obj.top();
		* boolean param_4 = obj.empty();
		*/
		```

      </details>

    -  <details>
         <summary>Click to expand code - Approach-2</summary>

		```java
		// Using only 1 queue
		class MyStack {

			Queue<Integer> q1;

			public MyStack() {
				q1 = new LinkedList<>();
			}

			public void push(int x) {
				int size = q1.size();
				q1.offer(x);
				while(size-->0) q1.offer(q1.poll());
			}

			public int pop() {
				return q1.poll();
			}

			public int top() {
				return q1.peek();
			}

			public boolean empty() {
				return q1.isEmpty();
			}
		}

		/**
		* Your MyStack object will be instantiated and called as such:
		* MyStack obj = new MyStack();
		* obj.push(x);
		* int param_2 = obj.pop();
		* int param_3 = obj.top();
		* boolean param_4 = obj.empty();
		*/
		```

       </details>

10. [Flatten Nested List Iterator](https://leetcode.com/problems/flatten-nested-list-iterator/)
    - [YT Solution](https://www.youtube.com/watch?v=0PFE_7S3X-U&list=PLpIkg8OmuX-JW5294URE-iwVhl_tdWEP5&index=12)
    -  <details>
         <summary>Click to expand code - Approach-1 (intuitve)</summary>

		```java
		/**
		 * // This is the interface that allows for creating nested lists.
		* // You should not implement it, or speculate about its implementation
		* public interface NestedInteger {
		*
		*     // @return true if this NestedInteger holds a single integer, rather than a nested list.
		*     public boolean isInteger();
		*
		*     // @return the single integer that this NestedInteger holds, if it holds a single integer
		*     // Return null if this NestedInteger holds a nested list
		*     public Integer getInteger();
		*
		*     // @return the nested list that this NestedInteger holds, if it holds a nested list
		*     // Return empty list if this NestedInteger holds a single integer
		*     public List<NestedInteger> getList();
		* }
		*/
		public class NestedIterator implements Iterator<Integer> {

			List<Integer> res;
			Iterator<Integer> itr;

			public NestedIterator(List<NestedInteger> nestedList) {
				res = new ArrayList<>();

				for(NestedInteger integer : nestedList)
				{
					if(integer.isInteger()) res.add(integer.getInteger());
					else{
						NestedIterator nestedItr = new NestedIterator(integer.getList());
						res.addAll(nestedItr.getList());
					}
				}

				itr = res.iterator();
			}

			List<Integer> getList(){ return res; }

			@Override
			public Integer next() {
				return itr.next();
			}

			@Override
			public boolean hasNext() {
				return itr.hasNext();
			}
		}

		/**
		* Your NestedIterator object will be instantiated and called as such:
		* NestedIterator i = new NestedIterator(nestedList);
		* while (i.hasNext()) v[f()] = i.next();
		*/
		```

       </details>

    -  <details>
         <summary>Click to expand code - Approach-2</summary>

		```java
		public class NestedIterator implements Iterator<Integer> {

			private final Deque<Iterator<NestedInteger>> stack;
			private Integer nextValue;

			public NestedIterator(List<NestedInteger> nestedList) {
				stack = new ArrayDeque<>();
				stack.push(nestedList.iterator());
			}

			@Override
			public Integer next() {
				Integer result = nextValue;
				nextValue = null;
				return result;
			}

			@Override
			public boolean hasNext() {

				// Already have the next integer buffered.
				if (nextValue != null) {
					return true;
				}

				while (!stack.isEmpty()) {

					Iterator<NestedInteger> itr = stack.peek();

					// Finished traversing this list.
					if (!itr.hasNext()) {
						stack.pop();
						continue;
					}

					NestedInteger current = itr.next();

					if (current.isInteger()) {
						nextValue = current.getInteger();
						return true;
					}

					// Traverse the nested list next.
					stack.push(current.getList().iterator());
				}

				return false;
			}
		}
		```

       </details>

11. [Seat Reservation Manager](https://leetcode.com/problems/seat-reservation-manager/description/)
    - [YT Solution](https://www.youtube.com/watch?v=fjwHZNvbr7g&list=PLpIkg8OmuX-JW5294URE-iwVhl_tdWEP5&index=13)
    -  <details>
         <summary>Click to expand  - Approach-1 (okayish)</summary>

		```java
		class SeatManager {

			TreeSet<Integer> seats;

			public SeatManager(int n) {
				seats = new TreeSet<>();
				for(int i = 1; i <=n ; i++) seats.add(i);
			}

			public int reserve() {
				int seat = seats.first();
				seats.remove(seat);
				return seat;
			}

			public void unreserve(int seatNumber) {
				seats.add(seatNumber);
			}
		}

		/**
		* Your SeatManager object will be instantiated and called as such:
		* SeatManager obj = new SeatManager(n);
		* int param_1 = obj.reserve();
		* obj.unreserve(seatNumber);
		*/
		```

       </details>

    -  <details>
         <summary>Click to expand  - Approach-2 (best)</summary>

		```java
		class SeatManager {

			private int nextSeat;
			private final PriorityQueue<Integer> availableSeats;

			public SeatManager(int n) {
				nextSeat = 1;
				availableSeats = new PriorityQueue<>();
			}

			public int reserve() {
				if (!availableSeats.isEmpty()) {
					return availableSeats.poll();
				}

				return nextSeat++;
			}

			public void unreserve(int seatNumber) {
				availableSeats.offer(seatNumber);
			}
		}
		```

       </details>

12. [Design a Food Rating System](https://leetcode.com/problems/design-a-food-rating-system/)
    - [YT Solution](https://www.youtube.com/watch?v=SF13GD8FPxM&list=PLpIkg8OmuX-JW5294URE-iwVhl_tdWEP5&index=14)
    -  <details>
         <summary>Click to expand code</summary>

		```java
		class FoodRatings {

			class FoodToCuisineMappingNode{
				String cuisine;
				Node node;

				FoodToCuisineMappingNode(String c, Node n)
				{
					cuisine = c;
					node = n;
				}
			}

			class Node{
				int rating;
				String food;

				Node(int r, String f)
				{
					rating = r;
					food = f;
				}
			}

			// cuisine -> set of nodes
			Map<String, TreeSet<Node>> cuisineMap;

			Comparator<Node> nodeComparator = (a,b) -> {
				if(a.rating != b.rating)
					return b.rating - a.rating;

				return a.food.compareTo(b.food);
			};

			// food -> node
			Map<String, FoodToCuisineMappingNode> foodToCuisineMap;

			public FoodRatings(String[] foods, String[] cuisines, int[] ratings) {

				cuisineMap = new HashMap<>();
				foodToCuisineMap = new HashMap<>();

				for(int i = 0; i < foods.length; i++)
				{
					Node node = new Node(ratings[i], foods[i]);

					String c = cuisines[i];

					if(!cuisineMap.containsKey(c))
						cuisineMap.put(c, new TreeSet<>(nodeComparator));

					cuisineMap.get(c).add(node);

					FoodToCuisineMappingNode mappingNode = new FoodToCuisineMappingNode(c, node);
					foodToCuisineMap.put(foods[i], mappingNode);
				}

			}

			public void changeRating(String food, int newRating) {
				FoodToCuisineMappingNode mappingNode = foodToCuisineMap.get(food);
				Node node = mappingNode.node;

				cuisineMap.get(mappingNode.cuisine).remove(node);
				node = new Node(newRating, food);
				cuisineMap.get(mappingNode.cuisine).add(node);

				foodToCuisineMap.put(food, new FoodToCuisineMappingNode(mappingNode.cuisine, node));
			}

			public String highestRated(String cuisine) {
				return cuisineMap.get(cuisine).first().food;
			}
		}

		/**
		* Your FoodRatings object will be instantiated and called as such:
		* FoodRatings obj = new FoodRatings(foods, cuisines, ratings);
		* obj.changeRating(food,newRating);
		* String param_2 = obj.highestRated(cuisine);
		*/
		```

       </details>

    -  <details>
         <summary>Click to expand code</summary>

		```java
		class FoodRatings {

			private static class Food {
				String name;
				String cuisine;
				int rating;

				Food(String name, String cuisine, int rating) {
					this.name = name;
					this.cuisine = cuisine;
					this.rating = rating;
				}
			}

			private final Comparator<Food> comparator = (a, b) -> {
				int cmp = Integer.compare(b.rating, a.rating);

				if (cmp != 0) {
					return cmp;
				}

				return a.name.compareTo(b.name);
			};

			private final Map<String, Food> foodMap;
			private final Map<String, TreeSet<Food>> cuisineMap;

			public FoodRatings(String[] foods, String[] cuisines, int[] ratings) {

				foodMap = new HashMap<>();
				cuisineMap = new HashMap<>();

				for (int i = 0; i < foods.length; i++) {

					Food food = new Food(
						foods[i],
						cuisines[i],
						ratings[i]
					);

					foodMap.put(food.name, food);

					cuisineMap
						.computeIfAbsent(food.cuisine, c -> new TreeSet<>(comparator))
						.add(food);
				}
			}

			public void changeRating(String foodName, int newRating) {

				Food food = foodMap.get(foodName);

				TreeSet<Food> foods = cuisineMap.get(food.cuisine);

				foods.remove(food);

				food.rating = newRating;

				foods.add(food);
			}

			public String highestRated(String cuisine) {
				return cuisineMap.get(cuisine).first().name;
			}
		}
		```

       </details>


13. [Most Frequent IDs]()
    - [YT Solution](https://www.youtube.com/watch?v=saAEj_iL_FQ&list=PLpIkg8OmuX-JW5294URE-iwVhl_tdWEP5&index=15)
    -  <details>
         <summary>Click to expand code</summary>

		```java
		class Solution {
		}
		```

       </details>

<!--
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
