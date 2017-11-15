class Sorter:
    """This class is used to sort("assign ranks") to
    mpi processes. It is initiated with a ranking mode
    'node', 'slot', 'core' and then it uses it's {code}compare{/code}
    method that takes as input a list of core ids that will be used
    and returns a list containing these ids in the order the assignment
    will take place."""
    def __init__(self, mode):
        self.mode = mode

    def compare(self, lst):
        if self.mode == 'core':
            return self.compareByCore(lst)
        elif self.mode == 'slot':
            return self.compareBySlot(lst)
        else:
            return self.compareByNode(lst)

    def compareByCore(self, lst):
        print 'CompareByCore invoked.'
        return sorted(lst, key=lambda x:(x.split(':')[2], x.split(':')[1], x.split(':')[0]))

    def compareBySlot(self, lst):
        print 'CompareBySlot invoked.'
        return sorted(lst, key=lambda x:(x.split(':')[0], x.split(':')[2], x.split(':')[1]))

    def compareByNode(self, lst):
        print 'CompareByNode invoked.'
        return sorted(lst, key=lambda x:(x.split(':')[1], x.split(':')[0], x.split(':')[2]))