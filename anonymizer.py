import sys

from partition_for_transaction import partition
from utils.read_data import read_data, read_tree_file


def get_result(att_tree, data, k=10):
    """
    run partition for one time, with k=10 by default
    """
    print("K=%d" % k)
    _, eval_result = partition(att_tree, data, k)
    print("NCP %0.2f" % eval_result[0] + "%")
    print("Running time %0.2f" % eval_result[1] + " seconds")


if __name__ == "__main__":
    INPUT_K = ""

    try:
        INPUT_K = sys.argv[1]
    except IndexError:
        pass

    print("BMS-WebView data")
    DATA = read_data()
    ATT_TREE = read_tree_file()

    # read generalization hierarchy
    # read record
    # remove duplicate items
    DATA = list(DATA)
    for i in range(len(DATA)):
        DATA[i] = list(set(DATA[i]))

    print("Begin Partition")

    if INPUT_K == "":
        get_result(ATT_TREE, DATA)  # K=10 by default
    else:
        try:
            INPUT_K = int(INPUT_K)
            get_result(ATT_TREE, DATA, INPUT_K)
        except ValueError:
            print("Usage: python anonymizer k")  # k=10 by default

    # anonymized dataset is stored in result
    print("Finish Partition!!")
