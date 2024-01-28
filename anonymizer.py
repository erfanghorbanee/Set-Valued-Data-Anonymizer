import sys

from partition_for_transaction import partition
from utils.read_data import read_data, read_tree_file


def get_result(att_tree, data, k=10):
    """
    run partition for one time, with k=10 by default
    """
    print(f"K={k}")
    result, eval_result = partition(att_tree, data, k)

    print(f"NCP {eval_result[0]:0.2f}%")
    print(f"Running time {eval_result[1]:0.2f} seconds")

    # write anonymized data to file
    # with open('output.csv', 'w') as file:
    #     for record in result:
    #         file.write(f"{record}\n")


if __name__ == "__main__":
    print("BMS-WebView data")

    # Read the necessary data and tree structure
    data = read_data()
    att_tree = read_tree_file()

    # Process data: remove duplicate items
    data = list(data)
    for i in range(len(data)):
        data[i] = list(set(data[i]))

    print("Begin Partition")

    # Determine K value from command-line arguments or use default k=10
    k = 10
    if len(sys.argv) > 1:
        try:
            k = int(sys.argv[1])
        except ValueError:
            print("Usage: python anonymizer.py [k]")
            print("k=10 by default")
            sys.exit(1)

    # Execute the main functionality
    get_result(att_tree, data, k)

    # Final message
    print("Finish Partition!!")
