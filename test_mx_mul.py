import mx_mul as utility
import pytest


@pytest.mark.parametrize("dimension_name, user_input, result",
                         [("height", "3", 3),
                          ("height", "1", 1)]
                         )
def test_input_dimension(dimension_name, user_input, result):
    utility.input = lambda x: user_input
    output = utility.Matrix.get_dimension(f"{dimension_name}")
    assert output == result


@pytest.mark.parametrize("dimension_name, user_input",
                         [("height", "Ahoj"),
                          ("height", "-1"),
                          ("height", "0")]
                         )
def test_input_dimension_nonsense(dimension_name, user_input):
    prints = []
    expected_result = "This is not valid data. Please enter valid dimension.\nRemaining attempts: 0"
    utility.input = lambda x: user_input
    utility.print = lambda y: prints.append(y)
    with pytest.raises(KeyboardInterrupt):
        utility.Matrix.get_dimension(f"{dimension_name}")
    assert expected_result == prints.pop()


@pytest.fixture
def create_valid_matrix() -> utility.Matrix:
    dimension = 2
    utility.input = lambda x: dimension
    test_matrix = utility.Matrix("A")
    return test_matrix


def test_define_itself(create_valid_matrix):
    test_matrix = create_valid_matrix
    assert test_matrix.dimensions == (2, 2)


def test_construct_itself(create_valid_matrix):
    test_matrix = create_valid_matrix
    assert test_matrix.body == []
    utility.input = lambda x: "2 2"
    test_matrix.construct_itself()
    assert test_matrix.body == [[2, 2], [2, 2]]


def test_multiplication(create_valid_matrix):
    matrix1 = create_valid_matrix
    matrix1.body = [[2, 2], [2, 2]]
    matrix2 = create_valid_matrix
    matrix2.body = [[2, 2], [2, 2]]
    expected_result = [["8", "8"], ["8", "8"]]
    assert (matrix1*matrix2) == expected_result
