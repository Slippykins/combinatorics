import numpy as np
import pandas as pd
from copy import deepcopy
from sympy.utilities.iterables import partitions, multiset_permutations

valid_matrices = []
row_number = 0


def main():
    # input params
    integer_to_partition = 10
    entries_01_only = False

    output = {}
    for lambda_partition in partitions(integer_to_partition):
        lambda_partition = convert_partition_to_list(lambda_partition)
        lambda_partition = sorted(lambda_partition, reverse=True)

        output[str(lambda_partition)] = {}

        for mu_partition in partitions(integer_to_partition):
            # reset global vars
            global valid_matrices, row_number
            valid_matrices = []
            row_number = 0

            mu_partition = convert_partition_to_list(mu_partition)
            mu_partition = sorted(mu_partition, reverse=True)

            current_matrix = [[0] * len(mu_partition)] * len(lambda_partition)

            iterate_over_row(row_sums=lambda_partition,
                             col_sums=mu_partition,
                             current_matrix=current_matrix,
                             entries_01_only=entries_01_only)

            output[str(lambda_partition)][str(mu_partition)] = len(valid_matrices)

    matrix = pd.DataFrame(output, columns=sorted(output.keys()), index=sorted(output.keys()))

    print(f"Transition matrix:\n{matrix.values}\n")
    print(f"Inverse transition matrix:\n{np.round(np.linalg.inv(matrix.values), 0)}\n")
    print(f"Order of partitions: {sorted(output.keys())}")


def iterate_over_row(row_sums: list, col_sums: list, current_matrix: list[list], entries_01_only: bool):
    global row_number
    global valid_matrices

    row_sum = row_sums[row_number]
    remaining_col_sums = list((np.array(col_sums) - np.sum(current_matrix, axis=0)).astype('int'))

    if entries_01_only:
        k = 1
    else:
        k = None

    for partition in partitions(row_sum, k=k):
        partition_list = convert_partition_to_list(partition)
        padded_partition = pad_partition(partition_list, remaining_col_sums)

        if (len(padded_partition) > len(col_sums)) | (max(padded_partition) > max(remaining_col_sums)):
            continue

        for row_permutation in multiset_permutations(padded_partition):
            if validate_row(row_permutation, remaining_col_sums):
                current_matrix[row_number] = row_permutation

                if row_number == len(row_sums) - 1:
                    if row_permutation == remaining_col_sums:
                        valid_matrices.append(deepcopy(current_matrix))
                else:
                    row_number += 1
                    iterate_over_row(row_sums=row_sums,
                                     col_sums=col_sums,
                                     current_matrix=current_matrix,
                                     entries_01_only=entries_01_only,)

    # exhausted all possibilities for this row, so we need to step back up
    row_number -= 1

    # reset current_matrix rows
    for row_index in range(row_number, len(row_sums)):
        current_matrix[row_index] = [0] * len(col_sums)


def convert_partition_to_list(partition: dict) -> list:
    output = []
    for key, value in partition.items():
        for _ in range(value):
            output.append(key)

    return output


def pad_partition(partition: list, column_sums: list) -> list:
    if len(partition) < len(column_sums):
        for _ in range(len(column_sums) - len(partition)):
            partition.append(0)

    return sorted(partition, reverse=True)


def validate_row(row: list, column_sums: list):
    # check row doesn't violate column sums
    if all(np.array(row) <= np.array(column_sums)):
        return True
    else:
        return False


if __name__ == "__main__":
    main()
