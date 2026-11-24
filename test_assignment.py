import importlib

import pytest

import assignment


@pytest.fixture
def q():
    return importlib.reload(assignment)


SAMPLE = [
    [30, 4],
    [-1, 3],
    [10, 5],
    [-1, 6],
    [40, -1],
    [20, 0],
    [99, 7],
    [-1, -1],
]


def build(q, nodes, first, empty):
    q.LinkedList = []
    for node in nodes:
        q.LinkedList.append([node[0], node[1]])
    q.FirstNode = first
    q.FirstEmpty = empty


def build_sample(q):
    build(q, SAMPLE, 2, 1)


def build_full(q):
    nodes = []
    for x in range(8):
        nodes.append([(x + 1) * 10, x + 1])
    nodes[7][1] = -1
    build(q, nodes, 0, -1)


def walk(q, start):
    items = []
    current = start
    steps = 0
    while current != -1 and steps < 20:
        items.append(current)
        current = q.LinkedList[current][1]
        steps = steps + 1
    return items


def data_in_list(q):
    values = []
    for index in walk(q, q.FirstNode):
        values.append(q.LinkedList[index][0])
    return values


def test1_initial_list(q):
    assert q.LinkedList == [
        [-1, 1],
        [-1, 2],
        [-1, 3],
        [-1, 4],
        [-1, 5],
        [-1, 6],
        [-1, 7],
        [-1, -1],
    ]
    assert q.FirstNode == -1
    assert q.FirstEmpty == 0


def test1_rows_are_separate(q):
    q.LinkedList[0][0] = 55
    assert q.LinkedList[1][0] == -1
    assert q.LinkedList[7][0] == -1


def test1_is_empty(q):
    assert q.IsEmpty() == True
    build_sample(q)
    assert q.IsEmpty() == False


def test1_is_full(q):
    assert q.IsFull() == False
    build_sample(q)
    assert q.IsFull() == False
    build_full(q)
    assert q.IsFull() == True


def test2_traverse(q):
    build_sample(q)
    assert q.Traverse() == [10, 20, 30, 40]


def test2_traverse_empty(q):
    assert q.Traverse() == []
    build(q, [[7, -1], [-1, -1]], 0, 1)
    assert q.Traverse() == [7]


def test2_traverse_keeps_list(q):
    build_sample(q)
    q.Traverse()
    q.Traverse()
    assert q.LinkedList == SAMPLE
    assert q.FirstNode == 2
    assert q.FirstEmpty == 1
    assert q.Traverse() == [10, 20, 30, 40]


@pytest.mark.parametrize("item, expected", [
    [10, 2],
    [20, 5],
    [30, 0],
    [40, 4],
    [99, -1],
    [7, -1],
])
def test3_search(q, item, expected):
    build_sample(q)
    assert q.Search(item) == expected


def test3_count_nodes(q):
    assert q.CountNodes() == 0
    build_sample(q)
    assert q.CountNodes() == 4
    build(q, [[7, -1], [-1, -1]], 0, 1)
    assert q.CountNodes() == 1
    build_full(q)
    assert q.CountNodes() == 8


def test4_insert_front_empty(q):
    assert q.InsertFront(10) == True
    assert q.FirstNode == 0
    assert q.FirstEmpty == 1
    assert q.LinkedList[0] == [10, -1]
    assert q.InsertFront(20) == True
    assert q.FirstNode == 1
    assert q.FirstEmpty == 2
    assert q.LinkedList[1] == [20, 0]
    assert data_in_list(q) == [20, 10]


def test4_insert_front_sample(q):
    build_sample(q)
    assert q.InsertFront(5) == True
    assert q.FirstNode == 1
    assert q.LinkedList[1] == [5, 2]
    assert q.FirstEmpty == 3
    assert data_in_list(q) == [5, 10, 20, 30, 40]
    assert walk(q, q.FirstEmpty) == [3, 6, 7]


def test4_insert_front_when_full(q):
    build_full(q)
    assert q.InsertFront(5) == False
    assert q.FirstNode == 0
    assert data_in_list(q) == [10, 20, 30, 40, 50, 60, 70, 80]


def test5_insert_end_empty(q):
    assert q.InsertEnd(10) == True
    assert q.FirstNode == 0
    assert q.FirstEmpty == 1
    assert q.LinkedList[0] == [10, -1]
    assert q.InsertEnd(20) == True
    assert q.LinkedList[0] == [10, 1]
    assert q.LinkedList[1] == [20, -1]
    assert data_in_list(q) == [10, 20]


def test5_insert_end_sample(q):
    build_sample(q)
    assert q.InsertEnd(50) == True
    assert q.FirstNode == 2
    assert q.LinkedList[1] == [50, -1]
    assert q.LinkedList[4] == [40, 1]
    assert q.FirstEmpty == 3
    assert data_in_list(q) == [10, 20, 30, 40, 50]
    assert walk(q, q.FirstEmpty) == [3, 6, 7]


def test5_insert_end_when_full(q):
    build_full(q)
    assert q.InsertEnd(90) == False
    assert data_in_list(q) == [10, 20, 30, 40, 50, 60, 70, 80]
    q2 = importlib.reload(assignment)
    for x in range(8):
        assert q2.InsertEnd(x) == True
    assert q2.InsertEnd(8) == False
    assert data_in_list(q2) == [0, 1, 2, 3, 4, 5, 6, 7]


def test6_delete_middle_and_last(q):
    build_sample(q)
    assert q.Delete(30) == True
    assert q.LinkedList[5] == [20, 4]
    assert data_in_list(q) == [10, 20, 40]
    assert q.Delete(40) == True
    assert q.LinkedList[5] == [20, -1]
    assert data_in_list(q) == [10, 20]


def test6_delete_first(q):
    build_sample(q)
    assert q.Delete(10) == True
    assert q.FirstNode == 5
    assert data_in_list(q) == [20, 30, 40]
    assert q.Delete(20) == True
    assert q.Delete(30) == True
    assert q.Delete(40) == True
    assert q.FirstNode == -1
    assert data_in_list(q) == []


def test6_not_found(q):
    build_sample(q)
    assert q.Delete(99) == False
    assert q.Delete(7) == False
    assert q.LinkedList == SAMPLE
    assert q.FirstNode == 2
    assert q.FirstEmpty == 1
    q2 = importlib.reload(assignment)
    assert q2.Delete(10) == False


def test6_node_goes_back_to_free_list(q):
    build_sample(q)
    q.Delete(30)
    assert q.LinkedList[0] == [-1, 1]
    assert q.FirstEmpty == 0
    assert walk(q, q.FirstEmpty) == [0, 1, 3, 6, 7]
    q.Delete(10)
    assert q.LinkedList[2] == [-1, 0]
    assert q.FirstEmpty == 2
    assert walk(q, q.FirstEmpty) == [2, 0, 1, 3, 6, 7]
