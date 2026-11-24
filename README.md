# Linked List 2

Python ADT PDF:     
https://drive.google.com/file/d/1jXGQdSvuUYjGXl-PUuHMUzKWEBGQoARL/view?usp=sharing

Python Exception handling:     
https://drive.google.com/file/d/1JaPWKbfL4jOw8IPTJo67dFypR-BhDm3t/view?usp=sharing

**Rules for this assignment**

- The linked list is stored in a global **2D array** called `LinkedList` with
  **10** nodes. Each node is a list: `[Data, Pointer]`.
- `FirstNode` stores the index of the first node in the linked list (`-1` = empty).
- `FirstEmpty` stores the index of the first node in the **free list** (`-1` = full).

**The example linked list**

Most tests use this list. The data is **not** in order in the array — only the
**pointers** give the order.

    Index   Data   Pointer
      0      25       3
      1      -1       5
      2      10       0      ← FirstNode = 2
      3      40       6
      4      -1       1      ← FirstEmpty = 4
      5      -1       7
      6      55      -1
      7      -1       8
      8      77       9      (old data — this node is in the free list)
      9      -1      -1

    Linked list:  2 → 0 → 3 → 6              10, 25, 40, 55
    Free list:    4 → 1 → 5 → 7 → 8 → 9

---

## Exercise 1

**(a)** Write program code for the procedure `Initialise()`.

`Initialise()`

- Sets `LinkedList` to **10** nodes. Every node has data `-1` and points to
  the **next** node. The last node points to `-1`.
- Sets `FirstNode` to `-1` and `FirstEmpty` to `0`.
- It must **reset** the list — calling it again empties a list that has items.

After `Initialise()`:

    [[-1, 1], [-1, 2], [-1, 3], [-1, 4], [-1, 5], [-1, 6], [-1, 7], [-1, 8], [-1, 9], [-1, -1]]

**(b)** Write program code for the procedure `OutputNodes()`.

`OutputNodes()`

- **Outputs** (prints) the data of every node in the linked list, in linked-list
  order, **one per line**.
- If the linked list is empty, outputs `Linked list is empty`
- Must not change the linked list.

**Example (the example list):**

    Input:
      OutputNodes()

    Output:
      10
      25
      40
      55

---

## Exercise 2

Write program code for the function `InsertInOrder(Item)`.

`InsertInOrder(Item)`

- Inserts `Item` into the linked list so the list **stays in ascending order**.
- Uses the node at `FirstEmpty` for the new item.
- Returns `True` if the item was inserted, `False` if there are no free nodes.

Think about **all** the places a new node can go:

1. The list is **empty**
2. The new item is **smaller** than the first item → it becomes the new first node
3. **In the middle** → the previous node must point to the new node
4. **At the end** → the new node points to `-1`

If the same value is already in the list, put the new item **after** it.

**Example (the example list):**

    Input:
      print(InsertInOrder(30))
      OutputNodes()
      print(FirstEmpty)

    Output:
      True
      10
      25
      30
      40
      55
      1

What changed:

    Index   Data   Pointer
      0      25       4      ← used to point to 3, now points to the new node
      4      30       3      ← the new node, points to 40

*Hint:* take the node off the free list (`FirstEmpty = LinkedList[NewNode][1]`)
**before** you change the new node's pointer.

---

## Exercise 3

Write program code for the function `Delete(Item)`.

`Delete(Item)`

- Removes the **first** node that holds `Item` from the linked list.
- The deleted node is added to the **front** of the free list: its data is set
  to `-1`, it points to the old `FirstEmpty`, and it becomes the new `FirstEmpty`.
- Returns `True` if the item was deleted, `False` if `Item` is not in the linked
  list (and nothing changes).

**Example (the example list):**

    Input:
      print(Delete(40))
      OutputNodes()
      print(FirstEmpty)
      print(Delete(77))

    Output:
      True
      10
      25
      55
      3
      False

`Delete(77)` is `False` — node 8 holds `77`, but it is in the free list, not in
the linked list.

What changed after `Delete(40)`:

    Index   Data   Pointer
      0      25       6      ← skips over node 3
      3      -1       4      ← deleted node, now at the front of the free list

    Free list:  3 → 4 → 1 → 5 → 7 → 8 → 9

---

## Exercise 4

Write program code for the function `LoadFromFile(FileName)`.

`LoadFromFile(FileName)`

- Calls `Initialise()` first, so the linked list starts empty.
- Opens the text file `FileName`. Each line of the file holds one whole number.
- Inserts each number into the linked list using `InsertInOrder()`.
- If the linked list becomes full, the remaining numbers are not stored.
- Returns the **number of items** that were stored in the linked list.
- If the file does not exist, outputs `File not found` and returns `-1`.
  Use **exception handling** (`try` / `except`).

**Example:**

`numbers.txt` contains:

    30
    10
    20

    Input:
      print(LoadFromFile("numbers.txt"))
      OutputNodes()
      print(LoadFromFile("missing.txt"))

    Output:
      3
      10
      20
      30
      File not found
      -1

To try it yourself, create `numbers.txt` next to `assignment.py`.

---

## Exercise 5

Write program code for the procedure `Reverse()`.

`Reverse()`

- Reverses the order of the linked list by **changing the pointers only**.
- The data must **not** move — every node keeps its data at the same index.
- The free list must not change.

**Example (the example list):**

    Input:
      Reverse()
      OutputNodes()
      print(FirstNode)

    Output:
      55
      40
      25
      10
      6

After `Reverse()`:

    Index   Data   Pointer
      0      25       2
      2      10      -1      ← now the last node
      3      40       0
      6      55       3      ← FirstNode = 6

*Hint:* walk through the list with three variables — `Previous`, `Current` and
`NextNode`. Save `NextNode` **before** you change `Current`'s pointer, or you
lose the rest of the list.

