class Bucket:
    """
    Class for Group, which is used to keep records
    Store tree node in instances.
    self.iloss: information loss of the whole group
    self.split_list: record picked values (used for revert)
    self.member: records in group
    self.value: group value
    self.splitable: True (False) means that group can (not) be split
    """

    def __init__(self, data: list, value: list[str] = ["*"]) -> None:
        self.iloss = 0.0
        self.split_list = []
        self.member = data
        self.value = value[:]
        self.splitable = True

    def __len__(self) -> int:
        """
        return the number of records in bucket
        """
        return len(self.member)
