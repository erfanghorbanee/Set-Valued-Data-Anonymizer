import pdb
import time
from itertools import combinations

from models.bucket import Bucket


def node_cmp(node1, node2):
    """
    Compare function for sorting tree nodes.
    """
    if node1 < node2:
        return -1
    elif node1 > node2:
        return 1
    else:
        return 0


def list_to_str(value_list, cmpfun=node_cmp, sep=";"):
    """
    Convert a list to a string with a specified separator.
    """

    def custom_sort(item):
        return (item in ["A", "B"], item)

    sorted_list = sorted(value_list, key=custom_sort)
    return sep.join(sorted_list)


def information_gain(bucket, pick_value):
    """
    return information gain from bucket accroding to pick_value.
    Information gain in this algorithm is different from its general meaning
    in information theory. It's one kind of distance fuction based on NCP for
    transaction.
    """

    ig = 0.0

    if len(ATT_TREE[pick_value]) == 0:
        return 0

    for record in bucket.member:
        ig += trans_information_gain(record, pick_value)

    return ig


def trans_information_gain(tran, pick_value):
    ig = 0.0
    ncp = len(ATT_TREE[pick_value])

    for t in tran:
        if pick_value in set(PARENT_LIST[t]):
            ig += ncp

    return ig


def pick_node(bucket):
    """
    The node expansion which maximizes information gain for
    the whole partition will be picked and used.
    """

    buckets = {}
    result_list = []
    max_ig = -10000
    max_value = ""

    check_list = [t for t in bucket.value if t not in bucket.split_list]

    for t in check_list:
        if len(ATT_TREE[t].child) != 0:
            ig = information_gain(bucket, t)
            if ig > max_ig:
                max_ig = ig
                max_value = t

    if max_value == "":
        return ("", {})

    index = bucket.value.index(max_value)
    child_value = [t.value for t in ATT_TREE[max_value].child]

    for i in range(1, len(child_value) + 1):
        temp = combinations(child_value, i)
        temp = [list(t) for t in temp]
        result_list.extend(temp)

    child_value = bucket.value[:]
    del child_value[index]

    for temp in result_list:
        temp_value = child_value[:]
        for t in temp:
            temp_value.insert(index, t)
        str_value = list_to_str(temp)
        buckets[str_value] = Bucket([], temp_value)

    bucket.split_list.append(max_value)

    return (max_value, buckets)


def distribute_data(bucket, buckets, pick_value):
    """
    Distribute records from parent_bucket to buckets (split buckets)
    according to record elements.
    """
    if len(buckets) == 0:
        print("Error: buckets is empty!")
        return

    record_set = bucket.member[:]

    for record in record_set:
        gen_list = []
        for t in record:
            parent_list = PARENT_LIST[t]
            try:
                pos = parent_list.index(pick_value)
                if pos > 0:
                    gen_list.append(parent_list[pos - 1])
                else:
                    print("Error: pick node is leaf, which cannot be split")
            except:
                continue

        gen_list = list(set(gen_list))
        str_value = list_to_str(gen_list)

        try:
            buckets[str_value].member.append(record)
        except KeyError:
            pdb.set_trace()
            print("Error: Cannot find key.")


def balance_partitions(parent_bucket, buckets, K, pick_value):
    """
    Handle buckets with less than K records.
    """
    global RESULT
    left_over = []

    for k, bucket in list(buckets.items()):
        if len(bucket) < K:
            left_over.extend(bucket.member[:])
            del buckets[k]

    if len(left_over) == 0:
        return

    flag = True

    while len(left_over) < K:
        check_list = [t for t in list(buckets.values()) if len(t) > K]

        if len(check_list) == 0:
            flag = False
            break

        min_ig = 10000000000000000
        min_key = (0, 0)

        for i, temp in enumerate(check_list):
            for j, t in enumerate(temp.member):
                ig = trans_information_gain(t, pick_value)
                if ig < min_ig:
                    min_ig = ig
                    min_key = (i, j)

        left_over.append(check_list[min_key[0]].member[min_key[1]][:])
        del check_list[min_key[0]].member[min_key[1]]

    if flag is False:
        parent_bucket.splitable = False

        try:
            min_ig = 10000000000000000
            min_key = ""

            for k, t in list(buckets.items()):
                ig = information_gain(t, pick_value)
                if ig < min_ig:
                    min_ig = ig
                    min_key = k

            left_over.extend(buckets[min_key].member[:])
            del buckets[min_key]
        except:
            print("Error: buckets is empty")
            pdb.set_trace()

    parent_bucket.member = left_over[:]
    str_value = list_to_str(parent_bucket.value)
    buckets[str_value] = parent_bucket


def check_splitable(bucket):
    """
    Check if the bucket can be further splitted down.
    """
    check_list = [t for t in bucket.value if t not in set(bucket.split_list)]

    if bucket.splitable:
        for t in check_list:
            if len(ATT_TREE[t].child) != 0:
                return True
        bucket.splitable = False

    return False


def anonymize(bucket, K):
    """
    Recursively split the dataset to create anonymization buckets.
    """
    global RESULT

    if check_splitable(bucket) is False:
        RESULT.append(bucket)
        return

    (pick_value, expandNode) = pick_node(bucket)
    distribute_data(bucket, expandNode, pick_value)
    balance_partitions(bucket, expandNode, K, pick_value)

    for t in list(expandNode.values()):
        anonymize(t, K)


def get_iloss(tran, middle):
    """
    Return the iloss caused by anon tran to middle.
    """
    iloss = 0.0

    for t in tran:
        ntemp = ATT_TREE[t]
        checktemp = ntemp.parent[:]
        checktemp.insert(0, ntemp)

        for ptemp in checktemp:
            if ptemp.value in set(middle):
                break
        else:
            print(f"Program Error!!!! t={t} middle={middle}")
            pdb.set_trace()

        if ptemp.value == t:
            continue

        iloss += len(ptemp)

    iloss = iloss * 1.0 / LEAF_NUM

    return iloss


def init(att_tree, data, k):
    """
    Initialize global variables.
    """
    global LEAF_NUM, PARENT_LIST, ATT_TREE, ELEMENT_NUM, RESULT

    PARENT_LIST = {}
    RESULT = []
    LEAF_NUM = 0
    ELEMENT_NUM = 0

    for tran in data:
        ELEMENT_NUM += len(tran)

    ATT_TREE = att_tree
    LEAF_NUM = len(ATT_TREE["*"])

    for k, node in list(ATT_TREE.items()):
        if len(node) == 0:
            PARENT_LIST[k] = [t.value for t in node.parent]
            PARENT_LIST[k].insert(0, k)


def partition(att_tree, data, k):
    """
    data: original transactions data
    """

    init(att_tree, data, k)
    result = []
    start_time = time.time()

    anonymize(Bucket(data, ["*"]), k)
    rtime = float(time.time() - start_time)
    ncp = 0.0

    for partition in RESULT:
        pncp = 0.0

        for mtemp in partition.member:
            pncp += get_iloss(mtemp, partition.value)
            result.append(partition.value[:])

        partition.iloss = pncp
        ncp += pncp

    ncp = ncp * 100.0 / ELEMENT_NUM

    return (result, (ncp, rtime))
