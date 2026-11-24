import ast
import importlib
import inspect
import textwrap

import pytest

import assignment


@pytest.fixture
def q():
    return importlib.reload(assignment)


SAMPLE = [
    [25, 3],
    [-1, 5],
    [10, 0],
    [40, 6],
    [-1, 1],
    [-1, 7],
    [55, -1],
    [-1, 8],
    [77, 9],
    [-1, -1],
]

EMPTY = [
    [-1, 1],
    [-1, 2],
    [-1, 3],
    [-1, 4],
    [-1, 5],
    [-1, 6],
    [-1, 7],
    [-1, 8],
    [-1, 9],
    [-1, -1],
]


def calls_in(function):
    tree = ast.parse(textwrap.dedent(inspect.getsource(function)))
    names = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                names.append(node.func.id)
            if isinstance(node.func, ast.Attribute):
                names.append("." + node.func.attr)
    return names


def build(q, nodes, first, empty):
    q.LinkedList = []
    for node in nodes:
        q.LinkedList.append([node[0], node[1]])
    q.FirstNode = first
    q.FirstEmpty = empty


def build_sample(q):
    build(q, SAMPLE, 2, 4)


def build_empty(q):
    build(q, EMPTY, -1, 0)


def build_full(q):
    nodes = []
    for x in range(10):
        nodes.append([(x + 1) * 10, x + 1])
    nodes[9][1] = -1
    build(q, nodes, 0, -1)


def walk(q, start):
    items = []
    current = start
    steps = 0
    while current != -1 and steps < 25:
        items.append(current)
        current = q.LinkedList[current][1]
        steps = steps + 1
    return items


def data_in_list(q):
    values = []
    for index in walk(q, q.FirstNode):
        values.append(q.LinkedList[index][0])
    return values


def test1_initialise(q):
    q.Initialise()
    assert q.LinkedList == EMPTY
    assert q.FirstNode == -1
    assert q.FirstEmpty == 0
    q.LinkedList[0][0] = 55
    assert q.LinkedList[1][0] == -1
    assert q.LinkedList[9][0] == -1


def test1_initialise_resets(q):
    build_sample(q)
    q.Initialise()
    assert q.LinkedList == EMPTY
    assert q.FirstNode == -1
    assert q.FirstEmpty == 0


def test1_output_nodes(q, capsys):
    build_sample(q)
    q.OutputNodes()
    assert capsys.readouterr().out == "10\n25\n40\n55\n"
    assert q.LinkedList == SAMPLE
    assert q.FirstNode == 2


def test1_output_empty(q, capsys):
    build_empty(q)
    q.OutputNodes()
    assert capsys.readouterr().out == "Linked list is empty\n"


def test2_insert_into_empty(q):
    build_empty(q)
    assert q.InsertInOrder(30) == True
    assert q.FirstNode == 0
    assert q.FirstEmpty == 1
    assert q.LinkedList[0] == [30, -1]
    assert data_in_list(q) == [30]


def test2_insert_middle(q):
    build_sample(q)
    assert q.InsertInOrder(30) == True
    assert q.LinkedList[4] == [30, 3]
    assert q.LinkedList[0] == [25, 4]
    assert q.FirstNode == 2
    assert q.FirstEmpty == 1
    assert data_in_list(q) == [10, 25, 30, 40, 55]
    assert walk(q, q.FirstEmpty) == [1, 5, 7, 8, 9]


def test2_insert_new_first(q):
    build_sample(q)
    assert q.InsertInOrder(5) == True
    assert q.FirstNode == 4
    assert q.LinkedList[4] == [5, 2]
    assert data_in_list(q) == [5, 10, 25, 40, 55]


def test2_insert_new_last(q):
    build_sample(q)
    assert q.InsertInOrder(60) == True
    assert q.LinkedList[4] == [60, -1]
    assert q.LinkedList[6] == [55, 4]
    assert data_in_list(q) == [10, 25, 40, 55, 60]


def test2_insert_many(q):
    build_empty(q)
    for item in [50, 20, 80, 20, 10, 60, 90, 30, 70, 40]:
        assert q.InsertInOrder(item) == True
    assert data_in_list(q) == [10, 20, 20, 30, 40, 50, 60, 70, 80, 90]
    assert q.FirstEmpty == -1
    assert q.InsertInOrder(15) == False
    assert data_in_list(q) == [10, 20, 20, 30, 40, 50, 60, 70, 80, 90]


def test3_delete_middle_and_last(q):
    build_sample(q)
    assert q.Delete(40) == True
    assert q.LinkedList[0] == [25, 6]
    assert data_in_list(q) == [10, 25, 55]
    assert q.Delete(55) == True
    assert q.LinkedList[0] == [25, -1]
    assert data_in_list(q) == [10, 25]


def test3_delete_first(q):
    build_sample(q)
    assert q.Delete(10) == True
    assert q.FirstNode == 0
    assert data_in_list(q) == [25, 40, 55]
    for item in [25, 40, 55]:
        assert q.Delete(item) == True
    assert q.FirstNode == -1
    assert data_in_list(q) == []


def test3_not_found(q):
    build_sample(q)
    assert q.Delete(77) == False
    assert q.Delete(30) == False
    assert q.LinkedList == SAMPLE
    assert q.FirstNode == 2
    assert q.FirstEmpty == 4
    build_empty(q)
    assert q.Delete(10) == False


def test3_node_goes_back_to_free_list(q):
    build_sample(q)
    q.Delete(40)
    assert q.LinkedList[3] == [-1, 4]
    assert q.FirstEmpty == 3
    assert walk(q, q.FirstEmpty) == [3, 4, 1, 5, 7, 8, 9]
    q.Delete(10)
    assert q.LinkedList[2] == [-1, 3]
    assert q.FirstEmpty == 2
    assert walk(q, q.FirstEmpty) == [2, 3, 4, 1, 5, 7, 8, 9]


def test4_load_from_file(q, tmp_path):
    path = tmp_path / "numbers.txt"
    path.write_text("30\n10\n20\n")
    assert q.LoadFromFile(str(path)) == 3
    assert data_in_list(q) == [10, 20, 30]
    assert q.FirstEmpty == 3


def test4_load_too_many(q, tmp_path):
    path = tmp_path / "numbers.txt"
    path.write_text("12\n5\n33\n8\n41\n19\n27\n2\n50\n16\n38\n1")
    assert q.LoadFromFile(str(path)) == 10
    assert data_in_list(q) == [2, 5, 8, 12, 16, 19, 27, 33, 41, 50]


def test4_load_starts_empty(q, tmp_path):
    build_sample(q)
    path = tmp_path / "numbers.txt"
    path.write_text("7\n3\n")
    assert q.LoadFromFile(str(path)) == 2
    assert data_in_list(q) == [3, 7]
    names = calls_in(q.LoadFromFile)
    assert "InsertInOrder" in names, "LoadFromFile() must call InsertInOrder()."


def test4_file_not_found(q, tmp_path, capsys):
    assert q.LoadFromFile(str(tmp_path / "missing.txt")) == -1
    assert "File not found" in capsys.readouterr().out


def test5_reverse(q):
    build_sample(q)
    q.Reverse()
    assert data_in_list(q) == [55, 40, 25, 10]
    assert q.FirstNode == 6
    assert q.LinkedList[2] == [10, -1]
    assert q.FirstEmpty == 4
    assert walk(q, q.FirstEmpty) == [4, 1, 5, 7, 8, 9]


def test5_data_does_not_move(q):
    build_sample(q)
    q.Reverse()
    assert data_in_list(q) == [55, 40, 25, 10]
    for index in [0, 2, 3, 6]:
        assert q.LinkedList[index][0] == SAMPLE[index][0]
    q.Reverse()
    assert q.LinkedList == SAMPLE
    assert q.FirstNode == 2


def test5_reverse_small(q):
    build_empty(q)
    q.Reverse()
    assert q.FirstNode == -1
    assert q.LinkedList == EMPTY
    build(q, [[-1, 2], [8, -1], [-1, -1]], 1, 0)
    q.Reverse()
    assert q.FirstNode == 1
    assert q.LinkedList == [[-1, 2], [8, -1], [-1, -1]]
    build_full(q)
    q.Reverse()
    assert data_in_list(q) == [100, 90, 80, 70, 60, 50, 40, 30, 20, 10]
