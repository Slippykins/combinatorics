from sympy.utilities.iterables import multiset_permutations


def main():
    # input params
    shape = (5, 4, 3, 1)
    type = (4, 3, 3, 2, 1)
    objects = [x + 1 for x in range(len(type))]

    numbers_to_place = []
    for i, object in enumerate(objects):
        # objects[0] is always placed in the first type[0] positions of row 1
        if i == 0:
            continue
        numbers_to_place += [object] * type[i]

    num_valid_tableau = 0

    # a tableau (valid or invalid) is just a multiset permutation of the numbers to be placed, ordered by rows
    for perm in multiset_permutations(numbers_to_place):
        # create the tableau
        tableau = []
        for i, row_length in enumerate(shape):
            if i == 0:
                row = [objects[0]] * type[0]
                row.extend(perm[: row_length - type[0]])
            else:
                offset = sum(shape[:i]) - type[0]
                row = perm[offset : offset + row_length]
            tableau.append(row)

        # check the tableau
        valid_flag = check_tableau(tableau)

        if valid_flag:
            num_valid_tableau += 1
            print(tableau)

    print(f"Valid tableau found: {num_valid_tableau}")


def check_tableau(tableau: list[list[int]]):
    # check rows
    for row in tableau:
        for i, entry in enumerate(row):
            if i > 0:
                # SSYT condition: rows must be non-decreasing
                if entry < row[i - 1]:
                    return False

    # check columns
    for column in range(len(tableau[0])):
        for row in range(len(tableau)):
            if row > 0:
                # if the row doesn't extend to the current column, skip
                if len(tableau[row]) < column + 1:
                    continue
                else:
                    # SSYT condition: columns must be strictly increasing
                    if tableau[row][column] <= tableau[row - 1][column]:
                        return False

    return True


if __name__ == "__main__":
    main()
