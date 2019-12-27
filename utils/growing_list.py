class GrowingList(list):
    """ Special thanks => https://stackoverflow.com/a/4544699 """

    def __setitem__(self, index, value):
        if index >= len(self):
            self.extend([0] * (index + 1 - len(self)))
        list.__setitem__(self, index, value)
