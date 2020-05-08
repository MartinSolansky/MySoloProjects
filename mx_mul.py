#!/usr/bin/python3
# Matrix multiplication utility without any mathematical library.
# All variables are handled at runtime

class Matrix:
    def __init__(self, name):
        self.name = name
        self.dimensions = self.define_itself()
        self.width = self.dimensions[0]
        self.height = self.dimensions[1]
        self.body = []

    @staticmethod
    def get_dimension(dimension_name):
        while True:
            try:
                dimension = int(input(f"{dimension_name}: "))
                return dimension
            except ValueError:
                print("This is not valid data. Please enter valid dimension")
                continue

    def define_itself(self):
        """This function will prompt user to input width and height parameters of given matrix"""
        print(f"Matrix {self.name} dimensions:")
        a_width = self.get_dimension("width")
        a_height = self.get_dimension("height")
        return a_width, a_height

    def construct_itself(self):
        """Function which prompt user to input elements (as integers) of matrix
        and than create matrix (as list of rows with lists of row_elements)"""
        result = []
        print(f"Matrix {self.name} values:")
        for _ in range(self.height):
            while True:
                try:
                    row = list(map(int, input("").split()))
                    if len(row) < self.width or len(row) > self.width:
                        print(f"Invalid row: Row need to be {self.width} numbers long and separated by spaces.")
                        continue
                    result.append(row)
                    break
                except ValueError:
                    print("Elements have to be number!")
                    continue
        print("")
        self.body = result

    def __mul__(self, other):
        """Determination od multiplication of Matrix elements"""
        new_matrix = []
        for row in self.body:
            new_row = []
            for r in range(len(other.body[0])):
                partial_result = 0
                for n, number in enumerate(row):
                    partial_result += (number * other.body[n][r])
                new_row.append(str(partial_result))
            new_matrix.append(new_row)
        return new_matrix



def printing_result(operation_result):
    """Function report resulting matrix to console"""
    for result_row in operation_result:
        print(" ".join(result_row))

def availability_check(matrix1: Matrix, matrix2: Matrix):
    """Function check if matrix1.width == matrix2.height (i.e. multiplication rule)
    and return inverted bool value of test to keep/terminate prompt cycle"""
    if matrix1.width == matrix2.height:
        return False
    else:
        print("These two matrices cannot be multiplied!\n\nNew multiplication:")
        return True

def main():
    """Utility body, returns list corresponding to multiplication"""
    loop = True
    while loop:
        matrixA = Matrix("A")
        print("")
        matrixB = Matrix("B")
        print("")
        loop = availability_check(matrixA, matrixB)
    matrixA.construct_itself()
    matrixB.construct_itself()
    print("Resulting matrix:")
    return matrixA * matrixB


if __name__ == "__main__":
    try:
        mul_result = main()
        printing_result(mul_result)

    except KeyboardInterrupt:
        print("\nEnding signal detected.\nEnd of the utility" + "."*30)
