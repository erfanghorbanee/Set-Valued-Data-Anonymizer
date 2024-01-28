from models.gentree import GenTree


def read_tree_file():
    att_tree = {}
    treefile = open("data/treefile_BMS.txt", "r")
    att_tree["*"] = GenTree("*")

    for line in treefile:
        # delete \n
        if len(line) <= 1:
            break
        line = line.strip()
        temp = line.split(";")
        # copy temp
        temp.reverse()
        for i, t in enumerate(temp):
            isleaf = False
            if i == len(temp) - 1:
                isleaf = True
            try:
                att_tree[t]
            except:
                # always satisfy
                att_tree[t] = GenTree(t, att_tree[temp[i - 1]], isleaf)

    treefile.close()
    return att_tree


def read_data():
    bms_webview2 = open("data/BMS-WebView-2.dat", "r")
    print("Reading Data...")
    bmwdata = {}
    for line in bms_webview2:
        line = line.strip()
        row = line.split("\t")
        # use try and except to speed up comparision
        try:
            bmwdata[row[0]].append(row[1])
        except:
            bmwdata[row[0]] = [row[1]]
    bms_webview2.close()

    return bmwdata.values()
