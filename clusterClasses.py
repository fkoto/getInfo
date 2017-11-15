class Core:
    def __init__(self, Id=None):
        #print 'creating core. id=' + str(Id)
        if Id is None:
            self.id = ''
        else:
            self.id = Id


class Slot:
    def __init__(self, Id=None, **kwargs):
        #print 'creating slots. id=' + str(Id)
        #print 'kwargs:{' + str(kwargs) + '}'
        if Id is None:
            self.id = ''
        else:
            self.id = Id

        self.parentNodeId = kwargs.get('parentId', -1)

        self.cores = []
        if kwargs.get('numOfCores') is not None:
            for c in range(kwargs.get('numOfCores')):
                temp = Core(str(c) + ':' + str(self.id) + ':' + str(self.parentNodeId))
                self.cores.append(temp)

    def createCoreGenerator(self):
            for core in self.cores:
                yield core

    def getNextAvailableCore(self):
        try:
            for cor in self.createCoreGenerator():
                return cor
        except StopIteration:
            return None

class Node:
    def __init__(self, Id=None, **kwargs):
        if Id is None:
            self.id = ''
        else:
            self.id = Id

        self.maxSlots = kwargs.get('maxSlots', -1)
        self.slots = []
        if kwargs.get('numOfSlots') is not None:
            coresPerSlot =  kwargs.get('numOfCoresPerSlot', 1)
            for sl in range(kwargs.get('numOfSlots')):
                temp = Slot(sl, numOfCores=coresPerSlot, parentId=self.id)
                self.slots.append(temp)

    def setSlots(self, numOfSlots, numOfCoresPerSlot):
        for i in range(numOfSlots):
            temp = Slot(i, numOfCores=numOfCoresPerSlot, parentId=self.id)
            self.slots.append(temp)

    def createSlotGenerator(self):
            for slot in self.slots:
                yield slot

    def getNextAvailableSlot(self):
        try:
            for sl in self.createSlotGenerator():
                return sl
        except StopIteration:
            return None

class Cluster:
    def __init__(self):
        self.nodes = []

    def getNodesFromHostFile(self, inputFile, numOfCoresPerSlot=1):
        cnt = 0
        for line in inputFile:
            #print (line)
            line = line.strip()  # remove trailing whitespaces
            if not line or line.startswith('#'):
                cnt += 1
                continue  # ignore comments and empty lines

            line = line.split('#')[0]  # ignore inline comments
            #print (line + ' (after removing comments)')
            splitted = line.split()

            node = Node()
            node.id = splitted[0]

            # a multicore node
            if ' slots=' in line:
                node.setSlots(int(splitted[1].split('=')[-1]), numOfCoresPerSlot)

            # maxSlots are defined
            if 'max-slots=' in line:
                node.maxSlots = int(splitted[-1].split('=')[-1])
                if len(node.slots) == 0:
                    node.setSlots(node.maxSlots, numOfCoresPerSlot)

            # a single core node (neither 'slots' nor 'max-slots' is defined)
            if 'slots' not in line:
                node.setSlots(1, 1)

            # add to cluster
            #print(node.id)
            #for slot in node.slots:
            #  print 'has->' + str(slot.id) + ' with ' + str(len(slot.cores)) + ' cores'
            self.nodes.append(node)

            #print('ignored:' + str(cnt) + ' lines!')

    def printClusterDetails(self):
        print self.nodes
        for nod in self.nodes:
            print 'Node id=' + str(nod.id)
            slots = len(nod.slots)
            print 'slots=' + str(slots)
            cores = sum(len(i.cores) for i in nod.slots)
            print 'cores=' + str(cores) + '\n'

    def createNodeGenerator(self):
            for node in self.nodes:
                yield node

    def getNextAvailableNode(self):
        try:
            for nod in self.createNodeGenerator():
                return nod
        except StopIteration:
            return None