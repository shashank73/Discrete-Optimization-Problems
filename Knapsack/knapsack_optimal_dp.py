def knapsack_dp(capacity, weights, values):
    """ Function to find the max value capacity of a knapsack
    Args:
        capacity: max weight knapsack can carry
        weights: weight array of individual indexed item
        values: value associated with the items in same item order as weights

    Returns:
        return the max value knapsack can contain
    """
    no_of_items = len(weights)
    # create a dp table to cache the subproblems with dimension (capacity * weights)
    table = [[0 for i in range(capacity + 1)] for j in range(no_of_items + 1)]

    # fill the table in bottom up manner with index (1, 1) using recurence relation
    for i in range(1, no_of_items + 1):
        for item_wt in range(1, capacity + 1):
            # check if the current weight satisfies the weight constraint
            if weights[i - 1] <= item_wt:
                # fill the current index either by not choosing the current item case 1 or
                #choose the current item and reduce the current weight and inc the value
                table[i][item_wt] = max(
                    # Case 1: item not chosen -> value upto previous item is considered
                    table[i - 1][item_wt],
                    # Case 2: item chosen -> inc value and dec capacity
                    table[i - 1][capacity - weights[i - 1]] + values[i - 1],
                )
            else:
                # copy the previous row value as current value
                table[i][item_wt] = table[i - 1][item_wt]
    print(table)
    # since the bottom right index gives the optimal solution of the whole problem
    return table[no_of_items][capacity]


if __name__ == "__main__":
    CAPACITY = 6
    WEIGHTS = [1, 2, 3, 4]
    VALUES = [3, 7, 4, 5]
    print("Max value of knapsack :", knapsack_dp(CAPACITY, WEIGHTS, VALUES))
