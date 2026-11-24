# Linked List

Read the Abstract Data Types lecture (Linked List section) before you start.
https://drive.google.com/file/d/1jXGQdSvuUYjGXl-PUuHMUzKWEBGQoARL/view?usp=sharing

**Rules for this assignment**

- The linked list is stored in a **2D array** called `LinkedList`. Each node is
  a list of two items: `[Data, Pointer]`.
- A pointer is the **index of the next node**. A pointer of `-1` means
  "points to nothing".
- `FirstNode` is the index of the first node in the linked list.
- `FirstEmpty` is the index of the first node in the **free list** (the empty nodes).
- Functions **return** their answer — do not print.
- Every function that changes `LinkedList`, `FirstNode` or `FirstEmpty` needs:
  `global LinkedList, FirstNode, FirstEmpty`


**The example linked list**

Exercises 2–6 are tested on this list. Notice the data is **not** in order in
the array — only the **pointers** give the order.

    Index   Data   Pointer
      0      30       4
      1      -1       3
      2      10       5      ← FirstNode = 2
      3      -1       6
      4      40      -1
      5      20       0
      6      99       7      (old data — this node is in the free list)
      7      -1      -1

    FirstNode = 2       Linked list:  2 → 5 → 0 → 4        10, 20, 30, 40
    FirstEmpty = 1      Free list:    1 → 3 → 6 → 7

---

## Exercise 1

**Problem:**

Set up an **empty** linked list with **8** nodes.

- `LinkedList` → a global 2D array of 8 nodes. Every node starts with data `-1`.
  Each node points to the **next** node, and the last node points to `-1`.
- `FirstNode` → `-1` (the linked list is empty)
- `FirstEmpty` → `0` (every node is in the free list, starting at node 0)

The array must look like this:

    [[-1, 1], [-1, 2], [-1, 3], [-1, 4], [-1, 5], [-1, 6], [-1, 7], [-1, -1]]

Then write two functions:

`IsEmpty()`

- Return `True` if the linked list has no nodes (`FirstNode` is `-1`), otherwise `False`

`IsFull()`

- Return `True` if there are no free nodes left (`FirstEmpty` is `-1`), otherwise `False`

**Careful:** build the array with a loop and `.append()`. Do **not** write
`[[-1, -1]] * 8` — that makes 8 copies of the **same** row, so changing one
row changes all of them.

---

## Exercise 2

**Problem:**

`Traverse()`

Return a list of the data in the linked list, **in linked-list order**.
Return `[]` if the list is empty. Do **not** change the linked list.

1. Start at `FirstNode`
2. While the current pointer is not `-1`:
    - add the data of the current node to your answer
    - move to the next node: `Current = LinkedList[Current][1]`

**Example (the example list):**

    Input:
      print(Traverse())

    Output:
      [10, 20, 30, 40]

*Hint:* if your answer is `[30, 10, 40, 20, 99]` you are reading the array
from top to bottom. Follow the **pointers** instead.

---

## Exercise 3

**Problem:**

Write two functions that follow the pointers, just like `Traverse()`.

`Search(Item)`

- Return the **index** of the node that holds `Item`
- Return `-1` if `Item` is not in the linked list

`CountNodes()`

- Return how many nodes are in the linked list

**Example (the example list):**

    Input:                 Output:
      Search(20)             5
      Search(40)             4
      Search(99)             -1
      CountNodes()           4

`Search(99)` is `-1`: node 6 still holds `99`, but node 6 is in the free
list, **not** in the linked list. Only follow pointers from `FirstNode`.

---

## Exercise 4

**Problem:**

`InsertFront(Item)`

Add `Item` as the new **first** node. Return `True`, or `False` if there are no
free nodes.

1. If there are no free nodes, return `False`
2. Take the first free node: `NewNode = FirstEmpty`
3. Move `FirstEmpty` to the next free node — **before** you change `NewNode`'s pointer!
4. Store `Item` in the new node, and point it to the old first node
5. The new node is now the first node: `FirstNode = NewNode`

**Example (the example list):**

    Input:
      print(InsertFront(5))
      print(Traverse())
      print(FirstNode, FirstEmpty)

    Output:
      True
      [5, 10, 20, 30, 40]
      1 3

Node 1 is now `[5, 2]` — it holds 5 and points to node 2 (the old first node).

---

## Exercise 5

**Problem:**

`InsertEnd(Item)`

Add `Item` as the new **last** node. Return `True`, or `False` if there are no
free nodes.

1. If there are no free nodes, return `False`
2. Take the first free node and move `FirstEmpty` on (like Exercise 4)
3. Store `Item` in the new node, and set its pointer to `-1` — it will be last
4. If the list was **empty**, the new node becomes `FirstNode`
5. Otherwise follow the pointers to the **last** node (the one whose pointer
   is `-1`), and point it to the new node

**Example (the example list):**

    Input:
      print(InsertEnd(50))
      print(Traverse())

    Output:
      True
      [10, 20, 30, 40, 50]

Node 1 is now `[50, -1]`, and node 4 (holding 40) changed from `[40, -1]` to `[40, 1]`.

---

## Exercise 6

**Problem:**

`Delete(Item)`

Remove the node holding `Item` from the linked list. Return `True`, or `False`
if `Item` is not in the list (and change nothing).

1. Follow the pointers from `FirstNode`, remembering the **previous** node as
   you go, until you find `Item` or reach `-1`
2. Not found → return `False`
3. If it is the **first** node → `FirstNode` moves to the next node
4. Otherwise → the previous node's pointer **skips over** the deleted node
5. Give the deleted node back to the **front** of the free list:
   set its data to `-1`, point it to the old `FirstEmpty`, and make it the new `FirstEmpty`

**Example (the example list):**

    Input:
      print(Delete(30))
      print(Traverse())
      print(FirstEmpty)

    Output:
      True
      [10, 20, 40]
      0

What changed:

    Index   Data   Pointer
      0      -1       1      ← deleted node, now at the front of the free list
      5      20       4      ← used to point to 0 (30), now skips to 4 (40)

    Free list:  0 → 1 → 3 → 6 → 7

